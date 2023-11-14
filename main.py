import os
import re
from pathlib import Path

import platformdirs
import tomlkit
from PySide6.QtCore import QDate
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDateEdit,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

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
    "date": "standard_variables",
    "attachment_path": "standard_paths",
}

# Create dictionary for the file filters
file_filter = {
    "in_path": "Markdown (*.md)",
    "template_path": "LaTeX (*.tex)",
}


class MainWindow(QMainWindow):
    """This is the main window of the application."""

    def __init__(self):
        super().__init__()

        # Addes a debug action on a key shortcut which prints the content of the str_input dictionary
        self.debug_action = QAction(self)
        self.debug_action.setShortcut("Ctrl+D")
        self.debug_action.triggered.connect(lambda: print(str_input))
        self.addAction(self.debug_action)

        # Set the name of the main window and its size
        self.setWindowTitle("Obsidian2LaTeX")
        self.resize(800, 450)

        # Addes menu bar
        menu = self.menuBar()

        # Addes the settings button to the menu bar
        self.settings_button = QAction("Settings", self)
        self.settings_button.triggered.connect(self.open_settings_window)

        menu.addAction(self.settings_button)

        # Create the convert button
        self.button = QPushButton("Convert")
        self.button.clicked.connect(self.convert)

        # Create the input fields
        self.lineedit_in_path = QLineEdit(text=config["standard_paths"]["in_path"])
        self.lineedit_in_path.textChanged.connect(lambda text: self.set_lineedit("in_path", text))

        self.lineedit_file_name = QLineEdit(placeholderText=config["standard_variables"]["file_name"])
        self.lineedit_file_name.textChanged.connect(lambda text: self.set_lineedit("file_name", text))

        self.lineedit_out_path = QLineEdit(text=config["standard_paths"]["out_path"])
        self.lineedit_out_path.textChanged.connect(lambda text: self.set_lineedit("out_path", text))

        self.lineedit_template_path = QLineEdit(text=config["standard_paths"]["template_path"])
        self.lineedit_template_path.textChanged.connect(lambda text: self.set_lineedit("template_path", text))

        self.lineedit_attachment_path = QLineEdit(text=config["standard_paths"]["attachment_path"])
        self.lineedit_attachment_path.textChanged.connect(lambda text: self.set_lineedit("attachment_path", text))

        self.lineedit_author = QLineEdit(placeholderText=config["standard_variables"]["author"])
        self.lineedit_author.textChanged.connect(lambda text: self.set_lineedit("author", text))

        self.lineedit_date = QDateEdit(QDate.fromString(config["standard_variables"]["date"], "yyyy-MM-dd"))
        self.lineedit_date.setCalendarPopup(True)
        self.lineedit_date.dateChanged.connect(self.set_date)

        # Create the labels for the input fields
        label_in_path = QLabel("Path to the input file")
        label_file_name = QLabel("Name of the output file")
        label_out_path = QLabel("Path to the output directory")
        label_template_path = QLabel("Path to the template file")
        self.label_attachment_path = QLabel("Path to the attachment directory")
        self.label_author = QLabel("Author of the document")
        self.label_date = QLabel("Date of the document")

        # Create the buttons for the input fields
        self.btn_in_path = QPushButton("in_path", text="Browse")
        self.btn_in_path.clicked.connect(lambda: self.browse_file("in_path"))

        self.btn_out_path = QPushButton("out_path", text="Browse")
        self.btn_out_path.clicked.connect(lambda: self.browse_dir("out_path"))

        self.btn_template_path = QPushButton("template_path", text="Browse")
        self.btn_template_path.clicked.connect(lambda: self.browse_file("template_path"))

        self.btn_attachment_path = QPushButton("attachment_path", text="Browse")
        self.btn_attachment_path.clicked.connect(lambda: self.browse_dir("attachment_path"))

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

        textbox_attachment_path = QHBoxLayout()
        textbox_attachment_path.addWidget(self.lineedit_attachment_path)
        textbox_attachment_path.addWidget(self.btn_attachment_path)

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

        attachment_path = QVBoxLayout()
        attachment_path.addWidget(self.label_attachment_path)
        attachment_path.addLayout(textbox_attachment_path)

        name = QVBoxLayout()
        name.addWidget(label_file_name)
        name.addWidget(self.lineedit_file_name)

        author = QVBoxLayout()
        author.addWidget(self.label_author)
        author.addWidget(self.lineedit_author)

        date = QVBoxLayout()
        date.addWidget(self.label_date)
        date.addWidget(self.lineedit_date)

        # Check if the standard template file contains AUTHOR
        # If it does, enable the author input field
        with open(config["standard_paths"]["template_path"]) as template_file:
            template = template_file.read()
            if "AUTHOR" in template:
                self.lineedit_author.show()
                self.label_author.show()
            else:
                self.lineedit_author.hide()
                self.label_author.hide()
                str_input["author"] = " "

            # Check if the standard template file contains DATE
            # If it does, hide the date input field
            if "DATE" in template and not config["behaviour"]["use_current_date"]:
                self.lineedit_date.show()
                self.label_date.show()
            else:
                self.lineedit_date.hide()
                self.label_date.hide()
                if config["behaviour"]["use_current_date"]:
                    str_input["date"] = "\\today"

        # Check if the input file contains an image
        # If it does, enable the attachment input field
        input_file = Path(config["standard_paths"]["in_path"])
        if os.path.exists(input_file) and input_file.suffix == ".md":
            with open(input_file) as MD_file:
                if re.finditer(r"(\.pdf|\.png|\.jpg|\.jpeg|\.gif)(|.*)*\]\]", MD_file.read(), re.MULTILINE):
                    self.lineedit_attachment_path.show()
                    self.btn_attachment_path.show()
                    self.label_attachment_path.show()
                    str_input["attachment_path"] = config["standard_paths"]["attachment_path"]
                else:
                    self.lineedit_attachment_path.hide()
                    self.btn_attachment_path.hide()
                    self.label_attachment_path.hide()
                    str_input["attachment_path"] = " "
        else:
            self.lineedit_attachment_path.hide()
            self.btn_attachment_path.hide()
            self.label_attachment_path.hide()
            str_input["attachment_path"] = " "

        # Disable the convert button if one of the input fields is empty
        if "" not in str_input.values() and re.match(r".*\.md", str_input["in_path"]):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

        # Create the layout
        layout = QVBoxLayout()

        # Add the elements to the layout
        layout.addLayout(name)
        layout.addLayout(author)
        layout.addLayout(date)
        layout.addLayout(in_path)
        layout.addLayout(out_path)
        layout.addLayout(template_path)
        layout.addLayout(attachment_path)
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
                        str_input["author"] = " "

                    # Check if the template file contains DATE
                    # If it does, enable the date input field
                    if "DATE" in template and not config["behaviour"]["use_current_date"]:
                        self.lineedit_date.show()
                        self.label_date.show()
                    else:
                        self.lineedit_date.hide()
                        self.label_date.hide()
                        if config["behaviour"]["use_current_date"]:
                            str_input["date"] = "\\today"

        # Check if the input field contains an image
        # If it does, enable the attachment input field
        if lbl == "in_path":
            input_file = Path(str_input["in_path"])
            print(input_file.suffix)
            if os.path.exists(input_file) and input_file.suffix == ".md":
                with open(input_file) as MD_file:
                    if re.search(r"(\.pdf|\.png|\.jpg|\.jpeg|\.gif)(|.*)*\]\]", MD_file.read(), re.MULTILINE):
                        self.lineedit_attachment_path.show()
                        self.btn_attachment_path.show()
                        self.label_attachment_path.show()
                        str_input["attachment_path"] = config["standard_paths"]["attachment_path"]
                    else:
                        self.lineedit_attachment_path.hide()
                        self.btn_attachment_path.hide()
                        self.label_attachment_path.hide()
                        str_input["attachment_path"] = " "
            else:
                self.lineedit_attachment_path.hide()
                self.btn_attachment_path.hide()
                self.label_attachment_path.hide()
                str_input["attachment_path"] = " "

        # Disable the convert button if one of the input fields is empty and the input file ends with .md
        if "" not in str_input.values() and re.match(r".*\.md", str_input["in_path"]):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    # Define the input function for the date field
    def set_date(self, date):
        str_input["date"] = date.toString("yyyy-MM-dd")

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

    # Define the open_settings_window function
    def open_settings_window(self):
        self.close()
        settings_window = SettingsWindow()
        settings_window.show()

    # Define the settings_closed function
    def settings_closed(self):
        # If the settings window was closed, update the text of the path fields

        self.lineedit_in_path.setText(config["standard_paths"]["in_path"])
        self.lineedit_out_path.setText(config["standard_paths"]["out_path"])
        self.lineedit_template_path.setText(config["standard_paths"]["template_path"])
        self.lineedit_attachment_path.setText(config["standard_paths"]["attachment_path"])

        # If the settings window was closed, update the placeholdertext of the variable fields
        self.lineedit_file_name.setPlaceholderText(config["standard_variables"]["file_name"])
        self.lineedit_author.setPlaceholderText(config["standard_variables"]["author"])

        str_input["file_name"] = self.lineedit_file_name.text()
        str_input["author"] = self.lineedit_author.text()

        # If the settings window was closed, update the date field
        self.lineedit_date.setDate(QDate.fromString(config["standard_variables"]["date"], "yyyy-MM-dd"))

        # If the settings window was closed, update the content of the str_input dictionary
        for key in config.keys():
            if "standard" in key:
                for subkey in config[key].keys():
                    str_input[subkey] = config[key][subkey]

        # If the use current date option is enabled, set the date to today
        if config["behaviour"]["use_current_date"]:
            self.lineedit_date.setDate(QDate.currentDate())
            str_input["date"] = "\\today"


