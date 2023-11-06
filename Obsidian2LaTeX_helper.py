import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


# We define a list subclass called lines that has a method to convert the list to a string
# It also has a method to get an boolean value if the specific item in the list starts with "$$"
class Lines(list):
    def __str__(self):
        return "\n".join(self)

    def is_math(self, index):
        return self[index].startswith("$$") and not (
            self[index + 1].startswith("\\begin{align}") or self[index - 1].startswith("\\end{align}")
        )

    def is_header(self, index):
        return self[index].startswith("#") and not self[index].startswith("##")

    def is_subheader(self, index):
        return self[index].startswith("##")

    def is_align(self, index):
        return self[index].startswith("$$") and (
            self[index + 1].startswith("\\begin{align}") or self[index - 1].startswith("\\end{align}")
        )


def convert(text):
    # We create a list of the lines in the text
    lines = Lines(text.split("\n"))

    # We loop through the lines and check if the line is a header
    for i in range(len(lines)):
        if lines.is_header(i):
            # If the line is a header we replace the "#" with the corresponding "\section{}"
            lines[i] = "\\section{" + lines[i].replace("# ", "") + "}"

    # We loop through the lines and check if the line is a subheader
    for i in range(len(lines)):
        if lines.is_subheader(i):
            # If the line is a subheader we replace the "##" with the corresponding "\subsection{}"
            lines[i] = "\\subsection{" + lines[i].replace("## ", "") + "}"

    # We loop through the lines and check if the line is a math environment
    last_was_end = True
    for i in range(len(lines)):
        if lines.is_math(i):
            # If the line is a math environment we replace the "$$"
            # with the corresponding "\begin{align}" and "\end{align}"
            if last_was_end:
                lines[i] = "\\[" + lines[i].replace("$$", "")
                last_was_end = False
            else:
                lines[i] = lines[i].replace("$$", "") + "\\]"
                last_was_end = True

    # We loop through the lines and check if the line is an align environment
    for i in range(len(lines)):
        if lines.is_align(i):
            # If the line is an align environment we replace the "$$"
            # with the corresponding an empty line
            lines[i] = ""

    # We join the items of lines to a string that will be returned
    output = ""
    output += str(lines) + "\n"

    # We get all ** in the text and replace them either with \\textbf{ or } depending on if it is the first or second
    while "**" in output:
        output = output.replace("**", "\\textbf{", 1)
        output = output.replace("**", "}", 1)

    # We get all * in the text and replace them either with \\textit{ or } depending on if it is the first or second
    while "*" in output:
        output = output.replace("*", "\\textit{", 1)
        output = output.replace("*", "}", 1)

    # We get all _ in the text and replace them either with \\underline{ or } depending on if it is the first or second
    while "_" in output:
        output = output.replace("_", "\\underline{", 1)
        output = output.replace("_", "}", 1)

    # We return the output string
    return output


def convert_MD2TeX(in_path, name, output_dir="output", template_dir="Template/standard_template.tex", author=""):
    # Creates a pathlib Path out of the output string input.
    output_dir = Path(output_dir)
    output_path = output_dir / ".TeX"

    # Creates a pathlib Path out of the template string input.
    template_dir = Path(template_dir)

    # Gets the content of the template file and stores it in the template variable
    with open(template_dir) as template:
        template_text = template.read()

    # Gets the content of the input MD file and stores it in the MDtext variable
    with open(in_path) as MD:
        MDtext = MD.read()

    # Creates the output path if it doesn't exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Runs the content from the MD file through the convert function to convert the syntax to a .tex compatible one
    text = convert(MDtext)

    # Creates a .tex file with the content we created
    file_path = output_path / (name + ".tex")

    # Replaces the content of the template file with the content we created
    text = template_text.replace("CONTENT", text).replace("TITLE", name).replace("AUTHOR", author)

    # Writes the content to the .tex file
    with open(file_path, "w") as file:
        file.write(text)


def bake_TeX(name, output_dir="output"):
    # Creates a pathlib Path out of the output string input
    output_dir = Path(output_dir)
    try:
        # Create a temporary directory and get its path
        temp_dir = Path(tempfile.mkdtemp())

        # Copy the generated .tex file in the temporary directory
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
