import sys
import os
import pandas as pd
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validator import validate_drivers, validate_rides
from anomaly import detect_anomalies
from processor import calculate_driver_performance


def setup_logging():
    log_file = "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  
            logging.StreamHandler()
        ]
    )


def main():
    setup_logging()  

    logging.info("Starting Ride Fare Analytics Engine")

    drivers = pd.read_csv("data/drivers.csv")
    rides = pd.read_csv("data/rides.csv")

    # Validate
    valid_drivers = validate_drivers(drivers)
    valid_rides = validate_rides(rides, valid_drivers['driver_id'])

    # Process
    performance = calculate_driver_performance(valid_rides)

    # Detect anomalies
    anomalies = detect_anomalies(valid_rides)

    # Save outputs
    performance.to_csv("driver_performance.csv", index=False)
    pd.DataFrame(anomalies).to_csv("anomaly_report.csv", index=False)

    logging.info("Processing completed successfully")


if __name__ == "__main__":
    main()