class SettingsWindow(QWidget):
    """This is the window containing the settings."""

    def __init__(self):
        super().__init__()

        # Define debug action on a key shortcut which prints the content of the config dictionary
        self.debug_action = QAction(self)
        self.debug_action.setShortcut("Ctrl+D")
        self.debug_action.triggered.connect(lambda: print(config))

        # Define temporary dictionary for the changed values
        self.temp_config = {}
        for key in config.keys():
            self.temp_config[key] = {}
            for subkey in config[key].keys():
                self.temp_config[key][subkey] = config[key][subkey]

        # Set the name of the settings window and its size
        self.setWindowTitle("Settings")
        self.resize(500, 300)

        # Create a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # Settings for the paths

        paths = QVBoxLayout()
        paths.addWidget(QLabel("Paths"))

        # Input field for the standard path to the input file
        settings_in_path = QVBoxLayout()

        settings_textbox_in_path = QHBoxLayout()

        self.settings_lineedit_in_path = QLineEdit(self.temp_config["standard_paths"]["in_path"])
        self.settings_lineedit_in_path.textChanged.connect(lambda text: self.set_lineedit("in_path", text))

        self.settings_btn_in_path = QPushButton("in_path", text="Browse")
        self.settings_btn_in_path.clicked.connect(lambda: self.browse_dir("in_path"))

        settings_textbox_in_path.addWidget(self.settings_lineedit_in_path)
        settings_textbox_in_path.addWidget(self.settings_btn_in_path)

        settings_in_path.addWidget(QLabel("Standard path to the input file"))
        settings_in_path.addLayout(settings_textbox_in_path)

        paths.addLayout(settings_in_path)

        # Input field for the standard path to the output directory
        settings_out_path = QVBoxLayout()

        settings_textbox_out_path = QHBoxLayout()

        self.settings_lineedit_out_path = QLineEdit(self.temp_config["standard_paths"]["out_path"])
        self.settings_lineedit_out_path.textChanged.connect(lambda text: self.set_lineedit("out_path", text))

        self.settings_btn_out_path = QPushButton("out_path", text="Browse")
        self.settings_btn_out_path.clicked.connect(lambda: self.browse_dir("out_path"))

        settings_textbox_out_path.addWidget(self.settings_lineedit_out_path)
        settings_textbox_out_path.addWidget(self.settings_btn_out_path)

        settings_out_path.addWidget(QLabel("Standard path to the output directory"))
        settings_out_path.addLayout(settings_textbox_out_path)

        paths.addLayout(settings_out_path)

        # Input field for the standard path to the template file
        settings_template_path = QVBoxLayout()

        settings_textbox_template_path = QHBoxLayout()

        self.settings_lineedit_template_path = QLineEdit(self.temp_config["standard_paths"]["template_path"])
        self.settings_lineedit_template_path.textChanged.connect(lambda text: self.set_lineedit("template_path", text))

        self.settings_btn_template_path = QPushButton("template_path", text="Browse")
        self.settings_btn_template_path.clicked.connect(lambda: self.browse_file("template_path"))

        settings_textbox_template_path.addWidget(self.settings_lineedit_template_path)
        settings_textbox_template_path.addWidget(self.settings_btn_template_path)

        settings_template_path.addWidget(QLabel("Standard path to the template file"))
        settings_template_path.addLayout(settings_textbox_template_path)

        paths.addLayout(settings_template_path)

        # Input field for the standard path to the attachment directory
        settings_attachment_path = QVBoxLayout()

        settings_textbox_attachment_path = QHBoxLayout()

        self.settings_lineedit_attachment_path = QLineEdit(self.temp_config["standard_paths"]["attachment_path"])
        self.settings_lineedit_attachment_path.textChanged.connect(
            lambda text: self.set_lineedit("attachment_path", text)
        )  # noqa: E501

        self.settings_btn_attachment_path = QPushButton("attachment_path", text="Browse")
        self.settings_btn_attachment_path.clicked.connect(lambda: self.browse_dir("attachment_path"))

        settings_textbox_attachment_path.addWidget(self.settings_lineedit_attachment_path)
        settings_textbox_attachment_path.addWidget(self.settings_btn_attachment_path)

        settings_attachment_path.addWidget(QLabel("Standard path to the attachment directory"))
        settings_attachment_path.addLayout(settings_textbox_attachment_path)

        paths.addLayout(settings_attachment_path)

        # Create a separator afrer the paths
        separator_paths = QFrame()
        separator_paths.setFrameShape(QFrame.HLine)
        separator_paths.setFrameShadow(QFrame.Sunken)

        paths.addWidget(separator_paths)

        # Settings for the variables

        variables = QVBoxLayout()
        variables.addWidget(QLabel("Variables"))

        # Input field for the standard name of the output file

        settings_file_name = QVBoxLayout()

        self.settings_lineedit_file_name = QLineEdit(self.temp_config["standard_variables"]["file_name"])
        self.settings_lineedit_file_name.textChanged.connect(lambda text: self.set_lineedit("file_name", text))

        settings_file_name.addWidget(QLabel("Standard name of the output file"))
        settings_file_name.addWidget(self.settings_lineedit_file_name)

        variables.addLayout(settings_file_name)

        # Input field for the standard author of the document
        settings_author = QVBoxLayout()

        self.settings_lineedit_author = QLineEdit(self.temp_config["standard_variables"]["author"])
        self.settings_lineedit_author.textChanged.connect(lambda text: self.set_lineedit("author", text))

        settings_author.addWidget(QLabel("Standard author of the document"))
        settings_author.addWidget(self.settings_lineedit_author)

        variables.addLayout(settings_author)

        # Input field for the standard date of the document
        settings_date = QVBoxLayout()

        # Convert the date string to a QDate object

        self.settings_lineedit_date = QDateEdit(
            QDate.fromString(self.temp_config["standard_variables"]["date"], "yyyy-MM-dd")
        )  # noqa: E501
        self.settings_lineedit_date.setCalendarPopup(True)
        self.settings_lineedit_date.dateChanged.connect(self.set_date)

        settings_date.addWidget(QLabel("Standard date of the document"))
        settings_date.addWidget(self.settings_lineedit_date)

        variables.addLayout(settings_date)

        # Create a separator afrer the variables
        separator_variables = QFrame()
        separator_variables.setFrameShape(QFrame.HLine)
        separator_variables.setFrameShadow(QFrame.Sunken)

        variables.addWidget(separator_variables)

        # Settings for the behaviour

        behaviour = QVBoxLayout()
        behaviour.addWidget(QLabel("Behaviour"))

        # Create a tick box for the metadata override behaviour option
        self.settings_checkbox_override = QCheckBox("Overwrite content with metadata (if available)")
        self.settings_checkbox_override.setChecked(self.temp_config["behaviour"]["override_with_metadata"])
        self.settings_checkbox_override.stateChanged.connect(
            lambda state: self.set_checkbox("override_with_metadata", state)
        )  # noqa: E501

        behaviour.addWidget(self.settings_checkbox_override)

        # Create a tick box for the current date behaviour option
        self.settings_checkbox_date = QCheckBox("Use current date as standard date")
        self.settings_checkbox_date.setChecked(self.temp_config["behaviour"]["use_current_date"])
        self.settings_checkbox_date.stateChanged.connect(lambda state: self.set_checkbox("use_current_date", state))

        behaviour.addWidget(self.settings_checkbox_date)

        # Create a separator afrer the tick boxes
        separator_tickboxes = QFrame()
        separator_tickboxes.setFrameShape(QFrame.HLine)
        separator_tickboxes.setFrameShadow(QFrame.Sunken)

        behaviour.addWidget(separator_tickboxes)

        # Create a layout for the buttons
        settings_buttons = QHBoxLayout()

        # Create the save button
        self.settings_button_save = QPushButton("Save")
        self.settings_button_save.clicked.connect(self.save)

        settings_buttons.addWidget(self.settings_button_save)

        # Create the reset button
        self.settings_button_reset = QPushButton("Reset")
        self.settings_button_reset.clicked.connect(self.reset)

        settings_buttons.addWidget(self.settings_button_reset)

        # Create the return button
        self.settings_button_return = QPushButton("Return")
        self.settings_button_return.clicked.connect(self.return_to_main)

        settings_buttons.addWidget(self.settings_button_return)

        # Create the layout
        layout = QVBoxLayout()

        # Add the elements to the layout
        layout.addWidget(QLabel("Settings"))
        layout.addWidget(separator)
        layout.addLayout(paths)
        layout.addLayout(variables)
        layout.addLayout(behaviour)
        layout.addLayout(settings_buttons)

        # Set the layout
        self.setLayout(layout)

    # Define the input functions for the text fields
    def set_lineedit(self, lbl, text):
        self.temp_config[config_key[lbl]][lbl] = text
        print(config)

    # Define the input function for the date field
    def set_date(self, date):
        self.temp_config["standard_variables"]["date"] = date.toString("yyyy-MM-dd")

    # Define the input function for checkboxes
    def set_checkbox(self, lbl, state):
        if state == 2:
            self.temp_config["behaviour"][lbl] = True
        else:
            self.temp_config["behaviour"][lbl] = False

    # Define the input functions for the browse_dir buttons
    def browse_dir(self, lbl):
        name = QFileDialog.getExistingDirectory(self, "Select Directory", self.temp_config["standard_paths"][lbl])
        if name:
            if lbl == "out_path":
                self.settings_lineedit_out_path.setText(name)
            elif lbl == "attachment_path":
                self.settings_lineedit_attachment_path.setText(name)
            elif lbl == "in_path":
                self.settings_lineedit_in_path.setText(name)

    # Define the input functions for the browse_file buttons
    def browse_file(self, lbl):
        name = QFileDialog.getOpenFileName(
            self, "Select Directory", self.temp_config["standard_paths"][lbl], file_filter[lbl]
        )[
            0
        ]  # noqa: E501
        if name:
            if lbl == "template_path":
                self.settings_lineedit_template_path.setText(name)

    # Define the save function
    def save(self):
        # Write the changed values from the temporary dictionary into the config dictionary
        for key in self.temp_config.keys():
            for subkey in self.temp_config[key].keys():
                config[key][subkey] = self.temp_config[key][subkey]

        # Add the new content to the config file
        with open(config_dir + "/config.toml", "w") as config_file:
            config_file.write(tomlkit.dumps(config))

        # Close the settings window and opens the main window
        self.return_to_main()

    def return_to_main(self):
        window.show()
        self.close()

    # Define the reset function
    def reset(self):
        # Reset the temporary dictionary to the values of the config dictionary
        for key in self.temp_config.keys():
            for subkey in self.temp_config[key].keys():
                self.temp_config[key][subkey] = config[key][subkey]

        # Reset the input fields to the values of the config dictionary
        self.settings_lineedit_in_path.setText(config["standard_paths"]["in_path"])
        self.settings_lineedit_out_path.setText(config["standard_paths"]["out_path"])
        self.settings_lineedit_template_path.setText(config["standard_paths"]["template_path"])
        self.settings_lineedit_file_name.setText(config["standard_variables"]["file_name"])
        self.settings_lineedit_author.setText(config["standard_variables"]["author"])
        self.settings_lineedit_date.setDate(QDate.fromString(config["standard_variables"]["date"], "yyyy-MM-dd"))
        self.settings_lineedit_attachment_path.setText(config["standard_paths"]["attachment_path"])

        # Reset the tick boxes to the values of the config dictionary
        self.settings_checkbox_override.setChecked(config["behaviour"]["override_with_metadata"])
        self.settings_checkbox_date.setChecked(config["behaviour"]["use_current_date"])

    # Define the closeEvent function
    def closeEvent(self, event):
        # Reset the temporary dictionary to the values of the config dictionary
        for key in self.temp_config.keys():
            for subkey in self.temp_config[key].keys():
                self.temp_config[key][subkey] = config[key][subkey]
        # Send a signal to the main window that the settings window was closed
        window.settings_closed()

        event.accept()


