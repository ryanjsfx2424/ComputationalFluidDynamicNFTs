import os
from pyairtable import Table
api_key = os.environ['airTable']

BASE_ID = "tblUnIXjelLvu8KlO"
TABLE_NAME = "Table 1".replace(" ","%20")

table = Table(api_key, BASE_ID, TABLE_NAME)
table.all()
