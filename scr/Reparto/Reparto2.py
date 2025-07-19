import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

class Reparto2:
    def __init__(self, num_destinos=4, semilla=42):
        self.num_destinos = num_destinos
        self.semilla = semilla
        self.origen = np.array([0, 0])
        self.destinos = None
        self.nodos = None
        self.coordenadas = None
        self.aristas_optimas = []
        self.costo_total = 0.0

    def generar_nodos(self):
        np.random.seed(self.semilla)
        self.destinos = np.random.randint(-10, 10, size=(self.num_destinos, 2))
        self.coordenadas = [self.origen] + list(self.destinos)
        self.nodos = list(range(len(self.coordenadas)))

    def construir_aristas(self):
        aristas = []
        for i in self.nodos:
            for j in self.nodos:
                if i < j:
                    d = euclidean(self.coordenadas[i], self.coordenadas[j])
                    aristas.append((d, i, j))
        return aristas

    def calcular_arbol_optimo(self):
        parent = {i: i for i in self.nodos}

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                return True
            return False

        aristas = self.construir_aristas()
        aristas.sort()
        for peso, u, v in aristas:
            if union(u, v):
                self.aristas_optimas.append((u, v, peso))
                self.costo_total += peso

    def visualizar(self, ax):
        ax.clear()

        coords = self.coordenadas
        for i, punto in enumerate(coords):
            ax.plot(*punto, 'o', markersize=10)
            ax.text(punto[0]+0.3, punto[1]+0.3, f"N{i}", fontsize=10, color='black')

        for u, v, peso in self.aristas_optimas:
            p1, p2 = coords[u], coords[v]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='blue', linewidth=2)
            mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
            ax.text(mx, my, f"{peso:.2f}", color='red', fontsize=8)

        ax.set_title("Árbol mínimo")
        ax.grid(True)
        ax.set_aspect('equal')

    def imprimir_resultados(self):
        print("Coordenadas de los nodos:")
        for i, coord in enumerate(self.coordenadas):
            print(f"N{i}: {coord}")
        print("\nAristas seleccionadas en el árbol óptimo:")
        for u, v, peso in self.aristas_optimas:
            print(f"N{u} <-> N{v} : {peso:.2f}")
        print(f"\nCosto total del reparto (distancia total): {self.costo_total:.2f}")
        
def main():
    r = Reparto2(num_destinos=4, semilla=123)
    r.generar_nodos()
    r.calcular_arbol_optimo()
    r.imprimir_resultados()

    fig, ax = plt.subplots()
    r.visualizar(ax)
    plt.show()


if __name__ == "__main__":
    main()