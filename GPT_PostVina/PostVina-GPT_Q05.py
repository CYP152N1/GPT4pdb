import sys
import re
import math

def parse_pdb_file(file_path):
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

def parse_pdbqt_file(file_path):
    with open(file_path, 'r') as f:
        pdbqt_lines = f.readlines()

    model_coordinates = []
    model_number = 0
    coordinates = []

    for line in pdbqt_lines:
        if line.startswith("MODEL"):
            model_number = int(line.split()[-1])

        if line.startswith("ATOM") or line.startswith("HETATM"):
            atom_label = line[12:16].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())

            coordinates.append((model_number, atom_label, [x, y, z]))

        if line.startswith("ENDMDL"):
            model_coordinates.append(coordinates)
            coordinates = []

    return model_coordinates

def distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

def find_nearby_residues(pdb_data, pdbqt_models, threshold=5.0):
    nearby_residues = []

    for model_coordinates in pdbqt_models:
        model_residues = set()

        for model_number, atom_label, qt_coord in model_coordinates:
            for pdb_label, residue_name, residue_number, x, y, z in pdb_data:
                pdb_coord = [x, y, z]
                if distance(pdb_coord, qt_coord) <= threshold:
                    model_residues.add((pdb_label, residue_name, model_number, atom_label))

        nearby_residues.append(model_residues)

    return nearby_residues

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <pdb_file> <pdbqt_file>")
        sys.exit(1)

    pdb_file = sys.argv[1]
    pdbqt_file = sys.argv[2]

    pdb_data = parse_pdb_file(pdb_file)
    pdbqt_models = parse_pdbqt_file(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models)

    for i, nearby_residues in enumerate(nearby_residues_list):
        print(f"MODEL {i + 1}:")
        for pdb_label, residue_name, model_number, atom_label in nearby_residues:
            print(f"PDB: {pdb_label} ({residue_name}), PDBQT: {atom_label} (Model {model_number})")
        print()

