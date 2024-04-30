import kivy
from kivy.lang import Builder

kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.widget import Widget


class GuessrGame(Widget):
    pass


class GuessrApp(App):
    def build(self):
        Builder.load_file('start.kv')
        return GuessrGame()


if __name__ == "__main__":
    GuessrApp().run()
