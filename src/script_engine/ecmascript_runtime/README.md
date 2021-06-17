This directory contains an implementation of ECMAScript (ECMA-262), ECMAScript
Internationalization API (ECMA-402), and The JSON data interchange syntax
(ECMA-404) on top of Dutyblasm runtime.

For now, the implementation conforms to the following editions of the standards:

- *none* (target: <https://ci.tc39.es/preview/tc39/ecma262/sha/c7d208f639c493ac221f1c3c4bd6a5c4b4b638b6/>
  merged into <https://github.com/tc39/ecma262>)

    To update grammar definition for parser generation, manually download
    `spec.html` from a target commit of <https://github.com/tc39/ecma262>, feed
    it to `{fecer_browser_root}/util/extract_grammar.py` and feed an output of
    the util to `ecmascript.grammar`.

- <https://402.ecma-international.org/7.0/> (*wip*)
- <https://www.ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf> (*wip*)

A conformance test suit for these standards is located in
`{fecer_browser_root}/tests/conformance_test262`.
