from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL.Image import open as openImage
from json import load as loadJson
from plyer import notification
import youtube_dl
import requests
import sys


class LofiTrayApp:
    def __init__(self):
        self.current_stream_number = 0
        self.is_play = False
        self.icon = openImage("icon.png")
        self.ydl = youtube_dl.YoutubeDL()
        self.instance = vlc.Instance("--no-video")
        self.player = self.instance.media_player_new()
        self.videos = []

        try:
            f = open("settings.json")
            self.data = loadJson(f)
            f.close()
        except:
            notification.notify(
                message="А хде собсна мой settings.json...",
                app_name="LofiTray",
                app_icon="icon.ico",
                title="Не понял",
                ticker="LofiTray",
            )
            sys.exit()

        for video_url in list(self.data["streams"].values()):
            try:
                vid = self.ydl.extract_info(
                    video_url,
                    download=False,
                )
                self.videos.append(vid)
            except:
                self.data["streams"] = {key:val for key, val in self.data["streams"].items() if val != video_url}
                continue

        try:
            self.app__ = icon(
                "LofiTray",
                self.icon,
                "LofiTray",
                menu=menu(*self.generate_menu(self.data)),
            )
        except Exception as e:
            notification.notify(
                message="Мда.. ну тут два стула:\n либо ты в settings.json намудрил \n либо переустанови прогу..",
                app_name="LofiTray",
                app_icon="icon.ico",
                title="Миша, всё фигня, давай по новой",
                ticker="LofiTray",
            )
            sys.exit()

    def run(self):
        self.app__.run()

    def exit_app(self, app, query):
        app.stop()

    def play_stream(self):
        self.player.stop()
        url = self.videos[self.current_stream_number]["url"]
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    def on_clicked_play(self, app, item):
        self.is_play = not item.checked
        if self.is_play:
            self.play_stream()
        else:
            self.player.stop()

    def set_current_stream(self, v):
        def inner(icon, item):
            self.current_stream_number = v
            if self.is_play:
                self.play_stream()

        return inner

    def is_current_stream(self, v):
        def inner(item):
            return self.current_stream_number == v

        return inner

    def generate_streams(self, data):
        def get_default(i, streams):
            if i == list(streams)[0]:
                return True
            return False

        return [
            item(
                list(data["streams"])[i],
                self.set_current_stream(i),
                checked=self.is_current_stream(i),
                radio=True,
            )
            for i in range(len(data["streams"]))
        ]

    def generate_menu(self, data):
        app_menu = []
        app_menu.append(
            item(
                "🎧 Играть",
                lambda app, item: self.on_clicked_play(app, item),
                checked=lambda item: self.is_play,
            )
        )
        app_menu.append(
            item(
                "🎵 Стримы",
                menu(*self.generate_streams(data)),
            )
        )
        app_menu.append(menu.SEPARATOR)
        app_menu.append(item("⛔ Выйти", lambda app, query: self.exit_app(app, query)))
        return app_menu


if __name__ == "__main__":
    try:
        import vlc
    except:
        notification.notify(
            message="Установи VLC media player с официального сайта",
            app_name="LofiTray",
            app_icon="icon.ico",
            title="А как я проигрывать то буду..",
            ticker="LofiTray",
        )
        sys.exit()
    try:
        requests.head("https://google.com/", timeout=1)
    except requests.ConnectionError:
        notification.notify(
            message="Подключись к интернету и врубай по новой",
            app_name="LofiTray",
            app_icon="icon.ico",
            title="Инета чёт нема..",
            ticker="LofiTray",
        )
        sys.exit()
    app = LofiTrayApp()
    app.run()
