import os

import platformdirs
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from tomlkit import parse

from Obsidian2LaTeX_helper import bake_TeX, convert_MD2TeX

# Add the specifications for platformdirs
appname = "Obsidian2LaTeX"
appauthor = "Itron al Lenn"

# Get the file path for the config file
config_dir = platformdirs.user_config_dir(appname=appname, appauthor=appauthor, ensure_exists=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the name of the main window and its size
        self.setWindowTitle("Obsidian2LaTeX")

        # Create the convert button
        self.button = QPushButton("Convert")
        self.button.clicked.connect(self.convert)
        if "" in str_input.values():
            self.button.setEnabled(False)

        # Create the input fields
        self.textbox_in_path = QLineEdit(placeholderText=config["standard_paths"]["in_path"])
        self.textbox_in_path.textChanged.connect(self.set_in_path)

        self.textbox_name = QLineEdit(placeholderText=config["standard_variables"]["file_name"])
        self.textbox_name.textChanged.connect(self.set_name)

        self.textbox_out_path = QLineEdit(placeholderText=config["standard_paths"]["out_path"])
        self.textbox_out_path.textChanged.connect(self.set_out_path)

        self.textbox_template_path = QLineEdit(placeholderText=config["standard_paths"]["template_path"])
        self.textbox_template_path.textChanged.connect(self.set_template_path)

        self.textbox_author = QLineEdit(placeholderText=config["standard_variables"]["author"])
        self.textbox_author.textChanged.connect(self.set_author)

        # Create the labels for the input fields
        label_in_path = QLabel("Path to the input file")
        label_name = QLabel("Name of the output file")
        label_out_path = QLabel("Path to the output directory")
        label_template_path = QLabel("Path to the template file")
        self.label_author = QLabel("Author of the document")

        # Creates BoxLayouts which combine the label and the input field
        in_path = QVBoxLayout()
        in_path.addWidget(label_in_path)
        in_path.addWidget(self.textbox_in_path)

        name = QVBoxLayout()
        name.addWidget(label_name)
        name.addWidget(self.textbox_name)

        out_path = QVBoxLayout()
        out_path.addWidget(label_out_path)
        out_path.addWidget(self.textbox_out_path)

        template_path = QVBoxLayout()
        template_path.addWidget(label_template_path)
        template_path.addWidget(self.textbox_template_path)

        author = QVBoxLayout()
        author.addWidget(self.label_author)
        author.addWidget(self.textbox_author)

        # Check if the standard template file contains AUTHOR
        # If it does, enable the author input field
        with open(config["standard_paths"]["template_path"]) as template_file:
            template = template_file.read()
            if "AUTHOR" in template:
                self.textbox_author.show()
                self.label_author.show()
                print("show")
            else:
                self.textbox_author.hide()
                self.label_author.hide()
                print("hide")

        # Create the layout
        layout = QVBoxLayout()

        # Add the elements to the layout
        layout.addLayout(name)
        layout.addLayout(in_path)
        layout.addLayout(out_path)
        layout.addLayout(template_path)
        layout.addLayout(author)
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
    def set_in_path(self, text):
        if text == "":
            str_input["in_path"] = config["standard_paths"]["in_path"]
        else:
            str_input["in_path"] = text

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_name(self, text):
        if text == "":
            str_input["name"] = config["standard_variables"]["file_name"]
        else:
            str_input["name"] = text

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_out_path(self, text):
        if text == "":
            str_input["out_path"] = config["standard_paths"]["out_path"]
        else:
            str_input["out_path"] = text

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_template_path(self, text):
        if text == "":
            str_input["template_path"] = config["standard_paths"]["template_path"]
        else:
            str_input["template_path"] = text

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

        # Check if the template file contains AUTHOR
        # If it does, enable the author input field
        with open(str_input["template_path"]) as template_file:
            template = template_file.read()
            if "AUTHOR" in template:
                self.textbox_author.show()
                self.label_author.show()
            else:
                self.textbox_author.hide()
                self.label_author.hide()
                print("hide")

    def set_author(self, text):
        if text == "":
            str_input["author"] = config["standard_variables"]["author"]
        else:
            str_input["author"] = text

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)


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

    # Create the input dictionary
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
