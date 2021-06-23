import matplotlib.pyplot as plt

import numpy as np
import nest

nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.1})

nest.Install("energy_module")


params = {
    'C_m': 130.0,
    'g_L': 10.0,
    'V_th': -53.0,
    'Delta_T': 2.0,
    'a': 4.0,
    'tau_w': 120.0,
    'b': 60.0,
    'V_reset': -49.0,
    'I_e': 0.0,
    't_ref': 0.0,
    'E_u': -50.0,
    'alpha': 1.0,
    'E_d': -35.0,
    'epsilon_0': 0.5,
    'epsilon_c': 0.15,
    'delta': 0.02,
    'gamma': 200.0,
    'tau_e': 500.0,
    'I_KATP': 1.0,
    'V_m': -60.0,
    'epsilon': 1.2,
    'E_f': -45.0,
    'E_0': -55.0
}


nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.1})

n    = nest.Create("madexp_psc_alpha", params=params)

starttime = 3000.
simtime   = 1000.
resttime  = 10000.
Istart    = 0.

mm = nest.Create("multimeter", params={"record_from": ['V_m', 'w', 'epsilon'], "interval": 0.1, "start": starttime})
nest.Connect(mm, n)

try:
    # NEST 3
    nest.NodeCollection()
    spike_rec = "spike_recorder"
except:
    # NEST 2
    spike_rec = "spike_detector"

sd = nest.Create(spike_rec)
nest.Connect(n, sd)

nest.Simulate(starttime)

num_steps = 10

tt = [starttime]
II = [Istart]

for Ie in np.linspace(Istart, 250., num_steps):
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
w     = data["w"]
epsilon   = data["epsilon"]

spks = nest.GetStatus(sd, "events")[0]["times"]

pos = np.digitize(spks, times) - 1
Vm[pos] = -10.

fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(9, 4.5), sharex=True)

times /= 1000.

ax1.plot(times, Vm)
ax1.set_ylabel("V (mV)")

ax2.plot(times, w)
ax2.set_ylabel("w (pA)")

tt = np.array(tt) / 1000.
ax2b = ax2.twinx()
ax2b.plot(list(np.repeat(tt,2))[1:] + [times[-1]], list(np.repeat(II,2)[2:]) + [0, 0], c='k', alpha=0.5)
ax2b.set_ylabel("I (pA)")

ax3.plot(times, epsilon)
ax3.set_ylabel("$\epsilon$")
ax3.set_xlabel("Time (s)")

plt.tight_layout()
plt.show()
