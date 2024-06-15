from kivy.graphics.transformation import Matrix
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stencilview import StencilView
from kivy.graphics import Ellipse, Color


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
                self.children[0].update()
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


class ImagesScatter(ScatterLayout):
    def __init__(self, **kwargs):
        super(ImagesScatter, self).__init__(**kwargs)
        self.dragging = False
        self.last_touch = None

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

