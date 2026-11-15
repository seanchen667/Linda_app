"""Second-stage hardware requirement screen. Run after simulate.py.
Bounds here are assumptions to be met by future hardware, not measured specs.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import simulate as s


def faster(c):
    c=c.copy()
    c[:,1]=np.minimum(c[:,1],.025)
    c[:,2]=np.minimum(c[:,2],.010)
    c[:,3]=np.maximum(c[:,3],.16)
    return c


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    dev=np.unique(faster(s.grid_cases()),axis=0)
    val=faster(s.validation_cases())
    rows=[]
    for k in [400,600,800,1000,1500,2500,4000,8000]:
        for g in [.25,.5,1.]:
            m,_,_=s.run(k,g,dev,observer=True);rows.append(m)
    feasible=[r for r in rows if r['passes_screen']]
    best=min(feasible or rows,key=lambda r:r['worst_rmse_N'])
    baseline=min([r for r in rows if r['stiffness_N_m']==8000],key=lambda r:r['worst_rmse_N'])
    vm,tr,_=s.run(best['stiffness_N_m'],best['feedback_gain'],val,True,observer=True)
    bm,_,_=s.run(baseline['stiffness_N_m'],baseline['feedback_gain'],val,True,observer=True)
    nominal,_,_=s.run(best['stiffness_N_m'],best['feedback_gain'],dev,observer=True)
    old_dt=s.DT
    s.DT=.001
    fine,_,_=s.run(best['stiffness_N_m'],best['feedback_gain'],dev,observer=True)
    s.DT=old_dt
    # Limiting-case check: zero requested force, no motion, no disturbance.
    old_force=s.FORCE;s.FORCE=0
    zero,_,_=s.run(800,1,np.array([[0,.025,.010,.16,0,1.]]),observer=True)
    s.FORCE=old_force
    assert zero['worst_peak_N']==0 and zero['worst_rmse_N']==0
    result=dict(
        conclusion='CONDITIONAL MODEL PASS' if vm['passes_screen'] and feasible else 'MODEL NO-GO',
        change='Faster actuator/sensor assumptions; geometry disturbances unchanged. Not measured hardware.',
        requirements=dict(servo_time_constant_max_s=.025,end_to_end_delay_max_s=.010,
                          spool_speed_capability_min_m_s=.16,total_spool_travel_m=s.STROKE),
        screened_designs=len(rows),unique_development_cases=len(dev),validation_cases=len(val),
        feasible_designs=len(feasible),development=best,validation=vm,
        baseline_development=baseline,baseline_validation=bm,
        numerical_checks=dict(zero_input_pass=True,dt_2ms=nominal,dt_1ms=fine),
        all_development=rows)
    (out/'fast_hardware_envelope.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savetxt(out/'fast_validation_cases.csv',val,delimiter=',',
        header='frequency_Hz,servo_tau_s,delay_s,speed_limit_m_s,path_change_m,sign',comments='')
    import matplotlib.pyplot as plt
    t,ref,f,_=tr
    worst=int(np.argmax(np.sqrt(np.mean((f[t>=1]-ref[t>=1])**2,axis=0))))
    fig,ax=plt.subplots(figsize=(10,4),layout='constrained')
    ax.plot(t,ref[:,worst],'k--',label='10 N peak bench reference')
    ax.plot(t,f[:,worst],label='Selected design: held-out worst RMSE case')
    ax.set(xlim=(2.5,4.5),xlabel='Time (s)',ylabel='Cable tension (N)',
        title='Conditional model pass — faster hardware assumed, not demonstrated')
    ax.grid(alpha=.2);ax.legend();fig.savefig(out/'fast_envelope.png',dpi=170)
    print(json.dumps({k:v for k,v in result.items() if k not in ['all_development','numerical_checks']},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('results'))
    main(p.parse_args().out)
