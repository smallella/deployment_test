import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
server = app.server

# 讀取 CSV 檔案
df = pd.read_csv('realistic_e_commerce_sales_data.csv')

# 將 'Order Date' 轉換為日期格式
df['Order Date'] = pd.to_datetime(df['Order Date'])

# 提取年份和月份
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

# 篩選出 2023 年的資料
df_2023 = df[df['Year'] == 2023]

# 建立條形圖
fig = px.bar(
    df_2023,
    x='Month',
    y='Total Price',
    color='Region',
    color_discrete_map={'North': 'rgb(22, 50, 91)', 'South': 'rgb(185, 229, 232)', 'East': 'rgb(120, 183, 208)', 'West': 'rgb(255, 220, 127)'},
    title='Total Sales by Month in 2023')
fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))

# Create a app
app = Dash()
app.layout = html.Div(children=[
    html.H1("Interactive Sales Dashboard"),
    html.H4("Select Region"),
    dcc.Dropdown(
        options=[
            {'label': 'All', 'value': 'All'}, 
            {'label': 'North', 'value': 'North'},
            {'label': 'South', 'value': 'South'},
            {'label': 'East', 'value': 'East'},
            {'label': 'West', 'value': 'West'}
        ],
        value='All',
        placeholder='Select Region',
        id='region-dropdown'
    ),
    dcc.Graph(figure=fig, id='sales-barchart')
])

# Define a callback to update the graph
@app.callback(
    Output(component_id='sales-barchart', component_property='figure'),
    [Input(component_id='region-dropdown', component_property='value')]
)

def update_graph(region_chosen):
    df_copy = df_2023.copy(deep=True)
    title = "Total Sales by Month in 2023"
    if region_chosen != 'All':
        df_copy = df_copy[df_copy['Region']==region_chosen]
        title = f"Total Sales by Month in 2023 ({region_chosen})"
    new_fig = px.bar(
        df_copy,
        x='Month',
        y='Total Price',
        color='Region',
        color_discrete_map={'North': 'rgb(22, 50, 91)', 'South': 'rgb(185, 229, 232)', 'East': 'rgb(120, 183, 208)', 'West': 'rgb(255, 220, 127)'},
        title=title
    )
    return new_fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)