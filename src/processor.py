import pandas as pd
import logging

logger = logging.getLogger(__name__)

def calculate_driver_performance(rides_df):
    logger.info("Calculating driver performance")

    performance = rides_df.groupby('driver_id').agg(
        total_rides=('ride_id', 'count'),
        total_earnings=('fare_amount', 'sum'),
        avg_fare=('fare_amount', 'mean')
    ).reset_index()

    logger.info("Driver performance calculated")
    return performance