import random
from PyQt5.QtWidgets import *
from world_rando import randomize_world_map
from area_param_rando import randomize_area_params
from level_rando import randomize_level_content
from text_rando import randomize_text
from PyQt5.QtCore import *
import os
import subprocess
import tools
import zstandard
import sarc
import byml
import pymsyt
import wrapt

VERSION = "1.1.0"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Mario Bros. Wonder Randomizer")

        self.console = QTextEdit(self)
        self.console.setStyleSheet("border: 1px solid lightgray; background-color: transparent")
        self.console.setReadOnly(True)

        self.left_side_frame = QFrame(self)
        self.left_side_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.left_side = QVBoxLayout(self.left_side_frame)

        info_label = QLabel(f"Super Mario Bros. Wonder Randomizer by CharlesDev\nv{VERSION}")
        info_label.setAlignment(Qt.AlignCenter)
        self.left_side.addWidget(info_label)

        options_label = QLabel("Options")
        options_label.setAlignment(Qt.AlignCenter)
        self.left_side.addWidget(options_label)

        self.wm_checkbox = self.make_checkbox("Randomize World Map?", on_check=self.wm_check)
        self.lc_frame = QFrame(self)
        self.lc_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.lc_layout = QVBoxLayout(self.lc_frame)

        self.lc_checkbox = self.make_checkbox("Randomize Level Content?", on_check=self.lc_check)

        self.en_frame = QFrame(self)
        self.en_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.en_frame.setVisible(False)
        self.en_layout = QVBoxLayout(self.en_frame)
        self.en_checkbox = self.make_checkbox("Randomize Enemies?", False, self.re_check, parent=self.lc_layout)
        # self.koarena_checkbox = self.make_checkbox("Randomize KO Arenas?", False, None, parent=self.en_layout)
        # self.wiggler_checkbox = self.make_checkbox("Randomize Wiggler Races?", True, None, parent=self.en_layout)
        self.lc_layout.addWidget(self.en_frame)

        self.we_frame = QFrame(self)
        self.we_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.we_frame.setVisible(False)
        self.we_layout = QVBoxLayout(self.we_frame)
        self.we_checkbox = self.make_checkbox("Randomize Wonder Effects?", False, self.we_check, parent=self.lc_layout)
        self.wetimer_checkbox = self.make_checkbox("Randomize Timer?", True, None, parent=self.we_layout)
        self.lc_layout.addWidget(self.we_frame)

        self.lc_frame.setVisible(False)
        self.left_side.addWidget(self.lc_frame)

        self.ls_checkbox = self.make_checkbox("Randomize Level Styles?", on_check=self.ls_check)
        self.text_checkbox = self.make_checkbox("Randomize Text?", on_check=self.text_check)

        self.left_side.addSpacerItem(QSpacerItem(0, 30))

        seed_label = QLabel("Seed (Leave blank for random)")
        seed_label.setAlignment(Qt.AlignCenter)
        self.left_side.addWidget(seed_label)

        self.seed_input = QLineEdit()
        self.left_side.addWidget(self.seed_input)

        self.warning_worlds = self.create_warning_text("No worlds folder provided!")
        self.warning_levels = self.create_warning_text("No levels folder provided!")
        self.warning_mals = self.create_warning_text("No mals folder provided!")
        self.warning_areaparams = self.create_warning_text("No area params folder provided!")

        self.randomize_button = QPushButton("Randomize!", clicked = self.randomize)
        self.left_side.addWidget(self.randomize_button)
        self.open_folder_button = QPushButton("Open Randomized Folder", clicked=self.open_randomized_folder)
        self.left_side.addWidget(self.open_folder_button)

        self.left_side.addStretch()

        self.resize(800, 600)
        self.show()

    def create_warning_text(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: red; background-color: yellow");
        font = label.font()
        font.setPointSize(10)
        label.setFont(font)
        self.left_side.addWidget(label)
        label.setVisible(False)
        return label

    def get_root_folder(self) -> str:
        return os.path.dirname(os.path.realpath(__file__)) + "\\..\\"

    def resizeEvent(self, _) -> None:
        self.left_side_frame.setGeometry(QRect(0, 0, int(self.geometry().width() / 2), self.geometry().height()))
        self.console.setGeometry(QRect(int(self.geometry().width() / 2), 0, int(self.geometry().width() / 2), self.geometry().height()))

    def make_checkbox(self, text = "", checked = False, on_check = None, parent=None):
        checkbox = QCheckBox(text)
        if on_check != None:
            checkbox.toggled.connect(on_check)
        if parent == None:
            parent = self.left_side
        checkbox.setChecked(checked)
        parent.addWidget(checkbox)

        return checkbox
    
    def wm_check(self, checked: bool):
        pass
    
    def re_check(self, checked: bool):
        self.en_frame.setVisible(checked)

    def we_check(self, checked: bool):
        self.we_frame.setVisible(checked)

    def ls_check(self, checked: bool):
        pass

    def text_check(self, checked: bool):
        pass

    def lc_check(self, checked: bool):
        self.lc_frame.setVisible(checked)

    def content_print(self, text: str):
        print(text)
        self.console.insertPlainText(f"{text}\n")

    def paintEvent(self, a0) -> None:
        self.open_folder_button.setEnabled(os.path.exists(self.get_root_folder() + "randomized"))
        self.warning_worlds.setVisible(not os.path.exists(self.get_root_folder() + "worlds"))
        self.warning_areaparams.setVisible(not os.path.exists(self.get_root_folder() + "areaparams"))
        self.warning_mals.setVisible(not os.path.exists(self.get_root_folder() + "mals"))
        self.warning_levels.setVisible(not os.path.exists(self.get_root_folder() + "levels"))
        return super().paintEvent(a0)

    def open_randomized_folder(self):
        randomized_folder = self.get_root_folder() + "randomized"
        if os.path.exists(randomized_folder):
            print(f"Opening {randomized_folder}")
            subprocess.Popen(rf'explorer /select,{randomized_folder}')

    def randomize(self):
        self.randomize_button.setEnabled(False)
        self.console.clear()

        if self.seed_input.text().strip() == "":
            self.seed_input.setText(f"{random.randint(-2147483648, 2147483647)}")

        normal_seed = self.seed_input.text()
        seed = hash(normal_seed)
        random.seed(seed)

        self.content_print(f"Starting randomization with seed {normal_seed}")

        if self.wm_checkbox.isChecked():
            randomize_world_map(self.content_print)
        if self.ls_checkbox.isChecked():
            randomize_area_params(self.content_print)
        if self.text_checkbox.isChecked():
            randomize_text(self.content_print)
        if self.lc_checkbox.isChecked():
            randomize_level_content(self.content_print, self.en_checkbox.isChecked(), self.we_checkbox.isChecked(), True, True, self.wetimer_checkbox.isChecked())

        self.content_print("Randomization finished!")
        self.randomize_button.setEnabled(True)
        pass

app = QApplication([])
mw = MainWindow()

app.exec_()

# randomize_world_map = input("Randomize world map? [y/n]: ").lower() in yes_list
# randomize_levels = input("Randomize level content? [y/n]: ").lower() in yes_list
# randomize_area_params = input("Randomize area params? [y/n]: ").lower() in yes_list
# randomize_text = input("Randomize text? [y/n]: ").lower() in yes_list

# print("Starting randomization...")
# if randomize_world_map:
#     import world_rando
# if randomize_area_params:
#     import area_param_rando
# if randomize_text:
#     import text_rando
# if randomize_levels:
#     import level_rando

# print("Randomization finished!")