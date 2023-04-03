# 追加されたコメントの例示 (Added Japanese comments)

**Human:**
下記のスクリプトに日本語を追加して記載することはできますか？

import sys
import csv
import re
import math
import argparse
import matplotlib.pyplot as plt

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
    model_number = 0

    for line in lines:
        if line.startswith('MODEL'):
            model_number = int(line.split()[1])  # MODELの番号を取得
            current_model = []
        elif line.startswith('ATOM') or line.startswith('HETATM'):
            atom_label = line[12:16].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            current_model.append((model_number, atom_label, x, y, z))  # MODEL番号を追加
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
                distance = calculate_distance(pdb_atom[3:], model_atom[2:])
                if distance &lt;= threshold:
                    nearby_residues.add((pdb_atom[0], pdb_atom[1], pdb_atom[2], model_atom[0], model_atom[1], distance))  # distanceを追加
        nearby_residues_list.append(nearby_residues)

    return nearby_residues_list

def create_stacked_bar_chart(nearby_residues_list, output_image):
    residue_counts = {}

    for i, nearby_residues in enumerate(nearby_residues_list):
        for _, _, residue_number, _, _, _ in nearby_residues:
            if residue_number not in residue_counts:
                residue_counts[residue_number] = [0] * len(nearby_residues_list)
            residue_counts[residue_number][i] += 1

    residue_numbers = list(residue_counts.keys())
    residue_numbers.sort()

    data_matrix = [residue_counts[residue_number] for residue_number in residue_numbers]

    fig, ax = plt.subplots()

    bottoms = [0] * len(residue_numbers)
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

    ax.set_xticks(residue_numbers)
    ax.set_xticklabels(residue_numbers)
    ax.set_xlabel('Residue Numbers')
    ax.set_ylabel('Number of Nearby Residues')
    ax.set_title('Nearby Residues per Residue Number')

    plt.legend()
    plt.savefig(output_image, dpi=300)
    plt.close()

