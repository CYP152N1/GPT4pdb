import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def draw_heatmap(file_path):
    try:
        # テキストファイルからデータをデータフレームに読み込みます。
        df = pd.read_csv(file_path, delimiter='\t')
        print("Dataframe loaded:")
        print(df.head())

        # iとjの軸でピボットし、pae_ijを値とするヒートマップ用のデータフレームを作成します。
        heatmap_df = df.pivot(index="i", columns="j", values="pae_ij")
        print("Heatmap dataframe created:")
        print(heatmap_df.head())

        # ヒートマップを描画します。
        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_df, annot=True, fmt='.3f', cmap='coolwarm', linewidths=0.5, square=True)
        plt.title('2D Heatmap of pae_ij')
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Draw a 2D heatmap from a text file.')
    parser.add_argument('file_path', type=str, help='Path to the input text file')

    args = parser.parse_args()

    draw_heatmap(args.file_path)
