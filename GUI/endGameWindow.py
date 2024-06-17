from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from TheWitcherGeoGuessr.GUI.mainWindow import switch_screens


class EndGameScreen(Screen):
    Builder.load_file('GUI/endGameWindow.kv')
    points_label = ObjectProperty(None)

    def on_enter(self):
        self.points_label.text = f"{App.get_running_app().game_engine.get_total_score():.2f} points"


class PointsLabel(Label):
    pass


class BackToMenuButton(Button):
    def on_release(self):
        switch_screens(self, 'menu')

