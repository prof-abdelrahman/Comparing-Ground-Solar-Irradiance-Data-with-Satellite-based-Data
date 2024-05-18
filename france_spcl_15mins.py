from datetime import datetime
import pvlib
import pandas as pd

# datetime(year, month, day, hour, minute, second, microsecond)
start = datetime(2020, 1, 27, 0, 0)
end = datetime(2020, 1, 27, 23, 59)
username="bsrnftp"
password="bsrn1"

france, metadata=pvlib.iotools.get_bsrn("pal", start, end, username, password, logical_records=('0100',), save_path="/Users/rijass/Desktop/FPS/special_days/France/")
print(france.columns)
print(france['ghi'])

import pandas as pd

# Assuming you already have the 'france' DataFrame with the required data

# Specify the start and end dates
start_date = '2020-01-27 00:00:00+00:00'
end_date = '2020-01-27 23:59:59+00:00'

# Filter the 'france' DataFrame based on the date range
france_spcl_day1 = france[(france.index >= start_date) & (france.index <= end_date)].copy()

# Extract the timestamps at 15-minute intervals
timestamps_15min = pd.date_range(start=start_date, end=end_date, freq='15T')

# Filter the 'france_spcl_day1' DataFrame to include only the specified timestamps
france_spcl_day1 = france_spcl_day1.loc[timestamps_15min]

# Save the filtered DataFrame to a new file
france_spcl_day1.to_csv('france_spcl_day1_15min.csv')
