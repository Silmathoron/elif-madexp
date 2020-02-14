from matplotlib import pyplot as plt
import numpy as np

from neuron import h
from neuron.units import ms

h.load_file('stdrun.hoc')

from nrn_impl import mAdExpNeuron


''' Create the neuron '''

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

neuron = mAdExpNeuron(params)


''' Record and stimulate '''

t_vec = h.Vector().record(h._ref_t)
v_vec = h.Vector().record(neuron._seg._ref_v)
w_vec = h.Vector().record(neuron._model._ref_w)
e_vec = h.Vector().record(neuron._model._ref_epsilon)

# current clamps
num_steps = 10
iclamps = []

times = [i*11000 for i in range(num_steps)]
amps  = [i for i in np.linspace(0, 250, num_steps)]

print(times, amps)

for t, I in zip(times, amps):
    i = h.IClamp(0.5, sec=neuron._sec)
    i.delay = t # ms
    i.dur = 1000. # ms
    i.amp = I
    iclamps.append(i)


''' Run and plot '''

h.finitialize(-60.)
h.continuerun((times[-1] + 10000) * ms)

t_vec /= 1000.

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

ax1.plot(t_vec, v_vec, label="nrn")
ax2.plot(t_vec, w_vec)
ax3.plot(t_vec, e_vec)

ax1.set_ylabel("V (mV)")
ax2.set_ylabel("w (pA)")
ax3.set_ylabel("epsilon")
ax3.set_xlabel("time (s)")

plt.show()
