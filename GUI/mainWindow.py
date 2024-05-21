from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivy.lang import Builder


class GuessrGame(Widget):
    Builder.load_file('GUI/mainWindow.kv')


class MainMenuScreenManager(ScreenManager):
    pass


class MainMenuBarButton(Button):
    pass
    # def on_release(self):
    #

class GameChooseLayout(FloatLayout):
    pass


class OptionsLayout(BoxLayout):
    pass


class StartGameButton(MainMenuBarButton):
    pass


class ExitButton(Button):
    pass

