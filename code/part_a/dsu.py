import numpy as np
from csv import DictReader
from sys import argv


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radius of Earth in kilometers
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = (
        np.sin(delta_phi / 2) ** 2
        + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    )
    res = R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 2)


class DSU:
    def __init__(self, n):
        self.a = [-1] * n

    def get(self, x):
        if self.a[x] < 0:
            return x
        self.a[x] = self.get(self.a[x])
        return self.a[x]

    def unite(self, x, y):
        x = self.get(x)
        y = self.get(y)

        if x == y:
            return False

        if self.a[x] < self.a[y]:
            x, y = y, x

        self.a[y] += self.a[x]
        self.a[x] = y

        return True


def dfs(u, p, graph, res):
    res.append(u)
    for v in graph[u]:
        if v != p:
            dfs(v, u, graph, res)


def main(in_file_name, out_file_name):
    # Take input
    ids = []
    locs = []

    depot_loc = (-1, -1)
    with open(in_file_name, "r") as in_file:
        reader = DictReader(in_file)
        for row in reader:
            ids.append(int(row["order_id"]))
            locs.append((float(row["lat"]), float(row["lng"])))
            depot_loc = (float(row["depot_lat"]), float(row["depot_lng"]))

    ids.insert(0, 0)
    locs.insert(0, depot_loc)

    num_nodes = len(ids)

    # Generate adjacency matrix
    dist = [[0] * len(ids) for _ in range(len(ids))]
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            dist[i][j] = dist[j][i] = haversine(*locs[i], *locs[j])

    # Compute travelling salesman
    edges = [(dist[i][j], i, j) for i in range(num_nodes) for j in range(num_nodes)]
    edges.sort()
    graph = [[] for _ in range(num_nodes)]
    dsu = DSU(num_nodes)
    for (
        w,
        u,
        v,
    ) in edges:
        if dsu.unite(u, v):
            graph[u].append(v)
            graph[v].append(u)

    res = []
    dfs(0, -1, graph, res)

    min_dist = 0
    for i in range(1, num_nodes):
        min_dist += dist[res[i - 1]][res[i]]
    min_dist += dist[0][res[-1]]
    # print(min_dist)
    # print(res)

    return min_dist, res


if __name__ == "__main__":
    assert len(argv) == 3
    main(argv[1], argv[2])
