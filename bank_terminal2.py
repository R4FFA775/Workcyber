import json
import hashlib
import re
import random

def gerar_numero_conta(contas):
    while True:
        numero = random.randint(1000, 9999)
        numero_conta = f"{numero}-5"
        if numero_conta not in contas:
            return numero_conta

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha_digitada, senha_criptografada):
    return criptografar_senha(senha_digitada) == senha_criptografada

def validar_cpf(cpf):
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    return re.match(padrao, cpf) is not None

def validar_email(email):
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(padrao, email) is not None

def cadastrar_conta(contas):
    print("Cadastrando conta...")
    if input("Deseja continuar? (s/n): ").lower() != 's':
        return contas
    nome = input("Digite seu nome (ou 'voltar' para retornar ao menu): ")
    if nome.lower() == 'voltar':
        return contas
    cpf = input("Digite seu CPF (ou 'voltar' para retornar ao menu): ")
    if cpf.lower() == 'voltar':
        return contas
    email = input("Digite seu e-mail (ou 'voltar' para retornar ao menu): ")
    if email.lower() == 'voltar':
        return contas
    senha = input("Digite sua senha (ou 'voltar' para retornar ao menu): ")
    if senha.lower() == 'voltar':
        return contas
    saldo = float(input("Digite o saldo inicial (ou 'voltar' para retornar ao menu): "))
    
    numero_conta = gerar_numero_conta(contas)
    
    conta = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": criptografar_senha(senha),
        "saldo": saldo,
        "movimentacoes": []
    }
    
    contas[numero_conta] = conta
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")
    return contas

def editar_conta(contas):
    numero_conta = input("Digite o número da conta a ser editada (ou 'voltar' para retornar ao menu): ")
    if numero_conta.lower() == 'voltar':
        return contas
    if numero_conta in contas:
        senha_digitada = input("Digite sua senha para confirmar (ou 'voltar' para retornar ao menu): ")
        if senha_digitada.lower() == 'voltar':
            return contas
        if not verificar_senha(senha_digitada, contas[numero_conta]["senha"]):
            print("Senha incorreta!")
            return contas
            
        print("Conta atual:")
        print(contas[numero_conta])
        if input("Deseja continuar? (s/n): ").lower() != 's':
            return contas
        novo_nome = input("Digite o novo nome (ou 'voltar' para retornar ao menu): ")
        if novo_nome.lower() == 'voltar':
            return contas
        novo_saldo = float(input("Digite o novo saldo (ou 'voltar' para retornar ao menu): "))
        contas[numero_conta]["nome"] = novo_nome
        contas[numero_conta]["saldo"] = novo_saldo
    else:
        print("Conta não encontrada.")
    return contas

def verificar_conta(contas):
    numero_conta = input("Digite o número da conta a ser verificada (ou 'voltar' para retornar ao menu): ")
    if numero_conta.lower() == 'voltar':
        return contas
    if numero_conta in contas:
        if input("Deseja continuar? (s/n): ").lower() != 's':
            return contas
        senha_digitada = input("Digite sua senha para verificar a conta (ou 'voltar' para retornar ao menu): ")
        if senha_digitada.lower() == 'voltar':
            return contas
        if verificar_senha(senha_digitada, contas[numero_conta]["senha"]):
            print("\n=== Dados Completos da Conta ===")
            print(f"Nome: {contas[numero_conta]['nome']}")
            print(f"CPF: {contas[numero_conta]['cpf']}")
            print(f"Email: {contas[numero_conta]['email']}")
            print(f"Saldo: R$ {contas[numero_conta]['saldo']:.2f}")
            print("==============================")
            print("Conta verificada com sucesso!")
        else:
            print("Senha incorreta.")
    else:
        print("Conta não encontrada.")
    return contas

def depositar(contas):
    numero_conta = input("Digite o número da conta para depósito (ou 'voltar' para retornar ao menu): ")
    if numero_conta.lower() == 'voltar':
        return contas
    if numero_conta in contas:
        if input("Deseja continuar? (s/n): ").lower() != 's':
            return contas
        valor = float(input("Digite o valor a ser depositado (ou 'voltar' para retornar ao menu): "))
        contas[numero_conta]["saldo"] += valor
        contas[numero_conta]["movimentacoes"].append(f"Depósito: +{valor}")
    else:
        print("Conta não encontrada.")
    return contas

