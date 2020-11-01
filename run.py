"""
Create main.pdf.
"""
import os
import subprocess

from pathlib import Path
from sys import platform
from typing import List

from generator.generate import Generator

INKSCAPE: str = "inkscape"
if platform == "darwin":
    INKSCAPE = "/Applications/Inkscape.app/Contents/Resources/bin/inkscape"

MAIN_ID: str = "main"

if __name__ == "__main__":
    generator = Generator("image")
    generator.generate()

    os.makedirs("pdf", exist_ok=True)
    for file_name in os.listdir("image"):  # type: str
        id_: str = file_name[:-4]
        command: List[str] = [
            INKSCAPE, "-z", "-A",
            str((Path(".") / "pdf" / f"{id_}.pdf").absolute()),
            str((Path(".") / "image" / f"{id_}.svg").absolute())]
        print(f"Converting {id_}...")
        subprocess.run(command)

    print("Creating PDF...")
    subprocess.run(["makeindex", MAIN_ID])
    subprocess.run(["bibtex", MAIN_ID])
    subprocess.run(["pdflatex", "-interaction=nonstopmode", MAIN_ID])
