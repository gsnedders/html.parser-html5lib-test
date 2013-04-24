What is this?
=============

This is a very quickly hacked together harness to get the html5lib
tree construction tests running under Python 3's stdlib html.parser.

Why?
====

No, not _why. Why. Every so often (though really quite occasionally)
there's some debate on python-dev about the state of HTML parsing
support in the stdlib, given almost nobody uses html.parser, most
using one of BeautifulSoup, lxml.html, or html5lib. There's always
some debate where quite a few people claim it'd be simpler to fix
html.parser to comply with the HTML spec than it would be to import
html5lib, so I thought I'd see how html.parser does.

How?
====

html5lib-tests is a repo contains a bit over a thousand tests for the
parser, called "tree construction" tests. We run these, using code
hacked from html5lib-python, using nose. (If someone wants to make
them run under unittest, feel free to submit a pull request!)

So, how does html.parser fare?
==============================

Badly. Currently, ignoring the fragment tests (html.parser claims no
support for parsing fragments), the version included with Python 3.3.1
fails 1240 of 1240 tests. Um, yeah. Fairly certain my test harness
isn't to blame, either. html5lib, for comparison, fails 4… and that's
with running all the fragment tests.
