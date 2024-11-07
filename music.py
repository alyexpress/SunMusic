from vlc import MediaPlayer, Media
from config import SOURCE_DIR
from file_utils import create, clear


class Player:
    def __init__(self):
        self.playing = False
        self.player = MediaPlayer()
        self.queue, self.i = [], 0

    def playlist(self, queue):
        for i, music in enumerate(queue):
            data = list(music)
            filename = f"{SOURCE_DIR}{i + 1}."
            create(filename + "mp3", data[2])
            create(filename + data[4], data[3])
            data[2] = Media(filename + "mp3")
            data[3] = filename + data[4]
            self.queue.append(data)
        music = self.queue[self.i][2]
        self.player.set_media(music)

    def get_position(self):
        position = self.player.get_position()
        return round(position * 1000)

    def set_position(self, position):
        self.player.set_position(position / 1000)

    def play(self):
        if self.playing:
            self.player.pause()
        else:
            self.player.play()
        self.playing = not self.playing
        return self.playing

    def next(self):
        self.i = (self.i + 1) % len(self.queue)
        music = self.queue[self.i][2]
        self.player.stop()
        self.player.set_media(music)
        self.player.play()
        self.playing = True

    def back(self):
        if self.get_position() < 15:
            self.i = (self.i - 1) % len(self.queue)
        music = self.queue[self.i][2]
        self.player.stop()
        self.player.set_media(music)
        self.player.play()
        self.playing = True

    def __getitem__(self, item: int):
        return self.queue[self.i][item]

    def stop(self):
        self.player.stop()
        clear(SOURCE_DIR)
