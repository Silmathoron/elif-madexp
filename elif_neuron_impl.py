from matplotlib import pyplot as plt
import numpy as np

from neuron import h
from neuron.units import ms

h.load_file('stdrun.hoc')

from nrn_impl import eLIFNeuron


''' Create the neuron '''

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
    "t_ref": 2.,
    "epsilon_0": 0.5,
    "epsilon_c": 0.18,
    "delta": 0.01,
    "V_reset": -62.,
    "tau_e": 200.,
}

neuron = eLIFNeuron(params)


''' Record and stimulate '''

t_vec = h.Vector().record(h._ref_t)
v_vec = h.Vector().record(neuron._seg._ref_v)
e_vec = h.Vector().record(neuron._model._ref_epsilon)

# current clamps
num_steps = 10
iclamps = []

times = [i*11000 for i in range(num_steps)]
amps  = [i for i in np.linspace(0, 120, num_steps)]

for t, I in zip(times, amps):
    i = h.IClamp(0.5, sec=neuron._sec)
    i.delay = t # ms
    i.dur = 1000. # ms
    i.amp = I
    iclamps.append(i)


''' Run and plot '''

h.finitialize(-61.)
neuron.epsilon = 0.32

h.continuerun((times[-1] + 10000) * ms)

t_vec /= 1000.

fig, (ax1, ax2) = plt.subplots(2, sharex=True)

pos = (np.array(v_vec) >= neuron.V_th)*(np.array(e_vec) >= neuron.epsilon_c)
v_vec = np.array(v_vec)
v_vec[pos] = -10.

ax1.plot(t_vec, v_vec, label="nrn")
ax2.plot(t_vec, e_vec)

ax1.set_ylabel("V (mV)")
ax2.set_ylabel("epsilon")
ax2.set_xlabel("time (s)")

plt.show()
