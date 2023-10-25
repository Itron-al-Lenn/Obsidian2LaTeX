import os
import shutil


def convert_MD2TeX(in_path, name):
    output_path = "output/.TeX"

    with open(in_path) as MD:
        MDtext = MD.read()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_path = os.path.join(output_path, name + ".tex")

    with open(file_path, "w") as file:
        file.write(MDtext)


def bake_TeX(name):
    output_path = "pdf/"

    os.chdir("output/")

    shutil.copy(
        "C:/Users/jolle/Desktop/Libary/Python/Obsidian2LaTeX/output/.TeX/" + name + ".tex",
        "C:/Users/jolle/Desktop/Libary/Python/Obsidian2LaTeX/output/" + name + ".tex",
    )

    os.system("pdflatex " + name + ".tex")

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    shutil.move(name + ".pdf", output_path + name + ".pdf")
