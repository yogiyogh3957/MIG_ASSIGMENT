from main.config import Config_db, Config_app
from sqlalchemy.orm import relationship
from main import db

class AuthModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    token = db.Column(db.String(200))

    activity = relationship("ActivityModel", back_populates = "owned_by_parents")

class ActivityModel(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)

    owned_by = db.Column(db.Text, db.ForeignKey("users.id"))
    owned_by_parents = relationship("AuthModel", back_populates="activity")

    type = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

db.create_all()
