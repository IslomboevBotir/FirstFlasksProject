from sqlalchemy import text
from flaskr.csv.treatment import parse_in_data_base
import pandas as pd
from database import db, app
from controller import (all_data_logic, most_expensive_unit_logic, largest_area_unit_logic, all_villa_logic,
                        projects_logic, search_get_logic, search_post_logic, search_params_route)


@app.route('/')
def all_data():
    return all_data_logic()


@app.route('/most_expensive_unit')
def most_expensive_unit():
    return most_expensive_unit_logic()


@app.route('/largest_area_unit')
def largest_area_unit():
    return largest_area_unit_logic()


@app.route('/all_villa')
def all_vila():
    return all_villa_logic()


@app.route('/projects')
def projects():
    return projects_logic()


@app.route('/search', methods=['GET'])
def search_get():
    return search_get_logic()


@app.route('/search', methods=['POST'])
def search_post():
    return search_post_logic()


@app.route('/search_params', methods=['GET'])
def search_params():
    return search_params_route()


if __name__ == '__main__':
    query_insert_in_table = text("""
                        INSERT INTO project (cid, unit, w_id, utype, beds, area, price, date, is_mode, is_del) 
                        VALUES (:cid, :unit, :w_id, :utype, :beds, :area, :price, :date, :is_mode, :is_del)
                        ON CONFLICT (w_id) DO UPDATE SET 
                        cid = EXCLUDED.cid,
                        unit = EXCLUDED.unit,
                        utype = EXCLUDED.utype,
                        beds = EXCLUDED.beds,
                        area = EXCLUDED.area,
                        price = EXCLUDED.price,
                        date = EXCLUDED.date,
                        is_mode = EXCLUDED.is_mode,
                        is_del = EXCLUDED.is_del
                        """)
    with app.app_context():
        db.create_all()
        parse_in_data_base(db.engine, pd.read_csv('csv/axcapital_09082023.csv'), query_insert_in_table)
    app.run(debug=True)
