import sys
import csv
import math
import argparse
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.PDB.PDBExceptions import PDBConstructionWarning
from Bio.PDB.Polypeptide import protein_letters_3to1

def read_pdb(pdb_file):
    parser = PDB.PDBParser(QUIET=True, PERMISSIVE=False)
    structure = parser.get_structure("structure", pdb_file)
    return structure

def extract_phi_psi(structure, chain_id):
    if chain_id not in [chain.id for chain in structure[0]]:
        raise ValueError(f"Chain {chain_id} not found in PDB structure.")

    ppb = PPBuilder()
    phi_psi = []

    for pp in ppb.build_peptides(structure[0][chain_id], aa_only=False):
        for residue, angles in zip(pp, pp.get_phi_psi_list()):
            res_name = residue.get_resname()
            res_id = residue.get_id()[1]

            if res_name in PDB.Polypeptide.aa3:
                res_name_1 = protein_letters_3to1[res_name]
                phi, psi = angles

                if phi and psi:
                    # Round phi and psi angles to 3 decimal places
                    phi_degrees = round(math.degrees(phi), 3)
                    psi_degrees = round(math.degrees(psi), 3)
                    abego = classify_abego(phi_degrees, psi_degrees)
                    phi_psi.append([res_name_1, res_id, phi_degrees, psi_degrees, abego])

    return phi_psi

def classify_abego(phi, psi):
    if (-180 <= phi < 0) and (-90 <= psi < 50):
        return 'A'
    elif (-180 <= phi < 0) and (50 <= psi < 180):
        return 'B'
    elif (0 <= phi < 180) and (-180 <= psi < 0):
        return 'E'
    elif (0 <= phi < 180) and (0 <= psi < 180):
        return 'G'
    else:
        return 'O'

def write_to_csv(phi_psi_data, output_filename):
    with open(output_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)", "ABEGO"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    # Set up argparse to handle command line arguments
    parser = argparse.ArgumentParser(description="Calculate Phi-Psi angles and ABEGO classification from a PDB file.")
    parser.add_argument("pdb_file", help="Path to the input PDB file.")
    parser.add_argument("chain_id", help="Chain ID to process.")
    parser.add_argument("-o", "--output", default=None, help="Output CSV file name. If not specified, the output file will be named based on the input PDB file.")
    
    args = parser.parse_args()

    # Set output file name based on input arguments
    if args.output:
        output_filename = args.output
    else:
        output_filename = f"{args.pdb_file[:-4]}_{args.chain_id}_phi_psi_abego.csv"

    # Process the PDB file, extract phi-psi angles, and write the results to a CSV file
    try:
        structure = read_pdb(args.pdb_file)
        phi_psi_data = extract_phi_psi(structure, args.chain_id)
        write_to_csv(phi_psi_data, output_filename)
        print(f"Phi-Psi angles and ABEGO classification written to {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
