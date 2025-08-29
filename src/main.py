import flet as ft
from app.views.auth_view import loginView  #importando a classe loginView
from app.models.database import create_table #Importanto a função crete_table

def main(page: ft.Page):
  create_table() #Para criar as nossas tabelas no banco de dados

  page.title = "Sistema de Gestão de Estoque"
  
  login_view = loginView(page)  #Instânciando a class em uma variável local
  login_view.build() #Chama a função dentro da class que possui a página
  


ft.app(target=main)