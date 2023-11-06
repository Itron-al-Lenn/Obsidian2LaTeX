from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

from Obsidian2LaTeX_helper import bake_TeX, convert_MD2TeX

str_input = {"in_path": "", "name": "", "output_dir": "", "template_dir": "", "author": ""}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the name of the main window and its size
        self.setWindowTitle("Obsidian2LaTeX")

        # Create the convert button
        self.button = QPushButton("Convert")
        self.button.clicked.connect(self.convert)
        self.button.setEnabled(False)

        # Create the input fields
        self.textbox_in_path = QLineEdit()
        self.textbox_in_path.textChanged.connect(self.set_in_path)

        self.textbox_name = QLineEdit()
        self.textbox_name.textChanged.connect(self.set_name)

        self.textbox_output_dir = QLineEdit()
        self.textbox_output_dir.textChanged.connect(self.set_output_dir)

        self.textbox_template_dir = QLineEdit()
        self.textbox_template_dir.textChanged.connect(self.set_template_dir)

        self.textbox_author = QLineEdit()
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
        str_input["in_path"] = text
        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_name(self, text):
        str_input["name"] = text
        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_output_dir(self, text):
        str_input["output_dir"] = text
        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_template_dir(self, text):
        str_input["template_dir"] = text
        if "" in str_input.values():
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def set_author(self, text):
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
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
