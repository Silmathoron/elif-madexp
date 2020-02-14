: Insert in a passive compartment to get an adaptive-exponential (Brette-Gerstner)
: integrate-and-fire neuron with a refractory period.
: This calculates the adaptive current, sets the membrane potential to the
: correct value at the start and end of the refractory period, and prevents spikes
: during the refractory period by clamping the membrane potential to the reset
: voltage with a huge conductance.
:
: Reference:
:
: Brette R and Gerstner W. Adaptive exponential integrate-and-fire
:   model as an effective description of neuronal activity. 
:   J. Neurophysiol. 94: 3637-3642, 2005.
:  
: Implemented by Andrew Davison. UNIC, CNRS, March 2009.

NEURON {
    POINT_PROCESS mAdExp
    RANGE V_reset, t_ref, V_spike, V_th, V_peak, spikewidth, C_m
    RANGE w, winit, epsilon
    RANGE a, b, tau_w, g_L, Delta_T, E_0, E_u, E_d, E_f
    RANGE gamma, tau_e, epsilon_0, epsilon_c, delta, I_KATP, alpha
    NONSPECIFIC_CURRENT i, I_e
}

UNITS {
    (mV) = (millivolt)
    (pA) = (picoamp)
    (nS) = (nanosiemens)
}

PARAMETER {
    V_th = -50   (mV)   : spike threshold for exponential calculation purposes
    V_reset  = -60   (mV)   : reset potential after a spike
    V_spike  = -43   (mV)   : spike detection threshold
    V_peak   = 0     (mV)   : peak of spike
    t_ref = 1     (ms)   : refractory period
    gon     = 1e9   (nS)   : refractory clamp conductance
    spikewidth = 1e-12 (ms) : must be less than t_ref

    E_0 = -55. (mV)
    E_u = -50. (mV)
    E_d = -35. (mV)
    E_f = -45. (mV)
    
    epsilon_0 = 0.5
    epsilon_c = 0.15
    alpha = 1. <0, 1e9>
    delta = 0.02
    tau_e = 500. (ms) <0, 1e9>
    gamma = 200. (pA) <0, 1e9>
    I_KATP = 1 (pA)

    a 	    = 0.  (nS)   : level of adaptation
    b	    = 80.5 (pA)   : increment of adaptation
    tau_w   = 144    (ms)   : time constant of adaptation

    g_L	    = 30.   (nS)   : leak conductance (must be equal to g_pas(S/cm2)*membrane area(um2)*1e-2)
    Delta_T   = 2      (mV)   : steepness of exponential approach to threshold

    I_e = 0 (pA)
    winit  = 0      (pA)
}


ASSIGNED {
    i (pA)
    irefrac (pA)
    iexp (pA)
    grefrac (nS)
    refractory
    spike_threshold (mV)
}

STATE {
    w  (pA)
    epsilon
}

INITIAL {
    grefrac = 0
    net_send(0,4)
    w = winit
    epsilon = alpha*epsilon_0
    if (Delta_T == 0) {
        spike_threshold = V_th
    } else {
        spike_threshold = V_spike
    }
}

FUNCTION E_L (epsilon) (mV) {
    E_L = E_0 + (E_u - E_0)*(1 - epsilon/epsilon_0)
}

BREAKPOINT {
    SOLVE states METHOD derivimplicit  : cnexp
    irefrac = grefrac*(v-V_reset)
    iexp = exp_current(v, epsilon)
    i = ( g_L*(v - E_L(epsilon)) + iexp + w + irefrac - I_e)
}

DERIVATIVE states {		: solve eq for adaptation variable
    w' = (a*(v-E_L(epsilon)) - w + I_KATP*epsilon_c/(2*epsilon + epsilon_c)) / tau_w
    epsilon' = ((1-epsilon/(alpha*epsilon_0))*(1-epsilon/(alpha*epsilon_0))*(1-epsilon/(alpha*epsilon_0)) - (v-E_f)/(E_d-E_f) - w/gamma) / tau_e
}

FUNCTION exp_current(v, epsilon) {  : handle the case where Delta_T is 0 or very small
    if (Delta_T == 0) {
        exp_current = 0
    } else if ((v - V_th)/Delta_T > 100) {
        exp_current = -g_L*Delta_T*(epsilon-epsilon_c)*exp(99)/epsilon_0
    } else {
        exp_current = -g_L*Delta_T*(epsilon-epsilon_c)*exp((v-V_th)/Delta_T)/epsilon_0
    }
}

FUNCTION threshcrossing (v (mV), epsilon) {
    if ((v > V_spike) && (epsilon > epsilon_c)) {
        threshcrossing = 1
    }
    else {
        threshcrossing = -1
    }
}

NET_RECEIVE (weight) {
    if (flag == 1) {        : beginning of spike
        v = V_peak
        w = w + b
        epsilon = epsilon - delta
        net_send(spikewidth, 2)
        net_event(t)
        :printf("spike: t = %f  v = %f   w = %f   i = %f\n", t, v, w, i)
    } else if (flag == 2) { : end of spike, beginning of refractory period
        v = V_reset
        grefrac = gon
        if (t_ref > spikewidth) {
            net_send(t_ref-spikewidth, 3)
        } else { : also the end of the refractory period
            grefrac = 0
        }
        :printf("refrac: t = %f  v = %f   w = %f   i = %f\n", t, v, w, i)
    } else if (flag == 3) { : end of refractory period
        v = V_reset
        grefrac = 0
        :printf("end_refrac: t = %f  v = %f   w = %f   i = %f\n", t, v, w, i)
    } else if (flag == 4) { : watch membrane potential
        WATCH ( threshcrossing(v, epsilon) > 0 ) 1
    }
}
