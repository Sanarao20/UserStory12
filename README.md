# UserStory12
Ride Fare Analytics &amp; Driver Performance Engine where we process the data validate records, detect anomalies, and calculate driver performance.

# Ride Fare Analytics & Driver Performance Engine

## Overview

This project processes ride and driver data to:

* Validate records
* Filter invalid entries
* Detect anomalies
* Calculate driver performance metrics

It ensures only clean and reliable data is used for analytics.

## Features

### Data Validation

* Filters only **ACTIVE drivers**

* Removes:

  * BLOCKED drivers
  * Missing driver IDs

* Keeps only valid rides:

  * `ride_status = COMPLETED`
  * `fare_amount > 0`
  * Valid `ride_time`
  * Driver must exist and be ACTIVE

### Anomaly Detection

Detects:

* **High Fare** → fare > 500
* **Rapid Rides** → more than 2 rides within 2 minutes

### Driver Performance Metrics

For each driver:

* Total rides
* Total earnings
* Average fare

## Project Structure

```
UserStory12/
│── src/
│   ├── main.py
│   ├── validator.py
│   ├── anomaly.py
│   ├── processor.py
│
│── tests/
│   ├── test_engine.py
│
│── data/
│   ├── drivers.csv
│   ├── rides.csv
│
│── driver_performance.csv
│── anomaly_report.csv
│── app.log
```

## Setup Instructions

### Install Dependencies

```bash
pip install pandas
```

### Run the Application

```bash
python3 src/main.py
```

### Output Files Generated

* `driver_performance.csv` → Driver metrics
* `anomaly_report.csv` → Detected anomalies
* `app.log` → Execution logs

## Running Tests

### Run all tests (recommended)

```bash
python3 -m unittest discover -s tests -v
```

### Run specific test file

```bash
python3 -m unittest tests.test_engine
```

## Test Cases Covered

* `test_invalid_driver_rejected`
* `test_blocked_driver_rejected`
* `test_negative_fare_ignored`
* `test_high_fare_flag`
* `test_rapid_rides_flag`
* `test_driver_earnings_calculation`

## Logging

Logs are written to:

```
app.log
```

Includes:

* Data validation steps
* Processing steps
* Anomaly detection
* Errors (if any)

## Assumptions

* Input CSV files exist in `data/` folder
* Column names match expected schema
* Time format is parseable

## Future Enhancements

* Real-time streaming (Kafka)
* Dashboard visualization
* API integration (Flask/FastAPI)
* Scalable processing using Spark
