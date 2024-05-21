import kivy
from kivy.config import ConfigParser
from kivy.app import App
from kivy.lang import Builder

from TheWitcherGeoGuessr.GUI.mainWindow import GuessrGame

kivy.require('2.3.0')


class GuessrApp(App):
    def build(self):
        config = ConfigParser()

        config.read('C:\\Users\\igopo\\OneDrive\\Pulpit\\Wszystko i nic\\IST 22-27\\IV sem\\JS\\TheWitcherGeoGuessr'
                    '\\TheWitcherGeoGuessr\\GUI\\config.ini')

        width = config.getint('graphics', 'width')
        height = config.getint('graphics', 'height')

        self.config_app(width, height)

        return GuessrGame()

    def config_app(self, width, height):
        from kivy.config import Config

        Config.set('graphics', 'fullscreen', 1)
        Config.set('graphics', 'width', width)
        Config.set('graphics', 'height', height)
