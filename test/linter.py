import pylint.lint
import pylint.reporters.text as text
import io
import os
import sys
import pathlib
for file in sys.argv[1:]:
    if(pathlib.Path(file).suffix==".py"):
        pylint_opts = ['--rcfile=test/pylintrc', file]
        pylint.lint.Run(pylint_opts)
