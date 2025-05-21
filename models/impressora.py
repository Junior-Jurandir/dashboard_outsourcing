from app import db
from sqlalchemy.orm import relationship

class Impressora(db.Model):
    __tablename__ = "impressoras"

    ID = db.Column(db.Integer, primary_key=True)
    Serie = db.Column(db.String(50), nullable=False)
    Modelo = db.Column(db.String(50), nullable=False)
    Contrato = db.Column(db.String(4), nullable=False)
    Secretaria = db.Column(db.String(10), nullable=False)
    Localizacao = db.Column(db.String(255), nullable=False)
    IP = db.Column(db.String(50), nullable=True)
    Tipo = db.Column(db.String(15), nullable=False)
    localizacao_id = db.Column(
        db.Integer, db.ForeignKey("localizacoes.id"), nullable=False
    )
    localizacao = relationship("Localizacao", back_populates="impressoras")
    DT_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    DT_mod = db.Column(
        db.DateTime(6),
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False,
    )
    Chamados = relationship("Chamado", back_populates="Impressora")
    Bilhetagem = relationship("Bilhetagem", back_populates="Impressora")