def main():
    convert_MD2TeX(str_input, config["behaviour"])
    bake_TeX(str_input)


if __name__ == "__main__":
    # If no config file exists, create one and write the content of the default config file into it
    if not os.path.exists(config_dir + "/config.toml"):
        with open(config_dir + "/config.toml", "w") as config_file:
            with open("config_preset.toml") as preset_config_file:
                config_file.write(preset_config_file.read())

    # Read the config file
    with open(config_dir + "/config.toml") as config_file:
        config = tomlkit.parse(config_file.read())

    # If the config file has not all keys, add the missing keys
    with open("config_preset.toml") as preset_config_file:
        preset_config = tomlkit.parse(preset_config_file.read())
        for key in preset_config.keys():
            if key not in config.keys():
                config[key] = preset_config[key]

                # Write the new content to the config file
                with open(config_dir + "/config.toml", "w") as config_file:
                    config_file.write(tomlkit.dumps(config))

            for subkey in preset_config[key].keys():
                if subkey not in config[key].keys():
                    config[key][subkey] = preset_config[key][subkey]

                    # Write the new content to the config file
                    with open(config_dir + "/config.toml", "w") as config_file:
                        config_file.write(tomlkit.dumps(config))

    # Set the standard values for the input fields
    # We copy all the values from the config dictionary which the key contains standard to the str_input dictionary
    str_input = {}
    for key in config.keys():
        if "standard" in key:
            for subkey in config[key].keys():
                str_input[subkey] = config[key][subkey]

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
