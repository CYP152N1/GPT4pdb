import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def draw_heatmap(file_path, cmap='bwr', csv_output=None):  # Add 'csv_output' argument
    try:
        # テキストファイルからデータをデータフレームに読み込みます。
        df = pd.read_csv(file_path, delimiter='\t')
        print("Dataframe loaded:")
        print(df.head())

        # iとjの軸でピボットし、pae_ijとpae_jiを値とするヒートマップ用のデータフレームを作成します。
        heatmap_df_ij = df.pivot(index="i", columns="j", values="pae_ij")
        heatmap_df_ji = df.pivot(index="j", columns="i", values="pae_ji")

        # NaNを0に置き換えます。
        heatmap_df_ij.fillna(0, inplace=True)
        heatmap_df_ji.fillna(0, inplace=True)

        # インデックスと列を1から始めるように調整します。
        index_range = range(1, heatmap_df_ij.index.max()+1)
        column_range = range(1, heatmap_df_ij.columns.max()+1)
        heatmap_df_ij = heatmap_df_ij.reindex(index=index_range, columns=column_range, fill_value=0)
        index_range = range(1, heatmap_df_ji.index.max()+1)
        column_range = range(1, heatmap_df_ji.columns.max()+1)
        heatmap_df_ji = heatmap_df_ji.reindex(index=index_range, columns=column_range, fill_value=0)
        combined_heatmap_df = heatmap_df_ij.add(heatmap_df_ji)

        # Save combined heatmap dataframe to CSV if output filename is provided
        if csv_output:
            combined_heatmap_df.to_csv(csv_output)
            print(f"Combined heatmap dataframe saved to {csv_output}")
        
        print("Adjusted heatmap dataframe:")
        print(heatmap_df_ij.head())
        print(heatmap_df_ji.head())
        print(combined_heatmap_df.head())

        # ヒートマップを描画します。
        plt.figure(figsize=(10, 8))
        sns.heatmap(combined_heatmap_df, annot=False, fmt='.3f', cmap=cmap, linewidths=0, square=True, vmin=0, vmax=31)
        plt.title('2D Heatmap of pae_ij')
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Draw a 2D heatmap from a text file.')
    parser.add_argument('file_path', type=str, help='Path to the input text file')
    parser.add_argument('--cmap', type=str, default='bwr', help='Color map for the heatmap (default: bwr)')
    parser.add_argument('--csv_output', type=str, help='Output CSV file for the combined heatmap dataframe')  # Add 'csv_output' argument

    args = parser.parse_args()

    draw_heatmap(args.file_path, args.cmap, args.csv_output)  # Pass 'args.csv_output' to the 'draw_heatmap' function
