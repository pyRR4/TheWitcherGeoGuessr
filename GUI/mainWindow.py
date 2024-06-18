import os
import shutil

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder

from TheWitcherGeoGuessr.GUI.selectable_view import RV
from TheWitcherGeoGuessr.backend.file_manager import add_image, remove_image, images_path
from TheWitcherGeoGuessr.database.database_operations import load_image, get_all_images, delete_image_by_id

Builder.load_file('GUI/mainWindow.kv')


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.game_choose_layout = None
        self.image_add_layout = None
        self.image_remove_layout = None


class AnimationScreen(Screen):
    pass


class MainMenuScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainMenuScreenManager, self).__init__(**kwargs)

        self.transition = FadeTransition(duration=0.5)


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


class ImageAddButton(MainMenuBarButton):

    def on_release(self):
        if App.get_running_app().sm.current_screen.image_add_layout is None:
            App.get_running_app().sm.current_screen.image_add_layout = ImageUploadLayout()
            App.get_running_app().sm.current_screen.image_remove_layout = ImageRemoveLayout()
        super().show_layout(App.get_running_app().sm.current_screen.image_add_layout)


class ImageRemoveButton(MainMenuBarButton):

    def on_release(self):
        if App.get_running_app().sm.current_screen.image_remove_layout is None:
            App.get_running_app().sm.current_screen.image_remove_layout = ImageRemoveLayout()
            App.get_running_app().sm.current_screen.image_add_layout = ImageUploadLayout()
        super().show_layout(App.get_running_app().sm.current_screen.image_remove_layout)


class MainMenuBar(FloatLayout):
    def __init__(self, **kwargs):
        super(MainMenuBar, self).__init__(**kwargs)
        self.is_shown = False
        self.shown = None


class BaseMenuLayout(FloatLayout):
    pass


class ImageUploadLayout(BaseMenuLayout):
    def __init__(self, **kwargs):
        super(ImageUploadLayout, self).__init__(**kwargs)
        self.path = None
        self.coordinates = None
        self.map = None

    def show_file_chooser(self):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path=os.path.expanduser('~'),
                                          filters=['*.jpg', '*.jpeg'])
        buttons = BoxLayout(size_hint_y=None, height=50)

        select_button = Button(text="Choose")
        select_button.bind(on_release=lambda x: self.load_selected(filechooser.selection))
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_release=lambda x: self.popup.dismiss())

        buttons.add_widget(select_button)
        buttons.add_widget(cancel_button)

        content.add_widget(filechooser)
        content.add_widget(buttons)

        self.popup = Popup(title="Choose image",
                           content=content,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def load_selected(self, selection):
        if selection:
            selected_file = selection[0]
            self.path = selected_file
            self.ids.status_label.text = selected_file
            self.popup.dismiss()

    def select_map(self, selected_map):
        self.map = selected_map
        map_dict = {
            'velen_novigrad': "Velen and Novigrad",
            'skellige': "Skellige",
            'kaer_morhen': "Kaer Morhen",
            "bialy_sad": "White Orchard"
        }
        self.ids.map_status.children[0].text = map_dict[selected_map]

    def submit(self):
        try:
            coordinate_x = float(self.ids.coordinate_x.text)
            coordinate_y = float(self.ids.coordinate_y.text)

            load_image('images_database', os.path.join(images_path, os.path.basename(self.path)), self.map,
                       (coordinate_x, coordinate_y))
            add_image(self.path)
            remove_layout = App.get_running_app().sm.current_screen.image_remove_layout
            remove_layout.update_rv_data()

            information_popup("Success!", "Image loaded successfully.")

        except:
            information_popup("Failure!", "Failed to load image.")


class ImageRemoveLayout(BaseMenuLayout):
    def __init__(self, **kwargs):
        super(ImageRemoveLayout, self).__init__(**kwargs)
        self.selected_item = None
        self.data = get_all_images('images_database')
        self.rv = RV()
        box_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.update_rv_data()

        box_layout.add_widget(self.rv)

        box_layout.add_widget(self.delete_button())
        self.add_widget(box_layout)

    def delete_button(self):
        button = Button(text="Delete", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button.bind(on_release=self.delete_image)

        return button

    def delete_image(self, arg):
        if self.selected_item:
            for item in self.data:
                if str(item['id']) == self.selected_item:
                    self.data.remove(item)
                    delete_image_by_id('images_database', self.selected_item)
                    remove_image(item['img_path'])
                    self.update_rv_data()

    def update_rv_data(self):
        self.data = get_all_images('images_database')
        self.rv.data = [{'viewclass': 'SelectableLabel',
                         'text': f'id: {item["id"]}, map: {item["map"]}, '
                                 f'coordinates: {item["coordinate_x"]}, {item["coordinate_y"]}',
                         'selected': False} for item in self.data]


class GameChooseLayout(BaseMenuLayout):
    pass


class GameChooseButton(Button):
    def launch_basic_guessr(self):
        switch_screens(self, 'guessr_game')


class ExitButton(MainMenuBarButton):
    pass


def switch_screens(obj, screen, widgets=None):
    App.get_running_app().sm.current = 'animation_screen'
    anim = Animation(duration=1.0)
    if widgets and len(widgets) == 3:
        anim.bind(on_start=lambda x, y: switch_widgets(widgets[0], widgets[1], widgets[2]))
    anim.bind(on_complete=lambda x, y: do_fade_transition(screen))
    anim.start(obj)


def switch_widgets(parent_widget, old_widget, new_widget):
    parent_widget.remove_widget(old_widget)
    parent_widget.add_widget(new_widget)


def do_fade_transition(screen, *args):
    App.get_running_app().sm.current = screen


def information_popup(title, text):
    popup = Popup(title=title, size_hint=(None, None), size=(400, 200))

    label = Label(text=text)

    button = Button(text='Close', size_hint_y=None, height='40dp')
    button.bind(on_release=popup.dismiss)

    content = BoxLayout(orientation='vertical', padding=20)
    content.add_widget(label)
    content.add_widget(button)

    popup.content = content

    popup.open()
