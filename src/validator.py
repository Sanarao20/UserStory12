import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_drivers(drivers_df):
    logger.info("Validating drivers data")

    # Drop missing IDs
    drivers_df = drivers_df.dropna(subset=['driver_id'])

    # Keep only ACTIVE drivers
    valid_drivers = drivers_df[drivers_df['status'] == 'ACTIVE']

    logger.info(f"Valid drivers count: {len(valid_drivers)}")
    return valid_drivers


def validate_rides(rides_df, valid_driver_ids):
    logger.info("Validating rides data")

    # Convert ride_time
    rides_df['ride_time'] = pd.to_datetime(rides_df['ride_time'], errors='coerce')

    # Apply filters
    filtered = rides_df[
        (rides_df['driver_id'].isin(valid_driver_ids)) &
        (rides_df['fare_amount'] > 0) &
        (rides_df['ride_time'].notna()) &
        (rides_df['ride_status'] == 'COMPLETED')
    ]

    logger.info(f"Valid rides count: {len(filtered)}")
    return filtered