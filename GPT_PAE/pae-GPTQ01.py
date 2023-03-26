import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = '''
i j aa_i aa_j p(cbcb<8) maxdistbin pae_ij pae_ji
1 2 D S 0.999 5.12 1.349 1.319
1 3 D Q 0.946 7.31 2.918 3.042
1 4 D E 0.818 5.75 4.570 3.632
1 5 D N 0.851 6.06 3.203 2.435
1 6 D G 0.138 9.50 4.335 2.606
1 7 D V 0.033 10.75 7.324 3.632
1 8 D R 0.015 10.44 7.628 3.035
1 9 D L 0.013 12.31 8.223 3.078
1 10 D V 0.004 15.12 10.855 3.245
1 11 D H 0.001 15.75 13.483 3.033
'''

# データをデータフレームに読み込みます。
df = pd.read_csv(pd.StringIO(data), delimiter=' ')

# iとjの軸でピボットし、pae_ijを値とするヒートマップ用のデータフレームを作成します。
heatmap_df = df.pivot("i", "j", "pae_ij")

# ヒートマップを描画します。
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_df, annot=True, fmt='.3f', cmap='coolwarm', linewidths=0.5, square=True)
plt.title('2D Heatmap of pae_ij')
plt.show()