


#1 Carregando todas as bibliotecas
import pandas as pd
from scipy import stats as st
import matplotlib.pyplot as plt
import numpy as np
from math import ceil

#1.1 Set the maximum width for the output to be very large
pd.set_option('display.width', 1200)

# Ensure all columns are shown without being truncated with "..."
pd.set_option('display.max_columns', None)

#2 Carregue os arquivos de dados em diferentes DataFrames

df_calls = pd.read_csv('megaline_calls.csv') # change the 'call_date' column to data_type

df_internet = pd.read_csv('megaline_internet.csv') # may change the 'session_date' to data_type

df_messages = pd.read_csv('megaline_messages.csv') # may change the 'message_data' to data_type

df_plans = pd.read_csv('megaline_plans.csv', sep = ',')

df_users = pd.read_csv('megaline_users.csv') # the column 'reg_date' has only 34 non-null values

#3 Imprima informações gerais/resumo sobre o DataFrame dos planos

'''
print(df_plans.dtypes)
print()
display(df_plans.info())
print()
print(df_plans.describe())
print()
print(df_plans.columns)
print()
print(df_plans.shape)
print()

'''
#4 Imprima uma amostra de dados dos planos

#display(df_plans.head())

#5 replacing the datatypes
df_plans['usd_monthly_pay'] = df_plans['usd_monthly_pay'].astype('float64')

df_plans['usd_per_gb'] = df_plans['usd_per_gb'].astype('float64')

#6 creating a new column with gb instead of mb
df_plans['gb_per_month_included'] = df_plans['mb_per_month_included'] / 1024

#removing the unusefull column
df_plans = df_plans.drop(columns = ['mb_per_month_included'])

# rounding up the values
df_plans['gb_per_month_included'] = df_plans['gb_per_month_included'].apply(ceil)

#display(df_plans)


#7 Imprima informações gerais/resumo sobre o DataFrame dos usuários

'''print(df_users.dtypes)
print()
df_users.info()
print()
print(df_users.describe())
print()
print(df_users.columns)
print()
print(df_users.shape)
print()
'''

#8 Imprima uma amostra de dados dos usuários

#display(df_users.sample(5))

#9  Changing some columns to datetime64

df_users['reg_date'] = pd.to_datetime(df_users['reg_date'])

df_users['churn_date'] = pd.to_datetime(df_users['churn_date'])

#9.1
last_date = df_users['churn_date'].max()

#print(last_date)

#10 Já que os valores ausentes da coluna ['churn_date'] se referem a clientes ativos, faremos a Pandas preencher os valores nulos com a última data registrada na tabela churn_date, assim podemos deduzir o tempo de fidelidade dos clientes ativos. O último dia registrado será computado como o último dia em que a tabela csv foi preenchida.

df_users['churn_date'] = df_users['churn_date'].fillna(last_date)

df_users_tenure = df_users #criando um df paralelo para não comprometer o df principal

df_users_tenure['tenure'] = df_users_tenure['churn_date'] - df_users_tenure['reg_date']

#display(df_users_tenure.sample(5)) #Series contendo o tempo de fidelidade de cada cliente

df_users.info() #valores nulos preenchidos


#11 Imprima informações gerais/resumo sobre o DataFrame das chamadas

'''print(df_calls.dtypes)
print()
df_calls.info()
print()
print(df_calls.describe())
print()
print(df_calls.columns)
print()
print(df_calls.shape)
print()
display(df_calls.isna().sum()) #conferindo se há valores vazios nas colunas

'''
#12 Imprima uma amostra de dados das chamadas

#display(df_calls.sample(5))


#13 changing the column ['call_date'] to datetime64

df_calls['call_date'] = pd.to_datetime(df_calls['call_date'])

#df_calls.info()

#14 Checking for unusual call durations

print(df_calls['duration'].describe()) #análise estatística da coluna 'duration'

print(f"\nQuantidade de ligações que duraram zero segundos: {(df_calls['duration'] == 0).sum()}")

print(f"\nLigações mais demoradas (>30 min): {(df_calls['duration'] > 30).sum()}")

