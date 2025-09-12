import flet as ft

class BaseView:
    def __init__(self, page: ft.Page):
        self.page = page
        self._build_layout()

    def _build_layout(self):
        # Drawer
        self.page.drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(height=50),
                ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationDrawerDestination(icon=ft.Icons.DASHBOARD, label="DashBoard"),
                ft.NavigationDrawerDestination(icon=ft.Icons.INVENTORY, label="Produtos"),
                ft.NavigationDrawerDestination(icon=ft.Icons.LOCAL_SHIPPING, label="Fornecedores"),
                ft.NavigationDrawerDestination(icon=ft.Icons.COMPARE_ARROWS, label="Entrada/Saída"),
                ft.NavigationDrawerDestination(icon=ft.Icons.LOGOUT, label="Sair"),
            ]
        )

        # AppBar
        self.page.appbar = ft.AppBar(
            title=ft.Text("Sistema de Gestão de Estoque", size=24, weight="bold"),
            leading=ft.IconButton(ft.Icons.MENU, on_click=lambda e: self._open_drawer())
        )

    def _open_drawer(self):
        self.page.drawer.open = True
        self.page.drawer.on_change = self._navigate
        self.page.update()

    def _navigate(self, e):
        self.page.drawer.open = False
        self.page.update()

        #Cria a variávelque recebe o número da opção selecionada
        idx = self.page.drawer.selected_index
        
        #Faz o caminho de acordo com a opção selecioanda

        #Home
        if idx == 0:
            from app.views.home_view import homeView
            homeView(self.page).build()

        #Dashboard
        elif idx == 1:
            from app.views.dashboard_view import DashboardView
            DashboardView(self.page).build()

        #Prdodutos
        elif idx == 2:
            from app.views.product_view import productsView
            productsView(self.page).build()

        #Fornecedores
        elif idx == 3:
            from app.views.supplier_view import supplierView
            supplierView(self.page).build()

        #Entrada/saída
        elif idx == 4:
            from app.views.stock_view import stockView
            stockView(self.page).build()

        #Sair
        elif idx == 5:
            from app.views.auth_view import loginView
            loginView(self.page).build()
