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

    coordinates = []

    for line in pdbqt_lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())

            coordinates.append([x, y, z])

    return coordinates

def distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

def find_nearby_residues(pdb_data, pdbqt_coords, threshold=5.0):
    nearby_residues = set()

    for atom_label, residue_name, residue_number, x, y, z in pdb_data:
        pdb_coord = [x, y, z]
        for qt_coord in pdbqt_coords:
            if distance(pdb_coord, qt_coord) <= threshold:
                nearby_residues.add((atom_label, residue_name))

    return nearby_residues

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <pdb_file> <pdbqt_file>")
        sys.exit(1)

    pdb_file = sys.argv[1]
    pdbqt_file = sys.argv[2]

    pdb_data = parse_pdb_file(pdb_file)
    pdbqt_coords = parse_pdbqt_file(pdbqt_file)

    nearby_residues = find_nearby_residues(pdb_data, pdbqt_coords)

    for atom_label, residue_name in nearby_residues:
        print(atom_label, residue_name)
