import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def draw_heatmap(file_path, cmap='bwr', csv_output=None, threshold=None):  # Add 'threshold' argument
    try:
        # テキストファイルからデータをデータフレームに読み込みます。
        df = pd.read_csv(file_path, delimiter='\t')
        print("Dataframe loaded:")
        print(df.head())
        maxi=df['i'].max()+1

        if threshold is not None:
            filtered_df = df[(df['i'] < threshold) & (df['j'] > threshold)]
            avg_pae_ij = filtered_df['pae_ij'].mean()
            avg_pae_ji = filtered_df['pae_ji'].mean()
            sum_p_cbcb = filtered_df['p(cbcb<8)'].sum()
            sum_p_cbcb_div_threshold = sum_p_cbcb / threshold
            sum_p_cbcb_div_i_max_minus_threshold = sum_p_cbcb / (maxi-threshold)

            print(f"Average pae_ij for i < {threshold} and j > {threshold}: {avg_pae_ij}")
            print(f"Average pae_ji for i < {threshold} and j > {threshold}: {avg_pae_ji}")
            print(f"Sum p(cbcb<8) / threshold for i < {threshold} and j > {threshold}: {sum_p_cbcb_div_threshold}")
            print(f"Sum p(cbcb<8) / (i_max - threshold) for i < {threshold} and j > {threshold}: {sum_p_cbcb_div_i_max_minus_threshold}")
            print(maxi)

        if threshold is not None:
            filtered_df = df[(df['i'] < threshold) & (df['j'] > threshold)]
            i_mean_values = filtered_df.groupby('i')['p(cbcb<8)'].sum()
            j_mean_values = filtered_df.groupby('j')['p(cbcb<8)'].sum()

            plt.figure(figsize=(10, 6))
            i_mean_values.plot(kind='bar')
            plt.xlabel('i')
            plt.ylabel('Sum p(cbcb<8)')
            plt.title('Sum p(cbcb<8) for i < threshold and j > threshold (Grouped by i)')
            plt.savefig('i_sum_bar.png')
            plt.show()

            plt.figure(figsize=(10, 6))
            j_mean_values.plot(kind='bar')
            plt.xlabel('j')
            plt.ylabel('Sum p(cbcb<8)')
            plt.title('Sum p(cbcb<8) for i < threshold and j > threshold (Grouped by j)')
            plt.savefig('j_sum_bar.png')
            plt.show()

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
    parser.add_argument('--csv_output', type=str, help='Output CSV file for the combined heatmap dataframe')
    parser.add_argument('--threshold', type=int, help='Threshold value for calculating average values')  # Add 'threshold' argument

    args = parser.parse_args()

    draw_heatmap(args.file_path, args.cmap, args.csv_output, args.threshold)  # Pass 'args.threshold' to the 'draw_heatmap' function
