import flet as ft
from ..models.database import get_connection
from app.views.base_view import BaseView

class DashboardView(BaseView):
  def __init__(self, page: ft.Page):
    self.page = page
    self.chart = ft.BarChart( #Criando estilização do gráfico
      expand=True,
      border=ft.border.all(1, ft.Colors.GREY),
      horizontal_grid_lines=ft.ChartGridLines(width=1),
      vertical_grid_lines=ft.ChartGridLines(width=1),
      left_axis=ft.ChartAxis(labels_size=40),
      bottom_axis=ft.ChartAxis(labels_size=40),
      tooltip=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
      max_y=100,
      bar_groups=[],
    )
    self.total_products_text = ft.Text(size=24, weight="bold")

  def build(self):
    self.page.controls.clear()
    self._build_layout()


    self.page.add(
      ft.Column([
        ft.Text('Estoque atual', size=30, weight="bold"),
        self.total_products_text,
        self.chart,
      ], 
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      scroll=ft.ScrollMode.AUTO
      )
    )

    self._take_data()
    self.page.update()
    

  #Função para epgar dados do banco de dados
  def _take_data(self):
    with get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT name, quantidade FROM produtos")
      products = cursor.fetchall()

      #Atualizar o total de produtos
      total_products = len(products)
      self.total_products_text.value = f"Total de Produtos: {total_products}"

      #Atualizar o gráfico
      bar_groups = []
      max_quantity = 0

      for index, (name, quantidade) in enumerate(products):
        bar_groups.append(
          ft.BarChartGroup(
            x=index,
            bar_rods=[
              ft.BarChartRod(
                from_y=0,
                to_y=quantidade,
                width=20,
                color=ft.Colors.BLUE,
                tooltip=f"{name}: {quantidade}",
              )
            ],
          )
        )

        if quantidade > max_quantity:
          max_quantity = quantidade

    self.chart.bar_groups = bar_groups
    self.chart.bottom_axis = ft.ChartAxis(labels=[ft.ChartAxisLabel(value=index, label=ft.Text(name, size=10))for index, (name, _) in enumerate(products)]
    )

    self.chart.max_y = max(10, max_quantity + 10)



  #Função de retornar 
  def _go_back(self):
    from app.views.home_view import homeView
    home = homeView(self.page)
    home.build()