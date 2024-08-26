from app.controllers.datarecord import DataRecord
from bottle import template, redirect, request, response

class Application():

    def __init__(self):
        # Mapeia as páginas para seus respectivos métodos de renderização
        self.pages = {
            'index': self.index,
            'register': self.register,
            'home': self.home,
            'deposit': self.deposit,
            'withdraw': self.withdraw,
            'transfer': self.transfer
        }
        self.__model = DataRecord()  # Instancia o modelo de dados

    def render(self, page, identifier=None):
        # Renderiza a página solicitada, ou a página index por padrão
        content = self.pages.get(page, self.index)
        if identifier:
            return content(identifier)
        return content()

    def index(self):
        # Renderiza a página inicial
        return template('app/views/html/index')

    def register(self):
        # Renderiza a página de registro
        return template('app/views/html/register')

    def home(self):
        # Renderiza a página home para o usuário autenticado
        session_id = request.get_cookie('session_id')
        user = self.__model.getCurrentUser(session_id)
        if not user:
            redirect('/')
        return template('app/views/html/home', transfered=True, current_user=user)

    def deposit(self):
        # Renderiza a página de depósito para o usuário autenticado
        session_id = request.get_cookie('session_id')
        user = self.__model.getCurrentUser(session_id)
        if not user:
            redirect('/')
        return template('app/views/html/deposito', bank_account_id=user.bank_account_id)

    def withdraw(self):
        # Renderiza a página de saque para o usuário autenticado
        session_id = request.get_cookie('session_id')
        user = self.__model.getCurrentUser(session_id)
        if not user:
            redirect('/')
        return template('app/views/html/saque', bank_account_id=user.bank_account_id)

    def transfer(self):
        # Renderiza a página de transferência para o usuário autenticado
        session_id = request.get_cookie('session_id')
        user = self.__model.getCurrentUser(session_id)
        if not user:
            redirect('/')
        return template('app/views/html/transferencia', bank_account_id=user.bank_account_id)

    def get_current_user(self, session_id):
        # Obtém o usuário atual com base no ID de sessão
        return self.__model.getCurrentUser(session_id)

    def update_user(self, user):
        # Atualiza os dados do usuário no modelo
        self.__model.update_user(user)

    def is_authenticated(self, bank_account_id):
        # Verifica se o usuário está autenticado com base no ID da conta bancária
        session_id = request.get_cookie('session_id')
        current_user = self.__model.getCurrentUser(session_id)
        return current_user and bank_account_id == current_user.bank_account_id

    def authenticate_user(self, username, password):
        # Autentica o usuário com base no nome de usuário e senha
        session_id = self.__model.checkUser(username, password)
        if session_id:
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            redirect('/home')
        else:
            response.set_cookie('login_error', '1', max_age=10)
            redirect('/')

    def logout_user(self):
        # Encerra a sessão do usuário
        session_id = request.get_cookie('session_id')
        self.__model.logout(session_id)
        response.delete_cookie('session_id')
        redirect('/')

    def create_user(self, first_name, last_name, email, password, dob):
        # Cria um novo usuário no sistema
        if self.__model.email_exists(email):
            redirect('/register?error=email_exists')
        else:
            self.__model.book(first_name, last_name, email, password)
            session_id = self.__model.checkUser(email, password)
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            redirect('/home?registered=true')

    def email_exists(self, email):
        # Verifica se um email já está registrado
        return self.__model.email_exists(email)

    def process_deposit(self):
        # Processa o depósito de valores na conta do usuário
        session_id = request.get_cookie('session_id')
        user = self.get_current_user(session_id)
        if not user:
            return {'success': False, 'message': 'Usuário não autenticado'}
        deposit_data = request.json
        deposit_amount = deposit_data.get('amount')
        if deposit_amount and deposit_amount > 0:
            user.balance += deposit_amount  # Adiciona o valor do depósito ao saldo do usuário
            user.balance = round(user.balance, 2)  # Arredonda o saldo para duas casas decimais, mantendo a precisão financeira
            self.update_user(user)  # Atualiza os dados do usuário com o novo saldo
            return {'success': True, 'new_balance': user.balance}
        else:
            return {'success': False, 'message': 'Valor inválido para depósito'}

    def process_withdraw(self):
        # Processa o saque de valores da conta do usuário
        session_id = request.get_cookie('session_id')
        user = self.get_current_user(session_id)
        if not user:
            return {'success': False, 'message': 'Usuário não autenticado'}
        withdraw_data = request.json
        withdraw_amount = withdraw_data.get('amount')
        if withdraw_amount and withdraw_amount > 0:
            if user.balance >= withdraw_amount:  # Verifica se o saldo é suficiente para o saque
                user.balance -= withdraw_amount  # Subtrai o valor do saque do saldo do usuário
                user.balance = round(user.balance, 2)  # Arredonda o saldo restante para duas casas decimais
                self.update_user(user)  # Atualiza os dados do usuário com o novo saldo
                return {'success': True, 'new_balance': user.balance}
            else:
                return {'success': False, 'message': 'Saldo insuficiente'}
        else:
            return {'success': False, 'message': 'Valor inválido para saque'}

    def process_transfer(self):
        # Processa a transferência de valores entre contas
        session_id = request.get_cookie('session_id')
        user = self.get_current_user(session_id)
        if not user:
            return {'success': False, 'message': 'Usuário não autenticado'}
        transfer_data = request.json
        destination_account_id = transfer_data.get('destinationAccount')
        amount = transfer_data.get('amount')
        if amount <= 0:
            return {'success': False, 'message': 'Valor inválido para transferência'}
        if user.balance < amount:  # Verifica se o saldo é suficiente para a transferência
            return {'success': False, 'message': 'Saldo insuficiente'}
        if user.bank_account_id == destination_account_id:
            return {'success': False, 'message': 'Não é possível transferir para a própria conta'}
        destination_user = next((u for u in self.__model._DataRecord__user_accounts if u.bank_account_id == destination_account_id), None)
        if not destination_user:
            return {'success': False, 'message': 'Conta de destino não encontrada'}
        user.balance -= amount  # Subtrai o valor da transferência do saldo do usuário
        destination_user.balance += amount  # Adiciona o valor da transferência ao saldo do usuário de destino
        user.balance = round(user.balance, 2)  # Arredonda o saldo do usuário para duas casas decimais
        destination_user.balance = round(destination_user.balance, 2)  # Arredonda o saldo do usuário de destino para duas casas decimais
        self.update_user(user)  # Atualiza os dados do usuário
        self.update_user(destination_user)  # Atualiza os dados do usuário de destino
        return {'success': True, 'new_balance': user.balance}
