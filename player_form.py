from config import UI_DIR, MEDIA_DIR
from music import Player
from database import db

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import QTimer
from PyQt6 import uic


class PlayerForm(QWidget):
    def __init__(self, main_self):
        super().__init__()
        uic.loadUi(UI_DIR + "mediaplayer.ui", self)
        self.ms = main_self
        data = db.get_music_by_self(main_self)
        self.player = Player()
        self.player.playlist(data)
        self.load_music()
        # Setup buttons commands
        self.play_button.clicked.connect(self.play)
        self.next_button.clicked.connect(self.next)
        self.back_button.clicked.connect(self.back)
        self.progress.sliderReleased.connect(self.set_position)
        # Setup timer for progressbar
        self.progress.setMaximum(1000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_progress)
        self.timer.start(1000)

        self.play()

    def load_music(self):
        # Load preview picture
        preview = QPixmap(self.player[3]).scaled(270, 270)
        self.image_label.setPixmap(preview)
        # Load title & group labels
        if len(self.player[0]) > 17:
            font_size = 25
        elif len(self.player[0]) > 14:
            font_size = 30
        else:
            font_size = 35
        self.music_name.setFont(QFont("Arial", font_size))
        self.music_name.setText(self.player[0])
        self.music_group.setText(self.player[1])
        # Reset progressbar
        self.progress.setValue(0)

    def change_progress(self):
        if self.player.playing:
            position = self.player.get_position()
            self.progress.setValue(position)
            if position >= 999:
                self.next()

    def set_position(self):
        self.player.set_position(self.progress.value())

    def play(self):
        pause = self.player.play()
        icon = MEDIA_DIR + ("pause" if pause else "play")
        self.play_button.setIcon(QIcon(icon + ".png"))

    def next(self):
        self.player.next()
        self.load_music()
        icon = QIcon(MEDIA_DIR + "pause.png")
        self.play_button.setIcon(icon)

    def back(self):
        self.player.back()
        self.load_music()
        icon = QIcon(MEDIA_DIR + "pause.png")
        self.play_button.setIcon(icon)

    def closeEvent(self, event):
        self.player.stop()
        self.ms.player_is_open = False
