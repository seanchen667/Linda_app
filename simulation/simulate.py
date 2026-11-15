"""Assumption-based cable-assistance screening; no human or clinical model.
Run: python simulate.py --out results
Requires Python 3.10+, numpy, matplotlib. Fixed seeds make runs reproducible.
"""
import argparse
import csv
import itertools
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DT = 0.002
SECONDS = 8.0
R = 0.035  # assumed effective joint moment arm, m
FORCE = 10.0  # bench reference peak N; NOT a human prescription
STROKE = 0.100  # revised assumed spool displacement range m


def grid_cases():
    return np.array(list(itertools.product(
        [0.7, 1.2], [0.025, 0.065], [0.008, 0.032],
        [0.08, 0.16], [0.004, 0.010], [-1., 1.])))


def validation_cases():
    rng = np.random.default_rng(20261115)
    n = 96
    return np.column_stack([rng.uniform(a, b, n) for a, b in
        [(0.6, 1.3), (0.02, 0.075), (0.005, 0.040),
         (0.07, 0.18), (0.003, 0.012)]] + [rng.choice([-1., 1.], n)])


def run(k, gain, cases, mismatch=False, integral_gain=0, observer=False):
    """Prescribed joint trajectory + unilateral linear elastic cable.
    xdot = clip((xcmd-x)/tau, -vmax, vmax)
    F = max(0, k_actual * (x - R*theta - path_offset))
    xcmd = R*theta_delayed + Fref/k + gain*(Fref-F_delayed)/k
    Optional bounded integral offset and model-based path observer augment xcmd.
    End-to-end delay lumps sensing/computation/communication together.
    No force cap is applied: unsafe modeled peaks remain visible.
    """
    n = len(cases)
    freq, tau, delay, vmax, amp, sign = cases.T
    t = np.arange(0, SECONDS, DT)
    theta = .25 * np.sin(2*np.pi*t[:, None]*freq)
    phase = np.mod(t[:, None]*freq, 1.)
    ref = FORCE * np.maximum(0., np.sin(2*np.pi*phase))
    # Smooth 100 ms change in effective path length at t=3 s, then held.
    ramp = np.clip((t-3.0)/.1, 0., 1.)
    offset = (.5-.5*np.cos(np.pi*ramp[:, None]))*amp*sign
    rng = np.random.default_rng(17)
    ka = k * (rng.uniform(.8, 1.2, n) if mismatch else np.ones(n))
    noise = rng.normal(0, .10, (len(t), n)) if mismatch else np.zeros_like(theta)
    lag = np.maximum(1, np.rint(delay/DT).astype(int))
    f = np.zeros_like(theta)
    pos = np.zeros_like(theta)
    vel = np.zeros_like(theta)
    x = np.zeros(n)
    integral = np.zeros(n)
    path_estimate = np.zeros(n)
    idx = np.arange(n)
    for i in range(len(t)):
        f[i] = np.maximum(0, ka*(x-R*theta[i]-offset[i]))
        pos[i] = x
        j = np.maximum(0, i-lag)
        measured_f = np.maximum(0, f[j, idx] + noise[j, idx])
        error = ref[i]-measured_f
        integral = np.clip(integral+integral_gain*error/k*DT, -.020, .020)
        command = R*theta[j, idx] + ref[i]/k + gain*error/k + integral
        if observer:
            # Infer slowly varying path offset only while cable is tensioned.
            estimate = pos[j, idx]-R*theta[j, idx]-measured_f/k
            path_estimate += np.where(measured_f > .5,
                DT/.03*(np.clip(estimate,-.02,.02)-path_estimate),0)
            jp = np.maximum(0,j-1)
            angular_velocity=(theta[j,idx]-theta[jp,idx])/DT
            ref_velocity=(ref[i]-ref[max(0,i-1)])/DT
            # Fixed nominal servo compensation, not the true case-specific tau.
            command += path_estimate + .045*(R*angular_velocity+ref_velocity/k)
        command = np.clip(command, -STROKE/2, STROKE/2)
        v = np.clip((command-x)/tau, -vmax, vmax)
        vel[i] = v
        x = np.clip(x+v*DT, -STROKE/2, STROKE/2)
    use = t >= 1.
    rmse = np.sqrt(np.mean((f[use]-ref[use])**2, axis=0))
    peak = np.max(f[use], axis=0)
    extension = np.max(f[use]/ka, axis=0)
    # Prescribed-motion model cannot measure actual gait or balance effects.
    metric = dict(stiffness_N_m=float(k), feedback_gain=float(gain), integral_gain_per_s=float(integral_gain), observer=bool(observer),
        cases=n, worst_rmse_N=float(max(rmse)), mean_rmse_N=float(np.mean(rmse)),
        worst_peak_N=float(max(peak)), max_extension_mm=float(max(extension)*1000),
        max_abs_spool_mm=float(np.max(np.abs(pos[use]))*1000),
        speed_saturation_fraction=float(np.mean(np.abs(vel[use]) >= .999*vmax)))
    metric['passes_screen'] = bool(metric['worst_rmse_N'] <= 2.5 and
        metric['worst_peak_N'] <= 20 and metric['max_extension_mm'] <= 40 and
        metric['max_abs_spool_mm'] < 49.9)
    return metric, (t, ref, f, pos), rmse


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    train = grid_cases()
    rows = []
    for k, gain, ki, observer in itertools.product([250,400,600,800,1000,1500,2500,4000,8000], [0,.25,.5,1.], [0,4,12], [False,True]):
        metrics, _, _ = run(k, gain, train, integral_gain=ki, observer=observer)
        rows.append(metrics)
    feasible = [r for r in rows if r['passes_screen']]
    # Select on development cases only; do not retune after validation.
    best = min(feasible or rows, key=lambda r:r['worst_rmse_N'])
    baseline = min([r for r in rows if r['stiffness_N_m']==8000], key=lambda r:r['worst_rmse_N'])
    heldout = validation_cases()
    bm, bt, br = run(baseline['stiffness_N_m'], baseline['feedback_gain'], heldout, True, baseline['integral_gain_per_s'], baseline['observer'])
    cm, ct, cr = run(best['stiffness_N_m'], best['feedback_gain'], heldout, True, best['integral_gain_per_s'], best['observer'])
    summary = dict(model='prescribed-motion, unilateral elastic cable and delayed first-order spool servo',
        dt_s=DT, seconds=SECONDS, development_cases=len(train), validation_cases=len(heldout),
        screened_designs=len(rows), feasible_designs=len(feasible),
        selected_is_feasible=bool(feasible), assumed_screen=dict(worst_rmse_N=2.5, worst_peak_N=20,
            max_extension_mm=40, max_abs_spool_mm=49.9),
        development_baseline=baseline, development_selected=best,
        validation_baseline=bm, validation_selected=cm,
        validation_peak_reduction_pct=100*(bm['worst_peak_N']-cm['worst_peak_N'])/bm['worst_peak_N'])
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    with (out/'design_sweep.csv').open('w',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0])); w.writeheader();w.writerows(rows)
    with (out/'validation_cases.csv').open('w',newline='') as fp:
        w=csv.writer(fp);w.writerow(['frequency_Hz','servo_tau_s','delay_s','speed_limit_m_s','path_change_m','sign'])
        w.writerows(heldout)
    idx = int(np.argmax(br))
    t, ref, fbase, _ = bt
    fnew=ct[2]
    with (out/'example_trace.csv').open('w',newline='') as fp:
        w=csv.writer(fp);w.writerow(['time_s','reference_N','baseline_N','selected_N'])
        w.writerows(zip(t,ref[:,idx],fbase[:,idx],fnew[:,idx]))
    fig, ax = plt.subplots(2,1,figsize=(10,7),layout='constrained')
    ax[0].plot(t,ref[:,idx],color='black',ls='--',label='Reference')
    ax[0].plot(t,fbase[:,idx],label='Stiff baseline',alpha=.8)
    ax[0].plot(t,fnew[:,idx],label='Selected compliant design')
    ax[0].set(xlim=(2.7,4.5),ylabel='Cable tension (N)',title='Illustrative held-out case: baseline worst tracking case')
    ax[0].legend();ax[0].grid(alpha=.2)
    ax[1].scatter([r['stiffness_N_m'] for r in rows],[r['worst_rmse_N'] for r in rows],
        c=['#008675' if r['passes_screen'] else '#aaaaaa' for r in rows])
    ax[1].scatter([best['stiffness_N_m']],[best['worst_rmse_N']],marker='*',s=180,c='#c34a24',label='Selected')
    ax[1].set(xscale='log',xlabel='Assumed effective stiffness (N/m)',ylabel='Worst development RMSE (N)',
        title='216 screened designs; green = meets all assumed screening limits')
    ax[1].legend();ax[1].grid(alpha=.2)
    fig.suptitle('Numerical screening only — assumed parameters, no human validation')
    fig.savefig(out/'screening.png',dpi=170);plt.close(fig)
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('results'))
    main(ap.parse_args().out)
