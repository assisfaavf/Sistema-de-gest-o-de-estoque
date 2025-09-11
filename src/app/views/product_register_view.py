import flet as ft
import pandas as pd
from ..models.database import get_connection

class productsRegisterView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.product_name = ft.TextField(label="Nome do produto")
        self.product_unit = ft.TextField(label="Unidade do produto")
        self.product_quantity = ft.TextField(label="Quantidade do produto", on_submit=self._register_product)
        self.product_price = ft.TextField(label="Preço do produto")
        self.list_products_view = ft.ListView()

        # Criar o FilePicker
        self.file_picker = ft.FilePicker(on_result=self._import_from_csv)
        self.page.overlay.append(self.file_picker)

    def build(self):
        self.page.controls.clear()

        self.page.appbar = ft.AppBar(
            title=ft.Text('Cadastro de Produtos', size=24, weight="bold"),
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: self._go_back())
        )

        self.page.add(
            ft.Column([
                self.product_name,
                self.product_unit,
                self.product_quantity,
                self.product_price,
                ft.Row([
                    ft.ElevatedButton(text="Cadastrar produto", on_click=self._register_product),
                    ft.ElevatedButton(text="Importar CSV", on_click=lambda e: self.file_picker.pick_files(
                        allow_multiple=False,
                        file_type=ft.FilePickerFileType.CUSTOM,
                        allowed_extensions=["csv"]
                    ))
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Text("Produtos cadastrados", size=20, weight="bold"),
                self.list_products_view,
            ], expand=True, scroll=ft.ScrollMode.AUTO)
        )

        self.page.update()

    # Função de cadastro manual (já existia)
    def _register_product(self, e):
        name = self.product_name.value.strip()
        unit = self.product_unit.value.strip()
        try:
            price = float(self.product_price.value.strip())
            quantity = int(self.product_quantity.value.strip())
        except:
            print('O preço e a quantidade devem ser números!')
            return

        if not name or not unit:
            print('Preencha o nome e a unidade do produto!')
            return

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO produtos (name, unit, quantidade, price) VALUES (?, ?, ?, ?)',
                           (name, unit, quantity, price))
            conn.commit()

        print('Produto cadastrado com sucesso!')

        self.product_name.value = ""
        self.product_unit.value = ""
        self.product_quantity.value = ""
        self.product_price.value = ""
        self.page.update()

    # Função para importar CSV
    def _import_from_csv(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return

        file_path = e.files[0].path
        print(f"Importando CSV: {file_path}")

        try:
            # Lê o CSV (ajuste se tiver cabeçalho ou não)
            df = pd.read_csv(file_path, sep=";", encoding="utf-8", header=None)
            df.columns = ["name", "unit", "quantidade", "price"]

            with get_connection() as conn:
                cursor = conn.cursor()
                for _, row in df.iterrows():
                    cursor.execute(
                        "INSERT INTO produtos (name, unit, quantidade, price) VALUES (?, ?, ?, ?)",
                        (row["name"], row["unit"], int(row["quantidade"]), float(row["price"]))
                    )
                conn.commit()

            print("Produtos importados com sucesso!")
            self.page.update()

        except Exception as ex:
            print("Erro ao importar CSV:", ex)

    def _go_back(self):
        from app.views.home_view import homeView
        home = homeView(self.page)
        home.build()
