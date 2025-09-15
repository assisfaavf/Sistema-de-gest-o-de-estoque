import flet as ft
from ..models.database import get_connection
from app.views.base_view import BaseView


class supplierView(BaseView):
  def __init__(self, page:ft.Page):
    self.page = page
    self.supplier_name = ft.TextField(label="Nome do fornecedor")
    self.supplier_cellphone = ft.TextField(label="Telefone do fornecedor")
    self.supplier_email = ft.TextField(label="email do fornecedor", on_submit=self._register_supplier)
    self.list_supplier_view = ft.ListView()

    # Criar snackbar e adicionar ao overlay
    self.snack_bar = ft.SnackBar(content=ft.Text(""))
    self.page.overlay.append(self.snack_bar)



  def build(self):
    self.page.controls.clear()
    self._build_layout()

    self.page.add(
      ft.Column([
        self.supplier_name,
        self.supplier_cellphone,
        self.supplier_email,
        ft.Row([
          ft.ElevatedButton(text="Cadastrar fornecedor", on_click=self._register_supplier)
      ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Text("Fornecedores cadastrados", size=20, weight="bold"),
        self.list_supplier_view,
      ], expand=True, scroll=ft.ScrollMode.AUTO)

  )

    self.supplier_list()
    self.page.update()

  #Função para cadastrar fornecedor

  def _register_supplier(self, e):
    name = self.supplier_name.value.strip()
    cellphone = self.supplier_cellphone.value.strip()
    email = self.supplier_email.value.strip()
    
    if not name or not cellphone or not email: #Verifica se os campos nome, telefone e email foram preenchidos
      print('Preencha todos os campos!')
      self._show_message("Preencha todos os campos!", error=True)
      return
    
    with get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('INSERT INTO fornecedores (name, cellphone, email) VALUES (?, ?, ?)', (name, cellphone, email))
      conn.commit()

      print('Forncedor cadastrado com sucesso!')
      self._show_message("Forncedor cadastrado com sucesso!")

      self.supplier_name.value = ""
      self.supplier_cellphone.value = ""
      self.supplier_email.value = ""
      self.supplier_list()
      self.page.update()
  
  def supplier_list(self):
    self.list_supplier_view.controls.clear()

    with get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('SELECT name, cellphone, email FROM fornecedores')

      for name, cellphone, email in cursor.fetchall():
        self.list_supplier_view.controls.append(
          ft.ListTile(
            title=ft.Text(f"{name}"),
            subtitle=ft.Text(f"Telefone: {cellphone} | email: {email}")
          )
        )
    
        self.page.update()


  # Função para exibir alertas e erros
  def _show_message(self, message: str, error: bool = False):
    self.snack_bar.content = ft.Text(message, color="white")
    self.snack_bar.bgcolor = "red" if error else "green"
    self.snack_bar.open = True
    self.page.update()