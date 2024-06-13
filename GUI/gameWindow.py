from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stencilview import StencilView


class BoxStencil(BoxLayout, StencilView):
    pass


class ImagesScatter(ScatterLayout):

    def on_touch_down(self, touch):
        if self.parent.collide_point(touch.x, touch.y):
            if touch.is_mouse_scrolling:
                if touch.button == 'scrolldown':
                    if self.scale < self.scale_max:
                        self.scale = min(self.scale * 1.1, self.scale_max)
                elif touch.button == 'scrollup':
                    if self.scale > self.scale_min:
                        self.scale = max(self.scale * 0.8, self.scale_min)
                self.clamp_to_box_stencil()
            else:
                super(ImagesScatter, self).on_touch_down(touch)

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


class GameScreen(Screen):
    Builder.load_file('GUI/gameWindow.kv')