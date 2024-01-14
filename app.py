import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

features = pd.read_parquet('features_20240101.parquet')

PRODUCT_ID = st.number_input('PRODUCT_ID', value = 6659232268360)



data = features.copy().query(f"product_id == {PRODUCT_ID}")
PRODUCT_TITLE = data['product_title'].unique()[0]




#=======================================================
fig = px.histogram(x=data['representative_price'])
fig.update_xaxes(tickprefix="$", title = 'Representative price')


fig.update_layout(template = 'plotly_white',
                  xaxis=dict(showgrid=False), 
                  yaxis=dict(showgrid=False), 
                  title = f'Price distribution of product_id {PRODUCT_ID} - {PRODUCT_TITLE} ',
                  showlegend=False, height=500, width=800)

st.plotly_chart(fig)

#=======================================================


fig = px.histogram(x=data['view_sessions'])
fig.update_xaxes( title = 'Number of views')


fig.update_layout(template = 'plotly_white',
                  xaxis=dict(showgrid=False), 
                  yaxis=dict(showgrid=False), 
                  title = f'views distribution of product_id {PRODUCT_ID} - {PRODUCT_TITLE} ',
                  showlegend=False, height=500, width=800)

st.plotly_chart(fig)


#=======================================================




MIN_PRICE = st.number_input('MIN_PRICE', value = 60)
MAX_PRICE = st.number_input('MAX_PRICE', value = 200)


MIN_VIEWS = st.number_input('MIN_VIEWS', value = 60)
MAX_VIEWS = st.number_input('MAX_VIEWS', value = 5000)


#=======================================================


data_scatter = data.copy()
data_scatter['target'] = np.where((data_scatter['representative_price'] >= MIN_PRICE)
                                  & (data_scatter['representative_price'] <= MAX_PRICE)
                                  &(data_scatter['view_sessions'] >= MIN_VIEWS)
                                  & (data_scatter['view_sessions'] <= MAX_VIEWS),
                                     'Cumple la condición', 
                                     'No cumple')


fig = px.scatter(x = data_scatter['representative_price'], 
                 y = data_scatter['ordered_product_quantity'],
                 color = data_scatter['target'],
                 size = data_scatter['view_sessions'], trendline = 'ols'
                )




fig.update_layout(template = 'plotly_white',
                  xaxis=dict(showgrid=False), 
                  yaxis=dict(showgrid=False), 
                  title = 'First target: 1/17-1/21',
                  height=600, width=800)

fig.update_xaxes(tickprefix="$", title = 'Representative Price')
fig.update_yaxes( title = 'Ordered Product Quantity')

st.plotly_chart(fig)

#=======================================================


data_scatter = data.copy()
data_scatter['target'] = np.where((data_scatter['representative_price'] >= MIN_PRICE)
                                  & (data_scatter['representative_price'] <= MAX_PRICE)
                                  &(data_scatter['view_sessions'] >= MIN_VIEWS)
                                  & (data_scatter['view_sessions'] <= MAX_VIEWS),
                                     'Cumple la condición', 
                                     'No cumple')

data_scatter['gross_profit'] = data_scatter['ordered_product_quantity'] * (data_scatter['representative_price'] - data_scatter['cost'])
fig = px.scatter(x = data_scatter['representative_price'], 
                 y = data_scatter['gross_profit'],
                 color = data_scatter['target'],
                 size = data_scatter['view_sessions'], trendline = 'ols'
                )




fig.update_layout(template = 'plotly_white',
                  xaxis=dict(showgrid=False), 
                  yaxis=dict(showgrid=False), 
                  title = 'First target: 1/17-1/21 - Gross Profit',
                  height=600, width=800)

fig.update_xaxes(tickprefix="$", title = 'Representative Price')
fig.update_yaxes( title = 'Gross profit')

st.plotly_chart(fig)