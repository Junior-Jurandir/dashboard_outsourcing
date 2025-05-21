from app import db
from sqlalchemy.orm import relationship

class Bilhetagem(db.Model):
    __tablename__ = "bilhetagem"

    ID = db.Column(db.Integer, primary_key=True)
    Serie = db.Column(db.String(50), db.ForeignKey("impressoras.Serie"), nullable=False)
    Impressora = relationship("Impressora", back_populates="Bilhetagem")
    Contrato = db.Column(db.String(50), nullable=False)
    Localizacao = db.Column(db.String(255), nullable=False)
    Tipo = db.Column(db.String(50), nullable=False)
    Ano = db.Column(db.String(50), nullable=False)
    Mes = db.Column(db.String(50), nullable=False)
    QT_impresoes = db.Column(db.Integer, nullable=False)
    DT_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    DT_mod = db.Column(
        db.DateTime(6),
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False,
    )
