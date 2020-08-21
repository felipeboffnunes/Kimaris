# Python Standard Libraries

# External Libraries
import dash_table
import dash_html_components as html

# Database
from components.database.table import get_table_data

def get_table():
    df = get_table_data()
    
    table = html.Div([
        dash_table.DataTable(
            id="table",
            style_table={
                'overflowX': 'auto',
                'height': "92vh"
            },
            css=[{
                'selector': '.dash-spreadsheet td div',
                'rule': '''
                    line-height: 15px;
                    max-height: 60px; min-height: 60px; height: 60px;
                    display: block;
                    overflow-y: hidden;
                    
                '''
            },
                 {
                'selector': '.dash-spreadsheet-container .dash-spreadsheet-inner *, .dash-spreadsheet-container .dash-spreadsheet-inner *:after, .dash-spreadsheet-container .dash-spreadsheet-inner *:before',
                'rule': 'box-sizing: inherit; width: 100%;'
            }],
            tooltip_data=[
                {
                    column: {'value': str(value)}
                    for column, value in row.items()
                } for row in df.to_dict('rows')
            ],
            tooltip_duration=None,
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'minWidth': '10px', 'width': '90px', 'maxWidth': '540px',
            },
            data=df.to_dict("rows"),
            columns=[{"name": i, "id": i} for i in df.columns],
            
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            # To edit elements
            #columns=[{"name": i, "id": i, "editable": False if i == "id" else True} for i in df.columns],
            editable=False,
            row_deletable=False,
            page_size= 10,
        )
    ], style={"height": "100vh", "width": "100%"})
    
    return table
    
    