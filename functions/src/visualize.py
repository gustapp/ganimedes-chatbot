#%%
# CONSOLIDATE EXPERIMENT RESULTS
import pandas as pd
import numpy as np
import click

click.echo("Consolidating results...")
agg_metrics_df = pd.read_csv('./report/embedfs_evaluation_metrics.csv')
algo = 'PRED'

# Filter algo results
metrics_df = agg_metrics_df[(agg_metrics_df['algorithm'] == algo)] 

# Recall (fraction of recommendations explained)
unexplained_triples = metrics_df[metrics_df['explanation'].isnull()]

unexplained_n = len(unexplained_triples)
# total_n = len(concepts)*5
total_n = 100*5

# Considering the full search space
overall_recall = 1 - (unexplained_n/total_n)
click.echo(click.style('Overall Recall: {}'.format(overall_recall), fg='blue'))

#%%
# Recall x timeout constraint
timout_recall_curve = []
for i in np.linspace(0,10,21): # timeout (1 to 10 secs with 0.5 step)
    time_satisf_df = metrics_df[(metrics_df['execution_time'] < i)]
    time_agg = time_satisf_df.groupby(['theme', 'course'])

    avg_expl_n = 0
    avg_time = 0
    recall = 0
    if len(time_agg) != 0:
        avg_expl_n = sum([x[0] for x in time_agg.count()[['explanation']].values]) / len(time_agg)
        avg_time = sum([x[0] for x in time_agg.mean()[['execution_time']].values]) / len(time_agg)

        explained_n = len(time_agg)

        recall = explained_n/total_n
    timout_recall_curve.append([i, recall, avg_expl_n, avg_time])

time_recall_df = pd.DataFrame(data=timout_recall_curve, columns=['timeout', 'recall', 'avg_expl_n', 'avg_time'])
time_recall_df.set_index('timeout', inplace=True)
time_recall_df.to_csv('./report/recall_timout_curve_{}.csv'.format(algo))

# Explanation generation time
metrics_agg = metrics_df[~metrics_df['explanation'].isnull()].groupby(['theme', 'course'])
expls_time_df = metrics_agg['execution_time'].apply(list).reset_index(name="expls_time")

time_expln_boxplot = []
for n in range(1, 10): # explanation number
    first_n_expls_df = expls_time_df['expls_time'].apply(lambda x: sorted(x)[:n].pop())
    time_expln_boxplot.append([n, first_n_expls_df.values])

time_expln_boxplot_df = pd.DataFrame(data=time_expln_boxplot, columns=['explanation_n', 'execution_times'])
time_expln_boxplot_df = time_expln_boxplot_df.explode('execution_times')
time_expln_boxplot_df.to_csv('./report/time_expln_{}.csv'.format(algo))

#%%
import pandas as pd
import numpy as np

time_recall_df = pd.read_csv('./report/recall_timout_curve_{}.csv'.format(algo))

# VISUALIZE RESULTS
import matplotlib.pyplot as plt

# Plot recall metric for multiple timeout values
plt.style.context('default')

metric_ax = time_recall_df.plot(y=['recall'], color='red', legend=False, title='Recall x Timeout')
metric_ax.set_ylabel('Recall (fraction %)')
metric_ax.set_xlabel('Timeout (sec)')

plxt_ax = metric_ax.twinx()
time_recall_df.plot(y=['avg_expl_n'], color='magenta', legend=False, secondary_y=True, ax=plxt_ax, style='--')
plt.ylabel('Avg. Explanation nº')

diff_ax = plxt_ax.twinx()
diff_ax.set_ylabel('Avg. Execution Time (sec)')

rspine = diff_ax.spines['right']
rspine.set_position(('axes', 1.15))
time_recall_df.plot(y=['avg_time'], color='blue', legend=False, ax=diff_ax, style='-.')

diff_ax.legend([metric_ax.get_lines()[0], plxt_ax.right_ax.get_lines()[0], diff_ax.get_lines()[0]],\
['recall','avg. explanation nº','avg. exec. time'], bbox_to_anchor=(0.95, 0.5))

plt.savefig('./report/recall_x_timeout_{}.png'.format(algo))

#%%
time_expln_boxplot_df = pd.read_csv('./report/time_expln_{}.csv'.format(algo), usecols=[1,2], index_col=0)

#%%
agora_vai_crl = dict(zip(range(1, 10), [[] for i in range(10)]))
for index, value in time_expln_boxplot_df.iterrows():
    agora_vai_crl[index].append(value['execution_times'])

#%%
time_expln_boxplot_df = pd.DataFrame(agora_vai_crl)

#%%
# Box plot for explanation number
boxplot_fig = plt.figure()
boxplot_ax = time_expln_boxplot_df.boxplot()

boxplot_ax.set_xlabel("nº of explanations")
boxplot_ax.set_ylabel("execution time (sec)")

plt.savefig('./report/boxplot_time_x_expln_{}.png'.format(algo))