import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import PhotoImage

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

        # Fecha a janela do Matplotlib se estiver aberta
        plt.close()

        G = nx.Graph()
        for origem, vertice in self.vertices.items():
            for vizinho, peso in vertice.vizinhos.items():
                G.add_edge(origem, vizinho, weight=peso)

        pos = nx.spring_layout(G)  # Define o layout do grafo
        nx.draw(G, pos, with_labels=True)  # Desenha o grafo
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # Adiciona rótulos de peso nas arestas

        # Adiciona as arestas da árvore geradora mínima se estiverem disponíveis
        if arvore_minima:
            for aresta in arvore_minima:
                origem, destino, peso = aresta
                G.add_edge(origem, destino, weight=peso, color='yellow')

            # Desenha as arestas da árvore geradora mínima
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

# Função para exibir o grafo
def mostrar_grafo():
    grafo.visualizar_grafo()

# Função para exibir a árvore mínima
def mostrar_arvore_minima():
    kruskal = Kruskal(grafo)
    arvore_minima = kruskal.kruskal()
    grafo.visualizar_grafo(arvore_minima)

# Cria a interface
root = tk.Tk()
root.title('Algoritmo de Kruskal')
root.geometry('500x300')

background_image = PhotoImage(file='.\imagens\Tela.png')
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Cria o grafo
grafo = Grafo()
tabela = []
with open('Pontos_turisticos_do_Brasil.txt', 'r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        if not linha.startswith('#'):
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

# Botões
imagem_botao_grafo = tk.PhotoImage(file='.\imagens\grafo.png')
botao_grafo = tk.Button(root, text = 'Mostrar Grafo', image = imagem_botao_grafo, width=150, height=40, command = mostrar_grafo)
botao_grafo.place(x=90, y=230)

imagem_botao_arvore_minima = tk.PhotoImage(file='.\imagens\árvore mínima.png')
botao_arvore_minima = tk.Button(root, text = 'Mostrar Árvore Mínima', image = imagem_botao_arvore_minima, width=150, height=40, command = mostrar_arvore_minima)
botao_arvore_minima.place(x=270, y=230)

# Main
root.mainloop()
