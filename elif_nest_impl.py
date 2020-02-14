import matplotlib.pyplot as plt

import numpy as np
import nest

nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.1})

nest.Install("energy_module")


params = {
    "C_m": 100.,
    "g_L": 9.,
    "E_0": -62.5,
    "I_e": 0.,
    "E_u": -58.5,
    "V_th": -59.,
    "alpha": 1.,
    "E_d": -40.,
    "E_f": -62.,
    "epsilon_0": 0.5,
    "epsilon_c": 0.18,
    "delta": 0.01,
    "V_reset": -62.,
    "tau_e": 200.,
    "V_m": -61.,
    "epsilon": 0.32,
}


nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.1})

n    = nest.Create("elif_psc_alpha", params=params)

starttime = 3000.
simtime   = 1000.
resttime  = 10000.
Istart    = 0.

mm = nest.Create("multimeter", params={"record_from": ['V_m', 'epsilon'], "interval": 0.1, "start": starttime})
nest.Connect(mm, n)

sd = nest.Create("spike_detector")
nest.Connect(n, sd)

nest.Simulate(starttime)

num_steps = 10

tt = [starttime]
II = [Istart]

for Ie in np.linspace(Istart, 120., num_steps):
    nest.SetStatus(n, {"I_e": Ie})
    nest.Simulate(simtime)
    nest.SetStatus(n, {"I_e": 0.})
    nest.Simulate(resttime)
    II.extend([Ie, 0.])
    tt.extend([tt[-1] + simtime, tt[-1] + simtime + resttime])

nest.SetStatus(n, {"I_e": -10.})
nest.Simulate(simtime)
nest.SetStatus(n, {"I_e": 0.})
nest.Simulate(resttime)

II.extend([-10, 0.])
tt.extend([tt[-1] + simtime, tt[-1] + simtime + resttime])

data  = nest.GetStatus(mm, "events")[0]
times = data["times"]
Vm    = data["V_m"]
epsilon   = data["epsilon"]

spks = nest.GetStatus(sd, "events")[0]["times"]

pos = np.digitize(spks, times) - 1
Vm[pos] = -10.

fig, (ax1, ax2) = plt.subplots(2, figsize=(9, 4.5), sharex=True)

times /= 1000.

ax1.plot(times, Vm)
ax1.set_ylabel("V (mV)")

ax2.plot(times, epsilon)
ax2.set_ylabel("$\epsilon$")
ax2.set_xlabel("Time (s)")

tt = np.array(tt) / 1000.
ax2b = ax2.twinx()
ax2b.plot(list(np.repeat(tt,2))[1:] + [times[-1]], list(np.repeat(II,2)[2:]) + [0, 0], c='k', alpha=0.5)
ax2b.set_ylabel("I (pA)")

plt.tight_layout()
plt.show()
