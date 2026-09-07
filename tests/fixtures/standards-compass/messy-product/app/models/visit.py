from .db import db


class Visit(db.Model):
    __tablename__ = "visits"
    id = db.Column(db.String, primary_key=True)
    inspector_id = db.Column(db.String, db.ForeignKey("users.id"))
    site_name = db.Column(db.String)
    site_address = db.Column(db.String)
    client_email = db.Column(db.String)
    client_name = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    notes = db.Column(db.Text)
    report_html = db.Column(db.Text)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
