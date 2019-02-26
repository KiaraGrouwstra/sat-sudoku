import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_file = os.path.join(os.getcwd(), 'data', 'metrics.csv')
df = pd.read_csv(csv_file)
df['type'] = df['inputfile'].map(lambda s: s.split(os.path.sep)[-2])

# 'categorical':
# 'alg',
# 'fancy_beliefs',
# 'type',

# features:
# # 'givens',

plot_types = [
    'point',
    'bar',
    'strip',
    'swarm',
    'box',
    'violin',
    'boxen',
]

metrics = {
    # 'solved': 'whether a solution was found (True is better)',
    # 'assigned': 'number of assigned variables (higher is better)',
    'backtracks': 'number of backtracks (lower is better)',
    'splits': 'number of splits (lower is better)',
    'secs': 'seconds taken to solution (lower is better)',
    'pure_applied': 'number of times the pure literal rule was used',
    'unit_applied': 'number of times the unit clause rule was used',
}

sns.set_palette('pastel')
for metric, title in metrics.items():
    print(metric)
    log_metric = f'log_{metric}'
    df[log_metric] = df[metric].map(np.log10)

    # for plot_type in plot_types:
    #     print(plot_type)

    plot = sns.catplot(
        x='alg',
        y=log_metric,
        # row='fancy_beliefs',
        col='type',
        col_wrap=3,
        # hue='',
        data=df,
        # kind=plot_type,
    )
    plt.subplots_adjust(top=0.9)
    plt.suptitle(title, fontsize=40)

    fig_name = f'{metric}-{plot_type}.png'
    fig_path = os.path.join(os.getcwd(), 'results', fig_name)
    plot.savefig(fig_path)
