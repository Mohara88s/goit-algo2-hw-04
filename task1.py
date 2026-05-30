import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False

# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        
        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        
        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow

def main():
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

    # Додавання ребер з місткостями в граф
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

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


    # Збираємо унікальні назви вузлів
    unique_nodes = set()
    for u, v, _ in edges:
        unique_nodes.add(u)
        unique_nodes.add(v)
    
    # Додаємо віртуальні супервузли
    unique_nodes.add("Super Source")
    unique_nodes.add("Super Sink")
    
    # Створюємо мапінг: Рядок -> Число-індекс
    node_to_idx = {name: idx for idx, name in enumerate(sorted(unique_nodes))}
    num_nodes = len(node_to_idx)

    # Ініціалізуємо порожню матрицю суміжності (заповнену нулями)
    capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    # Заповнюємо матрицю реальними ребрами
    for u, v, cap in edges:
        capacity_matrix[node_to_idx[u]][node_to_idx[v]] = cap

    # З'єднуємо Суперджерело з реальними терміналами
    capacity_matrix[node_to_idx["Super Source"]][node_to_idx["Terminal 1"]] = float('inf')
    capacity_matrix[node_to_idx["Super Source"]][node_to_idx["Terminal 2"]] = float('inf')

    # З'єднуємо реальні магазини (Shop 1-14) з Суперстоком
    for i in range(1, 15):
        shop_name = f"Shop {i}"
        capacity_matrix[node_to_idx[shop_name]][node_to_idx["Super Sink"]] = float('inf')

    # Визначаємо індекси старту та фінішу для алгоритму
    source_idx = node_to_idx["Super Source"]
    sink_idx = node_to_idx["Super Sink"]

    # Виклик функції Едмондса-Карпа
    max_flow_value = edmonds_karp(capacity_matrix, source_idx, sink_idx)

    print(f"Maximal flow in the network: {max_flow_value}")
    

if __name__ == "__main__":
    main()