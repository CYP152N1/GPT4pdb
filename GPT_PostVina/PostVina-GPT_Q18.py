import sys
import csv
import re
import math


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

    print("PDB Data:")  # Debug print
    print(data_matrix)  # Debug print
    return data_matrix


def parse_pdbqt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    models = []
    current_model = []

    for line in lines:
        if line.startswith('MODEL'):
            current_model = []
        elif line.startswith('ATOM') or line.startswith('HETATM'):
            atom_label = line[12:16].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            current_model.append((atom_label, x, y, z))
        elif line.startswith('ENDMDL'):
            models.append(current_model)

    print("PDBQT Models:")  # Debug print
    print(models)  # Debug print
    return models


def distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))


def find_nearby_residues(pdb_data, pdbqt_models, threshold=5.0):
    nearby_residues_list = []

    for model in pdbqt_models:
        nearby_residues = set()
        for atom_pdbqt in model:
            for atom_pdb in pdb_data:
                if atom_pdb[0] not in ["C", "N", "O", "CA"]:
                    # distance関数の呼び出しを修正
                    dist = distance(atom_pdb[3:6], atom_pdbqt[1:4])
                    if dist <= threshold:
                        nearby_residues.add((atom_pdb[0], atom_pdb[1], atom_pdb[2], model.index(atom_pdbqt), atom_pdbqt[0]))
        nearby_residues_list.append(nearby_residues)

    print("Nearby Residues List:")  # Debug print
    print(nearby_residues_list)  # Debug print
    return nearby_residues_list


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py pdb_file pdbqt_file output_csv")
        sys.exit(1)

    pdb_file = sys.argv[1]
    pdbqt_file = sys.argv[2]
    output_csv = sys.argv[3]

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models)

    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PDB_Atom', 'Residue_Name', 'Residue_Number', 'PDBQT_Model', 'PDBQT_Atom'])
    
        for i, nearby_residues in enumerate(nearby_residues_list):
            for pdb_label, residue_name, residue_number, model_number, atom_label in nearby_residues:
                row = [pdb_label, residue_name, residue_number, model_number, atom_label]
                print("Writing row:", row)  # デバッグプリントを追加
                csv_writer.writerow(row)
