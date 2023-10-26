import os
import shutil
import time


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
    output_path = ".pdf/"

    os.chdir("output/")

    shutil.copy(
        ".TeX/" + name + ".tex",
        name + ".tex",
    )

    os.system("pdflatex " + name + ".tex")

    time.sleep(1)

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    shutil.move(name + ".pdf", output_path + name + ".pdf")
