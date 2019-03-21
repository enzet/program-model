<img align="right" width="400" src="https://raw.githubusercontent.com/enzet/program-model/master/out/first_page.png" />

# Program execution formal model #

This is a very rough draft. Use it on your own risk.

The main goal of the document is to propose a formal model of
  * concrete execution,
  * symbolic execution,
  * dynamic symbolic (concolic) execution,
  * and taint tracking.

## Build (Linux and macOS) ##

Run `./build.sh` to create PDF file `main.pdf`.

Requirements:
  * LaTeX,
  * Python 3 (for SVG graph generation),
  * [Inkscape](https://inkscape.org/en/) (for image conversion from SVG to PDF).

## Graph drawing ##

There is also a simple graph drawing [Python module](generator).
It is used to generate execution sequences, execution paths,
control flow graphs, and symbolic execution trees.
