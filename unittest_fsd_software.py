import unittest
from fsd_software import FSDSoftware

class TestFSDSoftware(unittest.TestCase):

    def setUp(self):
        """Setup the FSDSoftware instance before each test."""
        self.fsd = FSDSoftware()

    def test_obstacle_detection_within_range(self):
        """Test obstacle detection when distance is less than 5 meters."""
        result = self.fsd.detect_obstacle(4)  # Obstacle within 5 meters
        self.assertTrue(result)

    def test_obstacle_detection_at_boundary(self):
        """Test obstacle detection when distance is exactly 5 meters."""
        result = self.fsd.detect_obstacle(5)
        self.assertTrue(result)

    def test_no_obstacle_detection_out_of_range(self):
        """Test that no obstacle is detected if distance is greater than 5 meters."""
        result = self.fsd.detect_obstacle(6)  # Obstacle beyond 5 meters
        self.assertFalse(result)

    def test_driving_decision_stop_obstacle_detected(self):
        """Test that the decision is to stop if an obstacle is detected."""
        self.fsd.detect_obstacle(4)  # Simulate obstacle detection
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "STOP")

    def test_driving_decision_stop_red_traffic_signal(self):
        """Test that the decision is to stop if the traffic signal is red."""
        self.fsd.traffic_signal = "red"
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "STOP")

    def test_driving_decision_slow_down_yellow_signal(self):
        """Test that the decision is to slow down if the traffic signal is yellow."""
        self.fsd.traffic_signal = "yellow"
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "SLOW DOWN")

    def test_driving_decision_slow_down_pedestrian_detected(self):
        """Test that the decision is to slow down if a pedestrian is detected."""
        self.fsd.pedestrian_nearby = True
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "SLOW DOWN")

    def test_driving_decision_go_clear_conditions(self):
        """Test that the decision is to go if no obstacles, traffic signal is green, and no pedestrian."""
        self.fsd.traffic_signal = "green"
        self.fsd.pedestrian_nearby = False
        self.fsd.detect_obstacle(6)  # No obstacle
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "GO")

    def test_adjust_speed_within_valid_range(self):
        """Test adjusting the vehicle's speed within the allowed range."""
        result = self.fsd.adjust_vehicle_speed(80)
        self.assertEqual(result, 80)

    def test_adjust_speed_max_limit(self):
        """Test adjusting the vehicle's speed to the maximum limit."""
        result = self.fsd.adjust_vehicle_speed(120)
        self.assertEqual(result, 120)

    def test_adjust_speed_min_limit(self):
        """Test adjusting the vehicle's speed to the minimum limit."""
        result = self.fsd.adjust_vehicle_speed(0)
        self.assertEqual(result, 0)

    def test_adjust_speed_above_max_limit(self):
        """Test that adjusting the vehicle's speed above the max limit raises an exception."""
        with self.assertRaises(ValueError):
            self.fsd.adjust_vehicle_speed(150)  # Exceeds max limit

    def test_adjust_speed_below_min_limit(self):
        """Test that adjusting the vehicle's speed below the min limit raises an exception."""
        with self.assertRaises(ValueError):
            self.fsd.adjust_vehicle_speed(-10)  # Below min limit

    def test_traffic_signal_invalid_value(self):
        """Test that setting an invalid traffic signal raises an exception."""
        with self.assertRaises(ValueError):
            self.fsd.traffic_signal = "blue"  # Invalid signal value

    def test_system_reset(self):
        """Test that the system resets all states to default."""
        self.fsd.traffic_signal = "red"
        self.fsd.pedestrian_nearby = True
        self.fsd.detect_obstacle(4)  # Simulate obstacle detection
        self.fsd.reset_system()
        self.assertEqual(self.fsd.traffic_signal, "green")  # Default signal
        self.assertFalse(self.fsd.pedestrian_nearby)
        self.assertFalse(self.fsd.obstacle_detected)

if __name__ == '__main__':
    unittest.main()
