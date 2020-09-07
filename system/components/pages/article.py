# External Libraries
import dash_core_components as dcc
import dash_html_components as html

# Fragments
from components.fragments.article_menu import ARTICLE_MENU

article_page = html.Div([
                    html.Div([
                        html.Div(id="article-info"),
                        dcc.Upload(
                            id='upload-article-pdf',
                            children=html.P("Drag pdf article or click here"),
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
                        ),    
                    ],id="article-header", style={"padding": "2em", "width": "30%"}),
                    html.Div([
                        dcc.Tabs([
                            dcc.Tab(
                                html.Div(id="article-graph", style={"width": "100%", "padding-top": "2em"}), label="Graph"
                            ),
                            dcc.Tab(
                                html.Div([
                                        html.Div(id="iframe-article-div"),
                                ],id="article-pdf"), label="PDF"
                            ),
                            dcc.Tab(
                                dcc.Tabs([
                                    dcc.Tab(
                                        html.Div([
                                            html.P(id="text-article", ),
                                        ],id="article-metadata", style={'overflow-y': 'scroll', "height": "75vh"}
                                        ), label="Summarized text"
                                    ),
                                    dcc.Tab(
                                        dcc.Tabs([
                                            dcc.Tab(
                                                html.Div(id="common-words-div"), label="Words"
                                            ),
                                            dcc.Tab(
                                                html.Div(id="common-bigrams-div"), label="Bigrams"
                                            ),
                                            dcc.Tab(
                                                html.Div(id="common-trigrams-div"), label="Trigrams"
                                            ),
                                            dcc.Tab(
                                                html.Div(id="common-speech-tagging-div"), label="Speech Tagging"
                                            ),
                                        ]), label="Frequency"
                                    ),
                                    dcc.Tab(
                                        html.Div(id="knowledge-graph-div", style={"height": "80vh"}), label = "Knowledge Graph"
                                    ),
                                    dcc.Tab(
                                        html.Div(id="topic-modelling-div"), label="Topic Modelling"
                                    ),
                                ]), label="Metadata"
                            ),
                           
                        ])
                    ], id="article", style={"width": "70%"}),
                    
                    ARTICLE_MENU
], id="article-div", className="row")