menu = """"

[d] Depositar
[s] Sacar
[r] Regras de saque
[e] Extrato
[c] Sair

=> """

saldo = 0
QUANTIDADE_DE_SAQUES_DIARIOS = 3
LIMITE_CADA_SAQUE = 500
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

        if valor <= LIMITE_CADA_SAQUE and valor <= saldo and QUANTIDADE_DE_SAQUES_DIARIOS > 0 and valor > 0:
            saldo -= valor
            QUANTIDADE_DE_SAQUES_DIARIOS -= 1
            extrato += f"Saque: R$ {valor:.2f}\n"
            print("Saque realizado com sucesso!")
        
        else:
            print("Não foi possível realizar o operação! Verifique o motivo em Regras de saque")

    
    elif opcao == "r":
        print("\n")
        print(
            f"Sua quantidade de saques diários: {QUANTIDADE_DE_SAQUES_DIARIOS}\n Seu limite máximo por saque é de: R$ {LIMITE_CADA_SAQUE:.2f}\n Seu saldo atual é: R$ {saldo:.2f}"
        )
        print("\n")
        print("Se a quantidade de saques diários estiver zerada, se ultrapassar o limite por saque ou se seu saldo for insuficiente \n Você não poderá realizar o saque solicitado.")


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




       

