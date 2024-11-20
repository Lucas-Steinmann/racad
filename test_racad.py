import unittest
from racad import get_attribute_docstring, get_attribute_docstrings
from enum import Enum

def some_decorator(cls):
    return cls

class ModuleLevelClass:
    f = 30
    """Docstring for f."""

class TestRACAD(unittest.TestCase):
    def test_simple_class(self):
        class MyClass:
            a = 5
            """Docstring for a."""
            b: int = 10
            """Docstring for b."""
        docs = get_attribute_docstrings(MyClass)
        self.assertEqual(docs['a'], 'Docstring for a.')
        self.assertEqual(docs['b'], 'Docstring for b.')

    def test_nested_class(self):
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

    def test_enum_class(self):
        class Color(Enum):
            RED = 1
            """Represents red color."""
            BLUE = 2
            """Represents blue color."""
        docs = get_attribute_docstrings(Color)
        self.assertEqual(docs['RED'], 'Represents red color.')
        self.assertEqual(docs['BLUE'], 'Represents blue color.')

    def test_class_in_function(self):
        def create_class():
            class DynamicClass:
                e = 25
                """Docstring for e."""
            return DynamicClass

        DynamicClass = create_class()
        docs = get_attribute_docstrings(DynamicClass)
        self.assertEqual(docs['e'], 'Docstring for e.')

    def test_class_at_module_level(self):
        # Class defined at the module level
        docs = get_attribute_docstrings(ModuleLevelClass)
        self.assertEqual(docs['f'], 'Docstring for f.')

    def test_attribute_without_docstring(self):
        class NoDocClass:
            g = 30
            # No docstring for g
        docs = get_attribute_docstrings(NoDocClass)
        self.assertNotIn('g', docs)

    def test_multiline_docstring(self):
        class MultiLineDocClass:
            h = 35
            """This is a
            multiline docstring
            for attribute h."""
        docs = get_attribute_docstrings(MultiLineDocClass)
        self.assertEqual(docs['h'], 'This is a\nmultiline docstring\nfor attribute h.')

    def test_attribute_with_comment(self):
        class CommentClass:
            i = 40
            # This is a comment, not a docstring
        docs = get_attribute_docstrings(CommentClass)
        self.assertNotIn('i', docs)

    def test_decorated_class(self):
        @some_decorator
        class DecoratedClass:
            j = 45
            """Docstring for j."""
        docs = get_attribute_docstrings(DecoratedClass)
        self.assertEqual(docs['j'], 'Docstring for j.')

if __name__ == '__main__':
    unittest.main()
