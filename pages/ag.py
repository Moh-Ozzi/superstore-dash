import dash_ag_grid as dag
import dash
from dash import html, dcc
import pandas as pd

from dash import html, dcc, Output, Input, callback
from flask_login import current_user
from utils.login_handler import require_login


dash.register_page(__name__, title='ag', path='/ag')
require_login(__name__)

#hwfkhbwelfj3b
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

columnDefs = [
    # Row group by country and by year is enabled.
    {"field": "country", "sortable": True, "filter": True, "rowGroup": True, "hide": True},
    {"field": "year", "sortable": True, "filter": True, "rowGroup": True, "hide": True},
    {"field": "athlete", "sortable": True, "filter": True,
     "cellRendererParams": {
                        "checkbox": True,
                    },
     "cellRenderer": "agGroupCellRenderer"
     },
    {"field": "age", "sortable": True, "filter": True},
    {"field": "date", "sortable": True, "filter": True},
    {"field": "sport", "sortable": True, "filter": True},
    {"field": "total", "sortable": True, "filter": True},
]

layout = html.Div(
    [
        dcc.Markdown("Demonstration of row groupings in a Dash AG Grid."),
        dcc.Markdown("This grid groups first by country and then by year."),
        dag.AgGrid(
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            dashGridOptions={
                "autoGroupColumnDef": {
                    "cellRenderer": "agGroupCellRenderer",
                    "cellRendererParams": {
                        "checkbox": True,
                    },
                    "headerCheckboxSelection": True,
                },
                "rowSelection": "multiple",
                "groupSelectsChildren": True,
                "suppressRowClickSelection": True,
                "suppressAggFuncInHeader": True,
                "groupDisplayType": "multipleColumns",
            },
            defaultColDef=dict(
                resizable=True,
            ),
            id="grouped-grid",
            enableEnterpriseModules=True,
        ),
    ]
)

