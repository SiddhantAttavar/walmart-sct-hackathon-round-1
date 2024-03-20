#include <bits/stdc++.h>
#include <math.h>

float radians(float degrees) {
	return M_PI * degrees / 180;
}

float haversine(float lat1, float lon1, float lat2, float lon2) {
	float R = 6371;
	float phi1 = radians(lat1);
	float phi2 = radians(lat2);
	float delta_phi = radians(lat2 - lat1);
	float delta_lambda = radians(lon2 - lon1);
	float a = sin(delta_phi / 2) * sin(delta_phi / 2) * cos(phi1) * cos(phi2) * sin(delta_lambda / 2) * sin(delta_lambda / 2);
	float res = R * 2 * atan2(sqrt(a), sqrt(1 - a));
	return round(res * 100) / 100;
}

float tsp(int i, int m, std::vector<std::vector<float>> &memo, std::vector<std::vector<std::pair<int, int>>> &par, std::vector<std::vector<float>> &dist) {
	if (m == ((1 << i) | i)) {
		par[i][m] = {0, 0};
		return dist[0][i];
	}

	if (memo[i][m] != -1) {
		return memo[i][m];
	}

	int n = dist.size();
	for (int j = 1; j < n; j++) {
		if (m & (1 << j) and j != i) {
			int nm = m & (~(1 << i));
			float x = tsp(j, nm, memo, par, dist) + dist[i][j];
			if (x < memo[i][m]) {
				memo[i][m] = x;
				par[i][m] = {j, nm};
			}
		}
	}

	return memo[i][m];
}

int main(int argc, char* argv[]) {
	if (argc != 3) {
		return 0;
	}

	std::vector<int> ids = {0};
	std::vector<std::pair<float, float>> locs = {{-1, -1}};

	int num_nodes = ids.size();
	std::vector<std::vector<float>> dist(num_nodes, std::vector<float>(num_nodes));
	for (int i = 0; i < num_nodes; i++) {
		for (int j = i + 1; j < num_nodes; j++) {
			dist[i][j] = dist[j][i] = haversine(locs[i].first, locs[i].second, locs[j].first, locs[j].second);
		}
	}

	std::vector<std::vector<float>> memo(num_nodes, std::vector<float>(num_nodes, std::numeric_limits<float>::infinity()));
	std::vector<std::vector<std::pair<int, int>>> par(num_nodes, std::vector<std::pair<int, int>>(num_nodes, {-1, -1}));

	float min_dist = std::numeric_limits<float>::infinity();
	int m = (1 << num_nodes) - 1;
	int u = -1;
	for (int i = 0; i < num_nodes; i++) {
		float x = tsp(i, m, memo, par, dist) + dist[0][i];
		if (x < min_dist) {
			min_dist = x;
			u = i;
		}
	}

	std::vector<int> res = {0, u};
	while (u) {
		std::tie(u, m) = par[u][m];
		res.push_back(u);
	}

	std::cout << min_dist << std::endl;
	for (int i : res) {
		std::cout << i << ' ';
	}
	std::cout << std::endl;
}
