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
    POINT_PROCESS eLIF
    RANGE V_reset, t_ref, V_th, spikewidth, V_peak
    RANGE epsilon
    RANGE g_L, E_0, E_u, E_d, E_f
    RANGE tau_e, epsilon_0, epsilon_c, delta, alpha
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
    V_peak  = 0.   (mV)   : peak potential during a spike
    t_ref = 2     (ms)   : refractory period
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

    g_L	    = 30.   (nS)

    I_e = 0 (pA)
}


ASSIGNED {
    i (pA)
    irefrac (pA)
    grefrac (nS)
    refractory
}

STATE {
    w  (pA)
    epsilon
}

INITIAL {
    grefrac = 0
    net_send(0,4)
    epsilon = alpha*epsilon_0
}

FUNCTION E_L (epsilon) (mV) {
    E_L = E_0 + (E_u - E_0)*(1 - epsilon/epsilon_0)
}

BREAKPOINT {
    SOLVE states METHOD derivimplicit  : cnexp
    irefrac = grefrac*(v-V_reset)
    i = ( g_L*(v - E_L(epsilon)) + irefrac - I_e)
}

DERIVATIVE states {		: solve eq for adaptation variable
    epsilon' = ((1-epsilon/(alpha*epsilon_0))*(1-epsilon/(alpha*epsilon_0))*(1-epsilon/(alpha*epsilon_0)) - (v-E_f)/(E_d-E_f)) / tau_e
}

FUNCTION threshcrossing (v (mV), epsilon) {
    if ((v > V_th) && (epsilon > epsilon_c)) {
        threshcrossing = 1
    }
    else {
        threshcrossing = -1
    }
}

NET_RECEIVE (weight) {
    if (flag == 1) {        : beginning of spike
        v = V_peak
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
