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
                    dist = distance(atom_pdb[2:5], atom_pdbqt[1:4])
                    if dist <= threshold:
                        nearby_residues.add((atom_pdb[0], atom_pdb[1], atom_pdb[3], model.index(atom_pdbqt), atom_pdbqt[0]))
        nearby_residues_list.append(nearby_residues)

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

    # デバッグ情報を個別の.logファイルに追記
    with open('pdb_data.log', 'a') as log_file:
        log_file.write('PDB Data:\n')
        log_file.write(str(pdb_data) + '\n')

    with open('pdbqt_models.log', 'a') as log_file:
        log_file.write('PDBQT Models:\n')
        log_file.write(str(pdbqt_models) + '\n')

    with open('nearby_residues.log', 'a') as log_file:
        log_file.write('Nearby Residues List:\n')
        log_file.write(str(nearby_residues_list) + '\n')

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Atom PDB', 'Residue Name', 'Residue Number', 'Model Number', 'Atom PDBQT']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, nearby_residues in enumerate(nearby_residues_list):
            for atom_pdb, residue_name, residue_number, model_number, atom_pdbqt in nearby_residues:
                writer.writerow({'Atom PDB': atom_pdb, 'Residue Name': residue_name, 'Residue Number': residue_number, 'Model Number': model_number, 'Atom PDBQT': atom_pdbqt})

