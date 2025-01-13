# Simplified FSD software example

class FSDSoftware:
    def __init__(self):
        self.vehicle_speed = 0  # in km/h
        self.obstacle_detected = False
        self.traffic_signal = "green" 
        self.pedestrian_nearby = False

    def detect_obstacle(self, distance):

        """Simulates obstacle detection. If an object is too close, it triggers a warning."""
        if distance < 5:  # distance in meters
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False
        return self.obstacle_detected

    def make_driving_decision(self):

        """Decides whether to stop, go, or slow down based on the environment."""
        if self.obstacle_detected:
            return "STOP"
        elif self.traffic_signal == "red":
            return "STOP"
        elif self.pedestrian_nearby:
            return "SLOW DOWN"
        else:
            return "GO"

    def adjust_vehicle_speed(self, speed):

        """Adjust the vehicle's speed."""
        if 0 <= speed <= 120:  # Max speed of 120 km/h
            self.vehicle_speed = speed
        else:
            raise ValueError("Speed out of range")
        return self.vehicle_speed
