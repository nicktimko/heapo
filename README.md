# A Heap data type for Python

The goal of this repo is to build and document a heap object for eventual inclusion into Python.

## Mailing List Links

* [Python-ideas] Heap data type
  * mail.python.org Mailman thread: [Earliest (Apr 19, '09)][mailman-first] / [Latest (Dec 7, '09)][mailman-last]
  * [Google Groups thread][goog-groups]

## Heap Object spec

### Implemented
1. Provide all existing `heapq.heap*` functions provided by the [`heapq` module][heapq-py] as methods with identical semantics
2. Provide `collections.abc.Sequence` magic methods to the underlying heap structure
  * `__len__`
  * `__iter__`
  * `__getitem__`

### Todo
* Allow custom comparison/key operation

### Maybe
* ...

## Bling

+2 to legit

[![Travis CI][travis-badge]][travis-link]
[![Codecov.io][codecov-badge]][codecov-link]

[heapq-py]: https://docs.python.org/3/library/heapq.html
[goog-groups]: https://groups.google.com/d/topic/python-ideas/cLIAhBbQ8xA/discussion
[mailman-first]: https://mail.python.org/pipermail/python-ideas/2009-April/004173.html
[mailman-last]: https://mail.python.org/pipermail/python-ideas/2009-December/006634.html

[codecov-badge]: https://img.shields.io/codecov/c/github/nicktimko/heapo.svg?maxAge=2592000?style=flat-square
[codecov-link]: https://codecov.io/gh/nicktimko/heapo

[travis-badge]: https://img.shields.io/travis/nicktimko/heapo.svg?maxAge=2592000?style=flat-square
[travis-link]: https://travis-ci.org/nicktimko/heapo
