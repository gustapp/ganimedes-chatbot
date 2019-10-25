#%%
import pandas as pd
import click

df = pd.read_json('../ganimedes-chatbot/db_poli_v2.json')
df = df[['docentes']]
df[['docentes']].apply(lambda x_list: ['-'.join(x.split('-')[1:]).strip() for x in x_list.values])

# print(len(documents))
df.head()

#%%
from pybliometrics.scopus import ScopusSearch
other = ScopusSearch('AUTHOR-NAME ( cozman )  AND  AF-ID ( "Universidade de Sao Paulo - USP"   60008088 )', download=True)
other.get_results_size()

#%%
import pandas as pd
df = pd.DataFrame(pd.DataFrame(other.results))
df.columns

#%%
df.shape

#%%
pd.set_option('display.max_columns', None)
df.head()

#%%
