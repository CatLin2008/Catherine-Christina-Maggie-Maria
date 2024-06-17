import json
import os

class HighScoreManager:
    def __init__(self, file_name='high_score.json'):
        self.file_name = file_name
        self.high_score = 0
        self.load_high_score()

    def load_high_score(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.high_score = json.load(file).get('high_score', 0)
        else:
            self.high_score = 0

    def save_high_score(self):
        with open(self.file_name, 'w') as file:
            json.dump({'high_score': self.high_score}, file)

    def update_high_score(self, new_score):
        if new_score > self.high_score:
            self.high_score = new_score
            self.save_high_score()

    def get_high_score(self):
        return self.high_score
