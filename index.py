# step 1
from dash import Dash, Input, Output, State, html, dcc, dash_table, callback
# step 2
app = Dash(__name__)
# step 3
app.layout = html.Div(id= ‘div1’, children=[html.H1("My first Dash 2.0 app!")])
# step 4
if __name__ == "__main__":
    app.run_server(debug=True)
