#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Extracts all normative Grammarkdown fragments from a Ecmarkup document.
#
# The documest is expected in a standard input, the extracted fragments are fed
# into a standard output.
#
# NOTE: for proper output of Unicode characters into a standard output, set
# PYTHONIOENCODING="utf-8" environment variable before calling this script.
# For Bash:
#
# ```bash
# PYTHONIOENCODING=utf8 python extract_grammar.py < spec.html > out.txt
# ```
#
# For Windows CMD (unlike bash keeps the parameter set after python is done):
#
# ```winbatch
# set PYTHONIOENCODING=utf8 && python extract_grammar.py < spec.html > out.txt
# ```

import html
import re
import sys
import textwrap

# To distinguish between non-normative examples and actual grammar, use `type`
# attribute of `emu-grammar` elements. The attribute is available since
# ECMAScript 2017:
#
# > tc39/ecma262@aab1ea3
# > Editorial: Add type attribute to emu-grammar elements
# >
# > The type attribute is used to define emu-grammar elements that are
# > example productions, defintions of new productions, or references to
# > existing productions. This is useful information for proper styling of
# > the document as well as for tooling scenarios.
# >
# > Closes #960.
#
# The closed issue tc39/ecma262#960:
#
# > The ecmarkup-vscode plugin can perform some static verification of grammar
# > during editing, but it needs to be able to distinguish between emu-grammar
# > elements that add definitive grammar to the document vs. elements that are
# > used for examples or static semantics.

spec = sys.stdin.read()
matches = re.findall(r"""<emu-grammar type="(.*?)">(.*?)<\/emu-grammar>""", spec, re.DOTALL)
for grammar in [match[1] for match in matches if match[0] == "definition"]:
    print(html.unescape(textwrap.dedent(grammar).lstrip()))
