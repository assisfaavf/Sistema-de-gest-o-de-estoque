import flet as ft

class homeView:
  def __init__(self, page:ft.Page):
    self.page = page

  def build(self):
    self.page.controls.clear()

    self.page.drawer = ft.NavigationDrawer( #Cria a gaveta lateral de opções
      controls = [
        ft.Container(height=50),
        ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Home"),
        ft.NavigationDrawerDestination(icon=ft.Icons.DASHBOARD, label="DashBoard"),
        ft.NavigationDrawerDestination(icon=ft.Icons.INVENTORY, label="Produtos"),
        ft.NavigationDrawerDestination(icon=ft.Icons.LOCAL_SHIPPING, label="Fornecedores"),
        ft.NavigationDrawerDestination(icon=ft.Icons.COMPARE_ARROWS, label="Entrada/Saída"),
        ft.NavigationDrawerDestination(icon=ft.Icons.LOGOUT, label="Sair"),
      ]
    )

    self.page.appbar = ft.AppBar(
      title= ft.Text("Sistema de Gestão de Estoque", size=24, weight="bold"),
      leading=ft.IconButton(ft.Icons.MENU, on_click=lambda e: self._open_drawer()) #Cria o icone do menu e chama afunção que abre o menu
    )

    self.page.add(
      ft.Column([
        ft.Text('Bem vindo ao sistema de gestão de estoque', size=24, weight="bold"),
        ft.Text('Selecione uma opção no menu', size=16),
      ])
    )

    self.page.update()


  def _open_drawer(self):  #Função que abre oo menu
    self.page.drawer.open = True
    self.page.drawer.on_change = self._navigate
    self.page.update()


  def _navigate(self, e):
    #Home
    if self.page.drawer.selected_index == 0:
      ...
    
    #Dashboard
    elif self.page.drawer.selected_index == 1:
      from app.views.dashboard_view import DashboardView #Importa a classe
      dashborad_view = DashboardView(self.page) #Cria uma instância da classe
      dashborad_view.build() #Executa a função build da classe 

    #Produtos
    elif self.page.drawer.selected_index == 2:
      from app.views.product_view import productsView
      products_view = productsView(self.page)
      products_view.build()

    #Fornecedores
    elif self.page.drawer.selected_index == 3:
      from app.views.supplier_view import supplierView
      supplier_view = supplierView(self.page)
      supplier_view.build()

    #Entrada/Saída
    elif self.page.drawer.selected_index == 4:
      from app.views.stock_view import stockView
      stock_view = stockView(self.page)
      stock_view.build()

    #Sair
    elif self.page.drawer.selected_index == 5:
      ...
