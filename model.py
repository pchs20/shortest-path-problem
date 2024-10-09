from pyomo.environ import (
    AbstractModel,
    Binary,
    Constraint,
    Expression,
    minimize,
    NonNegativeReals,
    Objective,
    Param,
    Set,
    Var,
)
from pyomo.core.expr.relational_expr import EqualityExpression


def get_abstract_model() -> AbstractModel:
    model = AbstractModel(name='shortest-path')

    # Sets
    model.vertices = Set(
        name='vertices',
        doc='Vertices of the graph.',
        dimen=1
    )
    model.edges = Set(
        name='edges',
        doc='Edges of the graph.',
        dimen=2,
        within=model.vertices * model.vertices
    )

    # Parameters
    model.edge_weight = Param(
        model.edges,
        name='edge_weight',
        doc='Weight for each edge of the graph.',
        domain=NonNegativeReals,
    )
    model.start_vertex = Param(
        name='start_vertex',
        doc='Initial vertex for the path.',
        within=model.vertices,
    )
    model.end_vertex = Param(
        name='end_vertex',
        doc='Last vertex for the path.',
        within=model.vertices,
    )

    # Variables
    model.include_edge = Var(
        model.edges,
        name='include_edge',
        doc='Binary variable: 1 if edge is included in the path, 0 otherwise.',
        domain=Binary,
    )

    # Constraints
    model.constraint_start_of_the_path = Constraint(
        name='constraint_start_of_the_path',
        doc=constraint_start_of_the_path.__doc__,
        rule=constraint_start_of_the_path,
    )
    model.constraint_end_of_the_path = Constraint(
        name='constraint_end_of_the_path',
        doc=constraint_end_of_the_path.__doc__,
        rule=constraint_end_of_the_path,
    )
    model.constraint_adjacent_path = Constraint(
        model.vertices,
        name='constraint_adjacent_path',
        doc=constraint_adjacent_edges.__doc__,
        rule=constraint_adjacent_edges,
    )

    # Objective function
    model.objective_function = Objective(
        name='objective_function',
        doc='Minimize the sum of the edge weights that form the path.',
        rule=path_edges_weight,
        sense=minimize,
    )

    return model


# Constraints definition
def constraint_start_of_the_path(
        model: AbstractModel,
) -> EqualityExpression:
    """Define the beginning of the path.

    From the selected edges of the path, the initial vertex should have exactly one
    more outgoing edge than ingoing.
    """
    start_vertex = model.start_vertex.value
    outgoing_edges = _compute_outgoing_edges_of_a_vertex(model, start_vertex)
    ingoing_edges = _compute_ingoing_edges_of_a_vertex(model, start_vertex)
    return outgoing_edges == ingoing_edges + 1


def constraint_end_of_the_path(
        model: AbstractModel,
) -> EqualityExpression:
    """Define the end of the path.

    From the selected edges of the path, the last vertex should have exactly one more
    ingoing edge than outgoing.
    """
    end_vertex = model.end_vertex.value
    outgoing_edges = _compute_outgoing_edges_of_a_vertex(model, end_vertex)
    ingoing_edges = _compute_ingoing_edges_of_a_vertex(model, end_vertex)
    return outgoing_edges + 1 == ingoing_edges


def constraint_adjacent_edges(
        model: AbstractModel,
        vertex,
) -> EqualityExpression:
    """The path should be formed by adjacent edges.

    To guarantee that, every vertex (except for the initial and last ones) should have
    the same ingoing and outgoing selected edges.
    """
    if vertex in [model.start_vertex.value, model.end_vertex.value]:
        return Constraint.Skip
    outgoing_edges = _compute_outgoing_edges_of_a_vertex(model, vertex)
    ingoing_edges = _compute_ingoing_edges_of_a_vertex(model, vertex)
    return outgoing_edges == ingoing_edges


def _compute_outgoing_edges_of_a_vertex(model, vertex) -> Expression:
    outgoing_edges = sum(
        model.include_edge[(v, w)]
        for (v, w) in model.edges if v == vertex
    )
    return outgoing_edges


def _compute_ingoing_edges_of_a_vertex(model, vertex) -> Expression:
    ingoing_edges = sum(
        model.include_edge[(v, w)]
        for (v, w) in model.edges if w == vertex
    )
    return ingoing_edges


# Objective function definition
def path_edges_weight(model: AbstractModel) -> Expression:
    """Return the total weight for the included edges of the path."""
    return sum(
        model.edge_weight[edge] * model.include_edge[edge]
        for edge in model.edges
    )
