import flet as ft
from app.views.base_view import BaseView

class homeView(BaseView):
    def build(self):
        self.page.controls.clear()
        self._build_layout()  # garante o menu e appbar

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Bem-vindo ao sistema de gestão de estoque",
                            size=24,
                            weight="bold",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Selecione uma opção no menu",
                            size=16,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Image(
                            src="src/assets/estoque.jpg",
                            expand=True,
                            fit=ft.ImageFit.CONTAIN,  # pode trocar por COVER
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                expand=True,
                alignment=ft.alignment.center
            )
        )

        self.page.update()
