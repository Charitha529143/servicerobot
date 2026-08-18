import pandas as pd


class DataLoader:

    def __init__(self):

        self.file_path = "dataset/Adaptive_Service_Robot_Dataset.xlsx"

    def load(self):

        data = {

            "environment": pd.read_excel(
                self.file_path,
                sheet_name="Environment"
            ),

            "routes": pd.read_excel(
                self.file_path,
                sheet_name="Routes"
            ),

            "obstacles": pd.read_excel(
                self.file_path,
                sheet_name="Obstacles"
            ),

            "charging": pd.read_excel(
                self.file_path,
                sheet_name="ChargingStations"
            ),

            "tasks": pd.read_excel(
                self.file_path,
                sheet_name="Tasks"
            ),

            "sensor": pd.read_excel(
                self.file_path,
                sheet_name="SensorLogs"
            ),

            "execution": pd.read_excel(
                self.file_path,
                sheet_name="ExecutionLogs"
            ),

            "traffic": pd.read_excel(
                self.file_path,
                sheet_name="Traffic"
            )

        }

        return data