menu = """"

[d] Depositar
[s] Sacar
[i] Informações de saque
[e] Extrato
[c] Sair

=> """


QUANTIDADE_DE_SAQUES_DIARIOS = 3
LIMITE_CADA_SAQUE = 500
numero_de_saques = 0
saldo = 0
extrato = ""

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("informe o valor que deseja depositar: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        
        else:
            print("Não foi possível realizar o depósito! O valor informado está inválido")

    elif opcao == "s":
        valor = float(input("Informe o valor que deseja sacar: "))

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

    elif opcao == "i":
        print("".center(60, "="))
        print(
            f"\nSua quantidade de saques diárias atual é de: {numero_de_saques}\n \nSua quantidade máxima de saques diários: {QUANTIDADE_DE_SAQUES_DIARIOS}\n \nSeu limite máximo por saque é de: R$ {LIMITE_CADA_SAQUE:.2f}\n \n Seu saldo atual é: R$ {saldo:.2f}"
            )
        print("\n")
        print("".center(60, "="))

    elif opcao == "e":
        print("\n")
        print("EXTRATO".center(45, "*"))
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\n Saldo: R$ {saldo:.2f}")
        print("".center(45, "*"))

    elif opcao == "c":
        break

    else:
        print("Operação inválida, por favor selecione a operação desejada novamente.")




       

