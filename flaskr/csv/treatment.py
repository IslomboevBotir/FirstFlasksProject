import pandas as pd
from sqlalchemy import create_engine


def open_csv(csv_file: str):
    dataframe = pd.read_csv(csv_file)
    dataframe_to_dict = dataframe.to_dict(orient="records")

