import flet as ft
import pandas as pd
from ..models.database import get_connection


class productsView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.search_field = ft.TextField(
            label="Pesquisar produto",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self._filter_products,
            expand=True
        )
        self.list_products_view = ft.ListView(expand=True)

        # lista completa de produtos
        self.all_products = []

    def build(self):
        self.page.controls.clear()

        self.page.appbar = ft.AppBar(
            title=ft.Text('Produtos em estoque', size=24, weight="bold"),
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: self._go_back()),
            actions=[
                ft.IconButton(ft.Icons.ADD, tooltip="Cadastrar produto", on_click=lambda e: self._go_to_register(), icon_size=40)
            ]
        )

        self.page.add(
            ft.Column(
                [
                    self.search_field,
                    self.list_products_view,
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        self.product_list()
        self.page.update()

    # lista apenas produtos com quantidade > 0
    def product_list(self):
        self.list_products_view.controls.clear()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, unit, quantidade, price FROM produtos WHERE quantidade > 0')

            self.all_products = [
                {"name": name, "unit": unit, "quantidade": quantidade, "price": price}
                for name, unit, quantidade, price in cursor.fetchall()
            ]

        self._update_list(self.all_products)

    # renderiza a lista
    def _update_list(self, products):
        self.list_products_view.controls.clear()
        for p in products:
            self.list_products_view.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(p['name']),
                        subtitle=ft.Text(f"Unidade: {p['unit']} | Quantidade: {p['quantidade']} | Preço: R${p['price']:.2f}")
                    )
                )
            )
        self.page.update()

    # filtra produtos pelo nome digitado
    def _filter_products(self, e):
        query = self.search_field.value.lower()
        filtered = [p for p in self.all_products if query in p['name'].lower()]
        self._update_list(filtered)

    # abre a página de cadastro
    def _go_to_register(self):
        from app.views.product_register_view import productsRegisterView
        reg = productsRegisterView(self.page)
        reg.build()

    def _go_back(self):
        from app.views.home_view import homeView
        home = homeView(self.page)
        home.build()
