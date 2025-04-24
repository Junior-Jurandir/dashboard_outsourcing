# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_admin.menu import MenuLink

from admin.Views import HomeView, UserView, GenericView, ChamadoView
from models import *


def start_views(app, db):
    admin = Admin(
        app,
        name="Dashboard",
        base_template="admin/base.html",
        template_mode="bootstrap3",
        index_view=HomeView(),
    )
    admin.add_link(MenuLink(name="Logout", url="/logout/"))

    admin.add_view(GenericView(Role, db.session, "Funções", category="Admin"))
    admin.add_view(UserView(User, db.session, "Usuários", category="Admin"))
    admin.add_view(
        GenericView(Impressora, db.session, "Impressoras", category="Gestão")
    )
    admin.add_view(ChamadoView(Chamado, db.session, "Chamados", category="Gestão"))
    admin.add_view(GenericView(Bilhetagem, db.session, "Bilhetagem", category="Gestão"))
