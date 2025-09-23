import flet as ft
from app.views.auth_view import loginView  #importando a classe loginView
from app.models.database import create_table #Importanto a função crete_table
from app.views.home_view import homeView

def main(page: ft.Page):
  create_table() #Para criar as nossas tabelas no banco de dados

  page.title = "Sistema de Gestão de Estoque"
  
  home_view = homeView(page)
  home_view.build()
  #login_view = loginView(page)  #Instânciando a class em uma variável local
  #login_view.build() #Chama a função dentro da class que possui a página
  


ft.app(target=main, assets_dir="assets")