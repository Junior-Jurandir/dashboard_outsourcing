from app import db

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return self.name
