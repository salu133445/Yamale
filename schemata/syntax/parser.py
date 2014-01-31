import ast

from schemata import validators as val

# Get all validators in here for eval()
from schemata.validators.validators import *

# Allow validator strings to contain either tags or actual name
tags = {v.__tag__: v.__name__ for v in val.TYPES}
tags.update({v.__name__: v.__name__ for v in val.TYPES})


def parse(validator_string, custom_types=None):
    if custom_types is None:
        custom_types = ()

    try:
        tree = ast.parse(validator_string, mode='eval')

        for node in ast.walk(tree):
            node = _process_node(node)

        validator = eval(compile(tree, '<ast>', 'eval'))

        return validator
    except KeyError:
        raise SyntaxError('Invalid validation syntax in: %s' % validator_string)


def _process_node(node):
    if isinstance(node, ast.Call):
        # Only allow functions we list in `tags`
        node.func.id = tags[node.func.id]
