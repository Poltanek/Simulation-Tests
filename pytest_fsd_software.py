import pytest
from fsd_software import FSDSoftware

@pytest.fixture
def fsd():
    """Setup the FSDSoftware instance before each test."""
    return FSDSoftware()

def test_obstacle_detection_within_range(fsd):
    """Test obstacle detection when distance is less than 5 meters."""
    result = fsd.detect_obstacle(4)  # Obstacle within 5 meters
    assert result

def test_obstacle_detection_at_boundary(fsd):
    """Test obstacle detection when distance is exactly 5 meters."""
    result = fsd.detect_obstacle(5)
    assert result

def test_no_obstacle_detection_out_of_range(fsd):
    """Test that no obstacle is detected if distance is greater than 5 meters."""
    result = fsd.detect_obstacle(6)  # Obstacle beyond 5 meters
    assert not result

def test_driving_decision_stop_obstacle_detected(fsd):
    """Test that the decision is to stop if an obstacle is detected."""
    fsd.detect_obstacle(4)  # Simulate obstacle detection
    result = fsd.make_driving_decision()
    assert result == "STOP"

def test_driving_decision_stop_red_traffic_signal(fsd):
    """Test that the decision is to stop if the traffic signal is red."""
    fsd.traffic_signal = "red"
    result = fsd.make_driving_decision()
    assert result == "STOP"

def test_driving_decision_slow_down_yellow_signal(fsd):
    """Test that the decision is to slow down if the traffic signal is yellow."""
    fsd.traffic_signal = "yellow"
    result = fsd.make_driving_decision()
    assert result == "SLOW DOWN"

def test_driving_decision_slow_down_pedestrian_detected(fsd):
    """Test that the decision is to slow down if a pedestrian is detected."""
    fsd.pedestrian_nearby = True
    result = fsd.make_driving_decision()
    assert result == "SLOW DOWN"

def test_driving_decision_go_clear_conditions(fsd):
    """Test that the decision is to go if no obstacles, traffic signal is green, and no pedestrian."""
    fsd.traffic_signal = "green"
    fsd.pedestrian_nearby = False
    fsd.detect_obstacle(6)  # No obstacle
    result = fsd.make_driving_decision()
    assert result == "GO"

def test_adjust_speed_within_valid_range(fsd):
    """Test adjusting the vehicle's speed within the allowed range."""
    result = fsd.adjust_vehicle_speed(80)
    assert result == 80

def test_adjust_speed_max_limit(fsd):
    """Test adjusting the vehicle's speed to the maximum limit."""
    result = fsd.adjust_vehicle_speed(120)
    assert result == 120

def test_adjust_speed_min_limit(fsd):
    """Test adjusting the vehicle's speed to the minimum limit."""
    result = fsd.adjust_vehicle_speed(0)
    assert result == 0

def test_adjust_speed_above_max_limit(fsd):
    """Test that adjusting the vehicle's speed above the max limit raises an exception."""
    with pytest.raises(ValueError):
        fsd.adjust_vehicle_speed(150)  # Exceeds max limit

def test_adjust_speed_below_min_limit(fsd):
    """Test that adjusting the vehicle's speed below the min limit raises an exception."""
    with pytest.raises(ValueError):
        fsd.adjust_vehicle_speed(-10)  # Below min limit

def test_traffic_signal_invalid_value(fsd):
    """Test that setting an invalid traffic signal raises an exception."""
    with pytest.raises(ValueError):
        fsd.traffic_signal = "blue"  # Invalid signal value

def test_system_reset(fsd):
    """Test that the system resets all states to default."""
    fsd.traffic_signal = "red"
    fsd.pedestrian_nearby = True
    fsd.detect_obstacle(4)  # Simulate obstacle detection
    fsd.reset_system()
    assert fsd.traffic_signal == "green"  # Default signal
    assert not fsd.pedestrian_nearby
    assert not fsd.obstacle_detected

# New tests
def test_adjust_speed_just_below_max_limit(fsd):
    """Test adjusting the vehicle's speed to just below the maximum limit."""
    result = fsd.adjust_vehicle_speed(119)
    assert result == 119

def test_driving_decision_conflicting_inputs(fsd):
    """Test decision-making logic under conflicting inputs."""
    fsd.traffic_signal = "green"
    fsd.pedestrian_nearby = True
    fsd.detect_obstacle(4)  # Simulate obstacle detection
    result = fsd.make_driving_decision()
    assert result == "STOP"  # Ensure system prioritizes safety.

def test_logs_on_obstacle_detection(fsd, capsys):
    """Test that logs are generated correctly when an obstacle is detected."""
    fsd.detect_obstacle(4)
    captured = capsys.readouterr()
    assert "Obstacle detected at 4 meters." in captured.out

def test_system_reset_with_config(fsd):
    """Test that reset works with custom configurations."""
    fsd.traffic_signal = "yellow"
    fsd.pedestrian_nearby = True
    fsd.detect_obstacle(2)  # Simulate obstacle detection
    fsd.reset_system(default_signal="yellow")
    assert fsd.traffic_signal == "yellow"  # Custom default
    assert not fsd.pedestrian_nearby
    assert not fsd.obstacle_detected

