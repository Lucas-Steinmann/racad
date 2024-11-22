# RACAD
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Lucas-Steinmann/racad/unittest.yml?label=unittest)
[![pypi](https://img.shields.io/pypi/v/racad.svg)](https://pypi.python.org/pypi/racad)
[![versions](https://img.shields.io/pypi/pyversions/racad.svg)](https://github.com/Lucas-Steinmann/racad)
[![license](https://img.shields.io/github/license/Lucas-Steinmann/racad.svg)](https://github.com/Lucas-Steinmann/racad/blob/main/LICENSE)

RACAD stands for Runtime Access for Class Attribute Docstrings.
This is the source code accompanying [my blogpost](https://www.steinm.net/blog/runtime_accessible_class_attribute_docstrings/).

You can copy this code into your own project or use it as a library.

## Usage

Given a class defined as follows:

```python
class MyClass:
    a: int = 5
    """This is the docstring of a."""
```

to get the attribute docstring of one attribute of a class by its name, use:

```python
from racad import get_attribute_docstring

get_attribute_docstring(MyClass, 'a')
# Output: 'This is the docstring of a.'
```

alternatively, to get all docstrings of all attributes of a class, use:

```python
from racad import get_attribute_docstrings


get_attribute_docstrings(MyClass)
# Output: {'a': 'This is the docstring of a.'}
```

### Inheritance

If you want to also search the base classes, set `search_bases=True`:

```python
class MyChild(MyClass):
   b: str = "Hi"
   """This is the docstring for b."""

get_attribute_docstrings(MyChild, search_bases=True)
# Output: {'a': 'This is the docstring of a.', 'b': 'This is the docstring for b.'}
```

This also works for `get_attribute_docstring`.

## Limitation

Requires source code access via the `inspect` module. 
E.g. does not work if the class has been defined in a REPL.

