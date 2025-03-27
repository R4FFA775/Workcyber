import sqlite3
from datetime import datetime

class BankDatabase:
    def __init__(self, db_name="banco.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            numero_conta TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            saldo REAL NOT NULL
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_conta TEXT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            data TIMESTAMP NOT NULL,
            descricao TEXT,
            FOREIGN KEY (numero_conta) REFERENCES contas (numero_conta)
        )
        """)
        self.conn.commit()
    
    def get_saldo(self, numero_conta):
        self.cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else None

    def get_conta(self, numero_conta):
        self.cursor.execute("""
        SELECT numero_conta, nome, cpf, email, saldo 
        FROM contas WHERE numero_conta = ?""", (numero_conta,))
        return self.cursor.fetchone()

    def get_all_contas(self):
        self.cursor.execute("SELECT * FROM contas")
        return self.cursor.fetchall()

    def get_movimentacoes(self, numero_conta):
        self.cursor.execute("""
        SELECT tipo, valor, data, descricao 
        FROM movimentacoes 
        WHERE numero_conta = ? 
        ORDER BY data DESC""", (numero_conta,))
        return self.cursor.fetchall()

    def get_all_movimentacoes(self):
        self.cursor.execute("""
        SELECT m.*, c.nome 
        FROM movimentacoes m 
        JOIN contas c ON m.numero_conta = c.numero_conta 
        ORDER BY m.data DESC""")
        return self.cursor.fetchall()

    def adicionar_movimentacao(self, numero_conta, tipo, valor, descricao):
        self.cursor.execute("""
        INSERT INTO movimentacoes (numero_conta, tipo, valor, data, descricao)
        VALUES (?, ?, ?, ?, ?)""", 
        (numero_conta, tipo, valor, datetime.now(), descricao))
        self.conn.commit()

    def verificar_conta_existe(self, numero_conta):
        self.cursor.execute("SELECT * FROM contas WHERE numero_conta = ?", (numero_conta,))
        return self.cursor.fetchone() is not None

    def verificar_senha(self, numero_conta, senha):
        self.cursor.execute("SELECT senha FROM contas WHERE numero_conta = ?", (numero_conta,))
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado[0] == senha
        return False

    def ler_conta(self, numero_conta):
        try:
            self.cursor.execute("""
                SELECT numero_conta, nome, cpf, email, saldo 
                FROM contas 
                WHERE numero_conta = ?
            """, (numero_conta,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao ler conta: {e}")
            return None

    def listar_todas_contas(self):
        try:
            self.cursor.execute("SELECT numero_conta, nome, cpf, email, saldo FROM contas")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao listar contas: {e}")
            return []

    def ler_movimentacoes_conta(self, numero_conta):
        try:
            self.cursor.execute("""
                SELECT tipo, valor, data, descricao 
                FROM movimentacoes 
                WHERE numero_conta = ?
                ORDER BY data DESC
            """, (numero_conta,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao ler movimentações: {e}")
            return []

    def __del__(self):
        self.conn.close()