import sys
import csv
import re
import math
import argparse
import matplotlib.pyplot as plt

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

def calculate_distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

def find_nearby_residues(pdb_data, pdbqt_models, threshold):
    nearby_residues_list = []

    for model in pdbqt_models:
        nearby_residues = set()
        for pdb_atom in pdb_data:
            for model_atom in model:
                distance = calculate_distance(pdb_atom[3:], model_atom[2:])
                if distance <= threshold:
                    nearby_residues.add((pdb_atom[0], pdb_atom[1], pdb_atom[2], model_atom[0], model_atom[1], distance))  # distanceを追加
        nearby_residues_list.append(nearby_residues)

    return nearby_residues_list

def create_stacked_bar_chart(nearby_residues_list, output_image):
    residue_counts = {}

    for i, nearby_residues in enumerate(nearby_residues_list):
        for _, _, residue_number, _, _, _ in nearby_residues:
            if residue_number not in residue_counts:
                residue_counts[residue_number] = [0] * len(nearby_residues_list)
            residue_counts[residue_number][i] += 1

    residue_numbers = list(residue_counts.keys())
    residue_numbers.sort()

    data_matrix = [residue_counts[residue_number] for residue_number in residue_numbers]

    fig, ax = plt.subplots()

    for model_index, model_data in enumerate(zip(*data_matrix)):
        ax.bar(residue_numbers, model_data, bottom=[sum(x) for x in zip(*data_matrix[:model_index])], label=f'MODEL {model_index + 1}')

    ax.set_xticks(residue_numbers)
    ax.set_xticklabels(residue_numbers)
    ax.set_xlabel('Residue Numbers')
    ax.set_ylabel('Number of Nearby Residues')
    ax.set_title('Nearby Residues per Residue Number')

    plt.legend()
    plt.savefig(output_image, dpi=300)
    plt.close()


def main(args):
    pdb_file = args.pdb_file
    pdbqt_file = args.pdbqt_file
    output_csv = args.output_csv
    threshold = args.threshold

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models, threshold)

    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PDB_Atom', 'Residue_Name', 'Residue_Number', 'PDBQT_Model', 'PDBQT_Atom', 'Distance'])

        for i, nearby_residues in enumerate(nearby_residues_list):
            for pdb_label, residue_name, residue_number, model_number, atom_label, distance in nearby_residues:
                csv_writer.writerow([pdb_label, residue_name, residue_number, model_number, atom_label, distance])

    # 以下の行をmain関数内に移動
    output_image = args.output_csv.replace('.csv', '.png')
    create_stacked_bar_chart(nearby_residues_list, output_image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby residues in PDBQT models")
    parser.add_argument("pdb_file", type=str, help="Input PDB file")
    parser.add_argument("pdbqt_file", type=str, help="Input PDBQT file")
    parser.add_argument("output_csv", type=str, help="Output CSV file")
    parser.add_argument("-t", "--threshold", type=float, default=5.0, help="Distance threshold for nearby residues (default: 5.0)")

    args = parser.parse_args()
    main(args)
