# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship
from config import app_active, app_config
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from app import db

config = app_config[app_active]
manager = None


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    data_de_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    ultimo_update = db.Column(
        db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False
    )
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey(Role.id), nullable=False)
    funcao = relationship("Role")

    def __repr__(self):
        return "%s - %s" % (self.username, self.email)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def get_user_by_id(self, id):
        return User.query.get(id)

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def hash_password(self, password):
        try:
            return pbkdf2_sha256.hash(password)
        except Exception as e:
            print("Erro ao criptografar a senha: %s" % e)

    def verify_password(self, password_no_hash, password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash, password_database)
        except ValueError as e:
            print("Erro ao verificar a senha: %s" % e)
            return False


"""
class Localizacao(db.Model):
    __tablename__ = "localizacoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    endereco = db.Column(db.String(120), unique=True, nullable=False)
    contato = db.Column(db.String(15), nullable=False)
    secretaria = db.Column(db.String(50), nullable=False)
    data_de_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    ultimo_update = db.Column(
        db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False
    )
    impressoras = relationship("Impressora", back_populates="localizacao")

    def __repr__(self):
        return self.nome
"""


class Impressora(db.Model):
    __tablename__ = "impressoras"

    Serie = db.Column(db.String(50), primary_key=True)
    Modelo = db.Column(db.String(50), nullable=False)
    Contrato = db.Column(db.String(4), nullable=False)
    Secretaria = db.Column(db.String(10), nullable=False)
    Localizacao = db.Column(db.String(50), nullable=False)
    IP = db.Column(db.String(50), nullable=False)
    Tipo = db.Column(db.String(15), nullable=False)
    # localizacao_id = db.Column(
    #     db.Integer, db.ForeignKey("localizacoes.id"), nullable=False
    # )
    # localizacao = relationship("Localizacao", back_populates="impressoras")
    Data_de_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    Ultimo_update = db.Column(
        db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False
    )
    Chamados = relationship("Chamado", back_populates="Impressora")
    Bilhetagem = relationship("Bilhetagem", back_populates="Impressora")


class Chamado(db.Model):
    __tablename__ = "chamados"

    ID = db.Column(db.Integer, primary_key=True)
    Título = db.Column(db.String(50), nullable=False)
    Localizacao = db.Column(db.String(50), nullable=False)
    Descricao = db.Column(db.String(2000), nullable=False)
    Serie_impressora = db.Column(
        db.String(50), db.ForeignKey("impressoras.Serie"), nullable=False
    )
    Impressora = relationship("Impressora", back_populates="Chamados")
    Data_de_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    Ultimo_update = db.Column(
        db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False
    )


class Bilhetagem(db.Model):
    __tablename__ = "bilhetagem"

    ID = db.Column(db.Integer, primary_key=True)
    Serie = db.Column(db.String(50), db.ForeignKey("impressoras.Serie"), nullable=False)
    Impressora = relationship("Impressora", back_populates="Bilhetagem")
    Contrato = db.Column(db.String(50), nullable=False)
    Localizacao = db.Column(db.String(50), nullable=False)
    Tipo = db.Column(db.String(50), nullable=False)
    Ano = db.Column(db.String(50), nullable=False)
    Mes = db.Column(db.String(50), nullable=False)
    Bilhetagem = db.Column(db.Integer, nullable=False)
    Data_de_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    Ultimo_update = db.Column(
        db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False
    )
