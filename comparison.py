import pandas as pd


class Comparison:

    def __init__(self, baseline, admor):

        self.baseline = baseline
        self.admor = admor

    def compare(self):

        table = pd.DataFrame({

            "Metric": [

                "Distance",
                "Time",
                "Energy",
                "Obstacle Penalty",
                "Execution Time"

            ],

            "Baseline": [

                self.baseline["distance"],
                self.baseline["time"],
                self.baseline["energy"],
                self.baseline["penalty"],
                self.baseline["execution_time"]

            ],

            "ADMOR": [

                self.admor["distance"],
                self.admor["time"],
                self.admor["energy"],
                self.admor["penalty"],
                self.admor["execution_time"]

            ]

        })

        return table

    def display(self):

        table = self.compare()

        print("\n")
        print("="*70)
        print("PERFORMANCE COMPARISON")
        print("="*70)

        print(table)

        return table