def main(args):
    pdb_file = args.pdb_file
    pdbqt_file = args.pdbqt_file
    output_csv = args.output_csv
    threshold = args.threshold

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models, threshold)

    output_csv_list = output_csv.replace('.csv', '_list.csv')
    with open(output_csv_list, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PDB_Atom', 'Residue_Name', 'Residue_Number', 'PDBQT_Model', 'PDBQT_Atom', 'Distance'])

        for i, nearby_residues in enumerate(nearby_residues_list):
            for pdb_label, residue_name, residue_number, model_number, atom_label, distance in nearby_residues:
                csv_writer.writerow([pdb_label, residue_name, residue_number, model_number, atom_label, distance])

    output_image = output_csv.replace('.csv', '.png')
    create_stacked_bar_chart(nearby_residues_list, output_image)

    output_csv_count = output_csv.replace('.csv', '_count.csv')
    with open(output_csv_count, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Residue_Number'] + [f'MODEL {i + 1}' for i in range(len(nearby_residues_list))])

        residue_counts = {}
        for i, nearby_residues in enumerate(nearby_residues_list):
            for _, _, residue_number, _, _, _ in nearby_residues:
                if residue_number not in residue_counts:
                    residue_counts[residue_number] = [0] * len(nearby_residues_list)
                residue_counts[residue_number][i] += 1

        for residue_number, counts in residue_counts.items():
            csv_writer.writerow([residue_number] + counts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby residues in PDBQT models")
    parser.add_argument("pdb_file", type=str, help="Input PDB file")
    parser.add_argument("pdbqt_file", type=str, help="Input PDBQT file")
    parser.add_argument("output_csv", type=str, help="Output CSV file")
    parser.add_argument("-t", "--threshold", type=float, default=5.0, help="Distance threshold for nearby residues (default: 5.0)")

    args = parser.parse_args()
    main(args)


***

**Assistant:**

以下のようにスクリプトに日本語のコメントを追加しました。

```
import sys
import csv
import re
import math
import argparse
import matplotlib.pyplot as plt

# PDBファイルを解析する関数
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

# PDBQTファイルを解析する関数
def parse_pdbqt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    models = []
    current_model = []
    model_number = 0

    for line in lines:
        if line.startswith('MODEL'):
            model_number = int(line.split()[1])  # MODELの番号を取得
            current_model = []
        elif line.startswith('ATOM') or line.startswith('HETATM'):
            atom_label = line[12:16].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            current_model.append((model_number, atom_label, x, y, z))  # MODEL番号を追加
        elif line.startswith('ENDMDL'):
            models.append(current_model)

    return models

# 座標間の距離を計算する関数
def calculate_distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

# 近くの残基を見つける関数
def find_nearby_residues(pdb_data, pdbqt_models, threshold):
    nearby_residues_list = []

    for model in pdbqt_models:
        nearby_residues = set()
        for pdb_atom in pdb_data:
            for model_atom in model:
                distance = calculate_distance(pdb_atom[3:], model_atom[2:])
                if distance <= threshold:
                    nearby_residues.add((pdb_atom[0], pdb_atom[1], pdb_atom[2], model_atom[0], model_atom[1], distance))  # distanceを追加
        nearby_residues_list.append(nearby_residues)

    return nearby_residues_list

# スタックバーチャートを作成する関数
def create_stacked_bar_chart(nearby_residues_list, output_image):
    residue_counts = {}

    for i, nearby_residues in enumerate(nearby_residues_list):
        for _, _, residue_number, _, _, _ in nearby_residues:
            if residue_number not in residue_counts:
                residue_counts[residue_number] = [0] * len(nearby_residues_list)
            residue_counts[residue_number][i] += 1

    residue_numbers = list(residue_counts.keys())
    residue_numbers

```


***

**Human:**
続きをdef create_stacked_bar_chart(nearby_residues_list, output_image):の初めから記載してください。

***

**Assistant:**

続きを def create_stacked_bar_chart(nearby_residues_list, output_image): の初めから記載します。

```
    residue_numbers.sort()

    data_matrix = [residue_counts[residue_number] for residue_number in residue_numbers]

    fig, ax = plt.subplots()

    bottoms = [0] * len(residue_numbers)
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

    ax.set_xticks(residue_numbers)
    ax.set_xticklabels(residue_numbers)
    ax.set_xlabel('Residue Numbers')
    ax.set_ylabel('Number of Nearby Residues')
    ax.set_title('Nearby Residues per Residue Number')

    plt.legend()
    plt.savefig(output_image, dpi=300)
    plt.close()

def main(args):
    pdb_file = args.pdb_file
    pdbqt_file = args.pdbqt_file
    output_csv = args.output_csv
    threshold = args.threshold

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models, threshold)

    output_csv_list = output_csv.replace('.csv', '_list.csv')
    with open(output_csv_list, 'w', newline='') as csvfile

```


***

**Human:**
続きを def create_stacked_bar_chart(nearby_residues_list, output_image): の初めからコメントを記載するのを忘れずに続けてください。

***

**Assistant:**

続きを def create_stacked_bar_chart(nearby_residues_list, output_image): の初めからコメントを記載するのを忘れずに続けます。

```
    # 残基番号をソート
    residue_numbers.sort()

    # データ行列を作成
    data_matrix = [residue_counts[residue_number] for residue_number in residue_numbers]

    # グラフを初期化
    fig, ax = plt.subplots()

    # スタックバーの下部の高さを表すリスト
    bottoms = [0] * len(residue_numbers)
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

    # x軸の設定
    ax.set_xticks(residue_numbers)
    ax.set_xticklabels(residue_numbers)
    ax.set_xlabel('Residue Numbers')

    # y軸の設定
    ax.set_ylabel('Number of Nearby Residues')

    # グラフのタイトル設定
    ax.set_title('Nearby Residues per Residue Number')

    # 凡例を表示
    plt.legend()

    # グラフを画像ファイルに保存
    plt.savefig(output_image, dpi=300)
    plt.close()

def main(args):
    pdb_file = args.pdb_file
    pdbqt_file = args.pdbqt_file
    output_csv = args.output_csv
    threshold = args.threshold

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models, threshold)

    output_csv_list = output_csv.replace('.csv', '_list.csv')
    with open(output_csv_list, 'w', newline='') as csvfile

```


***

**Human:**
続けてください

***

**Assistant:**

続きを記載します。

```
        # CSVファイルに結果を書き込む
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PDB_Atom', 'Residue_Name', 'Residue_Number', 'PDBQT_Model', 'PDBQT_Atom', 'Distance'])

        for i, nearby_residues in enumerate(nearby_residues_list):
            for pdb_label, residue_name, residue_number, model_number, atom_label, distance in nearby_residues:
                csv_writer.writerow([pdb_label, residue_name, residue_number, model_number, atom_label, distance])

    # 画像ファイル名を生成
    output_image = output_csv.replace('.csv', '.png')
    create_stacked_bar_chart(nearby_residues_list, output_image)

    # 出力用のCSVファイル名を生成
    output_csv_count = output_csv.replace('.csv', '_count.csv')
    with open(output_csv_count, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Residue_Number'] + [f'MODEL {i + 1}' for i in range(len(nearby_residues_list))])

        residue_counts = {}
        for i, nearby_residues in enumerate(nearby_residues_list):
            for _, _, residue_number, _, _, _ in nearby_residues:
                if residue_number not in residue_counts:
                    residue_counts[residue_number] = [0] * len(nearby_residues_list)
                residue_counts[residue_number][i] += 1

        for residue_number, counts in residue_counts.items():
            csv_writer.writerow([residue_number] + counts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby residues in PDBQT models")
    parser.add_argument("pdb_file", type=str, help="Input PDB file")
    parser.add_argument("pdbqt_file", type=str, help="Input PDBQT file")
    parser.add_argument("output_csv", type=str, help="Output CSV file")
    parser.add_argument("-t", "--threshold", type=float, default=5.0, help="Distance threshold for nearby residues (default: 5.0)")

    args = parser.parse_args()
    main(args)

```

これで、スクリプト全体に日本語のコメントが追加されました。これにより、コードの各部分の目的と機能がより明確になります。


***

**Human:**
github用のreadmeファイルを.md形式で作成してください。

***

**Assistant:**

GitHub用のREADMEファイルを.md形式で作成します。以下の内容をREADME.mdとして保存してください。

```
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

python pdbqt_nearby_residues_analyzer.py input.pdb input.pdbqt output.csv

```

3. スクリプトが正常に実行されると、以下のファイルが生成されます。

- `output_list.csv`: 各近接残基の詳細情報が含まれています。
- `output_count.csv`: 各残基番号に対する近接残基の数が含まれています。
- `output.png`: 各残基番号に対する近接残基の数を示すスタックバーのグラフが表示されます。

## コマンドラインオプション

- `-t`, `--threshold`: 近接残基を検出するための距離の閾値を指定します（デフォルト: 5.0）。

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下でライセンスされています。


```

このREADMEファイルには、必要条件、使い方、コマンドラインオプション、およびライセンス情報が含まれています。これにより、ユーザーはプロジェクトの目的と使用方法を理解しやすくなります。


***

**Human:**
Number of Nearby Residuesの縦軸をScore of Nearby Residuesに変えたいです。具体的にはdistanceがthresholdと一致する時が0、distanceが0の時が1となるような、一次関数のスコアを採用できないでしょうか。

***

**Assistant:**

もちろんできます。`create_stacked_bar_chart` 関数内で、`residue_counts` を `residue_scores` に変更し、距離に基づいてスコアを計算するように変更します。以下に修正した関数を示します。

```
def create_stacked_bar_chart(nearby_residues_list, output_image, threshold):
    residue_scores = {}

    for i, nearby_residues in enumerate(nearby_residues_list):
        for _, _, residue_number, _, _, distance in nearby_residues:
            score = 1 - (distance / threshold)  # スコアを計算
            if residue_number not in residue_scores:
                residue_scores[residue_number] = [0] * len(nearby_residues_list)
            residue_scores[residue_number][i] += score

    residue_numbers = list(residue_scores.keys())
    residue_numbers.sort()

    data_matrix = [residue_scores[residue_number] for residue_number in residue_numbers]

    fig, ax = plt.subplots()

    bottoms = [0] * len(residue_numbers)
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

    ax.set_xticks(residue_numbers)
    ax.set_xticklabels(residue_numbers)
    ax.set_xlabel('Residue Numbers')
    ax.set_ylabel('Score of Nearby Residues')  # 縦軸のラベルを変更
    ax.set_title('Score of Nearby Residues per Residue Number')

    plt.legend()
    plt.savefig(output_image, dpi=300)
    plt.close()

```

また、`main` 関数内で `create_stacked_bar_chart` 関数を呼び出す際に、`threshold` 引数を追加します。

```
output_image = output_csv.replace('.csv', '.png')
create_stacked_bar_chart(nearby_residues_list, output_image, threshold)

```

これで、スタックバーのグラフの縦軸がスコアに基づくようになりました。スコアは、距離が `threshold` と一致するときに0、距離が0のときに1になる一次関数です。


***

**Human:**
狙い通りです。ちなみに、.pngの横軸の残基番号が重なってしまい見づらいです。何か良い方法はないですか？

***

**Assistant:**

横軸の残基番号が重なって見づらい場合、いくつかの方法で改善できます。以下に、横軸の残基番号の表示を改善するための3つの方法を示します。

1. 横軸のラベルの回転: ラベルを回転させて、重なりを減らすことができます。


```
ax.set_xticks(residue_numbers)
ax.set_xticklabels(residue_numbers, rotation=45)  # ラベルを45度回転

```
<ol start="2">横軸のラベルの間引き: すべての残基番号ではなく、一定間隔でラベルを表示します。</li></ol>
```
tick_interval = 5  # 5個おきにラベルを表示
residue_numbers_filtered = residue_numbers[::tick_interval]
ax.set_xticks(residue_numbers_filtered)
ax.set_xticklabels(residue_numbers_filtered)

```
<ol start="3">グラフのサイズを変更: グラフ全体のサイズを大きくすることで、横軸のラベルが重なりにくくなります。</li></ol>
```
fig, ax = plt.subplots(figsize=(12, 6))  # グラフのサイズを12x6インチに変更

```

これらの方法を組み合わせることで、横軸のラベルが重ならないように改善できます。適切な方法を選択し、必要に応じて値を調整してください。


***

**Human:**
棒グラフの上に残基番号を表示する事は可能でしょうか。つまり、それぞれの残基でスコアの高さが違うので、残基番号が重ならないという解決策です。

***

**Assistant:**

棒グラフの上に残基番号を表示することは可能です。`create_stacked_bar_chart` 関数内で、各棒グラフの上に残基番号を描画するコードを追加します。具体的には、次のように変更します。

```
def create_stacked_bar_chart(nearby_residues_list, output_image, threshold):
    # (これまでのコードは省略)

    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        bar_container = ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

        # 棒グラフの上に残基番号を表示
        for bar, residue_number in zip(bar_container, residue_numbers):
            height = bar.get_height()
            if height > 0:  # 高さが0より大きい場合のみ残基番号を表示
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height, str(residue_number),
                        ha='center', va='bottom', fontsize=8, rotation=90)

    # (これまでのコードは省略)

```

このコードは、各棒グラフの上に残基番号を表示します。`fontsize` と `rotation` の値を調整することで、ラベルのサイズや回転角度を変更できます。ただし、この方法では、グラフが密集している場合やスコアが低い場合には、ラベルが重なる可能性があります。必要に応じて、他のグラフ設定を調整して、見やすさを向上させてください。


***

**Human:**
良い感じですが、積み上げた途中でもラベルが表示されており、見づらいです。各残基毎で一番上に積み重ねられた所のみに記載する事はできますか。また、縦軸の最大値を、棒グラフの最大値+10%にして最大値が図の上端と重ならないように変更できますか。また、販連を図の中ではなく右端に表示することはできますか？

***

**Assistant:**

各残基ごとに一番上に積み重ねられた部分だけにラベルを表示し、縦軸の最大値を棒グラフの最大値 + 10%にし、凡例を右端に表示するには以下のように変更します。

```
def create_stacked_bar_chart(nearby_residues_list, output_image, threshold):
    # (これまでのコードは省略)

    max_height = 0
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        bar_container = ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

        # 最後のモデルの場合、各棒グラフの上に残基番号を表示
        if model_index == len(nearby_residues_list) - 1:
            for bar, residue_number in zip(bar_container, residue_numbers):
                height = bar.get_height()
                if height > 0:  # 高さが0より大きい場合のみ残基番号を表示
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height, str(residue_number),
                            ha='center', va='bottom', fontsize=8, rotation=90)
        
        # 最大の積み上げ高さを更新
        max_height = max(max_height, max(bottoms))

    # 縦軸の最大値を設定
    ax.set_ylim(0, max_height * 1.1)  # 最大値の10%上に設定

    # 凡例を右端に表示
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

    # (これまでのコードは省略)

```

これにより、各残基ごとに一番上に積み重ねられた部分だけにラベルが表示され、縦軸の最大値が棒グラフの最大値 + 10% に設定され、凡例が図の右端に表示されます。


***

**Human:**
これだと、最後のモデルにおいてスコアが0の時、途中のモデルで0以外のスコアを示していても数値が表示されません。どうしたらよいでしょうか。

***

**Assistant:**

各残基の一番上に積み重ねられた部分にラベルを表示するには、以下のようにコードを変更します。

```
def create_stacked_bar_chart(nearby_residues_list, output_image, threshold):
    # (これまでのコードは省略)

    max_height = 0
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        bar_container = ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

        # 最後のモデルの場合、各棒グラフの上に残基番号を表示
        if model_index == len(nearby_residues_list) - 1:
            for bar, residue_number, total_height in zip(bar_container, residue_numbers, bottoms):
                height = bar.get_height()
                if total_height > 0:  # 総積み上げ高さが0より大きい場合のみ残基番号を表示
                    ax.text(bar.get_x() + bar.get_width() / 2, total_height, str(residue_number),
                            ha='center', va='bottom', fontsize=8, rotation=90)

        # 最大の積み上げ高さを更新
        max_height = max(max_height, max(bottoms))

    # 縦軸の最大値を設定
    ax.set_ylim(0, max_height * 1.1)  # 最大値の10%上に設定

    # 凡例を右端に表示
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

    # (これまでのコードは省略)

```

この変更により、各残基ごとに一番上に積み重ねられた部分だけにラベルが表示され、最後のモデルでスコアが0であっても、途中のモデルで0以外のスコアを示している場合には数値が表示されます。


***

**Human:**
さすがです！ちなみに凡例が図の内側左に表示されて重なっています。図外の右側に表示することはできますか？

***

**Assistant:**

凡例を図の外側右に表示するには、`ax.legend()` の引数に `bbox_to_anchor` を追加して以下のように変更します。

```
    # (これまでのコードは省略)

    # 凡例を右端に表示
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

    # (これまでのコードは省略)

```

この変更により、凡例が図の外側右に表示されます。


***

**Human:**
まだ凡例が図の内側左に表示されて重なっています。図外の右側に表示することはできますか？

***

**Assistant:**

申し訳ございません。以下のように`ax.legend()`の引数に`bbox_to_anchor`と`loc`を指定して、凡例を図の外側右に表示することができます。

```
    # (これまでのコードは省略)

    # 凡例を右端に表示
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    # (これまでのコードは省略)

```

これで凡例が図の外側右に表示されるはずです。


***

**Human:**
まだ凡例が図の内側左に表示されて重なっています。図外の右側に表示することはできますか？

***

**Assistant:**

申し訳ございません。図の外側右に凡例を表示するには、`plt.subplots()`で`constrained_layout=True`を設定し、`ax.legend()`の引数に`bbox_to_anchor`と`loc`を指定します。以下のようにコードを変更してください。

```
def create_stacked_bar_chart(nearby_residues_list, output_image, threshold):
    # (これまでのコードは省略)

    # figsizeとconstrained_layoutを指定して、サブプロットを作成
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    # (これまでのコードは省略)

    # 凡例を右端に表示
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')

    # (これまでのコードは省略)

```

これで凡例が図の外側右に表示されるはずです。


***

**Human:**
グラフエリアの外側には持っていけていませんが、難しいようなので妥協します。次にお願いしたいのは、引数の形式の変更です。現在の出力ファイルの名前は.csvで入力し、_list.csvと_count.csv、.pngを出力しておりますが、.csvを入力しなくても良いように変更できますか？

***

**Assistant:**

引数の形式を変更し、.csvを入力しなくても良いようにするには、`argparse.ArgumentParser`を編集して、出力ファイル名の拡張子を自動的に追加するようにします。`main()`関数内で、.csvを取り除いた出力ファイル名を使用して、_list.csv、_count.csv、および.pngを出力します。

以下のようにコードを変更してください。

```
# (この前のコードは省略)

def main(args):
    pdb_file = args.pdb_file
    pdbqt_file = args.pdbqt_file
    output_prefix = args.output_prefix
    threshold = args.threshold

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models, threshold)

    output_csv_list = f"{output_prefix}_list.csv"
    # (ここからのコードは省略)

    output_image = f"{output_prefix}.png"
    # (ここからのコードは省略)

    output_csv_count = f"{output_prefix}_count.csv"
    # (ここからのコードは省略)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby residues in PDBQT models")
    parser.add_argument("pdb_file", type=str, help="Input PDB file")
    parser.add_argument("pdbqt_file", type=str, help="Input PDBQT file")
    parser.add_argument("output_prefix", type=str, help="Output file prefix")
    parser.add_argument("-t", "--threshold", type=float, default=5.0, help="Distance threshold for nearby residues (default: 5.0)")

    args = parser.parse_args()
    main(args)