df_calls['call_date'] = pd.to_datetime(df_calls['call_date'])



#14.1 As we have 26834 calls with duration = zero, let's remove it, so our future statistical analysis will not be bothered by them.

df_calls = df_calls[df_calls['duration']!= 0]

#print(f"\nCalls with 0 duration: {(df_calls['duration'] == 0).sum()}")


#15 Imprima informações gerais/resumo sobre o DataFrame das mensagens
'''
print(df_messages.dtypes)
print()
df_messages.info()
print()
print(df_messages.describe())
print()
print(df_messages.columns)
print()
print(df_messages.shape)
print()
'''

#16 Imprima uma amostra dos dados das mensagens

#display(df_messages.sample(5))


#17 datatype 'message_date' column to datetime64

df_messages['message_date'] = pd.to_datetime(df_messages['message_date'])

#df_messages.info()


#18 Checking for any unusual patterns
'''
print("Message date range:")
print(f"Earliest: {df_messages['message_date'].min()}")

print(f"Latest: {df_messages['message_date'].max()}")

print(f"\nTotal messages: {len(df_messages)}")

print(f"Unique users: {df_messages['user_id'].nunique()}")

print(f'\nWe have a mean of {len(df_messages) / df_messages['user_id'].nunique():.2f} messages per user.')

'''

#19 Imprima informações gerais/resumo sobre o DataFrame da internet

'''print(df_internet.dtypes)
print()
df_internet.info()
print()
print(df_internet.describe())
print()
print(df_internet.columns)
print()
print(df_internet.shape)
print()
'''

#20  Imprima uma amostra de dados para o tráfego da internet

#display(df_internet.sample(5))


#21

df_internet['session_date'] = pd.to_datetime(df_internet['session_date']) #session_date passa a ser do tipo datetime64

df_internet['gb_used'] = df_internet['mb_used'] / 1024 #criamos a coluna 'gb_used';


#22
#df_internet['gb_used'] = (df_internet['gb_used']).round(0).astype(int) # arredondando o valor para um número inteiro acima para se alinhar ao modo como a operadora cobra pelo consumo

sample = df_internet[df_internet['mb_used']== 0] # We have 13.747 rows with mb_used equals zero.


#23 Imprima as condições dos planos e certifique-se de que elas fazem sentido para você

from IPython.display import display, HTML

html_content = """
<h3>Description of the plans</h3>
<p>Note: Megaline rounds seconds to minutes and megabytes to gigabytes. For calls , each individual call is rounded up: even if a call lasted only one second, one minute will be counted. For web traffic , individual web sessions are not rounded up. Instead, the monthly total is rounded up. If someone uses 1,025 megabytes in a month, they will be charged for 2 gigabytes.
</p>
<p>Here is a description of the plans:</p>

<h5>Surf</h5>
<ol>
  <li>Monthly price: $20;</li>
  <li>500 monthly minutes, 50 text messages, and 15 GB of data;</li>
  <li>After exceeding the package limits:
    <ul>
        <li>1 minute: 3 cents;</li>
        <li>1 text message: 3 cents;</li>
        <li>1 GB of data: $10.</li>
    </ul>
  </li>
</ol>

<h5>Ultimate</h5>

<ol>
  <li>Monthly price: $70</li>
  <li>3,000 monthly minutes, 1000 text messages, and 30 GB of data</li>
  <li>After exceeding the package limits:
    <ul>
        <li>1 minute: 1 cents;</li>
        <li>1 text message: 1 cents;</li>
        <li>1 GB of data: $7.</li>
    </ul>
  </li>
</ol>

"""
#display(HTML(html_content))


#24 Calcule o número de chamadas feitas por cada usuário por mês. Salve o resultado.

df_calls['month'] = df_calls['call_date'].dt.month # the month each call was made;

calls_analise = df_calls[['user_id', 'id', 'month']] # a new df where i keep only the colums I need;

calls_per_month = calls_analise.groupby(['user_id', 'month']).agg(calls_qty=('id', 'count')) #garantindo que user_id não será o índice

#display(calls_per_month.head(5))


#25 Calcule a quantidade de minutos gastos por cada usuário por mês. Salve o resultado.

