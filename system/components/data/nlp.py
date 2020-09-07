
# External Libraries
import dash_core_components as dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_dangerously_set_inner_html
import dash_html_components as html

from components.fragments.nlp_tools import get_most_common_words, remove_common_stop_words, get_most_common_bigrams, topic_modelling, get_most_common_trigrams, processSentence, printGraph, getSentences, get_most_common_speech_tagging

def get_common_speech_tagging_graph(data):
    common_speech_tagging = get_most_common_speech_tagging(data)
    lenght = len(common_speech_tagging)
    counts = []
    words = []
    for word, count in common_speech_tagging.most_common(lenght):
        print(word)
        print(count)
        counts.append(count)
        words.append(word)

    fig = make_subplots(rows=1, cols=1, subplot_titles=["True", "True/Fake", "Fake"], shared_xaxes=True)

    fig.add_trace(
        go.Bar(x=counts, y=words, name="True", orientation='h'),
        row=1, col=1
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_title="Count", yaxis_title="Words")

    graph = dcc.Graph(id="em", figure = fig, config={ 'displayModeBar': False}, responsive=True, style={"height": "80vh"})
    
    return graph

def get_common_words_graph(data, number, bigram=False, trigram=False):
    
    if bigram:
        common_words = get_most_common_bigrams(data)
    elif trigram:
        common_words = get_most_common_trigrams(data)
    else:
        common_words = get_most_common_words(data)
    common_words = remove_common_stop_words(common_words)

    counts = []
    words = []
    for word, count in common_words.most_common(number):
        counts.append(count)
        words.append(word)

    fig = make_subplots(rows=1, cols=1, subplot_titles=["True", "True/Fake", "Fake"], shared_xaxes=True)

    fig.add_trace(
        go.Bar(x=counts, y=words, name="True", orientation='h'),
        row=1, col=1
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_title="Count", yaxis_title="Words")

    graph = dcc.Graph(id="em", figure = fig, config={ 'displayModeBar': False}, responsive=True, style={"height": "80vh"})
    
    return graph

def get_topics(title, data):
    topics = topic_modelling(title, data)
    print("heere")
    topic = html.Div([html.Iframe(srcDoc=str(topics), id = "iframe-topic")], id="div-topic")
    print("here")
    return topic

import spacy
import en_core_web_lg
def get_knowledge_graph(content):
    
    nlp_model = en_core_web_lg.load()
    
    sentences = getSentences(content)
    
    
    triples = []

    for sentence in sentences:
        triples.append(processSentence(nlp_model, sentence))

    pos, G = printGraph(triples)
    colors= []
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        colors.append(0)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        colors.append(1)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_z = []
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        text=list(pos.keys()),
        hoverinfo='text',
        opacity=0.2,
        marker=dict(
            showscale=False,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=colors,
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

    layout = go.Layout(
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode='closest', 
        hoverlabel = dict(
            bgcolor = 'white'
        )
    )
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=layout)
    config = {'responsive': True, "displaylogo": False, \
        'modeBarButtonsToRemove': ['pan3d', 'lasso3d', 'zoom3d', 'orbitRotation', 'tableRotation', \
            'resetCameraDefault3d', 'hoverClosest3d', 'resetCameraLastSave3d']}
    graph = dcc.Graph(figure=fig, config=config, style={"height": "80vh"})
    return graph

