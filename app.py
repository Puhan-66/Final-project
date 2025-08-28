import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd


final_df = pd.read_csv('final_df.csv')

qb_options = [{'label': qb, 'value': qb} for qb in sorted(final_df['displayName'].dropna().unique())]
pressure_options = [
    {'label': 'Not under pressure', 'value': 0},
    {'label': 'Under pressure', 'value': 1}
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Analysis of the interaction between NFL QB decision types and EPA"),
    html.Label("Choose the quarterback:"),
    dcc.Dropdown(id='qb_dropdown', options=qb_options, value=qb_options[0]['value']),
    html.Label("Select pressure state:"),
    dcc.Dropdown(id='pressure_dropdown', options=pressure_options, value=0),
    dcc.Graph(id='proportion_graph'),
    dcc.Graph(id='epa_graph')
])

@app.callback(
    [Output('proportion_graph', 'figure'),
     Output('epa_graph', 'figure')],
    [Input('qb_dropdown', 'value'),
     Input('pressure_dropdown', 'value')]
)
def update_graph(qb_name, under_pressure):
    data = final_df[(final_df['displayName'] == qb_name) & (final_df['under_pressure'] == under_pressure)]
    if data.empty:
        fig1 = px.bar(title="无数据")
        fig2 = px.bar(title="无数据")
    else:
        fig1 = px.bar(data, x='decision_type', y='proportion',
                      title=f"{qb_name} {'Under pressure' if under_pressure else 'Not under pressure'} the proportion of each decision type selected")
        fig2 = px.bar(data, x='decision_type', y='epa_mean',
                      title=f"{qb_name} {'Under pressure' if under_pressure else 'Not under pressure'} the average value of EPA for each decision type")
    return fig1, fig2

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)