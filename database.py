from random import choice, shuffle
from config import DATABASE_NAME
import sqlite3


class DataBase:
    def __init__(self, basename):
        self.db = sqlite3.connect(basename)
        self.cur = self.db.cursor()

    def get_cities(self):
        cities = self.cur.execute("SELECT name FROM cities").fetchall()
        return list(map(lambda x: x[0], cities))

    def get_mood_by_weather(self, weather):
        query = "SELECT id, icon FROM moods WHERE weather = ?"
        data = self.cur.execute(query, (weather,)).fetchall()
        return data[0] if data else (2, "sunny.png")

    def get_music_by_mood(self, mood):
        query = """SELECT title, preview, extension
                   FROM music WHERE mood = ?"""
        data = self.cur.execute(query, (mood,)).fetchall()
        return choice(data)

    def get_music_by_self(self, ms):
        query = """SELECT title, author, file, preview,
                   extension FROM music WHERE mood = ?"""
        data = self.cur.execute(query, (ms.mood,)).fetchall()
        first = list(filter(lambda x: x[0] == ms.first, data))[0]
        data.remove(first)
        shuffle(data)
        return [first] + data

    def get_list_moods(self):
        data = self.cur.execute("SELECT name FROM moods").fetchall()
        return list(map(lambda x: x[0], data))

    def add_music(self, *args):
        args = list(args)
        query = "SELECT id FROM moods WHERE name = ?;"
        args[2] = self.cur.execute(query, (args[2],)).fetchone()[0]
        query = """INSERT INTO music (title, author, mood, file,
                preview, extension) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cur.execute(query, tuple(args))
        self.db.commit()

    def close(self):
        self.db.close()


db = DataBase(DATABASE_NAME)
