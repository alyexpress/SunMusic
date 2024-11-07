from config import WEATHER_API_KEY, UI_DIR, WEATHER_DIR, SOURCE_DIR
from weather import Weather
from database import db
from file_utils import create, clear

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
import sys
import atexit

from player_form import PlayerForm
from add_music import AddMusicForm


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_DIR + 'main.ui', self)
        self.weather = Weather(WEATHER_API_KEY)
        self.player_is_open = False
        self.initUI()

    def initUI(self):
        self.play_button.clicked.connect(self.play)
        self.add_button.clicked.connect(self.add_music)
        self.cities_list.addItems(db.get_cities())
        self.cities_list.currentIndexChanged.connect(
            self.load_weather)
        self.load_weather()

    def load_weather(self):
        # city = self.cities_list.currentText()
        # (temp, weather, description, wind,
        #  clouds) = self.weather.get(city)
        # self.weather_temp.setText(f"{round(temp)}˚C")
        # if weather == "Clouds":  # Choose cloud icon
        #     weather += "_light" if clouds <= 50 else "_grey"
        # elif weather == "Drizzle":
        #     weather = "Rain"
        # mood, icon = db.get_mood_by_weather(weather)
        # icon = WEATHER_DIR + icon
        # self.weather_icon.setPixmap(QPixmap(icon))
        # text = description.capitalize() + ", "
        # text += f"Ветер {round(wind)}м/с"
        # self.weather_description.setText(text)
        # Setup player under weather
        mood = 6
        title, preview, extension = db.get_music_by_mood(mood)
        preview_path = SOURCE_DIR + "preview." + extension
        create(preview_path, preview)
        self.music_title.setText(title)
        preview = QPixmap(preview_path).scaled(45, 45)
        self.music_icon.setPixmap(preview)
        self.mood, self.first = mood, title

    def play(self):
        if not self.player_is_open:
            clear(SOURCE_DIR)
            self.player_form = PlayerForm(self)
            self.player_is_open = True
            self.player_form.show()

    def add_music(self):
        self.add_music_form = AddMusicForm()
        self.add_music_form.show()


def exit_handler():
    clear(SOURCE_DIR)
    db.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    atexit.register(exit_handler)
    sys.exit(app.exec())
