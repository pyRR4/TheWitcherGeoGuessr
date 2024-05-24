from kivy.animation import Animation
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder


class MainMenu(Screen):
    Builder.load_file('GUI/mainWindow.kv')
    game_choose_layout = ObjectProperty(None)


class MainMenuScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainMenuScreenManager, self).__init__(**kwargs)

        self.transition = FadeTransition(duration=1.0)


class MainMenuBarButton(Button):
    def show_layout(self, layout):
        if layout.opacity == 0:
            animation = Animation(opacity=1, duration=0.5)
        else:
            animation = Animation(opacity=0, duration=0.5)
        animation.start(layout)


class GameChooseLayout(FloatLayout):
    pass


class OptionsLayout(BoxLayout):
    pass


class StartGameButton(MainMenuBarButton):
    def on_release(self):
        layout_to_show = self.parent.parent.parent.game_choose_layout
        super().show_layout(layout_to_show)


class GameChooseButton(Button):

    def launch_basic_guessr(self):
        App.get_running_app().sm.current = 'guessr_game'


class ExitButton(Button):
    pass

