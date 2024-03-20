import os, csv
from dp import main as dp_main
from dsu import main as dsu_main

input_path = "./input_datasets/part_a/"
output_path = "./output_datasets/part_a/"

input_files = os.listdir(input_path)

permutations = {}
min_dists = {}
for f, file in enumerate(input_files):
    with open(input_path + file, "r") as in_file:
        rows = list(csv.reader(in_file))
    if len(rows) <= 21:
        ans = dp_main(input_path + file, output_path + file.replace("input", "output"))
    else:
        ans = dsu_main(input_path + file, output_path + file.replace("input", "output"))

    min_dist, res = ans
    permutations[f] = res
    min_dists[f] = min_dist

    print(f"File {file} done. Min dist: {min_dist}")

row_insert = {
    num: {node: pos + 1 for pos, node in enumerate(arr) if node}
    for num, arr in permutations.items()
}

for i, f in enumerate(input_files):
    rows = []
    with open(input_path + f, "r", newline="") as file:
        rows = list(csv.reader(file))
    with open(output_path + f.replace("input", "output"), "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(rows[0] + ["dlvr_seq_num"])
        for j in range(1, len(rows)):
            writer.writerow(rows[j] + [row_insert[i][j]])

with open(
    output_path + "part_a_best_routes_distance_travelled.csv", "w", newline=""
) as file:
    writer = csv.writer(file)
    writer.writerow(["Dataset", "Best Route Distance"])
    for i, f in enumerate(input_files):
        writer.writerow([f[:-4], min_dists[i]])
