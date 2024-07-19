import dash     
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Interactive Data Visualization Tool"

# Sample dataset
sample_data = pd.read_csv('data/sample.csv')

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Interactive Data Visualization Tool", className='text-center text-primary mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.Div(id='output-data-upload')
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("X-axis:"),
            dcc.Dropdown(id='x-axis', placeholder='Select X-axis', className='mb-3'),
            dbc.Label("Y-axis:"),
            dcc.Dropdown(id='y-axis', placeholder='Select Y-axis', className='mb-3'),
            dbc.Label("Chart Type:"),
            dcc.Dropdown(id='chart-type', options=[
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Histogram', 'value': 'histogram'}
            ], placeholder='Select Chart Type', className='mb-3')
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph'), width=12)
    ])
], fluid=True)



# Callback to update options of dropdowns based on uploaded data
@app.callback(
    [Output('x-axis', 'options'),
     Output('y-axis', 'options')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_dropdown_options(contents, filename):
    if contents is None:
        df = sample_data
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    options = [{'label': col, 'value': col} for col in df.columns]
    return options, options


# Callback to update the graph based on user selections
@app.callback(
    Output('graph', 'figure'),
    [Input('x-axis', 'value'),
     Input('y-axis', 'value'),
     Input('chart-type', 'value')],
    [State('upload-data', 'contents')]
)
def update_graph(x_axis, y_axis, chart_type, contents):
    if contents is None:
        df = sample_data
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    if x_axis is None or y_axis is None or chart_type is None:
        return px.scatter()

    if chart_type == 'scatter':
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif chart_type == 'line':
        fig = px.line(df, x=x_axis, y=y_axis)
    elif chart_type == 'bar':
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif chart_type == 'histogram':
        fig = px.histogram(df, x=x_axis)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
