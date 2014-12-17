from app import db
from datetime import datetime

place_history = db.Table('location_history',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('place_id', db.Integer, db.ForeignKey('place.id')),
    db.Column('checkin_time', db.DateTime, default=db.func.now(), nullable=True)
)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(128), index=True)
    country = db.Column(db.String(128), index=True)
    timezone = db.Column(db.String(128), nullable=True)
    place_latitude = db.Column(db.Float, nullable=True)
    place_longitude = db.Column(db.Float, nullable=True)
    users = db.relationship('User', backref='current_location', lazy='dynamic')
    user_history = db.relationship('UserLocationHistory', backref='place', lazy='dynamic')

    def __repr__(self):
        return '<Place: %r, Country: %r>' % (self.place_name, self.country)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    profile_pic_url = db.Column(db.String(120), nullable=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=True)
    places = db.relationship('UserLocationHistory', backref='user', lazy='dynamic')
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)

    def update_current_location(self, place):
        self.place_id = place.id
        self.last_updated = datetime.now()
        user_location_history = UserLocationHistory(user_id=self.id, place_id=place.id)
        db.session.add(user_location_history)
        db.session.commit()

    def __repr__(self):
        return '<User %r, Place %r>' % (self.nickname, self.current_location)

class UserLocationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    checkin_time = db.Column(db.DateTime, default=db.func.now(), nullable=True)

    def __repr__(self):
        return '<User: %r, Place: %r, when: %r' % (self.user, self.place, self.checkin_time)
