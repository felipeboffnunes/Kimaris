from collections import Counter

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from components.database.metadata import get_review_years, get_review_cites
import dash_core_components as dcc

def get_years_graph():
    
    years = get_review_years()
    counter = Counter(years)
    
    counts = []
    years = []
    for year, count in counter.most_common():
        counts.append(count)
        years.append(year)
    
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)

    fig.add_trace(
        go.Bar(x=counts, y=years, name="True", orientation='h'),
        row=1, col=1
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_title="Count", yaxis_title="Year")

    graph = dcc.Graph(id="em", figure = fig, config={ 'displayModeBar': False}, responsive=True, style={"height": "80vh"})
    
    return graph

def get_cites_graph():
    
    cites = get_review_cites()
    counter = Counter(cites)
    import re

    def atof(text):
        try:
            retval = float(text)
        except ValueError:
            retval = text
        return retval

    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        float regex comes from https://stackoverflow.com/a/12643073/190597
        '''
        return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]

    counts = []
    cites = []
    for cite, count in counter.most_common():
        counts.append(count)
        cites.append("c:" + str(cite))
    cites.sort(key=natural_keys)
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)

    fig.add_trace(
        go.Bar(x=counts, y=cites, name="True", orientation='h'),
        row=1, col=1
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_title="Count", yaxis_title="Cites")

    graph = dcc.Graph(id="em", figure = fig, config={ 'displayModeBar': False}, responsive=True, style={"height": "80vh"})
    
    return graph