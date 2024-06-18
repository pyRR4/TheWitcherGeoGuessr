from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

import TheWitcherGeoGuessr.GUI.mainWindow as main_window
import TheWitcherGeoGuessr.backend.engine as engine


class EndGameScreen(Screen):
    Builder.load_file('TheWitcherGeoGuessr\\GUI\\endGameWindow.kv')
    points_label = ObjectProperty(None)

    def on_enter(self):
        self.points_label.text = f"{App.get_running_app().game_engine.get_total_score():.2f} points"

        total_rounds = App.get_running_app().game_engine.get_rounds()
        App.get_running_app().game_engine = engine.GameEngine(total_rounds)
        App.get_running_app().game_screen.update_labels()


class PointsLabel(Label):
    pass


class BackToMenuButton(Button):
    def on_release(self):
        main_window.switch_screens(self, 'menu')

