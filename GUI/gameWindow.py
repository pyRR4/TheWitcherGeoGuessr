import os.path

from kivy.graphics.transformation import Matrix
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stencilview import StencilView
from kivy.graphics import Ellipse, Color
from kivy.uix.button import Button
from kivy.uix.image import Image

from TheWitcherGeoGuessr.backend.file_manager import random_map, random_image, images_path
from TheWitcherGeoGuessr.backend.score_calculator import RoundEngine

maps_path = (f"C:\\Users\\igopo\\OneDrive\\Pulpit\\Wszystko i nic\\IST 22-27\\IV sem\\JS\\TheWitcherGeoGuessr"
            f"\\TheWitcherGeoGuessr\\maps\\")


class BoxStencil(BoxLayout, StencilView):
    def update(self):
        pass


class MapBox(BoxStencil):

    def __init__(self, **kwargs):
        super(MapBox, self).__init__(**kwargs)
        self.selected_point = None
        self.point_to_draw = None
        self.point_instruction = None

    def on_touch_down(self, touch):
        if self.parent.parent.collide_point(touch.x, touch.y):
            if touch.button == 'left':
                self.point_to_draw = self.to_local(touch.x, touch.y)
                self.draw_point()
                transformation = self.children[0].transform
                x, y = self.point_to_draw
                self.selected_point = transformation.inverse().transform_point(x, y, 0)
                print(self.selected_point)
                print(calculate_image_coordinates(self.selected_point, self.children[0].children[0].children[0]))
            super(MapBox, self).on_touch_down(touch)

    def draw_point(self):
        if self.point_to_draw is not None:
            if self.point_instruction:
                self.canvas.remove(self.point_instruction)
            with self.canvas:
                Color(1, 0, 0)
                self.point_instruction = Ellipse(pos=(self.point_to_draw[0] - 2.5, self.point_to_draw[1] - 2.5),
                                                 size=(5, 5))

    def update(self):
        if self.point_to_draw is not None:
            transformation = self.children[0].transform
            x, y, z = self.selected_point
            self.point_to_draw = transformation.transform_point(x, y, z)
            self.draw_point()


class GameImage(Image):
    def __init__(self, **kwargs):
        super(GameImage, self).__init__(**kwargs)
        self.fit_mode = "scale-down"


class ImagesScatter(ScatterLayout):
    def __init__(self, source, **kwargs):
        super(ImagesScatter, self).__init__(**kwargs)
        self.dragging = False
        self.last_touch = None

        self.add_widget(GameImage(source=source))

    def on_touch_down(self, touch):
        if self.parent.collide_point(touch.x, touch.y):
            if touch.is_mouse_scrolling:
                if touch.button == 'scrolldown':
                    if self.scale < self.scale_max:
                        self.scale = min(self.scale * 1.1, self.scale_max)
                    self.parent.update()
                elif touch.button == 'scrollup':
                    if self.scale > self.scale_min:
                        self.scale = max(self.scale * 0.8, self.scale_min)
                    self.parent.update()
                self.clamp_to_box_stencil()
            elif touch.button == 'right':
                self.dragging = True
                self.last_touch = touch
                self.parent.update()
            elif touch.button == 'left':
                pass
            else:
                super(ImagesScatter, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.dragging and touch is self.last_touch:
            self.dragging = False
            self.last_touch = None
            return True
        return super(ImagesScatter, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        if self.dragging and touch is self.last_touch:
            dx = touch.dx
            dy = touch.dy
            self.apply_transform(Matrix().translate(dx, dy, 0))
            self.clamp_to_box_stencil()
            self.parent.update()
            return True
        return super(ImagesScatter, self).on_touch_move(touch)

    def on_transform_with_touch(self, touch):
        super(ImagesScatter, self).on_transform_with_touch(touch)
        self.clamp_to_box_stencil()

    def clamp_to_box_stencil(self):
        box_stencil = self.parent
        box_width, box_height = box_stencil.size
        scaled_width = self.width * self.scale
        scaled_height = self.height * self.scale

        if scaled_width < box_width:
            self.x = (box_width - scaled_width) / 2
        else:
            self.x = max(min(self.x, box_stencil.x), box_stencil.right - scaled_width)

        if scaled_height < box_height:
            self.y = (box_height - scaled_height) / 2
        else:
            self.y = max(min(self.y, box_stencil.y), box_stencil.top - scaled_height)


class MapWidget(ImagesScatter):
    pass


class GameScreen(Screen):
    Builder.load_file('GUI/gameWindow.kv')

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_map = random_map()
        self.img = random_image(self.game_map)
        self.round_engine = RoundEngine(self.game_map, self.img)
        self.map_box = None
        self.screen_layout = self.main_layout()

        self.add_widget(self.screen_layout)

    def main_layout(self):
        box_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        float_layout = FloatLayout(size_hint=(1, 0.7))

        box_stencil = BoxStencil(size_hint=(0.4, 0.6), pos_hint={'center_x': 0.75, 'center_y': 0.5})
        box_stencil.add_widget(ImagesScatter(os.path.join(images_path, self.game_map, self.img, "image.jpg")))
        float_layout.add_widget(box_stencil)

        self.map_box = MapBox(size_hint=(0.4, 0.6), pos_hint={'center_x': 0.25, 'center_y': 0.5})
        self.map_box.add_widget(ImagesScatter(os.path.join(maps_path, f"{self.game_map}.jpg")))
        float_layout.add_widget(self.map_box)

        box_layout.add_widget(float_layout)

        box_layout.add_widget(self.button_labels_layout())

        return box_layout

    def button_labels_layout(self):
        box_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))

        first_inner_layout = BoxLayout(orientation='vertical', size_hint=(0.6, 1), padding=0.1 * self.width)
        first_inner_layout.add_widget(ConfirmButton())
        box_layout.add_widget(first_inner_layout)

        second_inner_layout = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
        #second_inner_layout.add_widget()
        box_layout.add_widget(second_inner_layout)

        return box_layout


class ConfirmButton(Button):

    def __init__(self, **kwargs):
        super(ConfirmButton, self).__init__(**kwargs)
        self.is_confirmed = False

    def on_release(self):
        if not self.is_confirmed:
            coordinates = calculate_image_coordinates(self.get_root_window().selected_point,
                                                      self.children[0].children[0].children[0])
            labels_layout = self.parent.parent.children[1]


def calculate_image_coordinates(point, image):
    app_x, app_y, app_z = point

    image_width, image_height = image.texture.size

    widget_width, widget_height = image.parent.parent.size
    widget_x, widget_y = image.pos

    scale_x = widget_width / image_width
    scale_y = widget_height / image_height
    scale = min(scale_x, scale_y) #mniejsza skala jest poprawna, bez marginesow

    display_width = image_width * scale
    display_height = image_height * scale

    padding_x = (widget_width - display_width) / 2
    padding_y = (widget_height - display_height) / 2

    image_x = (app_x - widget_x - padding_x) / scale
    image_y = (app_y - widget_y - padding_y) / scale

    return image_x, image_y

