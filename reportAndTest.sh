#! /bin/bash
nosetests --with-coverage --cover-erase --cover-package=caMarkdown --cover-html

pylint --output-format=html --disable=C --disable=W0212 caMarkdown > cover/pylint.html

open "cover/index.html"
open "cover/pylint.html"
