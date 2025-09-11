import flet as ft
from ..models.database import get_connection


class stockView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.product_search_field = ft.TextField(
            label="Produto", 
            on_change=self._filter_products,
            autofocus=True
        )
        self.product_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=150, visible=False)  # lista de produtos filtrados
        self.selected_product_id = None
        self.product_quantity_field = ft.TextField(label="Quantidade")

    def build(self):
        self.page.controls.clear()

        self.page.appbar = ft.AppBar(
            title=ft.Text("Entrada/saída", size=24, weight="bold"),
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: self._go_back()),
        )

        self.page.add(
            ft.Column(
                [
                    self.product_search_field,
                    self.product_list,
                    self.product_quantity_field,
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Entrada", on_click=self._product_in),
                            ft.ElevatedButton(text="Saída", on_click=self._product_out),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
        self._take_product()
        self.page.update()

    # pega produtos do banco de dados
    def _take_product(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM produtos")
            self.products = [{"id": str(row[0]), "name": row[1]} for row in cursor.fetchall()]

        self._update_product_list(self.products)

    # atualiza lista de opções
    def _update_product_list(self, items):
        self.product_list.controls.clear()
        for product in items:
            self.product_list.controls.append(
                ft.ListTile(
                    title=ft.Text(product["name"]),
                    on_click=lambda e, p=product: self._select_product(p),
                )
            )
        self.product_list.visible = len(items) > 0
        self.page.update()

    # filtra produtos conforme o texto digitado
    def _filter_products(self, e):
        text = self.product_search_field.value.lower()
        filtered = [p for p in self.products if text in p["name"].lower()]
        self._update_product_list(filtered)

    # quando usuário escolhe um produto
    def _select_product(self, product):
        self.product_search_field.value = product["name"]
        self.selected_product_id = product["id"]
        self.product_list.visible = False
        self.page.update()

    def _product_in(self, e):
        self._refresh_stock(product_in=True)

    def _product_out(self, e):
        self._refresh_stock(product_in=False)

    # atualizar estoque
    def _refresh_stock(self, product_in=True):
        id_product = self.selected_product_id

        if not id_product:
            print("Selecione um produto!")
            return

        try:
            quantity = int(self.product_quantity_field.value)
            if quantity <= 0:
                raise ValueError
        except:
            print("Digite uma quantidade válida!")
            return

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (id_product,))
            result = cursor.fetchone()

            if not result:
                print("Produto não encontrado!")
                return

            current_quantity = result[0]
            new_quantity = current_quantity + quantity if product_in else current_quantity - quantity

            if new_quantity < 0:
                print("Quantidade insuficiente no estoque!")
                return

            cursor.execute("UPDATE produtos SET quantidade = ? WHERE id=?", (new_quantity, id_product))
            conn.commit()

            print("Estoque atualizado com sucesso!")
            self.product_quantity_field.value = ""
            self.page.update()

    def _go_back(self):
        from app.views.home_view import homeView
        home = homeView(self.page)
        home.build()
