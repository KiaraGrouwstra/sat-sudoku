import os
import pandas as pd

csv_file = os.path.join(os.getcwd(), 'data', 'metrics.csv')
df = pd.read_csv(csv_file)
df = df[df['splits'] == 0]
for fname in set(df['inputfile'].tolist()):
    os.remove(fname)
