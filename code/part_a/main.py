import numpy as np
from csv import DictReader
from sys import argv
from functools import cache

def haversine(lat1, lon1, lat2, lon2):
	R = 6371 # radius of Earth in kilometers
	phi1 = np.radians(lat1)
	phi2 = np.radians(lat2)
	delta_phi = np.radians(lat2 - lat1)
	delta_lambda = np.radians(lon2 - lon1)
	a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
	res = R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
	return np.round(res, 2)

def tsp(i, m, memo, dist):
	if m == ((1 << i) | 3):
		return dist[0]

def main(in_file_name, out_file_name):
	# Take input
	ids = []
	locs = []

	depot_loc = (-1, -1)
	with open(in_file_name, 'r') as in_file:
		reader = DictReader(in_file)
		for row in reader:
			ids.append(int(row['order_id']))
			locs.append((float(row['lat']), float(row['lng'])))
			depot_loc = (float(row['depot_lat']), float(row['depot_lng']))

	ids.insert(0, 0)
	locs.insert(0, depot_loc)

	num_nodes = len(ids)

	# Generate adjacency matrix
	dist = [[0] * len(ids) for _ in range(len(ids))]
	for i in range(num_nodes):
		for j in range(i + 1, num_nodes):
			dist[i][j] = dist[j][i] = haversine(*locs[i], *locs[j])
	
	for i in dist:
		print(*i)
	
	# Compute travelling salesman
	memo = [[-1] * (1 << num_nodes) for _ in range(num_nodes)]
	min_dist = float('inf')
	for i in range(n):
		pass
	
if __name__ == '__main__':
	assert(len(argv) == 3)
	main(argv[1], argv[2])
