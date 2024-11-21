"""Unit tests for the RACAD module."""

import unittest
from racad import get_attribute_docstring, get_attribute_docstrings
from enum import Enum
from typing import Any

def some_decorator(cls: Any) -> Any:
    return cls

class ModuleLevelClass:
    """Class defined at the module level for testing."""
    f = 30
    """Docstring for f."""


class TestRACAD(unittest.TestCase):
    """Test cases for the RACAD functions."""

    def test_simple_class(self) -> None:
        """Test retrieving docstrings from a simple class."""
        class MyClass:
            a = 5
            """Docstring for a."""
            b: int = 10
            """Docstring for b."""
        docs = get_attribute_docstrings(MyClass)
        self.assertEqual(docs['a'], 'Docstring for a.')
        self.assertEqual(docs['b'], 'Docstring for b.')

    def test_nested_class(self) -> None:
        """Test retrieving docstrings from a nested class."""
        class OuterClass:
            c = 15
            """Docstring for c."""

            class InnerClass:
                d = 20
                """Docstring for d."""
        docs_outer = get_attribute_docstrings(OuterClass)
        self.assertEqual(docs_outer['c'], 'Docstring for c.')

        docs_inner = get_attribute_docstrings(OuterClass.InnerClass)
        self.assertEqual(docs_inner['d'], 'Docstring for d.')

    def test_enum_class(self) -> None:
        """Test retrieving docstrings from an enum class."""
        class Color(Enum):
            RED = 1
            """Represents red color."""
            BLUE = 2
            """Represents blue color."""
        docs = get_attribute_docstrings(Color)
        self.assertEqual(docs['RED'], 'Represents red color.')
        self.assertEqual(docs['BLUE'], 'Represents blue color.')

    def test_class_in_function(self) -> None:
        """Test retrieving docstrings from a class defined in a function."""
        def create_class():
            class DynamicClass:
                e = 25
                """Docstring for e."""
            return DynamicClass

        DynamicClass = create_class()
        docs = get_attribute_docstrings(DynamicClass)
        self.assertEqual(docs['e'], 'Docstring for e.')

    def test_class_at_module_level(self) -> None:
        """Test retrieving docstrings from a module-level class."""
        # Class defined at the module level
        docs = get_attribute_docstrings(ModuleLevelClass)
        self.assertEqual(docs['f'], 'Docstring for f.')

    def test_attribute_without_docstring(self) -> None:
        """Test handling attributes without docstrings."""
        class NoDocClass:
            g = 30
            # No docstring for g
        docs = get_attribute_docstrings(NoDocClass)
        self.assertNotIn('g', docs)

    def test_multiline_docstring(self) -> None:
        """Test retrieving multiline docstrings."""
        class MultiLineDocClass:
            h = 35
            """This is a
            multiline docstring
            for attribute h."""
        docs = get_attribute_docstrings(MultiLineDocClass)
        self.assertEqual(docs['h'], 'This is a\nmultiline docstring\nfor attribute h.')

    def test_attribute_with_comment(self) -> None:
        """Test that comments are not mistaken for docstrings."""
        class CommentClass:
            i = 40
            # This is a comment, not a docstring
        docs = get_attribute_docstrings(CommentClass)
        self.assertNotIn('i', docs)

    def test_decorated_class(self) -> None:
        """Test retrieving docstrings from a decorated class."""
        @some_decorator
        class DecoratedClass:
            j = 45
            """Docstring for j."""
        docs = get_attribute_docstrings(DecoratedClass)
        self.assertEqual(docs['j'], 'Docstring for j.')

    def test_get_attribute_docstring(self) -> None:
        """Test the get_attribute_docstring function."""
        class SampleClass:
            x = 100
            """Docstring for x."""
            y = 200
            # No docstring for y

        # Test attribute with docstring
        doc_x = get_attribute_docstring(SampleClass, 'x')
        self.assertEqual(doc_x, 'Docstring for x.')

        # Test attribute without docstring
        doc_y = get_attribute_docstring(SampleClass, 'y')
        self.assertIsNone(doc_y)

        # Test non-existent attribute
        doc_z = get_attribute_docstring(SampleClass, 'z')
        self.assertIsNone(doc_z)

    def test_builtin_class(self) -> None:
        """Test that built-in classes return empty dictionaries."""
        # Built-in classes don't have accessible source code
        docs = get_attribute_docstrings(list)
        self.assertEqual(docs, {})

        docs = get_attribute_docstrings(dict)
        self.assertEqual(docs, {})

    def test_string_defined_class(self) -> None:
        """Test retrieving docstrings from a class defined in a string."""
        class_def = """
class StringDefinedClass:
    k = 50
    '''Docstring for k.'''
    
    l: int = 60
    '''Docstring for l.'''
"""
        namespace = {}
        exec(class_def, namespace)
        StringDefinedClass = namespace['StringDefinedClass']

        docs = get_attribute_docstrings(StringDefinedClass)
        self.assertEqual(docs, {})

if __name__ == '__main__':
    unittest.main()
