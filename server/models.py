from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  

    baked_goods = db.relationship('BakedGood', backref='bakery')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'baked_goods': [good.to_dict() for good in self.baked_goods]
        }
        return data


class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'bakery_id': self.bakery_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,  # Add this line
        }
    