import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

class Graphe:
    def __init__(self, sommets):
        self.nb_sommets = sommets + 1
        self.liste_adjacence = defaultdict(list)
        self.temps = 0

    def ajouter_arete(self, u, v):
        self.liste_adjacence[u].append(v)
        self.liste_adjacence[v].append(u)

    def points_articulation_util(self, u, visite, parent, bas, decouverte, pa):
        enfants = 0
        visite[u] = True
        decouverte[u] = self.temps
        bas[u] = self.temps
        self.temps += 1

        for v in self.liste_adjacence[u]:
            if not visite[v]:
                parent[v] = u
                enfants += 1

                self.points_articulation_util(v, visite, parent, bas, decouverte, pa)
                bas[u] = min(bas[u], bas[v])

                if parent[u] is None and enfants > 1:
                    pa[u] = True
                elif parent[u] is not None and bas[v] >= decouverte[u]:
                    pa[u] = True
            elif v != parent[u]:
                bas[u] = min(bas[u], decouverte[v])

    def trouver_points_articulation(self):
        visite = [False] * self.nb_sommets
        decouverte = [float('inf')] * self.nb_sommets
        bas = [float('inf')] * self.nb_sommets
        parent = [None] * self.nb_sommets
        pa = [False] * self.nb_sommets

        for i in range(self.nb_sommets):
            if not visite[i]:
                self.points_articulation_util(i, visite, parent, bas, decouverte, pa)

        return [index for index, est_pa in enumerate(pa) if est_pa]

class ApplicationGraphe:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Chercher les Points d'Articulation")

        self.graphe = None

        # Cadre principal pour aligner les widgets
        cadre_principal = tk.Frame(racine, padx=20, pady=20)
        cadre_principal.grid(row=0, column=0)

        # Champ d'entrée pour le nombre de sommets
        self.etiquette_sommets = tk.Label(cadre_principal, text="Nombre Total de Sommets:")
        self.etiquette_sommets.grid(row=0, column=0, sticky="w", pady=5)
        self.entree_sommets = tk.Entry(cadre_principal, width=30)
        self.entree_sommets.grid(row=0, column=1, pady=5)

        # Champ d'entrée pour les arêtes
        self.etiquette_aretes = tk.Label(cadre_principal, text="Ajouter les Arêtes (u v, u v, ...):")
        self.etiquette_aretes.grid(row=1, column=0, sticky="w", pady=5)
        self.entree_aretes = tk.Entry(cadre_principal, width=30)
        self.entree_aretes.grid(row=1, column=1, pady=5)

        # Bouton pour afficher le graphe et les points d'articulation
        self.bouton_afficher_graphe = tk.Button(cadre_principal, text="Afficher le Graphe et les Points d'Articulation", command=self.afficher_graphe, width=30)
        self.bouton_afficher_graphe.grid(row=2, column=0, columnspan=2, pady=15)

    def ajouter_les_aretes(self):
        try:
            sommets = int(self.entree_sommets.get())
            self.graphe = Graphe(sommets)

            entrees_aretes = self.entree_aretes.get().split(',')
            for entree in entrees_aretes:
                u, v = map(int, entree.strip().split())
                if u >= sommets + 1 or v >= sommets + 1:
                    messagebox.showerror("Erreur", "Les sommets doivent être inférieurs au nombre total de sommets.")
                    return
                self.graphe.ajouter_arete(u, v)

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer les arêtes au format indiqué.")

    def afficher_graphe(self):
        try:
            self.ajouter_les_aretes()

            points_articulation = self.graphe.trouver_points_articulation()

            G = nx.Graph()

            for i in range(1, self.graphe.nb_sommets):
                G.add_node(i)

            for u, v in self.graphe.liste_adjacence.items():
                for voisin in v:
                    G.add_edge(u, voisin)

            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=700, font_size=10, edge_color='black')
            nx.draw_networkx_nodes(G, pos, nodelist=points_articulation, node_color='orange', node_size=700)

            plt.title("Graphe avec Points d'Articulation (Orange)")
            plt.show()

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier pour les sommets.")

if __name__ == "__main__":
    racine = tk.Tk()
    app = ApplicationGraphe(racine)
    racine.mainloop()
