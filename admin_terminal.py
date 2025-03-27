from SQL_lite import BankDatabase
from bank_email import enviar_extrato_mensal, enviar_alerta_transacao

db = BankDatabase()

def visualizar_todas_contas():
    contas = db.get_all_contas()
    print("\n=== Lista de Todas as Contas ===")
    for conta in contas:
        print(f"\nConta: {conta[0]}")
        print(f"Nome: {conta[1]}")
        print(f"CPF: {conta[2]}")
        print(f"Email: {conta[3]}")
        print(f"Saldo: R$ {conta[5]:.2f}")
        print("------------------------")

def visualizar_movimentacoes():
    movimentacoes = db.get_all_movimentacoes()
    total_movimentacoes = len(movimentacoes)
    print("\n=== Movimentações de Todas as Contas ===")
    for mov in movimentacoes:
        print(f"Conta {mov[1]} - {mov[5]}:")
        print(f"- {mov[2]}: R$ {mov[3]:.2f} - {mov[4]}")
    print(f"\nTotal de movimentações: {total_movimentacoes}")

def menu_gestor():
    while True:
        print("\n=== Sistema Bancário - Área do Gestor ===")
        print("1 - Visualizar todas as contas")
        print("2 - Visualizar movimentações")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            visualizar_todas_contas()
        elif opcao == "2":
            visualizar_movimentacoes()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_gestor()
