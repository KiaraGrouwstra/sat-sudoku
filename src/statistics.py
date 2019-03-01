import os
import pandas as pd
from scipy.stats import mannwhitneyu

csv_file = os.path.join(os.getcwd(), 'data', 'metrics.csv')
df = pd.read_csv(csv_file)
df = df[df['splits'] != 0]

# ditch badly performing heuristics
df = df[df['alg'].map(lambda x: x not in [
    'DSCS',
    'FOM',
    'BOHM',
])]

a = df[df.fancy_beliefs == False]
b = df[df.fancy_beliefs]

metrics = {
    'splits': 'greater',
    'backtracks': 'less',
    'secs': 'greater',
}

def check_significance(df, metric):
    a = df[df.fancy_beliefs == False]
    b = df[df.fancy_beliefs]
    stat, p = mannwhitneyu(a[metric], b[metric], alternative=kind)
    return p

for metric, kind in metrics.items():
    print(metric)
    print('mean')
    print(a
        .groupby(['alg'])
        [metric].mean())
    print(b
        .groupby(['alg'])
        [metric].mean())
    print('min')
    print(a
        # .groupby(['alg'])
        [metric].min())
    print(b
        # .groupby(['alg'])
        [metric].min())
    print('max')
    print(a
        # .groupby(['alg'])
        [metric].max())
    print(b
        # .groupby(['alg'])
        [metric].max())
    print('p-value')
    print(df
        .groupby(['alg'])
        .apply(check_significance, metric))
