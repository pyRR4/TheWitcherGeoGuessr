import math

from TheWitcherGeoGuessr.backend.file_manager import get_file


class GameEngine:
    def __init__(self, total_rounds):
        self.total_score = 0
        self.total_rounds = total_rounds
        self.current_round = 0

    def get_total_score(self):
        return self.total_score

    def append_score(self, score):
        self.total_score += score

    def new_round(self):
        self.current_round += 1

        if self.current_round >= self.total_rounds:
            return False
        else:
            return True


class RoundEngine:

    def __init__(self, game_map, number, selected_point=None):
        self.selected_point = selected_point
        self.img, self.actual_point = get_file(game_map, number)
        self.score = 0
        self.accuracy = 0

    def calculate_score(self):
        selected_point_x, selected_point_y = self.selected_point
        actual_point_x, actual_point_y = self.actual_point

        x_squared_diff = (selected_point_x - actual_point_x) ** 2
        y_squared_diff = (selected_point_y - actual_point_y) ** 2

        distance = math.sqrt(x_squared_diff + y_squared_diff)

        if distance <= 1:
            self.score = 1000
        else:
            self.score = 1000 / distance

    def get_score_from_point(self, new_point):
        self.selected_point = new_point
        self.calculate_score()

        return self.score

    def get_accuracy(self):
        self.accuracy = self.score / 1000
        return self.accuracy
