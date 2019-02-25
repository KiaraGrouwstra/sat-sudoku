import os
import pandas as pd
import seaborn as sns

csv_file = os.path.join(os.getcwd(), 'data', 'metrics.csv')
df = pd.read_csv(csv_file)
x = 'givens'
y = 'secs'
hue = 'alg'
f_plot = sns.barplot(x=x, y=y, hue=hue, data=df)
# f_plot = titleNAxis(f_plot, title, label_i, label_j)
fig_name = 'foo'
fig_path = os.path.join(os.getcwd(), 'results' , fig_name + '.png')
path = f_plot.get_figure().savefig(fig_path)
print(path)
