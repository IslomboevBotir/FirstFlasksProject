from sqlalchemy import Column, Integer, String, Text, Date, Boolean, Float, text, func

from database import Base


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    cid = Column(Integer)
    unit = Column(String(255))
    w_id = Column(Integer, unique=True)
    utype = Column(String(255))
    beds = Column(Integer)
    area = Column(Float)
    price = Column(Integer)
    date = Column(Date)
    is_mode = Column(Boolean)
    is_del = Column(Boolean)

    def __init__(self, cid: int, unit: str, w_id: int, utype: str, beds: int,
                 area: float, price: int, date: date, is_mode: bool, is_del: bool):
        self.cid = cid
        self.unit = unit
        self.w_id = w_id
        self.utype = utype
        self.beds = beds
        self.area = area
        self.price = price
        self.date = date
        self.is_mode = is_mode
        self.is_del = is_del
