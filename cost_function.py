import math


# ==========================================================
# RISK WEIGHTS
# ==========================================================

RISK_WEIGHT = {
    "Low": 5,
    "Medium": 10,
    "High": 20
}


# ==========================================================
# CALCULATE OBSTACLE PENALTY
# ==========================================================

def obstacle_penalty(x1, y1, x2, y2, obstacles):

    penalty = 0

    # Midpoint of the edge
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    for _, obs in obstacles.iterrows():

        ox = obs["X"]
        oy = obs["Y"]

        distance = math.sqrt(
            (mx - ox) ** 2 +
            (my - oy) ** 2
        )

        # Obstacle close to the edge
        if distance <= 20:

            risk = obs["Risk"]

            penalty += RISK_WEIGHT.get(risk, 5)

    return penalty


# ==========================================================
# MULTI OBJECTIVE EDGE COST
# ==========================================================

def calculate_cost(
    distance,
    travel_time,
    energy,
    obstacle
):

    return round(

        0.40 * distance +

        0.25 * travel_time +

        0.20 * energy +

        0.15 * obstacle,

        2

    )


# ==========================================================
# CLASS USED BY PROPOSED ALGORITHM
# ==========================================================

class CostFunction:

    def __init__(
        self,
        w_distance=0.40,
        w_time=0.25,
        w_energy=0.20,
        w_obstacle=0.15
    ):

        self.w_distance = w_distance
        self.w_time = w_time
        self.w_energy = w_energy
        self.w_obstacle = w_obstacle

    def calculate(
        self,
        distance,
        travel_time,
        energy,
        obstacle
    ):

        return round(

            self.w_distance * distance +

            self.w_time * travel_time +

            self.w_energy * energy +

            self.w_obstacle * obstacle,

            2

        )