def sacar(contas):
    numero_conta = input("Digite o número da conta para saque (ou 'voltar' para retornar ao menu): ")
    if numero_conta.lower() == 'voltar':
        return contas
    if numero_conta in contas:
        senha_digitada = input("Digite sua senha para confirmar (ou 'voltar' para retornar ao menu): ")
        if senha_digitada.lower() == 'voltar':
            return contas
        if not verificar_senha(senha_digitada, contas[numero_conta]["senha"]):
            print("Senha incorreta!")
            return contas
            
        if input("Deseja continuar? (s/n): ").lower() != 's':
            return contas
        valor = float(input("Digite o valor a ser sacado (ou 'voltar' para retornar ao menu): "))
        if valor <= contas[numero_conta]["saldo"]:
            contas[numero_conta]["saldo"] -= valor
            contas[numero_conta]["movimentacoes"].append(f"Saque: -{valor}")
        else:
            print("Saldo insuficiente.")
    else:
        print("Conta não encontrada.")
    return contas

def transferir(contas):
    numero_origem = input("Digite o número da conta de origem (ou 'voltar' para retornar ao menu): ")
    if numero_origem.lower() == 'voltar':
        return contas
    
    if numero_origem in contas:
        senha_digitada = input("Digite sua senha para confirmar (ou 'voltar' para retornar ao menu): ")
        if senha_digitada.lower() == 'voltar':
            return contas
        if not verificar_senha(senha_digitada, contas[numero_origem]["senha"]):
            print("Senha incorreta!")
            return contas
            
        numero_destino = input("Digite o número da conta de destino (ou 'voltar' para retornar ao menu): ")
        if numero_destino.lower() == 'voltar':
            return contas
            
        if numero_origem in contas and numero_destino in contas:
            if input("Deseja continuar? (s/n): ").lower() != 's':
                return contas
            valor = float(input("Digite o valor a ser transferido (ou 'voltar' para retornar ao menu): "))
            if valor <= contas[numero_origem]["saldo"]:
                contas[numero_origem]["saldo"] -= valor
                contas[numero_destino]["saldo"] += valor
                contas[numero_origem]["movimentacoes"].append(f"Transferência para {contas[numero_destino]['nome']}: -{valor}")
                contas[numero_destino]["movimentacoes"].append(f"Transferência de {contas[numero_origem]['nome']}: +{valor}")
            else:
                print("Saldo insuficiente.")
    else:
        print("Conta de origem ou destino não encontrada.")
    return contas

def exibir_conta(contas):
    numero_conta = input("Digite o número da conta a ser exibida (ou 'voltar' para retornar ao menu): ")
    if numero_conta.lower() == 'voltar':
        return
    if numero_conta in contas:
        # Não precisa de senha pois mostra apenas informações públicas
        print("\n=== Informações Básicas da Conta ===")
        print(f"Nome: {contas[numero_conta]['nome']}")
        print(f"Número da Conta: {numero_conta}")
        print("=================================")
    else:
        print("Conta não encontrada.")

def exibir_extrato(contas):
    numero_conta = input("Digite o número da conta para exibir o extrato (ou 'voltar' para retornar ao menu): ")
    if numero_conta.lower() == 'voltar':
        return
    if numero_conta in contas:
        if input("Deseja continuar? (s/n): ").lower() != 's':
            return
        print("Extrato:")
        for mov in contas[numero_conta]["movimentacoes"]:
            print(mov)
        print(f"Saldo atual: {contas[numero_conta]['saldo']}")
    else:
        print("Conta não encontrada.")

def salvar_dados(contas):
    with open("dados_bancarios.json", "w", encoding='utf-8') as f:
        json.dump(contas, f, indent=4, ensure_ascii=False)
    print("Dados salvos com sucesso.")

def carregar_dados():
    try:
        with open("dados_bancarios.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Criando novo arquivo.")
        return {}
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo de dados. Verifique o formato.")
        return {}

def menu():
    print("\n--- Sistema Bancário ---")
    print("1 - Cadastrar conta")
    print("2 - Editar conta")
    print("3 - Verificar conta")
    print("4 - Depositar")
    print("5 - Sacar")
    print("6 - Transferir")
    print("7 - Exibir conta")
    print("8 - Exibir extrato")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def main():
    contas = carregar_dados()

    while True:
        opcao = menu()

        if opcao == "1":
            contas = cadastrar_conta(contas)
        elif opcao == "2":
            contas = editar_conta(contas)
        elif opcao == "3":
            contas = verificar_conta(contas)
        elif opcao == "4":
            contas = depositar(contas)
        elif opcao == "5":
            contas = sacar(contas)
        elif opcao == "6":
            contas = transferir(contas)
        elif opcao == "7":
            exibir_conta(contas)
        elif opcao == "8":
            exibir_extrato(contas)
        elif opcao == "0":
            salvar_dados(contas)
            break
        else:
            print("Opção inválida.")

    print("Programa encerrado.")

if __name__ == "__main__":
    main()