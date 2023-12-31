from Obsidian2LaTeX_helper import convert

behavior = {
    "override_with_metadata": True,
    "use_current_date": True,
    "store_attachments": False,
    "table_of_contents": False,
}


def test_convert():
    obsidian_text = "# Heading\n\nSome **bold**."
    expected_latex = "\\section*{Heading}\n\nSome \\textbf{bold}. \\\\\n\n"
    converted, metadata, image_names, drawing_names = convert(obsidian_text, behavior)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_subheader():
    obsidian_text = "# Heading\n\n## Subheading\n\nSome **bold**."
    expected_latex = "\\section*{Heading}\n\n\\subsection*{Subheading}\n\nSome \\textbf{bold}. \\\\\n\n"
    converted, metadata, image_names, drawing_names = convert(obsidian_text, behavior)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_math():
    obsidian_text = "# Heading\n\nSome **bold**.\n\n$$x^2 + y^2 = z^2\n$$\n\nMore text."
    expected_latex = "\\section*{Heading}\n\nSome \\textbf{bold}. \\\\\n\n\\[x^2 + y^2 = z^2\n\\]\n\nMore text. \\\\\n\n"  # noqa: E501
    converted, metadata, image_names, drawing_names = convert(obsidian_text, behavior)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_align():
    obsidian_text = "# Heading\n\nSome **bold**.\n\n$$\n\\begin{align}\nx &= y \nz &= w\n\\end{align}\n$$\n\nMore text."  # noqa: E501
    expected_latex = "\\section*{Heading}\n\nSome \\textbf{bold}. \\\\\n\n\\begin{align*}\nx &= y  \\\\\nz &= w \\\\\n\\end{align*}\n\nMore text. \\\\\n\n"  # noqa: E501
    converted, metadata, image_names, drawing_names = convert(obsidian_text, behavior)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_bold():
    obsidian_text = "# Heading\n\nSome **bold** text."
    expected_latex = "\\section*{Heading}\n\nSome \\textbf{bold} text. \\\\\n"
    converted, metadata, image_names, drawing_names = convert(obsidian_text, behavior)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_italic():
    obsidian_text = "# Heading\n\nSome _italic_ text."
    expected_latex = "\\section*{Heading}\n\nSome \\textit{italic} text. \\\\\n"
    converted, metadata, image_names, drawing_names = convert(obsidian_text, behavior)
    assert converted == expected_latex or converted == expected_latex + "\n"
