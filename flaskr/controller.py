from flask import jsonify, request, Response
from sqlalchemy import func
from models import DataBaseProject
from database import db
from serializer import ProjectSearchSchema, AllVilaSchema, ALLProjectSchema


def all_data_logic():
    query = db.session.query(DataBaseProject).order_by(DataBaseProject.id).all()
    if query:
        result_data = [ProjectSearchSchema(unit=project.unit, u_type=project.utype,
                                           beds=project.beds, area=project.area, price=project.price,
                                           date=project.date)
                       .dict() for project in query]
        return jsonify({"all_projects": result_data})
    return jsonify({"message": "No projects found"})


def most_expensive_unit_logic():
    query = (
        db.session.query(DataBaseProject)
        .order_by(DataBaseProject.price.desc()).first()
    )
    print(query)
    if query:
        result_data = [ProjectSearchSchema(unit=query.unit,  u_type=query.utype,
                                           beds=query.beds, area=query.area, price=query.price,
                                           date=query.date, ).dict()]
        return jsonify({"most_expensive_unit": result_data})
    return jsonify({"message": "No projects found"})


def largest_area_unit_logic():
    query = (
        db.session.query(DataBaseProject)
        .order_by(DataBaseProject.area.desc())
        .first()
    )

    if query:
        result_data = [ProjectSearchSchema(unit=query.unit, u_type=query.utype,
                                           beds=query.beds, area=query.area, price=query.price,
                                           date=query.date).dict()]
        return jsonify({"largest_area_unit": result_data})
    return jsonify({"message": "No projects found"})


def all_villa_logic():
    query = (
        db.session.query(DataBaseProject.unit, func.count().label('villa_count'))
        .filter(DataBaseProject.utype == 'Villa')
        .group_by(DataBaseProject.unit)
        .order_by(func.count().desc())
    )
    if query:
        result_data = [AllVilaSchema(unit=project.unit, villa_count=project.villa_count)
                       .dict() for project in query]
        return jsonify({"all_vila": result_data})
    return jsonify({"message": "No projects found"})


def projects_logic():
    query = (
        db.session.query(
            DataBaseProject.unit,
            DataBaseProject.utype,
            func.count().label('project_count')
        )
        .group_by(DataBaseProject.unit, DataBaseProject.utype)
        .order_by(func.count().desc())
        .all()
    )
    result_data = [ALLProjectSchema(unit=project.unit, u_type=project.utype,
                                    project_count=project.project_count).dict() for project in query]
    if query:
        return jsonify({"all_projects": result_data})
    return jsonify({"message": "No projects found"})


def search_get_logic() -> Response:
    unit = request.args.get('unit', '')
    return __treatment_search(unit, 'GET')


def search_post_logic() -> Response:
    unit = request.get_json().get('unit', '')
    return __treatment_search(unit, 'POST')


def __treatment_search(unit: str, query_type='GET') -> Response:
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
    if query_type == 'POST':
        request.get_json().get('unit', '')
    result_data = [ProjectSearchSchema(
        unit=project.unit, u_type=project.utype, beds=project.beds,
        area=project.area, price=project.price, date=project.date
    ).dict() for project in query]

    return jsonify({"project": result_data}) if result_data else jsonify({"message": "No projects found"})


def search_params_route():
    unit = request.args.get('unit', '')
    utype = request.args.get('utype', '')
    beds = request.args.get('beds', '')

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

    if utype:
        query = query.filter(DataBaseProject.utype == utype)
    if beds:
        query = query.filter(DataBaseProject.beds == beds)

    result_data = [
        ProjectSearchSchema(unit=project.unit, u_type=project.utype, beds=project.beds,
                            area=project.area, price=project.price, date=project.date).dict()
        for project in query
    ]

    return jsonify({"project": result_data})
