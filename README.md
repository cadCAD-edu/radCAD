# radCAD
![PyPI](https://badge.fury.io/py/radcad.svg)
[![Build Status](https://travis-ci.com/BenSchZA/radCAD.svg?branch=master)](https://travis-ci.com/BenSchZA/radCAD)

A [cadCAD](https://cadcad.org/) implementation in Rust, using PyO3 to generate Rust bindings for Python to be used as a native Python module. The performance and expressiveness of Rust, with the utility of the Python data-science stack.

See https://github.com/cadCAD-org/cadCAD

Goals:
* simple API for ease of use
* performance driven (more speed = more experiments, larger parameter sweeps, in less time)
* cadCAD compatible (standard functions, data structures, and simulation results)
* maintainable, testable codebase

## Features

* [x] Parameter sweeps

```python
params = {
    'a': [1, 2, 3],
    'b': [1]
}
```

* [x] Monte Carlo runs

```python
RUNS = 100 # Set to the number of Monte Carlo Runs
Simulation(model=model, timesteps=TIMESTEPS, runs=RUNS)
```

* [x] A/B tests

```python
model_a = Model(initial_state=states_a, state_update_blocks=state_update_blocks_a, params=params_a)
model_b = Model(initial_state=states_b, state_update_blocks=state_update_blocks_b, params=params_b)

simulation_1 = Simulation(model=model_a, timesteps=TIMESTEPS, runs=RUNS)
simulation_2 = Simulation(model=model_b, timesteps=TIMESTEPS, runs=RUNS)

# Simulate any number of models in parallel
data = run([simulation_1, simulation_2])
```

* [x] Parallel processing with multiple backend options: `multiprocessing`, `pathos`, `ray`
* [x] Distributed computing and remote execution in a cluster (AWS, GCP, Kubernetes, ...) using [Ray - Fast and Simple Distributed Computing](https://ray.io/)

* [x] cadCAD compatibility and familiar data structure

```bash
               a          b  simulation  subset  run  substep  timestep
0       1.000000        2.0           0       0    1        0         0
1       0.540302        2.0           0       0    1        1         1
2       0.540302        7.0           0       0    1        2         1
3       0.463338        7.0           0       0    1        1         2
4       0.463338       12.0           0       0    1        2         2
...          ...        ...         ...     ...  ...      ...       ...
799999  0.003162   999982.0           1       1    1        2     99998
800000  0.003162   999982.0           1       1    1        1     99999
800001  0.003162   999992.0           1       1    1        2     99999
800002  0.003162   999992.0           1       1    1        1    100000
800003  0.003162  1000002.0           1       1    1        2    100000
```

## Installation

```bash
pip install radcad
```

## Use

```python
from radcad import Model, Simulation
from radcad.engine import run

model = Model(initial_state=initial_state, state_update_blocks=state_update_blocks, params=params)
simulation = Simulation(model=model, timesteps=100_000, runs=1)

result = run(simulation)
# Or, multiple simulations: run([simulation_1, simulation_2, simulation_3])

df = pd.DataFrame(result)
```

### Remote Cluster Execution (using Ray)

Export the following AWS credentials (or see Ray documentation for alternative providers):
```bash
BACKEND=AWS
AWS_ACCESS_KEY_ID=***
AWS_SECRET_ACCESS_KEY=***
```

Start a new cluster (or use existing):
```bash
# Cluster config: single m5.large EC2 instance, us-west-2 region
ray up cluster/aws/minimal.yaml
# Test the connection
ray exec cluster/aws/minimal.yaml 'echo "hello world"'
```

Change the execution backend to `RAY_REMOTE`:
```python
from radcad.engine import run, Backend
import ray

# Connect to cluster head
ray.init(address='***:6379', _redis_password='***')

result = run(simulation, backend=Backend.RAY_REMOTE)
```

Finally, spin down the cluster:
```bash
ray down cluster/ray-aws.yaml
```

## Development

Build the [Rust](https://www.rust-lang.org/) core using [Nix](https://nixos.org/):
```bash
cd core/
nix-shell
make release
# or
make release-macos
```

Set up and enter the Python environment with [Poetry](https://python-poetry.org/):
```bash
poetry --help
poetry install
poetry env use python3
poetry shell
```

## Testing

```bash
poetry shell
python3 -m pytest
python3 -m unittest
```

## Benchmarking

See `benchmarks/`. radCAD has approximately a 10x speed increase over cadCAD locally - results may vary. Using Ray, potentially much better performance utilizing remote parallel processing.
