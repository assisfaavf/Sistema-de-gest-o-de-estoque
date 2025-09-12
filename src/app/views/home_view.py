import flet as ft
from app.views.base_view import BaseView

class homeView(BaseView):
    def build(self):
        self.page.controls.clear()
        self._build_layout()  # garante o menu e appbar

        self.page.add(
            ft.Column([
                ft.Text("Bem-vindo ao sistema de gestão de estoque", size=24, weight="bold"),
                ft.Text("Selecione uma opção no menu", size=16),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.page.update()
