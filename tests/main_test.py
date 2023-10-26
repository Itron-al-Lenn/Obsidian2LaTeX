import os

import pytest

from Obsidian2LaTeX_helper import bake_TeX, convert_MD2TeX

# Define a temporary test directory for test files
TEST_DIR = "test_files"


@pytest.fixture(scope="module")
def setup_teardown():
    # Setup: Create a temporary directory for testing
    os.makedirs(TEST_DIR)

    yield

    # Teardown: Remove the temporary directory and its contents
    if os.path.exists(TEST_DIR):
        for filename in os.listdir(TEST_DIR):
            file_path = os.path.join(TEST_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(TEST_DIR)


def test_convert_MD2TeX(setup_teardown):
    # Test the convert_MD2TeX function

    # Create a test Markdown file
    test_md_content = "This is a test markdown content."
    test_md_file = os.path.join(TEST_DIR, "test.md")
    with open(test_md_file, "w") as md_file:
        md_file.write(test_md_content)

    # Call the function to convert Markdown to LaTeX
    convert_MD2TeX(test_md_file, "test")

    # Check if the LaTeX file is created
    assert os.path.isfile(os.path.join(TEST_DIR, "test.tex"))


def test_bake_TeX(setup_teardown):
    # Test the bake_TeX function

    # Create a test LaTeX file
    test_tex_content = r"\documentclass{article}\begin{document}This is a test LaTeX content.\end{document}"
    test_tex_file = os.path.join(TEST_DIR, "test.tex")
    with open(test_tex_file, "w") as tex_file:
        tex_file.write(test_tex_content)

    # Call the function to bake LaTeX into PDF
    bake_TeX("test")

    # Check if the PDF file is created
    assert os.path.isfile(os.path.join(TEST_DIR, "test.pdf"))


if __name__ == "__main__":
    pytest.main()
