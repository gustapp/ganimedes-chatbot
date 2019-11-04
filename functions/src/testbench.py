import json
from flask import Flask, request
from main import get_dialogflow_fulfillment
from time import time
import pandas as pd
import numpy as np
import click
from  datetime import datetime

start_datetime = datetime.now()
click.echo("Launching experimental evaluation")

class RequestMock(object):
    def __init__(self, json_data):
        self.data = json_data
        self.headers = "mock headers"

    def get_json(self):
        return self.data

popular_concepts_df = pd.read_csv('./report/input/popular_concepts_en.csv')
# concepts = ['aprendizado de máquina', 'inteligência artificial']
concepts = popular_concepts_df['concepts']

# Recommendation Intent Dialogflow Request
with open('./functions/test/mock/getCourseSuggestion-theme.json') as json_file:
    rec_intent_req = json.load(json_file)

# Explanation Intent Dialogflow Request
with open('./functions/test/mock/getCourseSuggestion-explain.json') as json_file:
    expl_intent_req = json.load(json_file)

def fill_rec_request(theme, template):
    template['queryResult']['parameters']['theme'] = theme
    return template

def fill_expl_request(course, theme, template):
    template['queryResult']['parameters']['Course'] = course
    template['queryResult']['outputContexts'][0]['parameters']['theme'] = theme
    return template

click.echo(click.style('AAAI WICRS 2020 Experiments', fg='white', bold=True))
click.echo(click.style('Start datetime: {}'.format(start_datetime), fg='blue'))
click.echo("Launching experimental evaluation")
click.echo("Simulating User requests")
click.echo("Number of interactions: {}".format(len(concepts)))

click.echo(click.style('EXPLANATIONS EVALUATION IN PROGRESS', blink=True, bold=True))
eval_metrics = []
with click.progressbar(concepts, label='Testing',) as bar:
    for theme in bar:
        data = fill_rec_request(theme, rec_intent_req)
        request = RequestMock(data)
        courses = get_dialogflow_fulfillment(request)[:5] # top 5

        # Explain
        data = fill_expl_request(courses, theme, expl_intent_req)
        request = RequestMock(data)

        start_time = time()
        expl_responses = get_dialogflow_fulfillment(request)
        end_time = time()
        elapsed_time = end_time - start_time
        
        for expl_res in expl_responses:
            # responses from TRUE and PRED algos
            algo, reasons = expl_res

            expl_paths = []
            for pattern in reasons:
                expl_paths += pattern[1]
            
            expl_course = dict(zip(courses, [[] for i in range(len(courses))]))
            for path in expl_paths:
                execution_time = path[0]
                for recommendation in courses:
                    if recommendation.lower() in path[1]:
                        expl_course[recommendation].append((execution_time, path[1]))
                        break

            for course, explanations in expl_course.items():
                explanation_n = len(explanations)
                execution_time = elapsed_time

                for explanation in explanations:
                    execution_time = explanation[0]

                    eval_metrics.append([algo, theme, course, execution_time, explanation[1]])
                
                if explanation_n == 0: # miss
                    eval_metrics.append([algo, theme, course, execution_time])

click.echo("Finish testing...")

click.echo("Results saved on ./report/embedfs_evaluation_metrics.csv")
metrics_df = pd.DataFrame(data=eval_metrics, columns=['algorithm', 'theme', 'course', 'execution_time', 'explanation'])
metrics_df.to_csv('./report/embedfs_evaluation_metrics.csv')

#%%
# CONSOLIDATE EXPERIMENT RESULTS
import pandas as pd
import numpy as np
import click

click.echo("Consolidating results...")
agg_metrics_df = pd.read_csv('./report/embedfs_evaluation_metrics.csv')

for algo in ['TRUE', 'PRED']:
    click.echo("Processing {} results".format(algo))

    # Filter algo results
    metrics_df = agg_metrics_df[(agg_metrics_df['algorithm'] == algo)] 

    # Recall (fraction of recommendations explained)
    unexplained_triples = metrics_df[metrics_df['explanation'].isnull()]

    unexplained_n = len(unexplained_triples)
    total_n = len(concepts)*5

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

#%%
end_datetime = datetime.now()

click.echo(click.style('End datetime: {}'.format(end_datetime), fg='blue'))
click.echo(click.style('Finished Successfully! :)', fg='green'))

# %%
