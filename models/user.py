from app import db
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from .role import Role
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    DT_criacao = db.Column(
        db.DateTime(6), default=db.func.current_timestamp(), nullable=False
    )
    DT_mod = db.Column(
        db.DateTime(6),
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False,
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

    def verify_password(self, password_no_hash, password_DTbase):
        try:
            return pbkdf2_sha256.verify(password_no_hash, password_DTbase)
        except ValueError as e:
            print("Erro ao verificar a senha: %s" % e)
            return False
