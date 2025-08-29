import flet as ft
from ..models.database import get_connection
from passlib.hash import pbkdf2_sha256 #Importando modulo de criptografia 
from app.views.home_view import homeView #Importa a class da página inicial


class loginView:
  def __init__(self, page: ft.Page):
    self.page = page
    self.username = ft.TextField(label="Usuário")
    self.password = ft.TextField(label="Senha", password=True, can_reveal_password=True, on_submit=self._handle_login)

  
  def build(self):
    self.page.controls.clear()

    self.page.controls.append(
      ft.Column([
        ft.Text("Login", size=24, weight="bold"),
        self.username,
        self.password,        
        ft.ElevatedButton(text="Entrar", on_click= self._handle_login,),
        ft.ElevatedButton(text="Cadastrar", on_click= self._handle_register)
      ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
      )
    )

    self.page.update()

  def _handle_login(self, event):
    user = self.username.value.strip()
    passw = self.password.value.strip()

    if not user or  not passw:
      print("Preencha todos os campos !")
      return
    
    with get_connection() as conn:
      cursor = conn.cursor()
      #Seleciona senha dentro da tabela usuario onde o username dele é igual ao digitado
      cursor.execute('SELECT password FROM usuarios WHERE username = ?', (user,)) 
      results = cursor.fetchone() #Seleciona um usuário do banco de dados

      if results and pbkdf2_sha256.verify(passw, results[0]):
        print('Login feito com sucesso!')

        #Abrir a tela Inicial
        home_view = homeView(self.page)
        home_view.build()

      else:
        print('Login ou senha incorretos!')


#Criando código de registro de usuários
#Repetiu parte da estrutura de login, como os campos que pedem usuário e senha e o teste para saber se não preencheu algum
  def _handle_register(self, e):
    user = self.username.value.strip()
    passw = self.password.value.strip()

    if not user or not passw:
      print("Preencha todos os campos !")
      return
    
#Cria a criptografia com hash para a senha
    hashed_password = pbkdf2_sha256.hash(passw)

#Adiciona o usuário e a senha ao banco de dados
    try:
      with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios(username, password) VALUES (?, ?)',(user,hashed_password))
        conn.commit()

        print('Usuário cadastrados com sucesso!')

        self.username.value = ""
        self.password.value = ""
        self.page.update()

    except Exception as ex:
      print('Erro ao cadastrar: {ex}')
      
