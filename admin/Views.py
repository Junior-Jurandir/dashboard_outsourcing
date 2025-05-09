from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
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

    def is_accessible(self):
        return True

    # def inaccessible_callback(self, name, **kwargs):
    #    if current_user.is_authenticated:
    #        return redirect("/admin/")
    #    else:
    #        return redirect("/login/")

    column_display_pk = True  # Isso força a exibição da chave primária


class ChamadoView(GenericView):
    column_formatters = {
        "id": lambda v, c, m, p: Markup(
            f'<a href="https://itsm.santanadeparnaiba.sp.gov.br/front/ticket.form.php?id={m.id}" target="_blank">{m.id}</a>'
        )
    }
