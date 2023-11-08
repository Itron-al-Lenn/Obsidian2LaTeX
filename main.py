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

        self.textbox_output_dir = QLineEdit(placeholderText=config["standard_paths"]["out_path"])
        self.textbox_output_dir.textChanged.connect(self.set_output_dir)

        self.textbox_template_dir = QLineEdit(placeholderText=config["standard_paths"]["template_path"])
        self.textbox_template_dir.textChanged.connect(self.set_template_dir)

        self.textbox_author = QLineEdit(placeholderText=config["standard_variables"]["author"])
        self.textbox_author.textChanged.connect(self.set_author)

        # Create the labels for the input fields
        self.label_in_path = QLabel("Path to the input file")
        self.label_name = QLabel("Name of the output file")
        self.label_output_dir = QLabel("Path to the output directory")
        self.label_template_dir = QLabel("Path to the template file")
        self.label_author = QLabel("Author of the document")

        # Create the layout
        layout = QVBoxLayout()

        # Add the labels and the input fields to the layout
        layout.addWidget(self.label_in_path)
        layout.addWidget(self.textbox_in_path)
        layout.addWidget(self.label_name)
        layout.addWidget(self.textbox_name)
        layout.addWidget(self.label_output_dir)
        layout.addWidget(self.textbox_output_dir)
        layout.addWidget(self.label_template_dir)
        layout.addWidget(self.textbox_template_dir)
        layout.addWidget(self.label_author)
        layout.addWidget(self.textbox_author)
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

    def set_output_dir(self, text):
        if text == "":
            str_input["output_dir"] = config["standard_paths"]["out_path"]
        else:
            str_input["output_dir"] = text

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_template_dir(self, text):
        if text == "":
            str_input["template_dir"] = config["standard_paths"]["template_path"]
        else:
            str_input["template_dir"] = text

        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

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
        output_dir=str_input["output_dir"],
        template_dir=str_input["template_dir"],
        author=str_input["author"],
    )
    bake_TeX(name=str_input["name"], output_dir=str_input["output_dir"])


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
        "output_dir": config["standard_paths"]["out_path"],
        "template_dir": config["standard_paths"]["template_path"],
        "author": config["standard_variables"]["author"],
    }

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
