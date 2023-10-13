from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, Float, text, func
from serializer import ProjectSchema
import pandas as pd
from datetime import datetime
from models import DataBaseProject
from database import db, app

project_schema = ProjectSchema()


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


@app.route('/')
def all_data():
    all_projects = DataBaseProject.query.order_by('id').all()
    projects_list = [project_schema.dump(project) for project in all_projects]
    return projects_list


@app.route('/most_expensive_unit')
def most_expensive_unit():
    query = (
        db.session.query(DataBaseProject)
        .order_by(DataBaseProject.price.desc()).first()
    )

    if query:
        result_data = project_to_dict(query)
        return jsonify({"most_expensive_unit": result_data})
    return jsonify({"message": "No projects found"})


@app.route('/largest_area_unit')
def largest_area_unit():
    query = (
        db.session.query(DataBaseProject)
        .order_by(DataBaseProject.area.desc())
        .first()
    )

    if query:
        result_data = project_to_dict(query)
        return jsonify({"largest_area_unit": result_data})
    return jsonify({"message": "No projects found"})


@app.route('/all_villa')
def all_vila():
    query = (
        db.session.query(DataBaseProject.unit, func.count().label('villa_count'))
        .filter(DataBaseProject.utype == 'Villa')
        .group_by(DataBaseProject.unit)
        .order_by(func.count().desc())
            )
    if query:
        result_data = [{"unit": unit, "villa_count": villa_count} for unit, villa_count in query]
        return jsonify({"all_vila": result_data})
    return jsonify({"message": "No projects found"})


@app.route('/projects')
def projects():
    query = (
        db.session.query(
                         DataBaseProject.unit,
                         DataBaseProject.utype,
                         func.count().label('projects_count')
        )
        .group_by(DataBaseProject.unit, DataBaseProject.utype)
        .order_by(func.count().desc())
        .all()
    )
    if query:
        result_data = [{"project": unit, "utype": utype, "projects_count": projects_count}
                       for unit, utype, projects_count in query]
        return jsonify({"all_projects": result_data})
    return jsonify({"message": "No projects found"})


@app.route('/search', methods=['GET'])
def search_get():

    unit = request.args.get('unit', '')

    if not unit:
        return jsonify({"message": "Parameter 'unit' is required"})
    query = (
        db.session.query(
                        DataBaseProject.unit,
                        DataBaseProject.utype,
                        DataBaseProject.beds,
                        DataBaseProject.area,
                        DataBaseProject.price,
                        DataBaseProject.date
        )
        .filter(DataBaseProject.unit.ilike(f'%{unit}%'))
    )
    if query:
        result_data = [{"project": unit, "utype": utype, "beds": beds, "area": area, "price": price, "date": date}
                       for unit, utype, beds, area, price, date in query]
        return jsonify({"project": result_data})
    return jsonify({"message": "No projects found"})


@app.route('/search', methods=['POST'])
def search_post():

    data = request.get_json()
    unit = data.get('unit', '')

    if not unit:
        return jsonify({"message": "Parameter 'unit' is required"})
    query = (
        db.session.query(
            DataBaseProject.unit,
            DataBaseProject.utype,
            DataBaseProject.beds,
            DataBaseProject.area,
            DataBaseProject.price,
            DataBaseProject.date
        )
        .filter(DataBaseProject.unit.ilike(f'%{unit}%'))
    )
    if query:
        result_data = [{"project": unit, "utype": utype, "beds": beds, "area": area, "price": price, "date": date}
                       for unit, utype, beds, area, price, date in query]
        return jsonify({"project": result_data})
    return jsonify({"message": "No projects found"})


def project_to_dict(project):
    return {
        'id': project.id,
        'cid': project.cid,
        'unit': project.unit,
        'w_id': project.w_id,
        'utype': project.utype,
        'beds': project.beds,
        'area': project.area,
        'price': project.price,
        'date': project.date.isoformat(),
        'is_mode': project.is_mode,
        'is_del': project.is_del
    }


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
