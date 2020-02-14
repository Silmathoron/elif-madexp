""" Parameters """

iaf_psc_alpha = {"I_e": 450., "V_th": -61.699}
elif_psc_alpha = {
    "C_m": 104.,
    "g_L": 4.3,
    "E_0": -64.,
    "V_th": -60.,
    "V_reset": -61.,
    "I_e": 47.975,
    't_ref': 0.,
    # energy-related
    "E_u": -60.,
    "alpha": 1.,
    "E_d": -40.,
    "E_f": -46.,
    "epsilon_0": 0.5,
    "epsilon_c": 0.15,
    "delta": 0.01,
    "tau_e": 500.,
}
aeif_psc_alpha = {"I_e": 452.69, "V_th": -67.944},
madexp_psc_alpha = {
    "C_m": 104.,
    "g_L": 4.3,
    "E_0": -64.,
    "V_th": -58.,
    "Delta_T": 0.8,
    "a": 0.,
    "tau_w": 20.,
    "b": 0.5,
    "V_reset": -61.,
    "I_e": 103.54,
    't_ref': 0.,
    # energy-related
    "E_u": -60.,
    "alpha": 1.,
    "E_d": -40.,
    "E_f": -46.,
    "epsilon_0": 0.5,
    "epsilon_c": 0.15,
    "delta": 0.02,
    "gamma": 1000.,
    "tau_e": 500.,
    'I_KATP': 1.,
}
hh_psc_alpha = {"I_e": 6080.},

params = {
    "iaf_psc_alpha": iaf_psc_alpha,
    "iaf_psc_alpha_nestml": iaf_psc_alpha,
    "elif_psc_alpha": elif_psc_alpha,
    "elif_psc_alpha_fast": elif_psc_alpha,
    "aeif_psc_alpha": aeif_psc_alpha,
    "aeif_psc_alpha_nestml": aeif_psc_alpha,
    "madexp_psc_alpha": madexp_psc_alpha,
    "madexp_psc_alpha_fast": madexp_psc_alpha,
    "hh_psc_alpha": hh_psc_alpha,
    "hhca_psc_alpha": hh_psc_alpha
}
