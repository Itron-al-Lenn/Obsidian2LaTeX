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

# We define conditions to check if a line is a non standard math environment
# We define a list of math environments that are supported by LaTeX
math_environments = [
    "align",
    "align*",
    "equation",
    "equation*",
    "gather",
    "gather*",
    "multline",
    "multline*",
]


# We define a list subclass called lines that has a method to convert the list to a string
# It also has a method to get an boolean value if the specific item in the list starts with "$$"
class Lines(list):
    def __str__(self):
        return "\n".join(self)

    def is_math(self, index):
        return self[index].startswith("$$")

    def is_header(self, index):
        return self[index].startswith("#") and not self[index].startswith("##")

    def is_subheader(self, index):
        return self[index].startswith("##") and not self[index].startswith("###")

    def is_subsubheader(self, index):
        return self[index].startswith("###")

    def is_align(self, index):
        for i in math_environments:
            if self[index].startswith("\\begin{" + i + "}") or self[index].startswith("\\end{" + i + "}"):
                return True
        else:
            return False

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

    def has_excalidraw(self, index):
        if re.search(r"\!\[\[.*\.excalidraw(|.*)*\]\]", self[index]):
            return True

    def start_json(self, index):
        return self[index].startswith("```json")

    def end_json(self, index):
        return self[index].startswith("```")

    def is_chem(self, index):
        return "\\ce" in self[index]

    def is_table_comp_point(self, index):
        return re.search(r"-+[: ]*\|", self[index])


