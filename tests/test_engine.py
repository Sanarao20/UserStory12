import unittest
import pandas as pd
from src.validator import validate_drivers, validate_rides
from src.anomaly import detect_anomalies
from src.processor import calculate_driver_performance

class TestRideEngine(unittest.TestCase):

    def setUp(self):
        self.drivers = pd.DataFrame({
            'driver_id': [1, 2, 3],
            'status': ['ACTIVE', 'BLOCKED', 'ACTIVE']
        })

        self.rides = pd.DataFrame({
            'ride_id': [101, 102, 103, 104],
            'driver_id': [1, 2, 1, 3],
            'fare_amount': [100, -50, 600, 200],
            'ride_time': [
                '2024-01-01 10:00:00',
                '2024-01-01 10:01:00',
                '2024-01-01 10:02:00',
                'invalid_time'
            ],
            'ride_status': ['COMPLETED', 'COMPLETED', 'COMPLETED', 'COMPLETED']
        })

    def test_invalid_driver_rejected(self):
        drivers = validate_drivers(self.drivers)
        self.assertNotIn(2, drivers['driver_id'].values)

    def test_blocked_driver_rejected(self):
        drivers = validate_drivers(self.drivers)
        self.assertEqual(len(drivers), 2)

    def test_negative_fare_ignored(self):
        valid_drivers = validate_drivers(self.drivers)
        valid_rides = validate_rides(self.rides, valid_drivers['driver_id'])
        self.assertTrue((valid_rides['fare_amount'] > 0).all())

    def test_high_fare_flag(self):
        valid_drivers = validate_drivers(self.drivers)
        valid_rides = validate_rides(self.rides, valid_drivers['driver_id'])
        anomalies = detect_anomalies(valid_rides)

        reasons = [a['reason'] for a in anomalies]
        self.assertIn("HIGH_FARE", reasons)

    def test_rapid_rides_flag(self):
        valid_drivers = validate_drivers(self.drivers)
        valid_rides = validate_rides(self.rides, valid_drivers['driver_id'])
        anomalies = detect_anomalies(valid_rides)

        reasons = [a['reason'] for a in anomalies]
        self.assertIn("RAPID_RIDES", reasons)

    def test_driver_earnings_calculation(self):
        valid_drivers = validate_drivers(self.drivers)
        valid_rides = validate_rides(self.rides, valid_drivers['driver_id'])
        performance = calculate_driver_performance(valid_rides)

        driver_1 = performance[performance['driver_id'] == 1]
        self.assertEqual(driver_1['total_earnings'].values[0], 700)


if __name__ == '__main__':
    unittest.main()