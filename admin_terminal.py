import json
from bank_email import enviar_extrato_mensal, enviar_alerta_transacao

def carregar_dados():
    try:
        with open("dados_bancarios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def visualizar_todas_contas():
    contas = carregar_dados()
    print("\n=== Lista de Todas as Contas ===")
    for numero, conta in contas.items():
        print(f"\nConta: {numero}")
        print(f"Nome: {conta['nome']}")
        print(f"CPF: {conta['cpf']}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("------------------------")

def visualizar_movimentacoes():
    contas = carregar_dados()
    total_movimentacoes = 0
    print("\n=== Movimentações de Todas as Contas ===")
    for numero, conta in contas.items():
        print(f"\nConta {numero} - {conta['nome']}:")
        for mov in conta['movimentacoes']:
            print(f"- {mov}")
            total_movimentacoes += 1
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
