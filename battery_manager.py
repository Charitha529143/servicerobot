import random


class BatteryManager:

    def __init__(self, sensor_logs):

        self.sensor_logs = sensor_logs

    def get_battery(self):

        row = self.sensor_logs.sample(1).iloc[0]

        return int(row["Battery"])

    def battery_penalty(self):

        battery = self.get_battery()

        if battery >= 80:
            penalty = 0

        elif battery >= 60:
            penalty = 10

        elif battery >= 40:
            penalty = 30

        elif battery >= 20:
            penalty = 60

        else:
            penalty = 120

        return battery, penalty