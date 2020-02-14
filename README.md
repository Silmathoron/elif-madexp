# Energy-based models (eLIF and mAdExp)


## Content

This repository contains implementations of the eLIF and mAdExp models
for BRIAN, NEST, and NEURON.


## Installing the models

### BRIAN

Just install the BRIAN simulator via pip:

    pip install --user brian2

### NEST

* Install NEST (see [here](https://nest-simulator.readthedocs.io/en/stable/installation/index.html))
* Install NESTML (see [here](https://github.com/nest/nestml#installing-nestml))
* Then run ``python nestml/nestml_install.py`` to install the models

### NEURON

* Download and install NEURON (see [here](https://www.neuron.yale.edu/neuron/download))
* Compile the models via ``nrnivmodl elif.mod`` and
  ``nrnivmodl madexp.mod``


## Running the models

Once the installation of one of the simulators is done, you can run the
corresponding files:

* ``elif_brian_impl.py`` or ``madexp_brian_impl.py`` for BRIAN
* ``elif_nest_impl.py`` or ``madexp_nest_impl.py`` for NEST
* ``elif_neuron_impl.py`` or ``madexp_neuron_impl.py`` for NEURON

To do this, you can call them with python using e.g.
``python elif_brian_impl.py``.
