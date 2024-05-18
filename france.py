from datetime import datetime
import pvlib

# datetime(year, month, day, hour, minute, second, microsecond)
start = datetime(2020, 6, 21, 0, 0)
end = datetime(2020, 12, 21, 23, 59)
username="bsrnftp"
password="bsrn1"

france, metadata=pvlib.iotools.get_bsrn("pal", start, end, username, password, logical_records=('0100',), save_path="/Users/rijass/Desktop/untitled folder/France/")
print(france.columns)