
import inspect
import textwrap
import ast

def get_attribute_docstrings(cls):
    source = inspect.getsource(cls)
    source = textwrap.dedent(source)
    tree = ast.parse(source)

    class AttributeDocstringVisitor(ast.NodeVisitor):
        def __init__(self):
            self.docs = {}

        def visit_ClassDef(self, node):
            for i, stmt in enumerate(node.body):
                if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                    # Get attribute name
                    if isinstance(stmt, ast.Assign):
                        if len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                            attr_name = stmt.targets[0].id
                    elif isinstance(stmt, ast.AnnAssign):
                        if isinstance(stmt.target, ast.Name):
                            attr_name = stmt.target.id
                    else:
                        continue

                    # Check if next statement is docstring
                    if i + 1 < len(node.body):
                        next_stmt = node.body[i + 1]
                        if isinstance(next_stmt, ast.Expr) and isinstance(next_stmt.value, ast.Constant) and isinstance(next_stmt.value.value, str):
                            docstring = next_stmt.value.value
                            docstring = inspect.cleandoc(docstring)
                            self.docs[attr_name] = docstring

            # Visit nested classes
            for stmt in node.body:
                if isinstance(stmt, ast.ClassDef):
                    self.visit(stmt)

    visitor = AttributeDocstringVisitor()
    visitor.visit(tree)
    return visitor.docs

def get_attribute_docstring(cls, attr_name):
    docs = get_attribute_docstrings(cls)
    return docs.get(attr_name)
