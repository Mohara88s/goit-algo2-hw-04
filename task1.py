import networkx as nx
import matplotlib.pyplot as plt

# Створюємо граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    ("Terminal 1", "Store 1", 25),
    ("Terminal 1", "Store 2", 20),
    ("Terminal 1", "Store 3", 15),
    ("Terminal 2", "Store 3", 15),
    ("Terminal 2", "Store 4", 30),
    ("Terminal 2", "Store 2", 10),
    ("Store 1", "Shop 1", 15),
    ("Store 1", "Shop 2", 10),
    ("Store 1", "Shop 3", 20),
    ("Store 2", "Shop 4", 15),
    ("Store 2", "Shop 5", 10),
    ("Store 2", "Shop 6", 25),
    ("Store 3", "Shop 7", 20),
    ("Store 3", "Shop 8", 15),
    ("Store 3", "Shop 9", 10),
    ("Store 4", "Shop 10", 20),
    ("Store 4", "Shop 11", 10),
    ("Store 4", "Shop 12", 15),
    ("Store 4", "Shop 13", 5),
    ("Store 4", "Shop 14", 10),
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = nx.spring_layout(G, seed=42)

# Місткості на ребрах
labels = nx.get_edge_attributes(G, "capacity")

# Малюємо граф
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue",
        font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()
