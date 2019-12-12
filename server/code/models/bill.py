from db import db
from datetime import datetime


class BillModel(db.Model):

    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    usage = db.Column(db.Float(precision=2), nullable=False)
    date = db.Column(db.DateTime(timezone=False), default=datetime.today)
    description = db.Column(db.String(100))

    category_id = db.Column(db.Integer, db.ForeignKey('bill_categories.id'))
    category = db.relationship('BillCategoryModel')

    def __init__(self, usage, description, category_id):
        self.usage = usage
        self.description = description
        self.category_id = category_id

    def json(self):
        date = str(self.date)
        return {'category': self.category_id,
                'usage': self.usage,
                'date': date,
                'description': self.description
                }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_latest_bill(cls, category_id):
        """returns latest bill of given category (with the most recent date) """
        return cls.query.filter_by(category_id=category_id).order_by(cls.date.desc()).first()

    def save_to_db(self):
        """Inserts/update the item to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()