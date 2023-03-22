# GPT4PDB 
# -PDB treatment programs by ChatGPT-

誤ってChatGPTとのやり取りをgithubのレポジトリごと消去してしまった為、
修正お待ちください。



---

#GPT_Altloc/Altloc_GPT_Q04.py

---
markdown
Copy code
# PDB File Processor

This Python script processes PDB (Protein Data Bank) files by filtering and optionally modifying the 17th character of each line.

## Features

- Filters lines based on the 17th character.
- Option to replace the 17th character with a space.
- Supports both ATOM and HETATM records.

## Usage

```sh
python script.py input.pdb output.pdb [options]
```

Options
-s CHAR, --specified_char CHAR: The specified character to filter on. If not provided, the script will process lines with a space as the 17th character.
-r, --replace_17th_char: Replace the 17th character with a space.
Examples
Process a PDB file, keeping only lines with a space as the 17th character:

```sh
python script.py input.pdb output.pdb
```
Process a PDB file, keeping only lines with "A" as the 17th character and replacing the 17th character with a space:


```sh
python script.py input.pdb output.pdb -s A -r
```

---



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
pdb_file: Path to the PDB file.
chain_id: Chain ID to process.
-a, --altloc: (Optional) Alternate conformation ID. Leave blank for default.
-o, --output: (Optional) Output CSV file name. If not specified, the output file will be named based on the input PDB file.

## Example
```
python ocnh_dihedral_calculator.py example.pdb A -a A -o output.csv
```
This command will process the PDB file example.pdb, calculate the O-C-N-H dihedral angles for chain A, and write the results to output.csv.

## Known Limitations
The script assumes that the input PDB file has a standard naming convention for atom names and residue names.
The script may not handle non-standard amino acids or non-standard atom names correctly.
