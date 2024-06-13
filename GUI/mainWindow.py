import time

from kivy.animation import Animation
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.game_choose_layout = None
        self.options_layout = None

    Builder.load_file('GUI/mainWindow.kv')


class AnimationScreen(Screen):
    pass


class MainMenuScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainMenuScreenManager, self).__init__(**kwargs)

        self.transition = FadeTransition(duration=1.0)


class MainMenuBarButton(Button):
    def show_layout(self, layout):
        if self.parent.is_shown:
            App.get_running_app().sm.current_screen.remove_widget(self.parent.shown)
            self.parent.is_shown = False
            if not isinstance(layout, self.parent.shown.__class__):
                self.show_layout(layout)
        else:
            App.get_running_app().sm.current_screen.add_widget(layout)
            self.parent.is_shown = True
            self.parent.shown = layout


class StartGameButton(MainMenuBarButton):

    def on_release(self):
        if App.get_running_app().sm.current_screen.game_choose_layout is None:
            App.get_running_app().sm.current_screen.game_choose_layout = GameChooseLayout()
        super().show_layout(App.get_running_app().sm.current_screen.game_choose_layout)


class OptionsButton(MainMenuBarButton):

    def on_release(self):
        if App.get_running_app().sm.current_screen.options_layout is None:
            App.get_running_app().sm.current_screen.options_layout = OptionsLayout()
        super().show_layout(App.get_running_app().sm.current_screen.options_layout)


class MainMenuBar(FloatLayout):
    def __init__(self, **kwargs):
        super(MainMenuBar, self).__init__(**kwargs)
        self.is_shown = False
        self.shown = None


class BaseMenuLayout(FloatLayout):
    pass


class OptionsLayout(BaseMenuLayout):
    pass


class GameChooseLayout(BaseMenuLayout):
    pass


class GameChooseButton(Button):
    def launch_basic_guessr(self):

        App.get_running_app().sm.current = 'animation_screen'
        anim = Animation(duration=1.0)
        anim.bind(on_complete=self.do_fade_transition)
        anim.start(self)

    def do_fade_transition(self, *args):
        App.get_running_app().sm.current = 'guessr_game'


class ExitButton(Button):
    pass

