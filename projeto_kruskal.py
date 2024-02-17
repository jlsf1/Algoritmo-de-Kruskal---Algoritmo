import networkx as nx
import matplotlib.pyplot as plt

class Vertice:
    def __init__(self, nome):
        self.nome = nome
        self.vizinhos = {}

    def adicionar_vizinho(self, vizinho, peso):
        self.vizinhos[vizinho] = peso

class Grafo:
    def __init__(self):
        self.vertices = {}
        self.indice_vertices = {}  

    def adicionar_vertice(self, vertice):
        if isinstance(vertice, Vertice) and vertice.nome not in self.vertices:
            indice = len(self.vertices)  
            self.vertices[vertice.nome] = vertice
            self.indice_vertices[vertice.nome] = indice  
            return True
        else:
            return False
        
    def adicionar_aresta(self, origem, destino, peso):
        if origem in self.vertices and destino in self.vertices:
            self.vertices[origem].adicionar_vizinho(destino, peso)
            self.vertices[destino].adicionar_vizinho(origem, peso)
            return True
        else:
            return False

    def visualizar_grafo(self, arvore_minima=None):
            G = nx.Graph()
            for origem, vertice in self.vertices.items():
                for vizinho, peso in vertice.vizinhos.items():
                    G.add_edge(origem, vizinho, weight=peso)

            pos = nx.spring_layout(G)  #Define o layout do grafo
            nx.draw(G, pos, with_labels=True)  #Desenha o grafo
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  #Adiciona rótulos de peso nas arestas

            #Adiciona as arestas da árvore geradora mínima se estiverem disponíveis
            if arvore_minima:
                for aresta in arvore_minima:
                    origem, destino, peso = aresta
                    G.add_edge(origem, destino, weight=peso, color='yellow')

                #Desenha as arestas da árvore geradora mínima em vermelho
                nx.draw_networkx_edges(G, pos, edgelist=arvore_minima, edge_color='yellow', width=2)

            plt.show()
            
class Kruskal:
    def __init__(self, grafo):
        self.grafo = grafo
        self.arvore_minima = []

    def encontrar(self, subset, i):
        if 0 <= i < len(subset):  # Verifica se o índice está dentro dos limites da lista
            if subset[i] == -1:
                return i
            return self.encontrar(subset, subset[i])
        return -1  # Retorna -1 se o índice estiver fora dos limites da lista

    def unir(self, subset, x, y):
        x_raiz = self.encontrar(subset, x)
        y_raiz = self.encontrar(subset, y)
        subset[x_raiz] = y_raiz

    def kruskal(self):

        grafo_ordenado = []
        # Coletando todas as arestas do grafo
        for origem, vertice in self.grafo.vertices.items():
            for vizinho, peso in vertice.vizinhos.items():
                grafo_ordenado.append((origem, vizinho, peso))

        # Ordenando as arestas pelo peso
        grafo_ordenado = sorted(grafo_ordenado, key=lambda item: item[2])

        vertices = len(self.grafo.vertices)
        subset = [-1] * vertices
        arestas_adicionadas = 0
        index = 0

        while arestas_adicionadas < vertices - 1:
            origem, destino, peso = grafo_ordenado[index]
            index += 1
            # Obtém o índice do vértice
            x = self.encontrar(subset, self.grafo.indice_vertices[origem]) 
            y = self.encontrar(subset, self.grafo.indice_vertices[destino])

            if x != y:
                self.arvore_minima.append((origem, destino, peso))
                self.unir(subset, x, y)
                arestas_adicionadas += 1

        return self.arvore_minima

if __name__ == "__main__":
    grafo = Grafo()
    tabela = []
    with open('Pontos_turisticos_do_Brasil.txt', 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            dados = linha.split(', ')  # Divide a linha em partes separadas por espaços em branco
            coluna1 = dados[0]  # Primeira coluna
            coluna2 = dados[1]  # Segunda coluna
            coluna3 = float(dados[2])  # Terceira coluna convertida para float
            tupla = (coluna1, coluna2, coluna3)  # Cria uma tupla com os dados
            tabela.append(tupla)  # Adiciona a tupla à lista

    # Adicionando vértices e arestas com base na tabela
    for origem, destino, peso in tabela:
        if origem not in grafo.vertices:
            grafo.adicionar_vertice(Vertice(origem))
        if destino not in grafo.vertices:
            grafo.adicionar_vertice(Vertice(destino))
        grafo.adicionar_aresta(origem, destino, peso)

    # Visualizando o grafo
    grafo.visualizar_grafo()

    kruskal = Kruskal(grafo)
    arvore_minima = kruskal.kruskal()

    print("Arestas da árvore geradora mínima:")
    for aresta in arvore_minima:
        print(aresta)

    # Visualizando o grafo da árvore mínima gerada
    grafo.visualizar_grafo(arvore_minima)