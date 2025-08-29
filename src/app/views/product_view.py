import flet as ft
from ..models.database import get_connection


class productsView:
  def __init__(self, page:ft.Page):
    self.page = page
    self.product_name = ft.TextField(label="Nome do produto")
    self.product_price = ft.TextField(label="Preço do produto")
    self.product_quantity = ft.TextField(label="Quantidade do produto", on_submit=self._register_product)
    self.list_products_view = ft.ListView()



  def build(self):
    self.page.controls.clear()

    self.page.appbar = ft.AppBar(
      title=ft.Text('Cadastro de Produtos', size=24, weight="bold"),
      leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click= lambda e: self._go_back())
    )

    self.page.add(
      ft.Column([
        self.product_name,
        self.product_price,
        self.product_quantity,
        ft.Row([
          ft.ElevatedButton(text="Cadastrar produto", on_click=self._register_product)
      ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Text("Produtos cadastrados", size=20, weight="bold"),
        self.list_products_view,
      ], expand=True, scroll=ft.ScrollMode.AUTO)

  )

    self.product_list()
    self.page.update()

  #Função para cadastrar produto

  def _register_product(self, e):
    name = self.product_name.value.strip()
    try: #Garante que os dados de preço e quantidade são em formato de número
      price = float(self.product_price.value.strip())
      quantity = int(self.product_quantity.value.strip())
    
    except:
      print('O preço e a quantidade devem ser números!')
      return
    
    if not name: #Verifica se o campo de nome foi preencido (Não é necessário para o preço e quantidade pois a verificação anterior garante que foram preenchidos)
      print('Preencha o nome do produto!')
      return
    
    with get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('INSERT INTO produtos (name, price, quantidade) VALUES (?, ?, ?)', (name, price, quantity))
      conn.commit()

      print('Produto cadastrado com sucesso!')

      self.product_name.value = ""
      self.product_price.value = ""
      self.product_quantity.value = ""
      self.product_list()
      self.page.update()
  
  def product_list(self):
    self.list_products_view.controls.clear()

    with get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('SELECT name, price, quantidade FROM produtos')

      for name, price, quantidade in cursor.fetchall():
        self.list_products_view.controls.append(
          ft.ListTile(
            title=ft.Text(f"{name}"),
            subtitle=ft.Text(f"Preço: R${price:.2f} | Quantidade: {quantidade}")
          )
        )
    
        self.page.update()


  def _go_back(self):
    from app.views.home_view import homeView
    home = homeView(self.page)
    home.build()