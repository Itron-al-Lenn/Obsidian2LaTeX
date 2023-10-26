import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def convert_MD2TeX(in_path, name, Output_dir="output"):
    output_dir = Path(Output_dir)
    output_path = output_dir / ".TeX"

    with open(in_path) as MD:
        MDtext = MD.read()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_path = output_path / (name + ".tex")

    with open(file_path, "w") as file:
        file.write(MDtext)


def bake_TeX(name, Output_dir="output"):
    output_dir = Path(Output_dir)
    try:
        # Create a temporary directory and get its path
        temp_dir = Path(tempfile.mkdtemp())

        # Copy the generated .tex file in the temporary directory.
        shutil.copy(
            output_dir / ".TeX/" / (name + ".tex"),
            temp_dir / (name + ".tex"),
        )

        # Run pdflatex with the file in the temporary directory
        # and make sure that pdflatex is finished before the program continuous
        subprocess.check_call(["pdflatex", str(temp_dir) + "/" + name + ".tex"], cwd=temp_dir)
        time.sleep(1)

        # Create the output directory for the .pdf if it doesn't exists

        if not os.path.exists(output_dir / ".pdf/"):
            os.mkdir(output_dir / ".pdf/")

        # Move the new .pdf file in the output/.pdf/ directory
        shutil.move(temp_dir / (name + ".pdf"), output_dir / ".pdf" / (name + ".pdf"))

        # Delete the temporary folder and its contents
        shutil.rmtree(temp_dir)

        print(f"Temporary folder '{temp_dir}' has been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
