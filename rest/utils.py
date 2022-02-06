import ast
from collections import ChainMap
from inspect import getclosurevars, getsource
from textwrap import dedent


class CaseConverter:
    @staticmethod
    def camel_case_to_snake_case(field):
        output = ""
        for letter in field:
            if letter.upper() == letter and letter != "_":
                output += "_" + letter.lower()
            else:
                output += letter
        return output

    @staticmethod
    def snake_case_to_camel_case(field):
        output = ""
        next_case_upper = False

        for letter in field:
            if letter == "_":
                next_case_upper = True
            elif next_case_upper:
                output += letter.upper()
                next_case_upper = False
            else:
                output += letter
        return output


def get_exceptions(func, ids=set()):
    try:
        vars = ChainMap(*getclosurevars(func)[:3])
        source = dedent(getsource(func))
    except TypeError:
        return

    class _visitor(ast.NodeTransformer):
        def __init__(self):
            self.nodes = []
            self.other = []

        def visit_Raise(self, n):
            self.nodes.append(n.exc)

        def visit_Expr(self, n):
            if not isinstance(n.value, ast.Call):
                return
            c, ob = n.value.func, None
            if isinstance(c, ast.Attribute):
                parts = []
                while getattr(c, "value", None):
                    parts.append(c.attr)
                    c = c.value
                if c.id in vars:
                    ob = vars[c.id]
                    for name in reversed(parts):
                        ob = getattr(ob, name)

            elif isinstance(c, ast.Name):
                if c.id in vars:
                    ob = vars[c.id]

            if ob is not None and id(ob) not in ids:
                self.other.append(ob)
                ids.add(id(ob))

    v = _visitor()
    v.visit(ast.parse(source))
    for n in v.nodes:
        if isinstance(n, (ast.Call, ast.Name)):
            name = n.id if isinstance(n, ast.Name) else n.func.id
            if name in vars:
                yield vars[name]

    for o in v.other:
        yield from get_exceptions(o)
