"""Module for retrieving docstrings of class attributes at runtime."""

import inspect
import textwrap
import ast
from typing import Any, Dict, Optional, Type

class AttributeDocstringVisitor(ast.NodeVisitor):
    """AST NodeVisitor that collects docstrings of class attributes.
    
    Attributes of nested classes are ignored.
    Multiple class definitions as siblings are not supported and will lead
    to an undefined output.
    """

    def __init__(self) -> None:
        """Initialize the visitor with an empty docs dictionary."""
        self.docs: Dict[str, str] = {}
        self.last_attr_name: Optional[str] = None
        # Indicates if a parent already is a class definition.
        # We skip nested classes. Otherwise, the attributes of nested classes
        # would be added to the top class.
        self._in_ClassDef: bool = False

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class definition node.

        Args:
            node: The class definition AST node to visit.
        """
        if self._in_ClassDef:
            # skip nested classes
            self.last_attr_name = None
            return
        self._in_ClassDef = True
        # Visit all statements in the class body
        for stmt in node.body:
            self.visit(stmt)
        # Reset the last attribute name after processing the class
        self.last_attr_name = None
        # Reset the flag that we are in a class definition
        self._in_ClassDef = False
    
    def _store_target_attr_name(self, target: ast.expr) -> None:
        if isinstance(target, ast.Name):
            self.last_attr_name = target.id
        else:
            self.last_attr_name = None

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit an assignment node.

        Args:
            node: The assignment AST node to visit.
        """
        # Handle simple assignments
        if len(node.targets) == 1: 
            self._store_target_attr_name(node.targets[0])
        else:
            # Ignore multi assignments such as `a = b = 5`
            self.last_attr_name = None

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Visit an annotated assignment node.

        Args:
            node: The annotated assignment AST node to visit.
        """
        # Handle annotated assignments
        self._store_target_attr_name(node.target)

    def visit_Expr(self, node: ast.Expr) -> None:
        """Visit an expression node.

        Args:
            node: The expression AST node to visit.
        """
        # Check if the expression is a docstring for the last attribute
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            if self.last_attr_name:
                # Removes leading/trailing whitespace 
                # (especially necessary for multi-line docstrings)
                docstring = inspect.cleandoc(node.value.value)
                self.docs[self.last_attr_name] = docstring
        # Reset the last attribute name after processing
        self.last_attr_name = None


def _get_attribute_docstrings(
        cls: Type[Any], 
) -> Dict[str, str]:
    try:
        source = inspect.getsource(cls)
    except (TypeError, OSError):
        # TypeError is raised for built-in classes
        # OSError is raised for classes defined in the interactive shell
        return {}
    source = textwrap.dedent(source)
    tree = ast.parse(source)

    visitor = AttributeDocstringVisitor()
    visitor.visit(tree)
    return visitor.docs


def _recursive_collect(class_list):
    if len(class_list) == 0:
        return {}
    base_docs = _recursive_collect(class_list[1:])
    base_docs.update(_get_attribute_docstrings(class_list[0]))
    return base_docs


def get_attribute_docstrings(
        cls: Type[Any], 
        search_bases: bool = False
) -> Dict[str, str]:
    """Get the docstrings of all attributes of a class.

    Args:
        cls: The class to inspect.
        search_bases: If true, follows the MRO and merges the docstrings.
            Docstrings of attributes take earlier in the MRO 
            take precedence in the case of name conflicts.

    Returns:
        A dictionary mapping attribute names to their docstrings.
    """
    class_list = cls.__mro__ if search_bases else [cls]
    return _recursive_collect(class_list)


def get_attribute_docstring(
        cls: Type[Any], 
        attr_name: str,
        search_bases: bool = False
) -> Optional[str]:
    """Get the docstring of a specific class attribute.

    Args:
        cls: The class to inspect.
        attr_name: The name of the attribute.
        search_bases: If true, follows the MRO until it finds a docstring.

    Returns:
        The docstring of the attribute, or None if not found.
    """
    class_list = cls.__mro__ if search_bases else [cls]
    doc = None
    for _cls in class_list:
        docs = _get_attribute_docstrings(_cls)
        doc = docs.get(attr_name)
        if doc is not None:
            break
    return doc
