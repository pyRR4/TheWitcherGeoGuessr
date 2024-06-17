import kivy
from kivy.config import ConfigParser
from kivy.app import App

from .gameWindow import GameScreen
from .mainWindow import MainMenu, MainMenuScreenManager, AnimationScreen
from TheWitcherGeoGuessr.backend.score_calculator import GameEngine

kivy.require('2.3.0')


class GuessrApp(App):

    def __init__(self, **kwargs):
        super(GuessrApp, self).__init__(**kwargs)
        self.game_engine = GameEngine()

    def build(self):
        config = ConfigParser()

        config.read('C:\\Users\\igopo\\OneDrive\\Pulpit\\Wszystko i nic\\IST 22-27\\IV sem\\JS\\TheWitcherGeoGuessr'
                    '\\TheWitcherGeoGuessr\\GUI\\config.ini')

        width = config.getint('graphics', 'width')
        height = config.getint('graphics', 'height')

        self.config_app(width, height)

        self.sm = MainMenuScreenManager()
        self.sm.add_widget(MainMenu(name='menu'))
        self.sm.add_widget(GameScreen(name='guessr_game'))
        self.sm.add_widget(AnimationScreen(name='animation_screen'))

        return self.sm

    def config_app(self, width, height):
        from kivy.config import Config

        Config.set('graphics', 'fullscreen', 1)
        Config.set('graphics', 'width', width)
        Config.set('graphics', 'height', height)
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Config.set('input', 'showtouch', '0')

