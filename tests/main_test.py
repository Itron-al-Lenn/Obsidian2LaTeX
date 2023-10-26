# import os

import pytest

from Obsidian2LaTeX_helper import convert_MD2TeX

# from Obsidian2LaTeX_helper import bake_TeX


@pytest.fixture(scope="function")
def temporary_md_file(tmp_path):
    # Create a temporary Markdown file for testing
    md_path = tmp_path / "test.md"
    with open(md_path, "w") as md_file:
        md_file.write("# Test Markdown\n\nThis is a test.")
    return md_path


def test_convert_MD2TeX(temporary_md_file, tmp_path):
    name = "test"
    in_path = temporary_md_file

    convert_MD2TeX(in_path, name, str(tmp_path))

    # Check if the .tex file was created
    assert in_path.is_file()
    out_path = tmp_path / ".TeX" / (name + ".tex")
    assert out_path.is_file()


# def test_bake_TeX(tmp_path):
#     name = "test"

#     # Create a temporary .tex file for testing
#     temp_dir = tmp_path / ".TeX"
#     os.makedirs(temp_dir)
#     with open(temp_dir / (name + ".tex"), "w") as tex_file:
#         tex_file.write("\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}")

#     # Run the bake_TeX function
#     bake_TeX(name, tmp_path)

#     # Check if the .pdf file was created in the output directory
#     output_pdf_path = tmp_path / ".pdf" / (name + ".pdf")
#     assert output_pdf_path.is_file()


# Add more test cases as needed
