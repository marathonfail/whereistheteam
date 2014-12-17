import gmail
from gmail import message
import os
import datetime
from app import db, models
import re

password = os.environ['PASS']
mygmail = gmail.login('sridhar87', password)
print mygmail.logged_in

emails = mygmail.inbox().mail(after=datetime.date(2014, 12, 15), sender='sridhar87@gmail.com', unread=True)
print len(emails)


for email in emails:
    email.fetch()
    email_id = re.search('<(.+)>', email.fr)
    if email_id:
        email_id = email_id.group(1)
    sender = email_id
    user = db.session.query(models.User).filter(models.User.nickname==email_id).first()
    if not user:
        user = models.User(nickname=email_id)
        db.session.add(user)
        db.session.commit()
    sent_at = email.sent_at
    place_name = email.subject
    place = db.session.query(models.Place).filter(models.Place.place_name.ilike('%' + place_name + '%')).first()
    if place:
        user.update_current_location(place)
    email.read()
