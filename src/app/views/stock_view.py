import flet as ft
from ..models.database import get_connection



class stockView:
  def __init__(self, page:ft.Page):
    self.page = page
    self.product_dropdown = ft.Dropdown(label="Produto", options=[])
    self.product_quantity_field = ft.TextField(label="Quantidade")
  
  def build(self):
    self.page.controls.clear()  #Limpando controls
    
    self.page.appbar = ft.AppBar(
      title=ft.Text('Estoque', size=24, weight="bold"),
      leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click= lambda e: self._go_back())
    )

    self.page.add(
       ft.Column([
          self.product_dropdown,
          self.product_quantity_field,
          ft.Row([
             ft.ElevatedButton(text= "Entrada", on_click= self._product_in),
             ft.ElevatedButton(text= "Saída", on_click= self._product_out)
          ], alignment=ft.MainAxisAlignment.CENTER),
       ], expand= True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
    )
    self._take_product()
    self.page.update()

  #Função para pegar produtos do banco de dados
  def _take_product(self):
     self.product_dropdown.options.clear()  #Limpa as opções do dropdown

     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM produtos")
        for id_product, name in cursor.fetchall():
           self.product_dropdown.options.append(
              ft.dropdown.Option(str(id_product), name)
           )
      
     self.page.update() 

  #Função de entrada de produtos
  def _product_in(self, e):
     self._refresh_stock(product_in=True)

  #Função de saída de produtos
  def _product_out(self, e):
     self._refresh_stock(product_in=False)

  #Função para atualizar o banco de dados do estoque
  def _refresh_stock(self, product_in=True):
     id_product = self.product_dropdown.value

     if not id_product:
        print("Selecione um produto!")
        return
     
     try:
        quantity = int(self.product_quantity_field.value)
        if quantity <= 0:
           raise ValueError
     except:
        print('Digite uma quantidade valida!')
        return
     
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (id_product))
        result = cursor.fetchone()

        if not result:
          print('Produtonão encontrado!')
          return
        
        current_quantity = result[0]
        new_quantity = current_quantity + quantity if product_in else current_quantity - quantity #Nova quantidade vai ser quantidade atual mais a quantidade inserida, porém se product_in for False sera quantidade atual menos a quantidade inserida

        if new_quantity <0:
           print('Quantidade insufieciente no estoque!')

        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id=?", (new_quantity, id_product)) #Atualizando a quantidade na tabela produtos de acordo com o id
        conn.commit()

        print('Estoque atualizado com sucesso!')
        self.product_quantity_field.value = ""
        self.page.update()





  #Função de retornar 
  def _go_back(self):
      from app.views.home_view import homeView
      home = homeView(self.page)
      home.build()