def convert(text, behavior):
    # We create a list of the lines in the text
    lines = Lines((text + "\n").split("\n"))

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

    # Handy tools which help us later
    last_was_end = True
    image_names = []
    drawing_names = []
    del_index = []
    id_to_check: list = []
    first_id = 0

    # We loop through the lines
    for i in range(len(lines)):
        # Check if the line is a header
        if lines.is_header(i):
            # If the line is a header we replace the "#" with the corresponding "\section{}"
            if behavior["table_of_contents"]:
                lines[i] = "\\section{" + lines[i].replace("# ", "") + "}"
            else:
                lines[i] = "\\section*{" + lines[i].replace("# ", "") + "}"

        # Check if the line is a subheader
        elif lines.is_subheader(i):
            # If the line is a subheader we replace the "##" with the corresponding "\subsection{}"
            if behavior["table_of_contents"]:
                lines[i] = "\\subsection{" + lines[i].replace("## ", "") + "}"
            else:
                lines[i] = "\\subsection*{" + lines[i].replace("## ", "") + "}"

        # Check if the line is a subsubheader
        elif lines.is_subsubheader(i):
            # If the line is a subsubheader we replace the "###" with the corresponding "\subsubsection{}"
            if behavior["table_of_contents"]:
                lines[i] = "\\subsubsection{" + lines[i].replace("### ", "") + "}"
            else:
                lines[i] = "\\subsubsection*{" + lines[i].replace("### ", "") + "}"

        # Check if the line is a math environment
        elif lines.is_math(i):
            # If the line one after or before is a align environment we add their index to an list
            if lines.is_align(i - 1) or lines.is_align(i + 1):
                del_index.append(i)
            else:
                # If the line is a math environment we replace the "$$"
                # with the corresponding "\\[" and "\\]"
                if last_was_end:
                    lines[i] = "\\[" + lines[i].replace("$$", "")
                else:
                    lines[i] = lines[i].replace("$$", "") + "\\]"
            if last_was_end:
                last_was_end = False
                first_id = i
            else:
                last_was_end = True
                id_pair: tuple = (first_id, i)
                id_to_check.append(id_pair)

        elif lines.is_table_comp_point(i):
            # We get the number of columns
            columns = lines[i].count("|") - 1
            # We get the number of rows
            rows = 0
            for j in range(i, len(lines)):
                if lines[j].endswith("|"):
                    rows += 1
                else:
                    break
            # We create a string with the correct number of columns
            columns_string = ""
            for j in range(columns):
                columns_string += "c|"
            # We delete the last "|" in the string
            columns_string = columns_string[:-1]
            # We get the content of the table
            row_content = []
            for j in range(i - 1, i + rows):
                row_content.append(lines[j].split("|")[1:-1])
            # We replace multipels of whitespace in the row_content with a single whitespace
            for key in range(rows + 1):
                for subkey, k in enumerate(row_content[key]):
                    new_content = re.sub(r"[\s]{2,}", " ", k, 0, re.MULTILINE)
                    row_content[key][subkey] = new_content

            # We create the string for the table
            lines[i - 1] = "\\begin{table}[H]\n\\centering\n\\begin{tabular}{" + columns_string + "}\n"
            new_content = ""
            for j in row_content[0]:
                new_content += j + " & "
            else:
                lines[i] = new_content[:-3] + " \\\\ \n\\hline"

            for j in range(2, rows + 1):
                new_content = ""
                for k in row_content[j]:
                    new_content += k + " & "
                else:
                    lines[i + j - 1] = new_content[:-3] + " \\\\ \n"

            lines[i + rows - 1] += "\n\\end{tabular}\n\\end{table}"

        elif re.search(r"[\w.\$]+[\s]*$", lines[i]):
            lines[i] = lines[i] + " \\\\"

        # These before were mutually exclusive, this is why we used elif

        # Check if the line is an image
        if lines.has_image(i):
            # We get the names of the image files and remove everything after the file extension
            for j in image_formats:
                if j in lines[i]:
                    image_names.append(lines[i].split("[[")[1].split(j)[0] + j)

            # If the line is an image we replace the "![" with the corresponding "\\includegraphics{}"
            lines[i] = lines[i].replace("![[", "\\begin{figure}[H]\n\\includegraphics[width=0.5\\textwidth]{", 1)
            lines[i] = re.sub(r"(\|.*)*\]\]", "}\\n\\\\centering\\n\\\\end{figure}", lines[i], 1)

        # Check if the line is an excalidraw
        if lines.has_excalidraw(i):
            # We get the names of the drawings and remove everything before the last "/" and after the file extension
            drawing_names.append(lines[i].split("[[")[1].split("/")[-1].split(".excalidraw")[0] + ".excalidraw.md")

            # If the line is an excalidraw we replace the "![" with the corresponding "\\includegraphics{}"
            lines[i] = re.sub(
                r"\!\[\[.*\/", "\\\\begin{figure}[H]\\n\\\\includegraphics[width=0.5\\\\textwidth]{", lines[i], 1
            )
            lines[i] = re.sub(r"\]\]", ".svg.png}\\n\\\\centering\\n\\\\end{figure}", lines[i], 1)

        if lines.is_chem(i):
            lines[i] = lines[i].replace("->", " -> ")

    # We ckeck if between the first and last id of the align and math environments are an empty line
    # If there is an empty line we add its index to the del_index list
    for i in id_to_check:
        for j in range(i[0], i[1]):
            if lines[j] == "":
                del_index.append(j)

    # We replace & with \\& in the lines that are not between the first and last id of the align and math environments
    for index, i in enumerate(id_to_check):
        if index == 0:
            for j in range(0, i[0]):
                lines[j] = re.sub(r"[^\\]&", r"\\&", lines[j], 0, re.MULTILINE)
        else:
            for j in range(id_to_check[index - 1][1], i[0]):
                lines[j] = re.sub(r"[^\\]&", r"\\&", lines[j], 0, re.MULTILINE)

    # We loop through the list of indexes and delete the corresponding lines
    del_index.sort()
    del_index.reverse()
    for i in del_index:
        del lines[i]

    # We join the items of lines to a string that will be returned
    output = ""
    for i in lines:
        output += i + "\n"

    # We get all ** in the text and replace them either with \\textbf{ or } depending on if it is the first or second
    while "**" in output:
        output = output.replace("**", "\\textbf{", 1)
        output = output.replace("**", "}", 1)

    # We get all _ in the text and replace them either with \\textit{ or } depending on if it is the first or second
    # unless it is followed by a {
    while "_ " in output:
        output = re.sub(r"_([^{])", r"\\textit{\1", output, 1)
        output = re.sub("_ ", "} ", output, 1)

    # Replace parameter characters with the normal ones
    output = output.replace("≤", "<=").replace("#", "\\#").replace("≥", ">=").replace("≠", "!=").replace("→", "->")

    # Replaces \pu with the LaTeX compatible \si
    output = output.replace("\\pu", "\\si")

    # Replace {align} with {align*}
    output = output.replace("{align}", "{align*}")

    # We return the output string, the metadata dictionary and the lists of image and drawing names
    return output, metadata, image_names, drawing_names


