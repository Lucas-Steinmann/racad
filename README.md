# RACAD

RACAD stands for runtime accessible class attribute docstrings.
This is the source code accompaning [my blogpost](https://www.steinm.net/blog/runtime_accessible_class_attribute_docstrings/).

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


## Limitation

Requires source code access via the `inspect` module. 
E.g. does not work if the class has been defined in a REPL.

