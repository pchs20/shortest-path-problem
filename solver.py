from typing import Optional

from pyomo.environ import ConcreteModel, SolverFactory, SolverStatus, value
from pyomo.opt.results import SolverResults


class Solver:
    def __init__(self, concrete_model: ConcreteModel):
        self.concrete_model: ConcreteModel = concrete_model
        self._solution: Optional[SolverResults] = None

    def solve(self) -> None:
        solver = SolverFactory('scip')
        solver.options['limits/time'] = 300
        self._solution = solver.solve(self.concrete_model, tee=True)

    def solution_exists(self) -> bool:
        solution_found = (
            self._solution.solver.status == SolverStatus.ok or
            self._solution.solver.status == SolverStatus.warning
        )
        return solution_found

    def print_solution(self) -> None:
        assert self.solution_exists(), 'The solver did not find any solution!'

        print()
        print('SOLUTION')
        total_weight = int(value(self.concrete_model.objective_function))
        print('Total weight: ' + str(total_weight))
        print('Path edges: ')
        for edge in self.concrete_model.edges:
            include_edge = bool(self.concrete_model.include_edge[edge].value)
            print(str(edge) + ': ' + str(include_edge))
        print()
