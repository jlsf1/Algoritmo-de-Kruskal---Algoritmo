<img width="100%" src="https://cdn.discordapp.com/attachments/965066624556232737/1107835977818456074/Horizontal-Vermelho-Logotipo-CIn-UFPE.png">

## Descrição:

O projeto aborda um cenário ilustrativo que seria conectar, a partir das menores distâncias, pontos turísticos do Brasil a partir da utilzação do Algoritmo de Kruskal, conforme proposto na atividade solicitada.

A implementação do projeto consistiu, primeiramente, em elencar pontos turísticos relevantes distribuídos por regiões do país e obter suas coordenadas (longitude e latitude). A partir disso, criamos um programa para calcular a distância em quilômetros a partir das coordenadas dos pontos turísticos.

Em posse desses dados, criamos um programa que cria um grafo de modo que os vértices se relacionariam entre sí, a partir do desejo da criação de um roteiro de interesses, as arestas teriam como peso as distâncias entre os locais turísticos.

O programa, continuando sua execução, aplica o Algoritmo de Kruskal para obter a árvore geradora mínima, com base no grafo supramencionado, para traçar um roteiro para contemplar todos os pontos turísticos, percorrendo a menor quantidade de quilômetros possível.

Além disso, o programa para facilitar a visualização e a interação com os dados implementou representação visual tanto do grafo gerado, quanto da árvore geradora mínima, ambos com suas respectivos vértices, arestas e pesos. Implementamos também uma interface com um design amigável e estéticamente agradável para facilitar a experiência do usuário.

## Bibliotecas:
- Matplotlib
- NetworkX

## Dupla:
- Júlia Nunes
- José Leandro