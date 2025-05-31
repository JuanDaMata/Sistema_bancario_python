from abc import ABC , abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
         
class PessoaFisica(Cliente):
     def __init__(self, nome, data_de_nascimento, cpf, endereco):
          super().__init__(endereco)
          self.nome = nome
          self.data_de_nascimento = data_de_nascimento
          self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property 
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nA operação de saque falhou! Sua conta não possui saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        
        else:
            print("\nA operação de saque falhou! O valor informado é inválido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n Depósito realizado com sucesso!")
        else:
            print("\n Não foi possível realizar o depósito! O valor informado está inválido")
            return False
        
        return True
             
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_cada_saque=500, quantidade_de_saques_diarios=3):
        super().__init__(numero, cliente)
        self.limite_cada_saque = limite_cada_saque
        self.quantidade_de_saques_diarios = quantidade_de_saques_diarios
    
    def sacar(self, valor):
        data_atual = datetime.now().strftime("%d/%m/%y")

        saques_hoje = [
            transacao for transacao in self.historico.transacao 
            if transacao["tipo"] == Saque.__name__ and transacao["data"].startswith(data_atual)
        ]

        numero_de_saques_hoje = len(saques_hoje)

        excedeu_limite_por_saque = valor > self.limite_cada_saque
        excedeu_quantidade_de_saque = numero_de_saques_hoje >= self.quantidade_de_saques_diarios

        if excedeu_limite_por_saque:
            print("\nA operação de saque falhou! Você ultrapassou o valor do limite por saque, consulte seu limite por saque em informações de saque.")

        elif excedeu_quantidade_de_saque:
            print("\nA operação de saque falhou! Você excedeu o limite de saques diários, consulte sua quantidade de saques diárias em informações de saque.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacao(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%y %H:%M:%S")
            }
        )
          
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)           
            
def menu():
    menu = """"\n

    =============== MENU ===============

    [d]Depositar
    [s]Sacar
    [i]Informações de saque
    [e]Extrato
    [nc]Novo cliente
    [cc]Criar conta
    [lc]Listar Contas
    [c]Sair

    => """

    return input(menu)

def depositar(clientes):
    cpf = input("informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
        
def sacar(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor que deseja sacar: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def informacoes_de_saque(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    if (conta, ContaCorrente):
        data_atual = datetime.now().strftime("%d/%m/%y")
        saques_de_hoje = [
            transacao for transacao in conta.historico.transacao 
            if transacao["tipo"] == Saque.__name__ and transacao["data"].startswith(data_atual)
        ]
        numero_de_saques_hoje = len(saques_de_hoje)

        print("Informações de saque:".center(60, "="))
        print(f"\nSua quantidade de saques disponíveis é de: {conta.quantidade_de_saques_diarios - numero_de_saques_hoje}")
        print(f"\nSeu limite máximo por saque é de: R$ {conta.limite_cada_saque:.2f}")
        print(f"\nSua quantidade máxima de saques diários: {conta.quantidade_de_saques_diarios}")
        print("=" * 60)
    else:
        print("\nA conta informada não é uma conta corrente.")

def exibir_extrato(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n")
    print("EXTRATO".center(45, "*"))
    transacoes = conta.historico.transacao

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\nR$ {transacao["valor"]:.2f}"

    print(extrato)
    print(f"\n Saldo:\nR$ {conta.saldo:.2f}")
    print("".center(45, "*"))

def criar_cliente(clientes):
     cpf = input("Informe seu CPF (somento números): ")
     cliente = filtrar_cliente(cpf, clientes)

     if cliente:
          print("\n Já existe um cliente com esse CPF!")
          return
     
     nome = input("Informe seu nome completo: ")
     data_de_nascimento = input("Informe sua data de nascimento nesse formato -> (dia/mês/ano): ")
     endereco = input("Informe seu endereço nesse formato -> (Logradouro, nº - bairro - cidade/sigla do estado): ")

     cliente = PessoaFisica(nome=nome, data_de_nascimento=data_de_nascimento, cpf=cpf, endereco=endereco)
     
     clientes.append(cliente)

     print("Cliente criado com sucesso!")

def filtrar_cliente(cpf, clientes):
     clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]

     return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    
    return cliente.contas[0]

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, criação de conta não concluída!")
        return
    
    conta = ContaCorrente(numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")
    
def listar_contas(clientes):
    cpf = input("Informe seu CPF para listar contas: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    if not cliente.contas:
        print("\nO cliente não possui nenhuma conta.")
        return

    print("\nContas do cliente:")

    for conta in cliente.contas:
        print("".center(100, "-"))
        print(str(conta))

def main():
    contas = [] 
    clientes = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "i":
            informacoes_de_saque(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nc":
             criar_cliente(clientes)

        elif opcao == "cc":
             numero_conta = len(contas) + 1
             criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
             listar_contas(clientes)
        
        elif opcao == "c":
            break

        else:
            print("Operação inválida, por favor selecione a operação desejada novamente.")

main()
