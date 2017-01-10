# Sparkstruck Python Code

## Dependencies

All code is written using python 3.5. Specific python dependencies are stored within `requirements.txt`.

Install python dependencies using `pip`.
```bash
$ pip3 install -r requirements.txt
```

Update dependencies with `pip`.
```bash
$ pip3 freeze > requirements.txt
```

## Standards

Code should follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) standards for code style. Using a linter like [flake8](http://flake8.readthedocs.io/en/latest/) to verify code meets PEP8 standards is recommended.

## Environment

Developers are encouraged to use [virtualenv](https://virtualenv.pypa.io/en/stable/) to maintain a clean environment for developing python code.

## Handling graphs in python

[`networkx`]((http://networkx.readthedocs.io/en/networkx-1.11/)) is a Python module for handling graph objects. It enables easy reading and writing to files, conversion between graph objects and various matrices related to graphs, and a variety of  useful tools for computing on / exploring graphs.

Functions for generating graphs can be found [here](https://networkx.github.io/documentation/development/reference/generators.html).