def convert_excalidraw(drawing_names, vault_path, attachment_path):
    # Convert the vault path to a pathlib Path
    vault_path = Path(vault_path)

    # We search the excalidraws in the vault and copy the json part of the file to the attachment path
    for i in drawing_names:
        for j in vault_path.rglob(i):
            new_file_name = j.name.split(".md")[0]
            with open(j) as file:
                content = file.read()
                content = content.split("```json")[1].split("```")[0]
                with open(attachment_path / new_file_name, "w") as file:
                    file.write(content)

            # We convert the excalidraws to .svg files using excalidraw_export
            username = os.getenv("username")
            subprocess.check_call(
                [rf"C:\Users\{username}\AppData\Roaming\npm\excalidraw_export.cmd", new_file_name], cwd=attachment_path
            )
            # We convert the .svg files to .png files using inkscape
            subprocess.check_call(
                [r"C:\Program Files\Inkscape\bin\inkscape.exe", "--export-type=png", new_file_name + ".svg"],
                cwd=attachment_path,
            )

            # We delete the .svg files
            os.remove(attachment_path / (new_file_name + ".svg"))


def convert_MD2TeX(string_input, behavior):
    in_path = Path(string_input["in_path"])
    out_path = Path(string_input["out_path"])
    file_name = string_input["file_name"]
    author = string_input["author"]
    template_path = Path(string_input["template_path"])
    date = string_input["date"]
    vault_path = Path(string_input["vault_path"])

    # We create a temporary directory and set it as the attachment path
    attachment_path = Path(tempfile.mkdtemp())

    # Creates a pathlib Path out of the output string input.
    out_path = Path(out_path)
    output_path = out_path / ".TeX"

    # Creates a pathlib Path out of the template string input.
    template_path = Path(template_path)

    # Gets the content of the template file and stores it in the template variable
    with open(template_path) as template:
        template_text = template.read()

    # If the tempalte conatins an uncommented line which creates a table of contents we set the behavior to true
    if not re.search(r"\%[\s]*\\tableofcontents", template_text) and re.search(r"\\tableofcontents", template_text):
        behavior["table_of_contents"] = True
    else:
        behavior["table_of_contents"] = False

    # Gets the content of the input MD file and stores it in the MDtext variable
    with open(in_path) as MD:
        MDtext = MD.read()

    # Creates the output path if it doesn't exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Runs the content from the MD file through the convert function to convert the syntax to a .tex compatible one
    text, metadata, image_names, drawing_names = convert(MDtext, behavior)

    # We search the images in the vault and copy them to the attachment path
    for i in image_names:
        for j in vault_path.rglob(i):
            shutil.copy(j, attachment_path)

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
        .replace("ATTACHMENT_PATH", (str(attachment_path).replace("\\", "/") + "/"))
        .replace("DATE", date)
    )

    # Writes the content to the .tex file
    with open(file_path, "w") as file:
        file.write(text)

    # We return the path to the temporary folder
    return attachment_path, drawing_names


def bake_TeX(string_input, temp_path):
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
        subprocess.check_call(["latexmk", "-pdf", str(temp_dir) + "/" + file_name + ".tex"], cwd=temp_dir)
        time.sleep(1)

        # Create the output directory for the .pdf if it doesn't exists
        if not os.path.exists(out_path / ".pdf/"):
            os.mkdir(out_path / ".pdf/")

        # Move the new .pdf file in the output/.pdf/ directory
        shutil.move(temp_dir / (file_name + ".pdf"), out_path / ".pdf" / (file_name + ".pdf"))

        # Delete the temporary folder and its contents
        shutil.rmtree(temp_dir)
        shutil.rmtree(temp_path)

        print(f"Temporary folder '{temp_dir}' has been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
        shutil.rmtree(temp_dir)
        shutil.rmtree(temp_path)
