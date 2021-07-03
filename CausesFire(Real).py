#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd

dfv = pd.read_csv('test.csv')

year_list = ["2015","2016","2017","2018","2019","2020"]

# Themes
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA]) # https://bootswatch.com/default/

# Modal Button
modal = html.Div(
    [
        dbc.Button("Click me!! For More Info about the Dropdown",color="info",id="open",style={'font-size': '15px',
                                                                                               'font-weight': 'bold',}), 
         html.Br(),
         html.Br(),
        
   
        dbc.Modal([
            dbc.ModalHeader("Information about dropdown",style={'font-size': '50px','font-weight': 'bold', 
                                                                'margin': '0 10px 0 10px'}),
            dbc.ModalBody(
                
                 html.H6("You can type and search inside the dropdown", className="card-text",
                         style={'font-size': '30px','font-weight': 'bold', 'margin': '0 10px 0 10px'}),
               
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close", className="ml-auto")
            ),

        ],
            id="modal",
            is_open=False,    # True, False
            size="xl",        # "sm", "lg", "xl"
            backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
            scrollable=True,  # False or True if modal has a lot of text
            centered=True,    # True, False
            fade=True         # True, False
        ),
    ]
)

alert = dbc.Alert("Please choose Causes of Fire from dropdown to avoid further disappointment!",style={'font-size': '20px'},
                  color="danger",
                  dismissable=True),  # use dismissable or duration=5000 for alert to close in x milliseconds





image_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.CardImg(src="/assets/ggs.png", title="Fire"),
                html.H6("Choose Year:", className="card-text",style={'font-size': '25px','font-weight': 'bold'}),
                html.Div(id="the_alert", children=[]),
                
                # Dropdown Button
                dcc.Dropdown(
                    id='year-dropdown', value='2015', clearable=True,
                    persistence=True, persistence_type='memory',
                    options=[{'label': x, 'value': x} for x in year_list]
                ),
                
               html.H6("Choose Cause of Fire:", className="card-text",style={'font-size': '25px','font-weight': 'bold'}),
               dcc.Dropdown(
                    id='cause-dropdown', value='Electricity', clearable=True,
                    options=[{'label': x, 'value': x} for x in sorted(dfv.CauseofFire.unique())],
                   
                   
                ),
                
                
                html.Hr(),
                modal
            ]
        ),
        
    ],
    style={"width": "70rvh",'height': '70rvh'},color="secondary",
)

graph_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Hover to the graph to see the data and click  'About Fire Causes Graph'  for more info", 
                        className="card-title", style={"text-align": "center",'font-weight': 'bold'}),
                # Pop Over Button
                dbc.Button(
                    "About Fire Causes Graph", id="popover-bottom-target", color="info",style={'font-size': '18px',
                                                                                              'font-weight': 'bold'}
                ),
                   dbc.Popover(
                    [
                        dbc.PopoverHeader("The 'Others' causes of fire can be identified as Explosion,"
                                          "Friction and Electrical insulation leaks",
                                          style={'font-size': '25px','font-weight': 'bold'}),
                        dbc.PopoverBody(
                            "P/S : If certain state did't show in the visualization it indicates that there is 0 value in" 
                            " the state",
                        style={'font-size': '20px'}),
                    ],
                    id="popover",
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="bottom",
                    is_open=False,
                ),
                dcc.Graph(id='my-bar', figure={},
                         style={'height':'90vh', "width" : "100%"}),

            ]
        ),
    ],
    color="secondary",
)
# *********************************************************************************************************
app.layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=4), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************
@app.callback(
    Output("popover", "is_open"),
    [Input("popover-bottom-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='cause-dropdown', component_property='value'),
     Input(component_id='year-dropdown', component_property='value')]
)
def display_value(cause_chosen, year_chosen):
    dfv_fltrd = dfv[dfv['CauseofFire'] == cause_chosen]
    
    fig = px.pie(dfv_fltrd,names='State',
                values=year_chosen,  
                hole=0.599,

                labels={"Cause of Fire":"The Fire Causes"},  
                title='Cause of Fire in Malaysia Summary :2015 to 2020', #map the labels
                template='ggplot2',)
    fig = fig.update_yaxes(tickprefix="Total", ticksuffix="")

    fig.update_traces(textposition='inside', textinfo='percent+label',
                        marker=dict(line=dict(color='#000000', width=3)),
                        pull=[0, 0, 0.2, 0], opacity=0.7, rotation=60, 
                        textfont=dict(
                        family="sans serif",
                        size=150,
                        color="black"
                        ))   

    fig.update_layout(
        
        margin=dict(t=80, b=15, l=0, r=0),
        annotations=[dict(text="<b>"+cause_chosen, x=0.500, y=0.5,font_size=29,showarrow=False)],
        title={
        'text': "<b>Causes of Fire in Malaysia Summary ("+year_chosen+")",
        'x':0.435,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="",
        yaxis_title="",
        legend_title="State",
        font=dict(
        family="san serif",
        size=30,
        color="black",          
    )     
)                         
    return fig

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




