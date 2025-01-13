# test_fsd_software.py - Unit test script using unittest

import unittest
from fsd_software import FSDSoftware

class TestFSDSoftware(unittest.TestCase):

    def setUp(self):

        """Setup the FSDSoftware instance before each test."""
        self.fsd = FSDSoftware()
    
    def test_obstacle_detection(self):

        """Test obstacle detection when distance is less than 5 meters."""
        result = self.fsd.detect_obstacle(4)  # Obstacle at 4 meters
        self.assertTrue(result)
    
    def test_no_obstacle_detection(self):

        """Test that no obstacle is detected if distance is greater than 5 meters."""
        result = self.fsd.detect_obstacle(10)  # Obstacle at 10 meters
        self.assertFalse(result)
    
    def test_driving_decision_stop_obstacle(self):

        """Test that the decision is to stop if an obstacle is detected."""
        self.fsd.detect_obstacle(4)  # Simulate obstacle detection
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "STOP")
    
    def test_driving_decision_stop_traffic_signal(self):

        """Test that the decision is to stop if the traffic signal is red."""
        self.fsd.traffic_signal = "red"
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "STOP")
    
    def test_driving_decision_slow_down_pedestrian(self):

        """Test that the decision is to slow down if a pedestrian is detected."""
        self.fsd.pedestrian_nearby = True
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "SLOW DOWN")
    
    def test_driving_decision_go(self):

        """Test that the decision is to go if no obstacles, traffic signal is green, and no pedestrian."""
        self.fsd.traffic_signal = "green"
        self.fsd.pedestrian_nearby = False
        self.fsd.detect_obstacle(10)  # No obstacle
        result = self.fsd.make_driving_decision()
        self.assertEqual(result, "GO")
    
    def test_adjust_speed_within_range(self):

        """Test adjusting the vehicle's speed within the allowed range."""
        result = self.fsd.adjust_vehicle_speed(100)
        self.assertEqual(result, 100)
    
    def test_adjust_speed_out_of_range(self):

        """Test that adjusting the vehicle's speed outside the range raises an exception."""
        with self.assertRaises(ValueError):
            self.fsd.adjust_vehicle_speed(150)  # Speed exceeds max limit
        with self.assertRaises(ValueError):
            self.fsd.adjust_vehicle_speed(-10)  # Speed below min limit

if __name__ == '__main__':
    unittest.main()
