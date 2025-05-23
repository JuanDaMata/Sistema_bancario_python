def menu():
    menu = """"\n

    =============== MENU ===============

    [d]Depositar
    [s]Sacar
    [i]Informações de saque
    [e]Extrato
    [nu]Novo usuário
    [cc]Criar conta
    [lc]Listar Contas
    [c]Sair

    => """

    return input(menu)

def depositar(saldo, valor, extrato, /): 
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("\n Depósito realizado com sucesso!")
        else:
            print("\n Não foi possível realizar o depósito! O valor informado está inválido")
        
        return saldo, extrato

def sacar(*, saldo, valor, extrato, LIMITE_CADA_SAQUE, numero_de_saques, QUANTIDADE_DE_SAQUES_DIARIOS):
            excedeu_saldo = valor > saldo
            excedeu_limite_por_saque = valor > LIMITE_CADA_SAQUE
            excedeu_quantidade_de_saque = numero_de_saques >= QUANTIDADE_DE_SAQUES_DIARIOS

            if excedeu_saldo:
                 print("\nA operação de saque falhou! Sua conta não possui saldo suficiente.")
            
            elif excedeu_limite_por_saque:
                 print("\nA operação de saque falhou! Você ultrapassou o valor do limite por saque, consulte seu limite por saque em informações de saque.")

            elif excedeu_quantidade_de_saque:
                 print("\nA operação de saque falhou! Você excedeu o limite de saques diários, consulte sua quantidade de saques diárias em informações de saque.")
            
            elif valor > 0:
                saldo -= valor
                numero_de_saques += 1
                extrato += f"Saque: R$ {valor:.2f}\n"
                print("\nSaque realizado com sucesso!")
        
            else:
                print("\nA operação de saque falhou! O valor informado é inválido.")

            return saldo, extrato, numero_de_saques

def informacoes_de_saque(*, QUANTIDADE_DE_SAQUES_DIARIOS, numero_de_saques, LIMITE_CADA_SAQUE, saldo):
    print("".center(60, "="))
    print(
         f"\nSua quantidade de saques diárias atual é de: {numero_de_saques}\n \nSua quantidade máxima de saques diários: {QUANTIDADE_DE_SAQUES_DIARIOS}\n \nSeu limite máximo por saque é de: R$ {LIMITE_CADA_SAQUE:.2f}\n \n Seu saldo atual é: R$ {saldo:.2f}"
         )
    print("\n")
    print("".center(60, "="))

def exibir_extrato(saldo, /, *, extrato):
    print("\n")
    print("EXTRATO".center(45, "*"))
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n Saldo: R$ {saldo:.2f}")
    print("".center(45, "*"))

def cadastrar_usuario(usuarios):
     cpf = input("Informe seu CPF (somento números): ")
     usuario = filtrar_usuario(cpf, usuarios)

     if usuario:
          print("\n Já existe um usuário com esse CPF!")
          return
     
     nome = input("Informe seu nome completo: ")
     data_nascimento = input("Informe sua data de nascimento nesse formato -> (dia/mês/ano): ")
     endereco = input("Informe seu endereço nesse formato -> (Logradouro, nº - bairro - cidade/sigla do estado): ")

     usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

     print("Usuário cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
     usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]

     return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_da_conta, usuarios):
     cpf = input("Informe seu CPF: ")
     usuario = filtrar_usuario(cpf, usuarios)

     if usuario:
          print("\n Conta criada com sucesso!")
          return {"agencia": agencia, "numero_da_conta": numero_da_conta, "usuario": usuario}
     
     print("\n Usuário não encontrado, criação de conta não concluída!")

def listar_contas(contas):
     for conta in contas:
         linha = f""""\n
            Agência: {conta["agencia"]}
            C/C: {conta["numero_da_conta"]}
            Titular: {conta["usuario"]["nome"]}
         """
         print("".center(100, "-"))
         print(linha)

def main():
    QUANTIDADE_DE_SAQUES_DIARIOS = 3
    AGENCIA = "0001"
    LIMITE_CADA_SAQUE = 500

    saldo = 0
    numero_de_saques = 0
    extrato = ""
    contas = [] 
    usuarios = []
    numero_conta = 1


    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("informe o valor que deseja depositar: "))

            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opcao == "s":
            valor = float(input("Informe o valor que deseja sacar: "))

            saldo, extrato, numero_de_saques = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                LIMITE_CADA_SAQUE = LIMITE_CADA_SAQUE,
                numero_de_saques = numero_de_saques,
                QUANTIDADE_DE_SAQUES_DIARIOS = QUANTIDADE_DE_SAQUES_DIARIOS
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato = extrato)

        elif opcao == "i":
             informacoes_de_saque(
                  numero_de_saques = numero_de_saques,
                  QUANTIDADE_DE_SAQUES_DIARIOS = QUANTIDADE_DE_SAQUES_DIARIOS,
                  LIMITE_CADA_SAQUE = LIMITE_CADA_SAQUE,
                  saldo = saldo
                  )
        
        elif opcao == "nu":
             cadastrar_usuario(usuarios)

        elif opcao == "cc":
             conta = criar_conta(AGENCIA, numero_conta, usuarios)

             if conta:
                contas.append(conta)
                numero_conta += 1
        
        elif opcao == "lc":
             listar_contas(contas)
        
        elif opcao == "c":
            break

        else:
            print("Operação inválida, por favor selecione a operação desejada novamente.")

main()