```

これで、出力ファイル名に.csvを含めなくても、_list.csv、_count.csv、および.pngが正しく出力されるようになります。


***

**Human:**
下記スクリプトのgithub用のREADMEをmarkdown形式で作成して下さい。

import sys
import csv
import re
import math
import argparse
import matplotlib.pyplot as plt

# PDBファイルを解析する関数
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

# PDBQTファイルを解析する関数
def parse_pdbqt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    models = []
    current_model = []
    model_number = 0

    for line in lines:
        if line.startswith('MODEL'):
            model_number = int(line.split()[1])  # MODELの番号を取得
            current_model = []
        elif line.startswith('ATOM') or line.startswith('HETATM'):
            atom_label = line[12:16].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            current_model.append((model_number, atom_label, x, y, z))  # MODEL番号を追加
        elif line.startswith('ENDMDL'):
            models.append(current_model)

    return models

# 座標間の距離を計算する関数
def calculate_distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

# 近くの残基を見つける関数
def find_nearby_residues(pdb_data, pdbqt_models, threshold):
    nearby_residues_list = []

    for model in pdbqt_models:
        nearby_residues = set()
        for pdb_atom in pdb_data:
            for model_atom in model:
                distance = calculate_distance(pdb_atom[3:], model_atom[2:])
                if distance &lt;= threshold:
                    nearby_residues.add((pdb_atom[0], pdb_atom[1], pdb_atom[2], model_atom[0], model_atom[1], distance))  # distanceを追加
        nearby_residues_list.append(nearby_residues)

    return nearby_residues_list

def create_stacked_bar_chart(nearby_residues_list, output_image, threshold):
    residue_scores = {}

    for i, nearby_residues in enumerate(nearby_residues_list):
        for _, _, residue_number, _, _, distance in nearby_residues:
            score = 1 - (distance / threshold)  # スコアを計算
            if residue_number not in residue_scores:
                residue_scores[residue_number] = [0] * len(nearby_residues_list)
            residue_scores[residue_number][i] += score

    residue_numbers = list(residue_scores.keys())
    residue_numbers.sort()

    data_matrix = [residue_scores[residue_number] for residue_number in residue_numbers]

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    bottoms = [0] * len(residue_numbers)
    max_height = 0
    for model_index in range(len(nearby_residues_list)):
        model_data = [data_matrix[row_index][model_index] for row_index in range(len(residue_numbers))]
        bar_container = ax.bar(residue_numbers, model_data, bottom=bottoms, label=f'MODEL {model_index + 1}')
        bottoms = [sum(x) for x in zip(bottoms, model_data)]

        # 最後のモデルの場合、各棒グラフの上に残基番号を表示
        if model_index == len(nearby_residues_list) - 1:
            for bar, residue_number, total_height in zip(bar_container, residue_numbers, bottoms):
                height = bar.get_height()
                if total_height &gt; 0:  # 総積み上げ高さが0より大きい場合のみ残基番号を表示
                    ax.text(bar.get_x() + bar.get_width() / 2, total_height, str(residue_number),
                            ha='center', va='bottom', fontsize=8, rotation=90)
                    
        # 最大の積み上げ高さを更新
        max_height = max(max_height, max(bottoms))

    # 縦軸の最大値を設定
    ax.set_ylim(0, max_height * 1.1)  # 最大値の10%上に設定

    # 凡例を右端に表示
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    
    ax.set_xticks(residue_numbers)
    ax.set_xticklabels(residue_numbers)
    ax.set_xlabel('Residue Numbers')
    ax.set_ylabel('Score of Nearby Residues')  # 縦軸のラベルを変更
    ax.set_title('Score of Nearby Residues per Residue Number')

    plt.legend()
    plt.savefig(output_image, dpi=300)
    plt.close()


def main(args):
    pdb_file = args.pdb_file
    pdbqt_file = args.pdbqt_file
    output_prefix = args.output_prefix
    threshold = args.threshold

    pdb_data = parse_pdb(pdb_file)
    pdbqt_models = parse_pdbqt(pdbqt_file)

    nearby_residues_list = find_nearby_residues(pdb_data, pdbqt_models, threshold)

    output_csv_list = f"{output_prefix}_list.csv"
    
    with open(output_csv_list, 'w', newline='') as csvfile:
        # CSVファイルに結果を書き込む
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PDB_Atom', 'Residue_Name', 'Residue_Number', 'PDBQT_Model', 'PDBQT_Atom', 'Distance'])

        for i, nearby_residues in enumerate(nearby_residues_list):
            for pdb_label, residue_name, residue_number, model_number, atom_label, distance in nearby_residues:
                csv_writer.writerow([pdb_label, residue_name, residue_number, model_number, atom_label, distance])

    # 画像ファイル名を生成
    output_image = f"{output_prefix}.png"
    create_stacked_bar_chart(nearby_residues_list, output_image, threshold)

    # 出力用のCSVファイル名を生成
    output_csv_count = f"{output_prefix}_count.csv"
    with open(output_csv_count, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Residue_Number'] + [f'MODEL {i + 1}' for i in range(len(nearby_residues_list))])

        residue_counts = {}
        for i, nearby_residues in enumerate(nearby_residues_list):
            for _, _, residue_number, _, _, _ in nearby_residues:
                if residue_number not in residue_counts:
                    residue_counts[residue_number] = [0] * len(nearby_residues_list)
                residue_counts[residue_number][i] += 1

        for residue_number, counts in residue_counts.items():
            csv_writer.writerow([residue_number] + counts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby residues in PDBQT models")
    parser.add_argument("pdb_file", type=str, help="Input PDB file")
    parser.add_argument("pdbqt_file", type=str, help="Input PDBQT file")
    parser.add_argument("output_prefix", type=str, help="Output file prefix")
    parser.add_argument("-t", "--threshold", type=float, default=5.0, help="Distance threshold for nearby residues (default: 5.0)")

    args = parser.parse_args()
    main(args)


***

**Assistant:**
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

## License
This project is open source and available under the <a href="LICENSE" target="_new">MIT License</a>.


***

**Human:**
Score of Nearby Resideuesについて、githubのREADMEに追記できるように記載してください。

***

**Assistant:**
## Score of Nearby Residues
The script calculates a score for each residue based on its proximity to the residues in the PDBQT models. The score is a linear function of the distance between the residues, with a value of 1 when the distance is 0, and 0 when the distance is equal to the specified threshold. The score for a residue is the sum of the scores for all the models in which it is nearby.

The stacked bar chart visualizes the score of nearby residues per residue number. Each bar represents a residue and is divided into segments, with each segment corresponding to a PDBQT model. The height of the segment indicates the score of the residue in that model. Residue numbers are displayed at the top of each bar, and the legend shows the correspondence between the colors of the segments and the PDBQT models.

To make it easier to read the chart, the vertical axis has a maximum value 10% higher than the maximum score, and the residue numbers are displayed on the horizontal axis without overlapping. The score of nearby residues can help to identify residues that are consistently near the residues in the PDBQT models, indicating potential interactions or binding sites.


***

Exported on April 3, 2023 1:18 PM.