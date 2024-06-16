import math

from TheWitcherGeoGuessr.backend.file_manager import get_file


class RoundEngine:

    def __init__(self, game_map, number, selected_point=None):
        self.selected_point = selected_point
        self.img, self.actual_point = get_file(game_map, number)
        self.score = 0

    def calculate_score(self):
        selected_point_x, selected_point_y, selected_point_z = self.selected_point
        actual_point_x, actual_point_y = self.actual_point

        x_squared_diff = (selected_point_x - actual_point_x) ** 2
        y_squared_diff = (selected_point_y - actual_point_y) ** 2

        distance = math.sqrt(x_squared_diff + y_squared_diff)

        self.score = 1000 / distance

    def get_score_from_point(self, new_point):
        self.selected_point = new_point
        self.calculate_score()

        return self.score


