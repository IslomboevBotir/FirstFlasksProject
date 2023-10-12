from marshmallow import Schema, fields


class ProjectSchema(Schema):
    cid = fields.Int()
    unit = fields.Str()
    w_id = fields.Int()
    u_type = fields.Str()
    beds = fields.Int()
    area = fields.Float()
    price = fields.Int()
    date = fields.Date()
    is_mode = fields.Bool()
    is_del = fields.Bool()


class Project:
    def __init__(self, cid, unit, w_id, u_type, beds, area, price, date, is_mode, is_del):
        self.cid = cid
        self.unit = unit
        self.w_id = w_id
        self.u_type = u_type
        self.beds = beds
        self.area = area
        self.price = price
        self.date = date
        self.is_mode = is_mode
        self.is_del = is_del
        