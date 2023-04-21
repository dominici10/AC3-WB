import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Lendo o arquivo CSV
data = pd.read_csv('../bases_de_upload/dados_upload.csv', delimiter=';')

top_precos = 20
top_titulos = 20

# título do aplicativo
st.title('Visualizações Gráficas - Produtos Arduino|Preços')

# primeira visualização usando o Streamlit
st.header('1 - Top 20 Produtos por Preço')
mean_price = data.groupby('titulo')['preco'].mean().reset_index()
mean_price = mean_price.sort_values('preco', ascending=False).head(top_precos)
st.bar_chart(mean_price, x='titulo', y='preco')
st.write('Este Grafico mostra os {} produtos com os maiores preços médios.'.format(top_precos))

# segunda visualização usando o Streamlit
st.header('2 - Preço Mínimo e Máximo por Produto')
min_max_price = data.groupby('titulo')['preco'].agg(['min', 'max']).reset_index()
min_max_price = min_max_price.sort_values('max', ascending=False).head(top_precos)
st.bar_chart(min_max_price, x='titulo', y=['min', 'max'])
st.write('Este Grafico mostra os {} produtos com os maiores preços máximos.'.format(top_precos))

# terceira visualização usando o Plotly
st.header('3 - Box Plot')
fig = px.box(data.groupby('titulo')['preco'].mean().reset_index(), x='titulo', y='preco')
fig.update_layout(xaxis=dict(showticklabels=False))
st.plotly_chart(fig)
st.write('Taxa de variação de preço dos produtos.')

# quarta visualização usando o Plotly
st.header('4 - Scatter Plot')
fig = px.scatter(data.groupby('titulo')['preco'].mean().reset_index(), x='preco', y='titulo')
fig.update_layout(yaxis=dict(showticklabels=False))
st.plotly_chart(fig)
st.write('Taxa de variação de preço dos produtos.')

# criando o gráfico de linha com o Plotly
st.header('5 - Preço Médio por Produto (Top {})'.format(top_titulos))
mean_price = data.groupby('titulo')['preco'].mean().reset_index()
mean_price = mean_price.sort_values(by='preco', ascending=False)[:top_titulos]
fig = go.Figure()
fig.add_trace(go.Scatter(x=mean_price['titulo'], y=mean_price['preco'], mode='lines+markers'))
st.plotly_chart(fig)
st.write('Este Grafico mostra os {} produtos com os maiores preços médios.'.format(top_titulos))

# Criando o gráfico de pizza
st.header('6 - Gráfico de Pizza (Top {})'.format(top_titulos))
above_130 = data[data['preco'] > 130]
pie_chart = above_130.groupby('titulo')['preco'].sum().reset_index()
pie_chart = pie_chart.sort_values('preco', ascending=False).head(top_titulos)

fig = go.Figure(data=[go.Pie(labels=pie_chart['titulo'], values=pie_chart['preco'])])
fig.update_layout(title='Top {} Produtos com Preço Acima de R$ 130'.format(top_titulos),
                  font=dict(size=16),
                  title_font=dict(size=20),
                  width=800,
                  height=600)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)
st.write('Este Grafico de pizza mostra os {} produtos com os maiores preços médios.'.format(top_titulos))