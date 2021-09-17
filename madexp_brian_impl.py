from brian2 import *
import matplotlib.pyplot as plt

defaultclock.dt = 0.1*ms

C_m       = 130.*pF           # Membrane capacitance
g_L       = 10.*nS            # Leak conductance
E_0       = -55.*mV           # Resting potential
V_th      = -53.*mV           # Spike generation threshold
Delta_T   = 2.*mV             # Slope factor
a         = 4.*nS             # subthreshold adaptation
tau_w     = 120.*ms           # timescale of the adaptation current
b         = 60.*pA            # spike-triggered adaptation
V_reset   = -49.*mV           # reset potential
I         = 0.*pA             # Constant input current
Vcut      = V_th + 5*Delta_T  # practical threshold condition

E_u       = -50.*mV           # upper potential
alpha     = 1.                # energetic health
E_d       = -35.*mV           # energy depletion potential
E_f       = -45.*mV           # energy inflexion potential
epsilon_0 = 0.5               # standard resting energy level
epsilon_c = 0.15              # energy threshold for spike generation
delta     = 0.02              # energy consumption per spike
gamma     = 200.*pA           # normalization of adaptation energy
tau_e     = 500.*ms           # time constant for energy production
I_KATP    = 1.*pA             # peak ATP-gated potassium current

N = 1

eqs = """
E_L = E_0 + (E_u - E_0)*(1-epsilon/epsilon_0) : volt

dV_m/dt  = (g_L*(E_L-V_m) + g_L*Delta_T*(epsilon - epsilon_c)*exp((V_m-V_th)/Delta_T)/epsilon_0 + I - w) / C_m : volt
dw/dt   = (a*(V_m-E_L) - w + I_KATP*epsilon_c/(epsilon_c + 2*epsilon)) / tau_w : amp
depsilon/dt = ((1-epsilon/(alpha*epsilon_0))**3 - (V_m-E_f)/(E_d-E_f) - w/gamma) / tau_e : 1
"""

neuron = NeuronGroup(N, model=eqs, threshold='V_m > Vcut and epsilon > epsilon_c',  # the epsilon check is necessary in case Delta_T == 0
                     reset="V_m = V_reset; w += b; epsilon -= delta",
                     method='rk4')
neuron.V_m  = -60*mV
neuron.w   = a * (neuron.V_m - E_0)
neuron.epsilon = 1.2

init_time = 3*second
run(init_time, report='text')  # we let the neuron relax to equilibrium

# record the state variables and run the simulation
spikes = SpikeMonitor(neuron)
states = StateMonitor(neuron, ("V_m", "w", "epsilon"), record=True,
                      when='start')

for I in np.linspace(0, 250, 10)*pA:
    run(1 * second, report='text')
    I = 0*pA
    run(10 * second, report='text')

# Get the values of V_reset and w for each spike
V  = states.V_m[0] / mV
w  = states.w[0] / pA
e  = states.epsilon[0]
tt = states.t / ms

pos = np.digitize(spikes.t / ms, tt) - 1
V[pos] = -10.

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

ax1.plot(tt, V)
ax1.set_ylabel('V (mV)')

ax2.plot(tt, w)
ax2.set_ylabel('w (pA)')

ax3.plot(tt, e)
ax3.set_ylabel('epsilon')
ax3.set_xlabel('Time (ms)')

plt.show()
