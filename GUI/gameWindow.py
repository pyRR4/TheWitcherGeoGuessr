from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class GameScreen(Screen):
    Builder.load_file('GUI/gameWindow.kv')