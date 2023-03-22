# GPT4PDB 
# -PDB treatment programs by ChatGPT-

誤ってChatGPTとのやり取りをgithubのレポジトリごと消去してしまった為、
修正お待ちください。



---

#GPT_Altloc/Altloc_GPT_Q05.py

---
markdown
Copy code
# Alternative location picker

This Python script processes PDB (Protein Data Bank) files by filtering and optionally modifying alternative location (the 17th character) of each line.

## Features

- Filters lines based on alternative location (the 17th character or ATOM).
- Option to replace the 17th character with a space.
- Supports both ATOM and HETATM records.

## Usage

```sh
python script.py input.pdb output.pdb [options]
```

## Options
- -s CHAR, --specified_char CHAR: The specified character to filter on. If not provided, the script will process lines with a space as the 17th character.
- -r, --replace_17th_char: Replace the 17th character with a space.

## Examples
Process a PDB file, keeping only lines with a space as alternative location (the 17th character):

```sh
python Altloc_GPT_Q05.py input.pdb output.pdb
```
Process a PDB file, keeping only lines with "A" as the alternative location (17th character) and replacing the 17th character with a space:


```sh
python Altloc_GPT_Q05.py input.pdb output.pdb -s A -r
```


## License
This project is licensed under the MIT License.

---

#GPT_Rama/OCNHdiGPT4_Q27.py

---

# O-C-N-H Dihedral Angle Calculator

This is a Python script that calculates the dihedral angles between consecutive amino acid residues in a protein structure. The script reads a PDB file, extracts the O-C-N-H dihedral angles for each consecutive pair of residues in a specified chain, and writes the results to a CSV file.

## Requirements
Python 3.7+
Biopython

## Installation
Install Biopython using pip:
```
pip install biopython
```
Download the ocnh_dihedral_calculator.py script from this repository.

## Usage
To use the OCNH Dihedral Angle Calculator, run the script from the command line with the following syntax:
```
python ocnh_dihedral_calculator.py pdb_file chain_id [-a altloc] [-o output]
```

## Arguments
- pdb_file: Path to the PDB file.
- chain_id: Chain ID to process.
- -a, --altloc: (Optional) Alternate conformation ID. Leave blank for default.
- -o, --output: (Optional) Output CSV file name. If not specified, the output file will be named based on the input PDB file.

## Example
```
python ocnh_dihedral_calculator.py example.pdb A -a A -o output.csv
```
This command will process the PDB file example.pdb, calculate the O-C-N-H dihedral angles for chain A, and write the results to output.csv.

## Known Limitations
The script assumes that the input PDB file has a standard naming convention for atom names and residue names.
The script may not handle non-standard amino acids or non-standard atom names correctly.

## License
This project is licensed under the MIT License.

---

GPT_ABEGO/abegoGPT4_Q06.py

---

# ABEGO Calculator

A Python script to calculate Phi-Psi angles and classify the ABEGO region of protein residues from a PDB file.

## Description
The abegoGPT4_Q06.py script processes a given PDB file and extracts the Phi-Psi angles for each amino acid residue in the specified chain. It then classifies the ABEGO region for each residue based on the calculated angles and writes the results to a CSV file.

## Dependencies
-Python 3.6 or later
-Biopython

## Installation
1. Install Python 3.6 or later if you haven't already.
2. Install Biopython using pip:

```
pip3 install biopython
```

## Usage

```
python abegoGPT4_Q06.py <pdb_file> <chain_id> [-o <output_csv>]
```

## Arguments
- <pdb_file>: The path to the input PDB file.
- <chain_id>: The chain ID to process.
- -o, --output (optional): The output CSV file name. If not specified, the output file will be named based on the input PDB file.

## Example
```
python abegoGPT4_Q06.py example.pdb A -o example_A_phi_psi_abego.csv
```

This command processes the example.pdb file, extracts the Phi-Psi angles and ABEGO classification for chain A, and writes the results to example_A_phi_psi_abego.csv.

## License
This project is licensed under the MIT License.

