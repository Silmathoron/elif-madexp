from brian2 import *
import matplotlib.pyplot as plt

defaultclock.dt = 0.1*ms

C_m       = 100.*pF           # Membrane capacitance
g_L       = 9.*nS             # Leak conductance
E_0       = -62.5*mV          # Resting potential
V_th      = -59.*mV           # Spike generation threshold
V_reset   = -62.*mV           # reset potential
I_e       = 0.*pA             # Constant input current

E_u       = -58.5*mV          # upper potential
alpha     = 1.                # energetic health
E_d       = -40.*mV           # energy depletion potential
E_f       = -62.*mV           # energy inflexion potential
epsilon_0 = 0.5               # standard resting energy level
epsilon_c = 0.18              # energy threshold for spike generation
delta     = 0.01              # energy consumption per spike
tau_e     = 200.*ms           # time constant for energy production

N = 1

eqs = """
E_L = E_0 + (E_u - E_0)*(1-epsilon/epsilon_0) : volt

dV_m/dt  = (g_L*(E_L-V_m) + I_e) / C_m : volt
depsilon/dt = ((1-epsilon/(alpha*epsilon_0))**3 - (V_m-E_f)/(E_d-E_f)) / tau_e : 1
"""

neuron = NeuronGroup(N, model=eqs, threshold='V_m > V_th and epsilon > epsilon_c',
                     reset="V_m = V_reset; epsilon -= delta",
                     method='rk4')
neuron.V_m  = -61*mV
neuron.epsilon = 0.32

init_time = 3*second
run(init_time, report='text')  # we let the neuron relax to equilibrium

# record the state variables and run the simulation
spikes = SpikeMonitor(neuron)
states = StateMonitor(neuron, ("V_m", "epsilon"), record=True,
                      when='start')

for I_e in np.linspace(0, 120, 10)*pA:
    run(1 * second, report='text')
    I_e = 0*pA
    run(10 * second, report='text')

# Get the values of V and epsilon
V  = states.V_m[0] / mV
e  = states.epsilon[0]
tt = states.t / ms

pos = np.digitize(spikes.t / ms, tt) - 1
V[pos] = -10.

fig, (ax1, ax2) = plt.subplots(2, sharex=True)

ax1.plot(tt, V)
ax1.set_ylabel('V (mV)')

ax2.plot(tt, e)
ax2.set_ylabel('epsilon')
ax2.set_xlabel('Time (ms)')

plt.show()
