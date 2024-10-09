# Shortest path problem

Given a directed weighted graph, this problem proposes to find a path between two 
vertices in the graph such that the sum of the weights of its constituent edges is 
minimized.

Find [here](modeling.pdf) the model expressed mathematically.

## Installation

- Base enviornment: You should have installed Python and pip.
- Miniconda (or Conda): It provides the most straightforward installation of the solver, 
already compiled. Check out 
[this](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#term-Miniconda)
page.


## Development tools

- Type checking with flake8:
```bash
$ flake8 --max-line-length=89
```

## Running
```bash
$ python main.py
```

## Code structure
- `main.py`: Main execution file. It orchestrates the execution.
- `model.py`: Model definition and construction.
- `solver.py`: Defines the solver and its functions.
- `concrete_model_dump.txt`: Internal structure of the model (for debugging)
- `conda-env.yml`: Environment for Conda/Miniconda.
- `requirements.txt`: Requirements of the project.
