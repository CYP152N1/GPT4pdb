import sys
import csv
import re
import math
import argparse
import matplotlib.pyplot as plt

# PDBファイルを解析する関数
def parse_pdb(file_path):
    with open(file_path, 'r') as f:
        pdb_lines = f.readlines()

    data_matrix = []

    for line in pdb_lines:
        if line.startswith("ATOM"):
            atom_label = line[12:16].strip()
            if atom_label not in ["C", "N", "O", "CA"]:
                residue_name = line[17:20].strip()
                residue_number = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())

                data_matrix.append([atom_label, residue_name, residue_number, x, y, z])

    return data_matrix

# PDBQTファイルを解析する関数
def parse_pdbqt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    models = []
    current_model = []
    model_number = 0

    for line in lines:
        if line.startswith('MODEL'):
            model_number = int(line.split()[1])  # MODELの番号を取得
            current_model = []
        elif line.startswith('ATOM') or line.startswith('HETATM'):
            atom_label = line[12:16].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            current_model.append((model_number, atom_label, x, y, z))  # MODEL番号を追加
        elif line.startswith('ENDMDL'):
            models.append(current_model)

    return models

# 座標間の距離を計算する関数
def calculate_distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

# 近くの残基を見つける関数
def find_nearby_residues(pdb_data, pdbqt_models, threshold):
    nearby_residues_list = []

    for model in pdbqt_models:
        nearby_residues = set()
        for pdb_atom in pdb_data:
            for model_atom in model:
                distance = calculate_distance(pdb_atom[3:], model_atom[2:])
                if distance <= threshold:
                    nearby_residues.add((pdb_atom[0], pdb_atom[1], pdb_atom[2], model_atom[0], model_atom[1], round(distance, 2)))  # distanceを小数点第2位まで丸める
        nearby_residues_list.append(nearby_residues)

    return nearby_residues_list

def create_stacked_bar_chart(nearby_residues_list, output_image, threshold):
    residue_scores = {}

    for i, nearby_residues in enumerate(nearby_residues_list):
        for _, _, residue_number, _, _, distance in nearby_residues:
            score = 1 - (distance / threshold)  # スコアを計算
            if residue_number not in residue_scores:
                residue_scores[residue_number] = [0] * len(nearby_residues_list)
            residue_scores[residue_number][i] += score

    residue_numbers = list(residue_scores.keys())
    residue_numbers.sort()

    data_matrix = [residue_scores[residue_number] for residue_number in residue_numbers]

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    bottoms = [0] * len(residue_numbers)
    max_height = 0
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        bar_container = ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

        # 最後のモデルの場合、各棒グラフの上に残基番号を表示
        if model_index == len(nearby_residues_list) - 1:
            for bar, residue_number, total_height in zip(bar_container, residue_numbers, bottoms):
                height = bar.get_height()
                if total_height > 0:  # 総積み上げ高さが0より大きい場合のみ残基番号を表示
                    ax.text(bar.get_x() + bar.get_width() / 2, total_height, str(residue_number),
                            ha='center', va='bottom', fontsize=8, rotation=90)
                    
        # 最大の積み上げ高さを更新
        max_height = max(max_height, max(bottoms))

    # 縦軸の最大値を設定
    ax.set_ylim(0, max_height * 1.1)  # 最大値の10%上に設定

    # 凡例を右端に表示
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    
    ax.set_xticks(residue_numbers)
    ax.set_xticklabels(residue_numbers)
    ax.set_xlabel('Residue Numbers')
    ax.set_ylabel('Score of Nearby Residues')  # 縦軸のラベルを変更
    ax.set_title('Score of Nearby Residues per Residue Number')

    plt.legend()
    plt.savefig(output_image, dpi=300)
    plt.close()


def main(args):
    pdb_file = args.pdb_file
    pdbqt_file = args.pdbqt_file
    output_prefix = args.output_prefix
    threshold = args.threshold

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models, threshold)

    output_csv_list = f"{output_prefix}_list.csv"
    
    with open(output_csv_list, 'w', newline='') as csvfile:
        # CSVファイルに結果を書き込む
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PDB_Atom', 'Residue_Name', 'Residue_Number', 'PDBQT_Model', 'PDBQT_Atom', 'Distance'])

        for i, nearby_residues in enumerate(nearby_residues_list):
            for pdb_label, residue_name, residue_number, model_number, atom_label, distance in nearby_residues:
                csv_writer.writerow([pdb_label, residue_name, residue_number, model_number, atom_label, distance])

    # 画像ファイル名を生成
    output_image = f"{output_prefix}.png"
    create_stacked_bar_chart(nearby_residues_list, output_image, threshold)

    # 出力用のCSVファイル名を生成
    output_csv_count = f"{output_prefix}_count.csv"
    with open(output_csv_count, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Residue_Number'] + [f'MODEL {i + 1}' for i in range(len(nearby_residues_list))])

        residue_counts = {}
        for i, nearby_residues in enumerate(nearby_residues_list):
            for _, _, residue_number, _, _, _ in nearby_residues:
                if residue_number not in residue_counts:
                    residue_counts[residue_number] = [0] * len(nearby_residues_list)
                residue_counts[residue_number][i] += 1

        for residue_number, counts in residue_counts.items():
            csv_writer.writerow([residue_number] + counts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby residues in PDBQT models")
    parser.add_argument("pdb_file", type=str, help="Input PDB file")
    parser.add_argument("pdbqt_file", type=str, help="Input PDBQT file")
    parser.add_argument("output_prefix", type=str, help="Output file prefix")
    parser.add_argument("-t", "--threshold", type=float, default=5.0, help="Distance threshold for nearby residues (default: 5.0)")

    args = parser.parse_args()
    main(args)
