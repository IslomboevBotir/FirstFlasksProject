
from datetime import datetime
import pandas as pd


def parse_in_data_base(engine, read_csv, query):
    csv_in_dict = read_csv.to_dict(orient="records")
    count = 0
    with engine.connect() as connection:
        for data in csv_in_dict:
            data['DATE'] = datetime.strptime(data['DATE'], '%d.%m.%Y').strftime('%Y-%m-%d')
            if pd.isna(data['IS_MODE']):
                data['IS_MODE'] = None
            if pd.isna(data['IS_DEL']):
                data['IS_DEL'] = None
            data = {
                'cid': data['CID'],
                'unit': data['UNIT'],
                'w_id': data['W_ID'],
                'utype': data['UTYPE'],
                'beds': data['BEDS'],
                'area': data['AREA'],
                'price': data['PRICE'],
                'date': data['DATE'],
                'is_mode': data['IS_MODE'],
                'is_del': data['IS_DEL'],
            }
            connection.execute(query, data)
            count += 1
            if count % 10 == 0:
                connection.commit()
        connection.commit()
