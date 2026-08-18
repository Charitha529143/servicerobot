import random


class TrafficManager:

    def __init__(self, traffic):

        self.traffic = traffic

    def current_traffic(self):

        row = self.traffic.sample(1).iloc[0]

        level = row["Crowd_Level"]

        if level == "Low":
            penalty = 5

        elif level == "Medium":
            penalty = 20

        else:
            penalty = 50

        return level, penalty