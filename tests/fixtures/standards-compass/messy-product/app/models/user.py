from .db import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String)
    phone = db.Column(db.String)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="inspector")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "phone": self.phone,
            "role": self.role,
        }
