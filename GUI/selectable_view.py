from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior


Builder.load_file('GUI\\selectable_view.kv')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    def select_with_touch(self, node, touch=None):
        if super().select_with_touch(node, touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        touch.grab(self)
        self.clear_selection()
        if self.select_node(node):
            self.selected_nodes.append(node)
        return True


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        remove_layout = App.get_running_app().sm.current_screen.image_remove_layout
        if remove_layout:
            remove_layout.selected_item = get_id_from_text(self.text)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

    def select_node(self, index):
        if index is not None:
            self.layout_manager.deselect_node(index)
        self.layout_manager.select_node(index)


def get_id_from_text(text):
    index = text.rfind("id: ")
    comma_index = text.find(",")
    return text[index + 4:comma_index]