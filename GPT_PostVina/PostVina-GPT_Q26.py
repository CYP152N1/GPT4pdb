import sys
import csv
import re
import math
import argparse

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

def calculate_distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

def find_nearby_residues(pdb_data, pdbqt_models, threshold):
    nearby_residues_list = []

    for model in pdbqt_models:
        nearby_residues = set()
        for pdb_atom in pdb_data:
            for model_atom in model:
                distance = calculate_distance(pdb_atom[3:], model_atom[1:])
                if distance <= threshold:
                    nearby_residues.add((pdb_atom[0], pdb_atom[1], pdb_atom[2], model.index(model_atom), model_atom[0], distance))
        nearby_residues_list.append(nearby_residues)

    return nearby_residues_list

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

        for i, nearby_residues in enumerate(nearby_residues_list):            for pdb_label, residue_name, residue_number, model_number, atom_label, distance in nearby_residues:
                csv_writer.writerow([pdb_label, residue_name, residue_number, model_number, atom_label, distance])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby residues in PDBQT models")
    parser.add_argument("pdb_file", type=str, help="Input PDB file")
    parser.add_argument("pdbqt_file", type=str, help="Input PDBQT file")
    parser.add_argument("output_csv", type=str, help="Output CSV file")
    parser.add_argument("-t", "--threshold", type=float, default=5.0, help="Distance threshold for nearby residues (default: 5.0)")

    args = parser.parse_args()
    main(args)

