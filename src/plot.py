import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_file = os.path.join(os.getcwd(), 'data', 'metrics.csv')
df = pd.read_csv(csv_file)
df = df[df['splits'] != 0]
df['type'] = df['inputfile'].map(lambda s: s.split(os.path.sep)[-2])
df = df[df['type'] != 'dimacs']
df['smart_ratio'] = df.apply(lambda x: 1 - x['backtracks'] / x['splits'], axis=1)
# df['split_to_backtrack'] = df.apply(lambda x: x['splits'] / x['backtracks'])

# ditch badly performing heuristics
df = df[df['alg'].map(lambda x: x not in [
    'DSCS',
    'FOM',
    'BOHM',
])]

a = df[df.fancy_beliefs == False]
b = df[df.fancy_beliefs]

plot_types = [
    # 'point',
    # 'bar',
    # 'strip',
    # 'swarm',  # does not terminate
    # 'box',  # grey version of boxen
    'violin',
    # 'boxen',
]

metrics = {
    # 'solved': 'whether a solution was found (True is better)',
    # 'assigned': 'number of assigned variables (higher is better)',
    'backtracks': 'number of backtracks (lower is better)',  # algorithm quality (more so than splits), problem difficulty
    'splits': 'number of splits (lower is better)',  # algorithm quality, problem difficulty (more so than backtracks)
    # 'smart_ratio': '1 - backtracks / splits: ratio of decisions that lead to a solution',  # algorithm quality
    'secs': 'seconds taken to solution (lower is better)',  # machine/implementation quality, algorithm quality, problem difficulty
    # 'pure_applied': 'number of times the pure literal rule was used',
    # 'unit_applied': 'number of times the unit clause rule was used',  # not enough data after removing outliers
}

sns.set_palette('pastel')
for plot_type in plot_types:
    print(plot_type)

    for metric, title in metrics.items():
        print(metric)
        # log_metric = f'log_{metric}'
        # df[log_metric] = df[metric].map(np.log10)

        df_ = df
        x = df[metric]
        df_ = df[x.between(x.quantile(.025), x.quantile(.975))]

        plot = sns.catplot(
            hue='fancy_beliefs',
            # x='fancy_beliefs',
            x='alg',
            y=metric,
            # y=log_metric,
            # row='type',
            # col='fancy_beliefs',
            # col_wrap=4,
            # data=df,
            data=df_,
            kind=plot_type,
            split=True,
        )

        # # title stuff
        # plt.subplots_adjust(top=0.8)
        # fig_title = title
        # # fig_title = f'log10 {title}'
        # plt.suptitle(fig_title, fontsize=28)

        fig_name = f'{metric}.png'
        # fig_name = f'{metric}-{plot_type}.png'
        fig_path = os.path.join(os.getcwd(), 'results', fig_name)
        plot.savefig(fig_path)
