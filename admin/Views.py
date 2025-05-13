from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.inspection import inspect
from flask_login import current_user
from flask import redirect
from flask_admin.helpers import get_url
from markupsafe import Markup

from config import app_config, app_active
from models import *

config = app_config[app_active]


class HomeView(AdminIndexView):
    extra_css = ["https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.css"]
    extra_js = [
        "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js",
        "/static/js/chart.js",
    ]

    @expose("/")
    def index(self):
        return self.render("home.html")
        # if current_user.is_authenticated:
        #    return self.render("admin/index.html")
        # else:
        #    return redirect("/login/")

    def is_acessible(self):
        return True

    # def inaccessible_callback(self, name, **kwargs):
    #    if current_user.is_authenticated:
    #        return redirect("/admin/")
    #    else:
    #        return redirect("/login/")


class UserView(ModelView):
    column_exclude_list = ["password"]
    form_excluded_columns = ["last_update"]

    form_columns = [
        "id",
        "username",
        "email",
        "password",
        "funcao",
        "data_de_criacao",
        "ativo",
    ]

    form_widget_args = {
        "password": {
            "autocomplete": "off",
            "type": "password",
        }
    }

    def on_model_change(self, form, User, is_created):
        if form.password.data is not None:
            User.set_password(form.password.data)
        else:
            del form.password

    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)

        columns_to_exclude = set(self.column_exclude_list or [])
        self.column_filters = [
            c.key for c in inspect(model).mapper.column_attrs
            if c.key not in columns_to_exclude
        ]

    def is_accessible(self):
        return True
    
    

    # def inaccessible_callback(self, name, **kwargs):
    #    if current_user.is_authenticated:
    #        return redirect("/admin/")
    #    else:
    #        return redirect("/login/")


class GenericView(ModelView):
    column_exclude_list = ["Data_de_criacao"]
    column_exclude_list = ["Ultimo_update"]
    form_excluded_columns = ["last_update"]

    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)

        # Gera filtros de forma automática para todas as colunas exceto as excluídas
        columns_to_exclude = set(self.column_exclude_list or [])
        self.column_filters = [
            c.key for c in inspect(model).mapper.column_attrs
            if c.key not in columns_to_exclude
        ]

    def is_accessible(self):
        return True

    # def inaccessible_callback(self, name, **kwargs):
    #    if current_user.is_authenticated:
    #        return redirect("/admin/")
    #    else:
    #        return redirect("/login/")

    column_display_pk = True  # Isso força a exibição da chave primária


class ChamadoView(GenericView):
    form_excluded_columns = ["last_update"]
    column_formatters = {
        "ID": lambda v, c, m, p: Markup(
            f'<a href="https://itsm.santanadeparnaiba.sp.gov.br/front/ticket.form.php?id={m.ID}" target="_blank">{m.ID}</a>'
        )
    }

    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)

        columns_to_exclude = set(self.column_exclude_list or [])
        self.column_filters = [
            c.key for c in inspect(model).mapper.column_attrs
            if c.key not in columns_to_exclude
        ]
