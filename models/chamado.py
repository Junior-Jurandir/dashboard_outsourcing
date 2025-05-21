from app import db

class Chamado(db.Model):
    __tablename__ = 'chamados'

    ID = db.Column(db.Integer, primary_key=True)  # ID do chamado no GLPI
    Titulo = db.Column(db.String(255), nullable=False)  # Título do chamado
    Descricao = db.Column(db.Text)  # Descrição
    Status = db.Column(db.Integer)  # Status (1=novo, 2=andamento, etc)
    Prioridade = db.Column(db.Integer)  # Prioridade
    ID_categoria_itil = db.Column(db.Integer)  # Categoria ITIL
    ID_grupo_tecnico = db.Column(db.Integer)  # Grupo atribuído
    ID_requerente = db.Column(db.Integer)  # Usuário solicitante
    DT_criacao = db.Column(db.DateTime)  # Quando foi criado no GLPI
    DT_mod = db.Column(db.DateTime)  # Última modificação no GLPI
    DT_sync = db.Column(db.DateTime, default=db.datetime.utcnow)  # Última vez que foi sincronizado localmente

    def __repr__(self):
        return f"<Ticket(id={self.ID}, name='{self.Titulo}', status={self.Status})>"
