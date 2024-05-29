import Pyro4

@Pyro4.expose
class Agenda:
    def __init__(self):
        self.contatos = []

    def adicionar_contato(self, nome, telefone):
        self.contatos.append((nome, telefone))
        return "Contato adicionado com sucesso!"

    def listar_contatos(self):
        return self.contatos

    def atualizar_contato(self, indice, nome, telefone):
        if indice < 0 or indice >= len(self.contatos):
            return "Índice de contato inválido!"
        self.contatos[indice] = (nome, telefone)
        return "Contato atualizado com sucesso!"

    def remover_contato(self, indice):
        if indice < 0 or indice >= len(self.contatos):
            return "Índice de contato inválido!"
        del self.contatos[indice]
        return "Contato removido com sucesso!"

daemon = Pyro4.Daemon()  
uri = daemon.register(Agenda())  

print("Pronto. URI da agenda:", uri)

daemon.requestLoop()  
