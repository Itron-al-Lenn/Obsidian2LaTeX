import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

# We define a list of image formats that are supported by LaTeX
image_formats = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".eps", ".pdf"]

# We define a list of metadata that we want to use
important_metadata = ["title", "author", "date"]


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

    def has_metadata(self):
        if self[0].startswith("---"):
            # Find the end of the metadata
            for i in range(1, len(self)):
                if self[i].startswith("---"):
                    return True, i
            return False, None
        else:
            return False, None

    def has_image(self, index):
        for i in image_formats:
            if i in self[index]:
                return True


def convert(text):
    # We create a list of the lines in the text
    lines = Lines(text.split("\n"))

    # We create a dictionary for the metadata
    metadata = {}

    # When has_metadata is true we write the relevant metadata to the dictionary
    has_metadata, end_metadata = lines.has_metadata()
    if has_metadata:
        for i in range(1, end_metadata):
            key, value = lines[i].split(": ")
            for j in important_metadata:
                if key == j:
                    metadata[key] = value

    # If has_metadata is true we delete the metadata
    if has_metadata:
        del lines[0 : end_metadata + 1]

    # We loop through the lines and check if the line is a header
    for i in range(len(lines)):
        if lines.is_header(i):
            # If the line is a header we replace the "#" with the corresponding "\section{}"
            lines[i] = "\\section*{" + lines[i].replace("# ", "") + "}"

    # We loop through the lines and check if the line is a subheader
    for i in range(len(lines)):
        if lines.is_subheader(i):
            # If the line is a subheader we replace the "##" with the corresponding "\subsection{}"
            lines[i] = "\\subsection*{" + lines[i].replace("## ", "") + "}"

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

    # We loop through the lines and check if the line is an image
    for i in range(len(lines)):
        if lines.has_image(i):
            # If the line is an image we replace the "![" with the corresponding "\\includegraphics{}"
            lines[i] = lines[i].replace("![[", "\\includegraphics[width=\\textwidth]{", 1)
            for j in image_formats:
                if j in lines[i]:
                    lines[i] = re.sub(j + r".*\]\]", "}", lines[i], 1)
                    break

    # We loop through the lines and check if the line is an align environment
    del_index = []
    for i in range(len(lines)):
        if lines.is_align(i):
            # If the line is an align environment we add their index to an list
            del_index.append(i)

    # We loop through the list of indexes and delete the corresponding lines
    del_index.reverse()
    for i in del_index:
        del lines[i]

    # We join the items of lines to a string that will be returned
    output = ""
    output += str(lines) + "\n"

    # We get all ** in the text and replace them either with \\textbf{ or } depending on if it is the first or second
    while "**" in output:
        output = output.replace("**", "\\textbf{", 1)
        output = output.replace("**", "}", 1)

    # We get all _ in the text and replace them either with \\textit{ or } depending on if it is the first or second
    # unless it is followed by a {
    while "_ " in output:
        output = re.sub(r"_([^{])", r"\\textit{\1", output, 1)
        output = re.sub("_ ", "} ", output, 1)

    # Replaces \pu with the LaTeX compatible \si
    output = output.replace("\\pu", "\\si")

    # Replace {align} with {align*}
    output = output.replace("{align}", "{align*}")

    # We return the output string
    return output, metadata


def convert_MD2TeX(string_input, behavior):
    in_path = string_input["in_path"]
    out_path = string_input["out_path"]
    file_name = string_input["file_name"]
    author = string_input["author"]
    template_path = string_input["template_path"]
    attachment_path = string_input["attachment_path"]
    date = string_input["date"]

    # Creates a pathlib Path out of the output string input.
    out_path = Path(out_path)
    output_path = out_path / ".TeX"

    # Creates a pathlib Path out of the template string input.
    template_path = Path(template_path)

    # Gets the content of the template file and stores it in the template variable
    with open(template_path) as template:
        template_text = template.read()

    # Gets the content of the input MD file and stores it in the MDtext variable
    with open(in_path) as MD:
        MDtext = MD.read()

    # Creates the output path if it doesn't exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Runs the content from the MD file through the convert function to convert the syntax to a .tex compatible one
    text, metadata = convert(MDtext)

    # If the metadata dictionary is not empty we override the default values
    if behavior["override_with_metadata"]:
        if metadata:
            if "title" in metadata:
                file_name = metadata["title"]
            if "author" in metadata:
                author = metadata["author"]
            if "date" in metadata:
                date = metadata["date"]

    # Creates a .tex file with the content we created
    file_path = output_path / (file_name + ".tex")

    # Replaces the content of the template file with the content we created
    text = (
        template_text.replace("CONTENT", text)
        .replace("TITLE", file_name)
        .replace("AUTHOR", author)
        .replace("ATTACHMENT_PATH", attachment_path)
        .replace("DATE", date)
    )

    # Writes the content to the .tex file
    with open(file_path, "w") as file:
        file.write(text)


def bake_TeX(string_input):
    out_path = string_input["out_path"]
    file_name = string_input["file_name"]

    # Creates a pathlib Path out of the output string input
    out_path = Path(out_path)
    try:
        # Create a temporary directory and get its path
        temp_dir = Path(tempfile.mkdtemp())

        # Copy the generated .tex file in the temporary directory
        shutil.copy(
            out_path / ".TeX/" / (file_name + ".tex"),
            temp_dir / (file_name + ".tex"),
        )

        # Run pdflatex with the file in the temporary directory
        # and make sure that pdflatex is finished before the program continuous
        subprocess.check_call(["pdflatex", str(temp_dir) + "/" + file_name + ".tex"], cwd=temp_dir)
        time.sleep(1)

        # Create the output directory for the .pdf if it doesn't exists
        if not os.path.exists(out_path / ".pdf/"):
            os.mkdir(out_path / ".pdf/")

        # Move the new .pdf file in the output/.pdf/ directory
        shutil.move(temp_dir / (file_name + ".pdf"), out_path / ".pdf" / (file_name + ".pdf"))

        # Delete the temporary folder and its contents
        shutil.rmtree(temp_dir)

        print(f"Temporary folder '{temp_dir}' has been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
