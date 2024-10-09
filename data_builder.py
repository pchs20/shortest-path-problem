from typing import Any, Dict, Optional


def get_problem_data() -> Dict[Optional[str], Any]:
    """Build and return input data for the problem."""
    return {
        None: {
            'vertices': {None: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']},
            'edges': {
                None: [
                    ('A', 'B'), ('B', 'H'), ('H', 'I'), ('I', 'J'),
                    ('A', 'C'), ('A', 'D'), ('D', 'E'),
                    ('A', 'G'), ('G', 'I'),
                    ('A', 'F'), ('F', 'D'),
                ]
            },
            'edge_weight': {
                ('A', 'B'): 1,
                ('B', 'H'): 1,
                ('H', 'I'): 1,
                ('I', 'J'): 1,
                ('A', 'C'): 1,
                ('A', 'D'): 1,
                ('D', 'E'): 1,
                ('A', 'G'): 1,
                ('G', 'I'): 1,
                ('A', 'F'): 1,
                ('F', 'D'): 1,
            },
            'start_vertex': {None: 'A'},
            'end_vertex': {None: 'B'},
        }
    }
