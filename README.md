# GPT4PDB 
# -PDB treatment programs by ChatGPT-

ChatGPTとのやり取りの一部はmarkdown形式で保存されております。

- GPT_Altloc

特定のAlthernative conformationだけを取得する。（依頼作成）

- GPT_OCNH

ωの代わりに、O-Cα-N-Hの二面角をリストアップする。（依頼作成）

- GPT_ABEGO

入力した構造のφ,ψの二面角からABEGOを調べる。

- GPT_pae

colabfoldのalphafold_advancedのログからPAEを描画する。

- GPT_PostVina

AutoDock Vinaの出力から、近接したアミノ酸を割り出すソフト。（依頼作成）


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

#GPT_OCNH/OCNHdiGPT4_Q27.py

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

---

GPT_pae/pae-GPTQ21.py

---

# 2D Heatmap Generator

This Python script generates a 2D heatmap from a tab-delimited text file containing `i`, `j`, `pae_ij`, and `pae_ji` values. The generated heatmap uses the combined values of `pae_ij` and `pae_ji` and supports custom color maps.

## Requirements

- Python 3.6+
- pandas
- seaborn
- matplotlib

You can install the required packages using the following command:

```
pip install pandas seaborn matplotlib
```

## Usage

```
python pae-GPTQ21.py <file_path> [--cmap <color_map>]
```

- `<file_path>`: The path to the input text file (required).
- `<color_map>`: The color map for the heatmap (optional, default: 'bwr').

The input text file should be tab-delimited and contain the following columns: `i`, `j`, `pae_ij`, and `pae_ji`.

## Example

```
python pae-GPTQ21.py input_file.txt --cmap coolwarm
```

This command will generate a 2D heatmap using the 'coolwarm' color map from the data in `input_file.txt`.

## License

This project is licensed under the [MIT License](LICENSE).

---

GPT_PostVina/PostVina-GPT_Q47.py

---

# Nearby Residues Finder
This Python script analyzes PDB and PDBQT files to find nearby residues within a specified distance threshold. It generates a CSV file with a list of nearby residues, a stacked bar chart in PNG format showing the score of nearby residues per residue number, and another CSV file with counts of nearby residues.
## Dependencies
- Python 3.6+
- matplotlib

## Installation
1. Clone the repository or download the script.
2. Install the required dependencies using pip:


```
pip install matplotlib

```
## Usage
```
python nearby_residues_finder.py PDB_FILE PDBQT_FILE OUTPUT_PREFIX [-t THRESHOLD]

```

- `PDB_FILE`: Path to the input PDB file.
- `PDBQT_FILE`: Path to the input PDBQT file.
- `OUTPUT_PREFIX`: Prefix for output files. The script will generate files with the following names: `&lt;OUTPUT_PREFIX&gt;_list.csv`, `&lt;OUTPUT_PREFIX&gt;_count.csv`, and `&lt;OUTPUT_PREFIX&gt;.png`.
- `-t THRESHOLD`: (Optional) Distance threshold for nearby residues. Default value is 5.0.

### Example
```
python nearby_residues_finder.py input.pdb input.pdbqt output -t 5.0

```

This will generate three output files:

- `output_list.csv`: List of nearby residues.
- `output_count.csv`: Counts of nearby residues.
- `output.png`: Stacked bar chart showing the score of nearby residues per residue number.

## Functions
- `parse_pdb(file_path)`: Parses a PDB file and returns a list of atom information.
- `parse_pdbqt(file_path)`: Parses a PDBQT file and returns a list of models.
- `calculate_distance(coord1, coord2)`: Calculates the Euclidean distance between two coordinates.
- `find_nearby_residues(pdb_data, pdbqt_models, threshold)`: Finds nearby residues within the specified threshold.
- `create_stacked_bar_chart(nearby_residues_list, output_image, threshold)`: Generates a stacked bar chart of the score of nearby residues per residue number.

## Score of Nearby Residues
The script calculates a score for each residue based on its proximity to the residues in the PDBQT models. The score is a linear function of the distance between the residues, with a value of 1 when the distance is 0, and 0 when the distance is equal to the specified threshold. The score for a residue is the sum of the scores for all the models in which it is nearby.

The stacked bar chart visualizes the score of nearby residues per residue number. Each bar represents a residue and is divided into segments, with each segment corresponding to a PDBQT model. The height of the segment indicates the score of the residue in that model. Residue numbers are displayed at the top of each bar, and the legend shows the correspondence between the colors of the segments and the PDBQT models.

To make it easier to read the chart, the vertical axis has a maximum value 10% higher than the maximum score, and the residue numbers are displayed on the horizontal axis without overlapping. The score of nearby residues can help to identify residues that are consistently near the residues in the PDBQT models, indicating potential interactions or binding sites.

## License
This project is open source and available under the <a href="LICENSE" target="_new">MIT License</a>.

--

# PDBQT Nearby Residues Analyzer

このプログラムは、PDBQTファイル内のモデルとPDBファイル内の構造の間の近接残基を検索し、それらをCSVファイルおよびスタックバーのグラフに出力します。

## 必要条件

- Python 3.6以上
- matplotlibライブラリ

## 使い方

1. 必要なライブラリをインストールします。


```

pip install matplotlib

```

2. スクリプトを実行します。以下のコマンド例では、入力ファイルとして`input.pdb`および`input.pdbqt`を指定し、出力CSVファイルとして`output.csv`を指定します。また、距離の閾値はデフォルトの5.0Åとしています。


```

python pdbqt_nearby_residues_analyzer.py input.pdb input.pdbqt output

```

3. スクリプトが正常に実行されると、以下のファイルが生成されます。

- `output_list.csv`: 各近接残基の詳細情報が含まれています。
- `output_count.csv`: 各残基番号に対する近接残基の数が含まれています。
- `output.png`: 各残基番号に対する近接残基の数を示すスタックバーのグラフが表示されます。

## コマンドラインオプション

- `-t`, `--threshold`: 近接残基を検出するための距離の閾値を指定します（デフォルト: 5.0）。

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下でライセンスされています。
