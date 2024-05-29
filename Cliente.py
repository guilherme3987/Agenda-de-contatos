import Pyro4
import tkinter as tk
from tkinter import messagebox

class AgendaCliente:
    def __init__(self, master, uri):
        self.master = master
        self.master.title("Agenda de Contatos")

        self.agenda = Pyro4.Proxy(uri)

        self.frame_adicionar = tk.Frame(self.master)
        self.frame_adicionar.pack(padx=10, pady=10)

        tk.Label(self.frame_adicionar, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(self.frame_adicionar)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_adicionar, text="Telefone:").grid(row=1, column=0, sticky="w")
        self.telefone_entry = tk.Entry(self.frame_adicionar)
        self.telefone_entry.grid(row=1, column=1, padx=5, pady=5)

        self.botao_adicionar = tk.Button(self.frame_adicionar, text="Adicionar", command=self.adicionar_contato)
        self.botao_adicionar.grid(row=2, column=0, columnspan=2, pady=5)

        self.botao_listar = tk.Button(self.frame_adicionar, text="Listar Contatos", command=self.listar_contatos)
        self.botao_listar.grid(row=3, column=0, columnspan=2, pady=5)

        self.frame_listar = tk.Frame(self.master)
        self.frame_listar.pack(padx=10, pady=10)

        self.lista_contatos = tk.Listbox(self.frame_listar, width=40)
        self.lista_contatos.pack()

        self.frame_atualizar = tk.Frame(self.master)
        self.frame_atualizar.pack(padx=10, pady=10)

        tk.Label(self.frame_atualizar, text="Selecione um contato:").grid(row=0, column=0, sticky="w")
        self.indice_entry = tk.Entry(self.frame_atualizar, width=5)
        self.indice_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_atualizar, text="Novo Nome:").grid(row=1, column=0, sticky="w")
        self.novo_nome_entry = tk.Entry(self.frame_atualizar)
        self.novo_nome_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_atualizar, text="Novo Telefone:").grid(row=2, column=0, sticky="w")
        self.novo_telefone_entry = tk.Entry(self.frame_atualizar)
        self.novo_telefone_entry.grid(row=2, column=1, padx=5, pady=5)

        self.botao_atualizar = tk.Button(self.frame_atualizar, text="Atualizar", command=self.atualizar_contato)
        self.botao_atualizar.grid(row=3, column=0, columnspan=2, pady=5)

        self.botao_remover = tk.Button(self.frame_atualizar, text="Remover", command=self.remover_contato)
        self.botao_remover.grid(row=4, column=0, columnspan=2, pady=5)

    def adicionar_contato(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()

        if nome and telefone:
            contatos = self.agenda.listar_contatos()
            if (nome, telefone) in contatos:
                messagebox.showerror("Erro", "Este contato já existe na lista.")
            else:
                mensagem = self.agenda.adicionar_contato(nome, telefone)
                messagebox.showinfo("Sucesso", mensagem)
                self.nome_entry.delete(0, tk.END)
                self.telefone_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def listar_contatos(self):
        self.lista_contatos.delete(0, tk.END)
        contatos = self.agenda.listar_contatos()
        if contatos:
            for i, contato in enumerate(contatos, start=1):
                self.lista_contatos.insert(tk.END, f"{i}. Nome: {contato[0]}, Telefone: {contato[1]}")
        else:
            messagebox.showinfo("Info", "Nenhum contato na lista.")

    def atualizar_contato(self):
        indice = self.indice_entry.get()
        novo_nome = self.novo_nome_entry.get()
        novo_telefone = self.novo_telefone_entry.get()

        if indice and novo_nome and novo_telefone:
            try:
                indice = int(indice) - 1
                contatos = self.agenda.listar_contatos()
                if 0 <= indice < len(contatos):
                    mensagem = self.agenda.atualizar_contato(indice, novo_nome, novo_telefone)
                    messagebox.showinfo("Sucesso", mensagem)
                    self.listar_contatos()
                    self.indice_entry.delete(0, tk.END)
                    self.novo_nome_entry.delete(0, tk.END)
                    self.novo_telefone_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Erro", "Índice de contato inválido.")
            except ValueError:
                messagebox.showerror("Erro", "Índice de contato inválido.")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def remover_contato(self):
        indice = self.indice_entry.get()

        if indice:
            try:
                indice = int(indice) - 1
                contatos = self.agenda.listar_contatos()
                if 0 <= indice < len(contatos):
                    mensagem = self.agenda.remover_contato(indice)
                    messagebox.showinfo("Sucesso", mensagem)
                    self.listar_contatos()
                    self.indice_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Erro", "Índice de contato inválido.")
            except ValueError:
                messagebox.showerror("Erro", "Índice de contato inválido.")
        else:
            messagebox.showerror("Erro", "Por favor, preencha o índice do contato.")

def main():
    uri = input("Digite a URI da agenda: ")
    root = tk.Tk()
    app = AgendaCliente(root, uri)
    root.mainloop()

if __name__ == "__main__":
    main()
