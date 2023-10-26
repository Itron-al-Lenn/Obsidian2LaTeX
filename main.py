from file_helper import delete_files_in_directory, get_file
from Obsidian2LaTeX_helper import bake_TeX, convert_MD2TeX


def main():
    name = "Test"
    get_file()
    convert_MD2TeX("test.md", name)
    bake_TeX(name)
    delete_files_in_directory("output")


if __name__ == "__main__":
    main()
