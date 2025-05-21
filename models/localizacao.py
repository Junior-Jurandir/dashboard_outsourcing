from app import db
from sqlalchemy.orm import relationship

class Localizacao(db.Model):
    __tablename__ = "localizacoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    endereco = db.Column(db.String(120), unique=True, nullable=False)
    contato = db.Column(db.String(15), nullable=False)
    secretaria = db.Column(db.String(50), nullable=False)
    DT_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    DT_mod = db.Column(
        db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False
    )
    impressoras = relationship("Impressora", back_populates="localizacao")

    def __repr__(self):
        return self.nome
