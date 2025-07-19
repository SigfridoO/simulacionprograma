import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial.distance import euclidean


class Reparto:
    def __init__(self, num_destinos=4, semilla=42):
        self.num_destinos = num_destinos
        self.semilla = semilla
        self.origen = np.array([0, 0])
        self.destinos = None
        self.nodos = None
        self.nombres_nodos = None
        self.G = None
        self.arbol_optimo = None
        self.posiciones = None
        self.costo_total = 0.0

    def generar_nodos(self):
        np.random.seed(self.semilla)
        self.destinos = np.random.randint(-10, 10, size=(self.num_destinos, 2))
        self.nodos = [self.origen] + list(self.destinos)
        self.nombres_nodos = ['O'] + [f'D{i+1}' for i in range(self.num_destinos)]

        self.construir_grafo()

    def construir_grafo(self):
        self.G = nx.Graph()
        for i, nombre in enumerate(self.nombres_nodos):
            self.G.add_node(nombre, pos=self.nodos[i])

        for i in range(len(self.nodos)):
            for j in range(i + 1, len(self.nodos)):
                distancia = euclidean(self.nodos[i], self.nodos[j])
                self.G.add_edge(self.nombres_nodos[i], self.nombres_nodos[j], weight=distancia)

        self.posiciones = nx.get_node_attributes(self.G, 'pos')

    def calcular_arbol_optimo(self):
        self.arbol_optimo = nx.minimum_spanning_tree(self.G, weight='weight')
        self.costo_total = sum(data['weight'] for _, _, data in self.arbol_optimo.edges(data=True))

    def visualizar(self, ax=None):
        if ax is None:
            if self.arbol_optimo is None:
                raise ValueError("Primero debes calcular el árbol óptimo.")

            plt.figure(figsize=(10, 7))
            nx.draw(self.G, self.posiciones, node_color='lightgray', with_labels=True,
                    node_size=800, font_weight='bold')
            nx.draw_networkx_edges(self.G, self.posiciones, edge_color='gray', alpha=0.3)
            nx.draw(self.arbol_optimo, self.posiciones, edge_color='blue', width=2)

            etiquetas = nx.get_edge_attributes(self.arbol_optimo, 'weight')
            etiquetas_redondeadas = {k: f"{v:.2f}" for k, v in etiquetas.items()}
            nx.draw_networkx_edge_labels(self.arbol_optimo, self.posiciones, edge_labels=etiquetas_redondeadas)

            plt.title("Red de transporte ramificada: 1 origen → 4 destinos")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            self.visualizar_en_canvas(ax)

    def imprimir_resultados(self):
        print("Coordenadas de los nodos:")
        for nombre, coord in zip(self.nombres_nodos, self.nodos):
            print(f"{nombre}: {coord}")
        print(f"\nCosto total de transporte ramificado: {self.costo_total:.2f}")

    def ejecutar_simulacion(self):
        self.generar_nodos()
        self.construir_grafo()
        self.calcular_arbol_optimo()
        self.visualizar()
        self.imprimir_resultados()

    def visualizar_en_canvas(self, ax ):
        ax.clear()

        # Dibujar todos los nodos
        nx.draw(self.G, self.posiciones, node_color='lightgray', with_labels=True,
                node_size=800, font_weight='bold', ax=ax)

        # Dibujar todas las aristas del grafo base en gris claro
        nx.draw_networkx_edges(self.G, self.posiciones, edge_color='lightgray', ax=ax, style='dotted', alpha=0.4)

        # Dibujar el árbol óptimo en azul (la trayectoria usada)
        nx.draw(self.arbol_optimo, self.posiciones, edge_color='blue', width=2.5, ax=ax)

        # Agregar etiquetas con pesos (distancias)
        etiquetas = nx.get_edge_attributes(self.arbol_optimo, 'weight')
        etiquetas_redondeadas = {k: f"{v:.2f}" for k, v in etiquetas.items()}
        nx.draw_networkx_edge_labels(self.arbol_optimo, self.posiciones, edge_labels=etiquetas_redondeadas, ax=ax)

        # Título y detalles
        ax.set_title("Trayectoria óptima de reparto (árbol mínimo)")
        ax.set_axis_off()
      
def main():
    reparto = Reparto(num_destinos=4, semilla=123)
    reparto.generar_nodos()
    reparto.calcular_arbol_optimo()
    reparto.visualizar()



if __name__ == "__main__":
    main()