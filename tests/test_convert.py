from Obsidian2LaTeX_helper import convert


def test_convert():
    obsidian_text = "# Heading\n\nSome **bold** and *italic* text."
    expected_latex = "\\section{Heading}\n\nSome \\textbf{bold} and \\textit{italic} text."
    converted = convert(obsidian_text)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_subheader():
    obsidian_text = "# Heading\n\n## Subheading\n\nSome **bold** and *italic* text."
    expected_latex = "\\section{Heading}\n\n\\subsection{Subheading}\n\nSome \\textbf{bold} and \\textit{italic} text."
    converted = convert(obsidian_text)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_math():
    obsidian_text = "# Heading\n\nSome **bold** and *italic* text.\n\n$$x^2 + y^2 = z^2\n$$\n\nMore text."
    expected_latex = "\\section{Heading}\n\nSome \\textbf{bold} and \\textit{italic} text.\n\n\\[x^2 + y^2 = z^2\n\\]\n\nMore text."  # noqa: E501
    converted = convert(obsidian_text)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_align():
    obsidian_text = "# Heading\n\nSome **bold** and *italic* text.\n\n$$\n\\begin{align}\nx &= y \nz &= w\n\\end{align}\n$$\n\nMore text."  # noqa: E501
    expected_latex = "\\section{Heading}\n\nSome \\textbf{bold} and \\textit{italic} text.\n\n\n\\begin{align}\nx &= y \nz &= w\n\\end{align}\n\n\nMore text."  # noqa: E501
    converted = convert(obsidian_text)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_bold():
    obsidian_text = "# Heading\n\nSome **bold** text."
    expected_latex = "\\section{Heading}\n\nSome \\textbf{bold} text."
    converted = convert(obsidian_text)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_italic():
    obsidian_text = "# Heading\n\nSome *italic* text."
    expected_latex = "\\section{Heading}\n\nSome \\textit{italic} text."
    converted = convert(obsidian_text)
    assert converted == expected_latex or converted == expected_latex + "\n"


def test_convert_underline():
    obsidian_text = "# Heading\n\nSome _underlined_ text."
    expected_latex = "\\section{Heading}\n\nSome \\underline{underlined} text."
    converted = convert(obsidian_text)
    assert converted == expected_latex or converted == expected_latex + "\n"