from app import db
from datetime import datetime

place_history = db.Table('location_history',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('place_id', db.Integer, db.ForeignKey('place.id')),
    db.Column('checkin_time', db.DateTime(), default=db.func.now())
)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(128), index=True)
    country = db.Column(db.String(128), index=True)
    timezone = db.Column(db.String(128), nullable=True)
    place_latitude = db.Column(db.Float, nullable=True)
    place_longitude = db.Column(db.Float, nullable=True)
    users = db.relationship('User', backref='current_location', lazy='dynamic')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    profile_pic_url = db.Column(db.String(120), nullable=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=True)
    places = db.relationship('Place', secondary=place_history, backref=db.backref('users', lazy='dynamic'))
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)

    def update_current_location(self, place):
        self.places.add(place)
        if self.place_id != place.id:
            self.place_id = place.id
        self.last_updated = datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.nickname)
