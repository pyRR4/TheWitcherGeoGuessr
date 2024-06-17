import kivy
from kivy.config import ConfigParser
from kivy.app import App

from .endGameWindow import EndGameScreen
from .gameWindow import GameScreen
from .mainWindow import MainMenu, MainMenuScreenManager, AnimationScreen
from TheWitcherGeoGuessr.backend.engine import GameEngine

kivy.require('2.3.0')

total_rounds = 1


class GuessrApp(App):

    def __init__(self, **kwargs):
        super(GuessrApp, self).__init__(**kwargs)
        self.game_engine = GameEngine(total_rounds)

    def build(self):
        config = ConfigParser()

        config.read('C:\\Users\\igopo\\OneDrive\\Pulpit\\Wszystko i nic\\IST 22-27\\IV sem\\JS\\TheWitcherGeoGuessr'
                    '\\TheWitcherGeoGuessr\\GUI\\config.ini')

        width = config.getint('graphics', 'width')
        height = config.getint('graphics', 'height')

        self.config_app(width, height)
        self.game_screen = GameScreen(name='guessr_game')
        self.main_menu_screen = MainMenu(name='menu')
        self.end_game_screen = EndGameScreen(name='end_game')

        self.sm = MainMenuScreenManager()
        self.sm.add_widget(self.main_menu_screen)
        self.sm.add_widget(self.game_screen)
        self.sm.add_widget(self.end_game_screen)
        self.sm.add_widget(AnimationScreen(name='animation_screen'))

        return self.sm

    def config_app(self, width, height):
        from kivy.config import Config

        Config.set('graphics', 'fullscreen', 1)
        Config.set('graphics', 'width', width)
        Config.set('graphics', 'height', height)
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Config.set('input', 'showtouch', '0')