minutes_per_month = df_calls.drop(columns= 'call_date') # a new df where i keep only the colums I need;

minutes_per_month = minutes_per_month.groupby(['user_id', 'month']).agg(minutes_qty=('duration', 'sum')) #prevenindo que user_id seja colocado como índice

#display(minutes_per_month.head(5))


#26.2 criar uma coluna esclusiva para os meses

df_messages['month'] = df_messages['message_date'].dt.month


#26.2 criar uma coluna esclusiva para os meses

df_messages['month'] = df_messages['message_date'].dt.month


#26.3 Calcule o número de mensagens enviadas por cada usuário por mês. Salve o resultado.

messages_per_month = df_messages.drop(columns= 'message_date') # a new df where i keep only the colums I need;

messages_per_month = messages_per_month.groupby(['user_id', 'month']).agg(messages_qty=('id', 'count')) # user_id nao pode ser índice

display(messages_per_month.head())


#27.2 creating a new column only for month

df_internet['month'] = df_internet['session_date'].dt.month


#27.3 Calcule o volume de tráfego de internet usado por cada usuário por mês. Salve o resultado.

gb_per_month = df_internet.drop(columns = 'session_date') #creating a new df and keeping only columns I need;

gb_per_month = gb_per_month.groupby(['user_id', 'month']).agg(gb_used=('gb_used','sum'))

gb_per_month['gb_used'] = gb_per_month['gb_used'].round(1) # I want only 1 number to decimal place

#display(gb_per_month.head(5))


#28 Junte os dados de chamadas, minutos, mensagens e internet com base em user_id e month

merged_df = calls_per_month.join([minutes_per_month, messages_per_month, gb_per_month], how = 'outer').reset_index()

merged_df.fillna(0, inplace = True) #replacing the null values with 0.

merged_df.info()


#28.1
#display(merged_df.sample(5))


#29.1 criar um novo df a partir de df_users para fazer merge com merged_df

users_analise = df_users[['user_id', 'plan']]

#users_analise.info()


#29 preparando para adicionar as informações do plano

users_merged_df = pd.merge(merged_df, users_analise, on = 'user_id')

#print(users_merged_df.head(5))


#29.1 melhorando o nome das colunas

users_merged_df = users_merged_df.rename(columns = {'calls_qty':'calls_used',
                                                    'minutes_qty': 'min_used',
                                                    'messages_qty': 'sms_used'
})

#users_merged_df.info()


#29.2 preparing the df_plans to the merge process

plans_analise = df_plans.rename(columns = {'messages_included': 'plan_sms',
                                           'minutes_included': 'plan_min',
                                           'usd_monthly_pay' :'plan_price',
                                           'usd_per_gb': '$_gb',
                                           'usd_per_message': '$_sms',
                                           'usd_per_minute': '$_min',
                                           'plan_name': 'plan',
                                           'gb_per_month_included': 'plan_gb'
                                           })

print(plans_analise)


#29.3  Adicione as informações sobre o plano

users_plans = pd.merge(users_merged_df, plans_analise, on = 'plan')

#display(users_plans.head(5))



def apply_threshold_calc(df, col_a, col_b, col_multiplier):
    """
    Calculates (ColA - ColB). 
    If result <= 0, returns 0. 
    Otherwise, returns (ColA + ColB) * Multiplier.
    """
    difference = (df[col_a] - df[col_b])
    return np.where(difference >= 0, 0, difference.abs() * df[col_multiplier])


# Now you can use it 3 times easily:

results_df = pd.DataFrame({
    'extra_min_us$': apply_threshold_calc(users_plans, 'plan_min', 'min_used', '$_min'),
    'extra_sms_us$': apply_threshold_calc(users_plans, 'plan_sms', 'sms_used', '$_sms'),
    'extra_gb_us$': apply_threshold_calc(users_plans, 'plan_gb', 'gb_used', '$_gb')
})

cols_to_round = ['extra_min_us$', 'extra_sms_us$', 'extra_gb_us$']

results_df[cols]

#print(results_df.head(5))


#30 Calcule a receita mensal para cada usuário



