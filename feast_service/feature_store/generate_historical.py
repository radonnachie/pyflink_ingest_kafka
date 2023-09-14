from datetime import datetime, timedelta
import base64
import os
from random import uniform
import pandas

date_zero = datetime(2000, 1, 1, 12, 00, 00)

df = pandas.DataFrame(
    [
        {
            'entity_no': entity_no,
            'title': ["Mr", "Mrs", "Ms", "Dr"][int(uniform(0, 4)//1)],
            'firstname': base64.b64encode(os.urandom(int(uniform(2, 20)//1))).decode('ascii'),
            'surname': base64.b64encode(os.urandom(int(uniform(2, 20)//1))).decode('ascii'),
            'date_of_birth': date_zero - timedelta(days=uniform(18, 65)*365),
            'sys_eff_to': date_zero + timedelta(days=uniform(180, 365*5)),
            'sys_eff_from': date_zero,
        }
        for entity_no in range(2000)
    ]
)

df.to_parquet("entities.parquet")
