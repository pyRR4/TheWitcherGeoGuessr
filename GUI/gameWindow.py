from kivy.graphics.transformation import Matrix
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stencilview import StencilView
from kivy.graphics import Ellipse, Color


class BoxStencil(BoxLayout, StencilView):
    pass


class ImagesScatter(ScatterLayout):

    def __init__(self, **kwargs):
        super(ImagesScatter, self).__init__(**kwargs)
        self.dragging = False
        self.last_touch = None

    def on_touch_down(self, touch):
        if self.parent.collide_point(touch.x, touch.y):
            if touch.is_mouse_scrolling:
                if touch.button == 'scrolldown':
                    self.zoom_to_mouse(touch)
                    # if self.scale < self.scale_max:
                    #     self.scale = min(self.scale * 1.1, self.scale_max)
                elif touch.button == 'scrollup':
                    self.zoom_to_mouse(touch)
                    # if self.scale > self.scale_min:
                    #     self.scale = max(self.scale * 0.8, self.scale_min)
                self.clamp_to_box_stencil()
            elif touch.button == 'right':
                self.dragging = True
                self.last_touch = touch
            else:
                super(ImagesScatter, self).on_touch_down(touch)

    def zoom_to_mouse(self, touch):
        scale = min(self.width / self.parent.parent.width, self.height / self.parent.parent.height)
        center_x = touch.pos[0] - self.x
        center_y = touch.pos[1] - self.y

        # Tworzenie macierzy transformacji
        trans = Matrix().translate(center_x - self.center_x, center_y - self.center_y, 0).scale(scale, scale, scale)

        # Stosowanie transformacji
        self.apply_transform(trans)
        self.clamp_to_box_stencil()

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
    selected_point = None

    def on_touch_down(self, touch):
        if self.parent.parent.collide_point(touch.x, touch.y):
            if touch.button == 'left':
                self.selected_point = self.to_local(touch.x, touch.y)
                self.draw_point()
            super(MapWidget, self).on_touch_down(touch)

    def draw_point(self):
        if self.selected_point is not None:
            self.canvas.after.clear()
            with self.canvas.after:
                Color(1, 0, 0)
                Ellipse(pos=self.selected_point, size=(5, 5))


class GameScreen(Screen):
    Builder.load_file('GUI/gameWindow.kv')

