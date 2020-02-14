from functools import reduce
from math import pi

from neuron import h


def _new_property(obj_hierarchy, attr_name):
    """
    Returns a new property, mapping attr_name to obj_hierarchy.attr_name.
    For example, suppose that an object of class A has an attribute b which
    itself has an attribute c which itself has an attribute d. Then placing
      e = _new_property('b.c', 'd')
    in the class definition of A makes A.e an alias for A.b.c.d
    """

    def set(self, value):
        obj = reduce(getattr, [self] + obj_hierarchy.split('.'))
        setattr(obj, attr_name, value)

    def get(self):
        obj = reduce(getattr, [self] + obj_hierarchy.split('.'))
        return getattr(obj, attr_name)
    return property(fset=set, fget=get)


class eLIFNeuron:

    def __init__(self, params=None):
        self._sec = h.Section()
        self._seg = self._sec(0.5)
        self._sec.L = 1000.
        self._seg.diam = 100. / pi

        self._model = h.eLIF(self._seg)

        if params is not None:
            for k, v in params.items():
                setattr(self, k, v)

    g_L = _new_property('_model', 'g_L')
    V_reset = _new_property('_model', 'V_reset')
    t_ref = _new_property('_model', 't_ref')

    E_0 = _new_property('_model', 'E_0')
    E_u = _new_property('_model', 'E_u')
    E_f = _new_property('_model', 'E_f')
    E_d = _new_property('_model', 'E_d')

    epsilon = _new_property('_model', 'epsilon')
    epsilon_0 = _new_property('_model', 'epsilon_0')
    alpha = _new_property('_model', 'alpha')
    epsilon_c = _new_property('_model', 'epsilon_c')
    delta = _new_property('_model', 'delta')
    tau_e = _new_property('_model', 'tau_e')

    @property
    def V_th(self):
        return self._model.V_th

    @V_th.setter
    def V_th(self, value):
        self._model.V_th = value

    @property
    def C_m(self):
        return self._seg.cm

    @C_m.setter
    def C_m(self, value):
        self._seg.cm = value


class mAdExpNeuron:

    def __init__(self, params=None):
        self._sec = h.Section()
        self._seg = self._sec(0.5)
        self._sec.L = 1000.
        self._seg.diam = 100. / pi

        self._model = h.mAdExp(self._seg)

        if params is not None:
            for k, v in params.items():
                setattr(self, k, v)

    g_L = _new_property('_model', 'g_L')
    V_reset = _new_property('_model', 'V_reset')
    t_ref = _new_property('_model', 't_ref')
    b = _new_property('_model', 'b')
    a = _new_property('_model', 'a')
    tau_w = _new_property('_model', 'tau_w')
    Delta_T = _new_property('_model', 'Delta_T')
    V_peak = _new_property('_model', 'V_peak')

    E_0 = _new_property('_model', 'E_0')
    E_u = _new_property('_model', 'E_u')
    E_f = _new_property('_model', 'E_f')
    E_d = _new_property('_model', 'E_d')

    epsilon_0 = _new_property('_model', 'epsilon_0')
    alpha = _new_property('_model', 'alpha')
    epsilon_c = _new_property('_model', 'epsilon_c')
    delta = _new_property('_model', 'delta')
    gamma = _new_property('_model', 'gamma')
    tau_e = _new_property('_model', 'tau_e')

    @property
    def V_th(self):
        return self._model.V_th

    @V_th.setter
    def V_th(self, value):
        self._model.V_th = value
        self._model.V_spike = value + 5*self.Delta_T

    @property
    def C_m(self):
        return self._seg.cm

    @C_m.setter
    def C_m(self, value):
        self._seg.cm = value

