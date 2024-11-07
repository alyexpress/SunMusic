from config import UI_DIR
from database import db
from file_utils import read

from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6 import uic
from eyed3 import load as mp3


class AddMusicForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_DIR + "add_music.ui", self)
        self.initUI()

    def initUI(self):
        self.moods.addItems(db.get_list_moods())
        self.file_button.clicked.connect(self.choose_file)
        self.preview_button.clicked.connect(self.choose_preview)
        self.close_button.clicked.connect(self.close)
        self.add_button.clicked.connect(self.add_music)

    def choose_file(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Выбрать Музыку', '', 'Музыка (*.mp3)')[0]
        if not filename:
            self.error_label.setText("Не удалось открыть файл")
        else:
            self.file.setText(filename)
            music = mp3(filename).tag
            self.title.setText(music.title)
            self.author.setText(music.artist)
            self.error_label.setText("")


    def choose_preview(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg;*.jpeg;*.png;*webp);;Все файлы (*)')
        if not filename[0]:
            self.error_label.setText("Не удалось открыть картинку")
        else:
            self.preview.setText(filename[0])
            self.error_label.setText("")

    def add_music(self):
        mood = self.moods.currentText()
        filename = self.file.text()
        if not filename:
            return self.error_label.setText("Файл (mp3) не выбран!")
        try:
            file_data = read(filename)
        except FileNotFoundError:
            return self.error_label.setText("Файл (mp3) не найден!")
        title = self.title.text()
        if not title:
            return self.error_label.setText("Название не указано!")
        author = self.author.text()
        preview = self.preview.text()
        extension = ""
        if preview:
            try:
                extension = preview.lower().split(".")[-1]
                if extension not in "png jpg jpeg webp".split():
                    return self.error_label.setText(
                        "Неверный формат картинки!")
                preview = read(preview)
            except FileNotFoundError:
                return self.error_label.setText("Картинка не найдена!")
        db.add_music(title, author, mood, file_data, preview, extension)
        self.close()