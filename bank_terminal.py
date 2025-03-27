import hashlib
import re
import random
from bank_email import enviar_notificacao_transacao 
from datetime import datetime
from SQL_lite import BankDatabase

# Inicializa conexão com banco
db = BankDatabase()

def gerar_numero_conta():
    while True:
        numero = random.randint(1000, 9999)
        numero_conta = f"{numero}-5"
        # Verifica se já existe no banco
        db.cursor.execute("SELECT numero_conta FROM contas WHERE numero_conta = ?", (numero_conta,))
        if not db.cursor.fetchone():
            return numero_conta

def cadastrar_conta():
    print("Cadastrando conta...")
    if input("Deseja continuar? (s/n): ").lower() != 's':
        return
    
    nome = input("Digite seu nome (ou 'voltar' para retornar ao menu): ")
    if nome.lower() == 'voltar':
        return
        
    cpf = input("Digite seu CPF (apenas números ou com pontuação): ")
    if cpf.lower() == 'voltar':
        return
    if not validar_cpf(cpf):
        print("CPF inválido! Por favor, digite um CPF válido.")
        return
    cpf_formatado = formatar_cpf(cpf)
    
    # Verifica CPF no banco
    db.cursor.execute("SELECT cpf FROM contas WHERE cpf = ?", (cpf_formatado,))
    if db.cursor.fetchone():
        print("CPF já cadastrado no sistema!")
        return
            
    email = input("Digite seu e-mail (ou 'voltar' para retornar ao menu): ")
    if email.lower() == 'voltar':
        return
    if not validar_email(email):
        print("Email inválido! Por favor, digite um email válido.")
        return
        
    senha = input("Digite sua senha (ou 'voltar' para retornar ao menu): ")
    if senha.lower() == 'voltar':
        return
    saldo = float(input("Digite o saldo inicial (ou 'voltar' para retornar ao menu): "))
    
    numero_conta = gerar_numero_conta()
    senha_criptografada = criptografar_senha(senha)
    
    # Insere no banco
    db.cursor.execute("""
    INSERT INTO contas (numero_conta, nome, cpf, email, senha, saldo)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (numero_conta, nome, cpf_formatado, email, senha_criptografada, saldo))
    
    db.conn.commit()
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")

def depositar():
    numero_conta = input("Digite o número da conta para depósito (ou 'voltar' para retornar ao menu): ")
    if numero_conta.lower() == 'voltar':
        return
        
    # Verifica se conta existe
    db.cursor.execute("SELECT saldo, email FROM contas WHERE numero_conta = ?", (numero_conta,))
    result = db.cursor.fetchone()
    
    if result:
        if input("Deseja continuar? (s/n): ").lower() != 's':
            return
            
        saldo_atual = result[0]
        email = result[1]
        valor = float(input("Digite o valor a ser depositado (ou 'voltar' para retornar ao menu): "))
        
        # Atualiza saldo
        novo_saldo = saldo_atual + valor
        db.cursor.execute("""
        UPDATE contas SET saldo = ? WHERE numero_conta = ?
        """, (novo_saldo, numero_conta))
        
        # Registra movimentação
        db.cursor.execute("""
        INSERT INTO movimentacoes (numero_conta, tipo, valor, data, descricao)
        VALUES (?, ?, ?, ?, ?)
        """, (numero_conta, "depósito", valor, datetime.now(), 
              f"Depósito realizado: R$ +{valor:.2f}"))
        
        db.conn.commit()
        
        transacao = f"Depósito realizado: R$ +{valor:.2f}\nSaldo atual: R$ {novo_saldo:.2f}"
        enviar_notificacao_transacao(transacao, email)
    else:
        print("Conta não encontrada.")

def criar_conta():
    print("\n=== Criar Nova Conta ===")
    numero_conta = input("Número da conta: ")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    senha = input("Senha: ")
    
    try:
        db.cursor.execute("""
        INSERT INTO contas (numero_conta, nome, cpf, email, senha, saldo)
        VALUES (?, ?, ?, ?, ?, 0.0)
        """, (numero_conta, nome, cpf, email, senha))
        db.conn.commit()
        print("Conta criada com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF ou número de conta já cadastrado!")

def realizar_deposito():
    numero_conta = input("Número da conta: ")
    valor = float(input("Valor do depósito: R$ "))
    
    if valor <= 0:
        print("Valor inválido!")
        return
        
    try:
        db.cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE numero_conta = ?", 
                         (valor, numero_conta))
        db.adicionar_movimentacao(numero_conta, "Depósito", valor, "Depósito em conta")
        db.conn.commit()
        print("Depósito realizado com sucesso!")
    except sqlite3.Error:
        print("Erro ao realizar depósito!")

def realizar_saque():
    numero_conta = input("Número da conta: ")
    valor = float(input("Valor do saque: R$ "))
    
    saldo = db.get_saldo(numero_conta)
    if saldo is None:
        print("Conta não encontrada!")
        return
        
    if valor > saldo:
        print("Saldo insuficiente!")
        return
        
    try:
        db.cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE numero_conta = ?", 
                         (valor, numero_conta))
        db.adicionar_movimentacao(numero_conta, "Saque", -valor, "Saque em conta")
        db.conn.commit()
        print("Saque realizado com sucesso!")
    except sqlite3.Error:
        print("Erro ao realizar saque!")

def consultar_saldo():
    numero_conta = input("Número da conta: ")
    saldo = db.get_saldo(numero_conta)
    
    if saldo is not None:
        print(f"Saldo atual: R$ {saldo:.2f}")
    else:
        print("Conta não encontrada!")

def consultar_conta():
    numero_conta = input("Digite o número da conta: ")
    conta = db.ler_conta(numero_conta)
    
    if conta:
        print("\n=== Dados da Conta ===")
        print(f"Número: {conta[0]}")
        print(f"Nome: {conta[1]}")
        print(f"CPF: {conta[2]}")
        print(f"Email: {conta[3]}")
        print(f"Saldo: R$ {conta[4]:.2f}")
        
        print("\n=== Últimas Movimentações ===")
        movimentacoes = db.ler_movimentacoes_conta(numero_conta)
        for mov in movimentacoes:
            print(f"Tipo: {mov[0]}")
            print(f"Valor: R$ {mov[1]:.2f}")
            print(f"Data: {mov[2]}")
            print(f"Descrição: {mov[3]}")
            print("--------------------")
    else:
        print("Conta não encontrada!")

def menu():
    while True:
        print("\n=== Sistema Bancário ===")
        print("1 - Criar conta")
        print("2 - Realizar depósito")
        print("3 - Realizar saque")
        print("4 - Consultar saldo")
        print("5 - Consultar conta completa")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            realizar_deposito()
        elif opcao == "3":
            realizar_saque()
        elif opcao == "4":
            consultar_saldo()
        elif opcao == "5":
            consultar_conta()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()