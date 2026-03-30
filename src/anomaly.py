import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

def detect_anomalies(rides_df):
    logger.info("Detecting anomalies")

    anomalies = []

    # High fare detection
    high_fare = rides_df[rides_df['fare_amount'] > 500]
    for _, row in high_fare.iterrows():
        anomalies.append({
            "ride_id": row['ride_id'],
            "driver_id": row['driver_id'],
            "reason": "HIGH_FARE"
        })

    # Rapid rides detection
    rides_df = rides_df.sort_values(by=['driver_id', 'ride_time'])

    for driver_id, group in rides_df.groupby('driver_id'):
        group = group.sort_values('ride_time')

        for i in range(1, len(group)):
            diff = group.iloc[i]['ride_time'] - group.iloc[i-1]['ride_time']
            if diff <= timedelta(minutes=2):
                anomalies.append({
                    "ride_id": group.iloc[i]['ride_id'],
                    "driver_id": driver_id,
                    "reason": "RAPID_RIDES"
                })

    logger.info(f"Total anomalies detected: {len(anomalies)}")
    return anomalies