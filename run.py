import os
import subprocess

from generator.generate import Generator


if __name__ == "__main__":
    generator = Generator("image")
    generator.generate()

    os.makedirs("pdf", exist_ok=True)
    for file_name in generator.file_names:
        print(file_name)
