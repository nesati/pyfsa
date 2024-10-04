FSA - Finite State Automaton processing in Python
-------------------------------------------------

This package contains functions for manipulating Finite-State Automata
(FSAs).  It includes functions for minimizing and determinizing FSAs,
computing FSA intersections and unions, compiling a (non-POSIX)
regular expression into an FSA, and compiling a set of regular
expression productions into a chart parser.

See the FSA_ module documentation for more information.

.. _FSA: FSA.html

About this fork
---------------

This fork improves regex syntax support. Notably:
- custom number of occurrences quantifier (e.g.: a{1,3})
- metacharacters in sets (e.g. [a-z\d])
