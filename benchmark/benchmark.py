""" Comparing speed of various models """

from time import time

import nest

nest.Install("energy_module")

print([m for m in nest.Models() if m.startswith("iaf")])

# list of models

models = [
    "iaf_psc_alpha",
    "aeif_psc_alpha",
    "hh_psc_alpha",
    "elif_psc_alpha", "elif_psc_alpha_fast",
    "madexp_psc_alpha", "madexp_psc_alpha_fast",
    "hhca_psc_alpha"
]


# simulate 5 minutes for each neurons and compare times

from benchmark_params import params

simtime = 1*60*1000.  # 5 minutes in milliseconds
runtime = {}
rates   = {}

# empty run
nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.01})

neuron = nest.Create("parrot_neuron")
sd     = nest.Create("spike_detector")
pg     = nest.Create("poisson_generator", params={"rate": 100.})

nest.Connect(neuron, sd)
nest.Connect(pg, neuron, syn_spec={"weight": 20.})

initial_time = time()
nest.Simulate(simtime)
runtime["baseline"] = time() - initial_time

# real

for i, model in enumerate(models):
    nest.ResetKernel()
    nest.SetKernelStatus(
        {"resolution": 0.01, "rng_seeds": [1], "grng_seed": 0})

    neuron = nest.Create(model, params=params[model])
    sd     = nest.Create("spike_detector")
    pg     = nest.Create("poisson_generator", params={"rate": 100.})

    nest.Connect(neuron, sd)
    nest.Connect(pg, neuron, syn_spec={"weight": 20.})

    initial_time = time()
    nest.Simulate(simtime)
    runtime[model] = time() - initial_time

    stimes = nest.GetStatus(sd, "events")[0]["times"]
    rates[model] = len(stimes) / (5*60.)

print("Runtimes:", runtime)
print("Num. spikes:", rates)
