import sys
import csv
import math
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.PDB.PDBExceptions import PDBConstructionWarning

def load_pdb_structure(pdb_file):
    parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    structure = parser.get_structure("structure", pdb_file)
    return structure

def extract_dihedral_angles(structure, chain_id, altloc="A"):
    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    torsion_angles = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for i in range(len(pp) - 3):
            try:
                atoms = []
                for atom_name in ['O', 'C', 'N', 'H']:
                    atom = pp[i].get_atom(atom_name, altloc)
                    if atom is not None:
                        atoms.append(atom)
                    else:
                        break
                else:
                    angle = PDB.calc_dihedral(*[atom.get_vector() for atom in atoms])
                    angle_degrees = math.degrees(angle)
                    res_id = pp[i+2].get_id()[1]
                    res_name = pp[i+2].get_resname()

                    if res_name in PDB.Polypeptide.aa3:
                        res_name_1 = three_to_one(res_name)
                        torsion_angles.append([res_name_1, res_id, angle_degrees])
            except KeyError:
                continue

    return torsion_angles

def write_dihedral_angles_to_csv(torsion_angles_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "O-C-N-H Dihedral Angle (degrees)"])
        for row in torsion_angles_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    pdb_file = input("Enter the path to your PDB file: ")
    chain_id = input("Enter chain ID: ")
    altloc = input("Enter alternate conformation ID (default is 'A'): ")
    output_filename = f"{pdb_file[:-4]}_{chain_id}_OCNH_dihedral.csv"

    try:
        structure = load_pdb_structure(pdb_file)
        torsion_angles_data = extract_dihedral_angles(structure, chain_id, altloc)
        write_dihedral_angles_to_csv(torsion_angles_data, output_filename)
        print(f"O-C-N-H dihedral angles written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
