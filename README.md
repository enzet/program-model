# Program execution formal model #

:warning: This is a very rough draft. Use it on your own risk.

The main goal of the document is to propose a formal model of
  * concrete execution,
  * symbolic execution,
  * dynamic symbolic (concolic) execution,
  * and taint tracking.

## Build (Linux and macOS) ##

To create PDF run `./build.sh`.

Requirements:
  * LaTeX,
  * Python 3 (for SVG graph generation),
  * [Inkscape](https://inkscape.org/en/) (for image conversion from SVG to PDF).

## Graph generation ##

There is also simple graph drawing [Python module](generator).
It is used to generate execution sequences, execution paths,
control flow graphs, and symbolic execution trees.
