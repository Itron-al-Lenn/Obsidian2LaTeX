import os

import platformdirs
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from tomlkit import parse

from Obsidian2LaTeX_helper import bake_TeX, convert_MD2TeX

# Add the specifications for platformdirs
appname = "Obsidian2LaTeX"
appauthor = "Itron al Lenn"

# Get the file path for the config file
config_dir = platformdirs.user_config_dir(appname=appname, appauthor=appauthor, ensure_exists=True)

# Create dictionary for the config keys
config_key = {
    "in_path": "standard_paths",
    "out_path": "standard_paths",
    "template_path": "standard_paths",
    "file_name": "standard_variables",
    "author": "standard_variables",
}

# Create dictionary for the file filters
file_filter = {
    "in_path": "Markdown (*.md)",
    "template_path": "LaTeX (*.tex)",
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the name of the main window and its size
        self.setWindowTitle("Obsidian2LaTeX")
        self.resize(500, 300)

        # Create the convert button
        self.button = QPushButton("Convert")
        self.button.clicked.connect(self.convert)

        # Create the input fields
        self.lineedit_in_path = QLineEdit(placeholderText=config["standard_paths"]["in_path"])
        self.lineedit_in_path.textChanged.connect(lambda text: self.set_lineedit("in_path", text))

        self.lineedit_file_name = QLineEdit(placeholderText=config["standard_variables"]["file_name"])
        self.lineedit_file_name.textChanged.connect(lambda text: self.set_lineedit("file_name", text))

        self.lineedit_out_path = QLineEdit(placeholderText=config["standard_paths"]["out_path"])
        self.lineedit_out_path.textChanged.connect(lambda text: self.set_lineedit("out_path", text))

        self.lineedit_template_path = QLineEdit(placeholderText=config["standard_paths"]["template_path"])
        self.lineedit_template_path.textChanged.connect(lambda text: self.set_lineedit("template_path", text))

        self.lineedit_author = QLineEdit(placeholderText=config["standard_variables"]["author"])
        self.lineedit_author.textChanged.connect(lambda text: self.set_lineedit("author", text))

        # Create the labels for the input fields
        label_in_path = QLabel("Path to the input file")
        label_file_name = QLabel("Name of the output file")
        label_out_path = QLabel("Path to the output directory")
        label_template_path = QLabel("Path to the template file")
        self.label_author = QLabel("Author of the document")

        # Create the buttons for the input fields
        self.btn_in_path = QPushButton("in_path", text="Browse")
        self.btn_in_path.clicked.connect(lambda: self.browse_file("in_path"))

        self.btn_out_path = QPushButton("out_path", text="Browse")
        self.btn_out_path.clicked.connect(lambda: self.browse_dir("out_path"))

        self.btn_template_path = QPushButton("template_path", text="Browse")
        self.btn_template_path.clicked.connect(lambda: self.browse_file("template_path"))

        # Creates BoxLayouts which combine the input field and the button
        textbox_in_path = QHBoxLayout()
        textbox_in_path.addWidget(self.lineedit_in_path)
        textbox_in_path.addWidget(self.btn_in_path)

        textbox_out_path = QHBoxLayout()
        textbox_out_path.addWidget(self.lineedit_out_path)
        textbox_out_path.addWidget(self.btn_out_path)

        textbox_template_path = QHBoxLayout()
        textbox_template_path.addWidget(self.lineedit_template_path)
        textbox_template_path.addWidget(self.btn_template_path)

        # Creates BoxLayouts which combine the label and the input field
        in_path = QVBoxLayout()
        in_path.addWidget(label_in_path)
        in_path.addLayout(textbox_in_path)

        out_path = QVBoxLayout()
        out_path.addWidget(label_out_path)
        out_path.addLayout(textbox_out_path)

        template_path = QVBoxLayout()
        template_path.addWidget(label_template_path)
        template_path.addLayout(textbox_template_path)

        name = QVBoxLayout()
        name.addWidget(label_file_name)
        name.addWidget(self.lineedit_file_name)

        author = QVBoxLayout()
        author.addWidget(self.label_author)
        author.addWidget(self.lineedit_author)

        # Check if the standard template file contains AUTHOR
        # If it does, enable the author input field
        with open(config["standard_paths"]["template_path"]) as template_file:
            template = template_file.read()
            if "AUTHOR" in template:
                self.lineedit_author.show()
                self.label_author.show()
                print("show")
            else:
                self.lineedit_author.hide()
                self.label_author.hide()
                str_input["author"] = None
                print("hide")

        # Disable the convert button if one of the input fields is empty
        if "" in str_input.values():
            self.button.setEnabled(False)

        # Create the layout
        layout = QVBoxLayout()

        # Add the elements to the layout
        layout.addLayout(name)
        layout.addLayout(author)
        layout.addLayout(in_path)
        layout.addLayout(out_path)
        layout.addLayout(template_path)
        layout.addWidget(self.button)

        # Create the container widget and set the layout
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(container)

    # Define that the main function runs after pressing the button
    def convert(self):
        main()

    # Define the input functions for the text fields
    def set_lineedit(self, lbl, text):
        if text == "":
            str_input[lbl] = config[config_key[lbl]][lbl]
        else:
            str_input[lbl] = text
        # Check if the template file contains AUTHOR
        # If it does, enable the author input field
        if lbl == "template_path":
            if os.path.exists(str_input[lbl]):
                with open(str_input[lbl]) as template_file:
                    template = template_file.read()
                    if "AUTHOR" in template:
                        self.lineedit_author.show()
                        self.label_author.show()
                        str_input["author"] = config["standard_variables"]["author"]
                    else:
                        self.lineedit_author.hide()
                        self.label_author.hide()
                        str_input["author"] = None
                        print("hide")

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    # Define the input functions for the browse_file buttons
    def browse_file(self, lbl):
        name = QFileDialog.getOpenFileName(self, "Select Directory", str_input[lbl], file_filter[lbl])[0]
        if name:
            if lbl == "in_path":
                self.lineedit_in_path.setText(name)
            elif lbl == "template_path":
                self.lineedit_template_path.setText(name)

    # Define the input functions for the browse_dir buttons
    def browse_dir(self, lbl):
        name = QFileDialog.getExistingDirectory(self, "Select Directory", str_input[lbl])
        if name:
            if lbl == "out_path":
                self.lineedit_out_path.setText(name)


def main():
    convert_MD2TeX(
        in_path=str_input["in_path"],
        name=str_input["name"],
        out_path=str_input["out_path"],
        template_path=str_input["template_path"],
        author=str_input["author"],
    )
    bake_TeX(name=str_input["name"], out_path=str_input["out_path"])


if __name__ == "__main__":
    # If no config file exists, create one and write the content of the default config file into it
    if not os.path.exists(config_dir + "/config.toml"):
        with open(config_dir + "/config.toml", "w") as config_file:
            with open("config_preset.toml") as preset_config_file:
                config_file.write(preset_config_file.read())

    # Read the config file
    with open(config_dir + "/config.toml") as config_file:
        config = parse(config_file.read())

    # Set the standard values for the input fields
    str_input = {
        "in_path": config["standard_paths"]["in_path"],
        "name": config["standard_variables"]["file_name"],
        "out_path": config["standard_paths"]["out_path"],
        "template_path": config["standard_paths"]["template_path"],
        "author": config["standard_variables"]["author"],
    }

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
