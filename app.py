import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html


df_backtest_parameters_table1 = pd.read_csv('data/backtest_parameters_table1.csv')
df_backtest_parameters_table2 = pd.read_csv('data/backtest_parameters_table2.csv')

df_performance_analysis = pd.read_csv('data/performance_analysis.csv')
df_performance_analysis2 = pd.read_csv('data/performance_analysis2.csv')




app = dash.Dash(__name__)
server = app.server

app.title = 'Factor Model Backtesting'


def make_dash_table( df ):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for _, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append( html.Td([ row[i] ]) )
        table.append( html.Tr( html_row ) )
    return table

def get_header():
    header =  html.Div([
                html.Div([
                    html.H5('Principle Component Analysis Factor Model Backtesting Report'),
                    html.H6('Based on Modern Portfolio Theory', style=dict(color='#7F90AC')),
                    ], className = "nine columns padded" ),

                html.Div([
                    html.H1([html.Span('12', style=dict(opacity=0.5)), html.Span('05')]),
                    html.H6('Wenkai Cui')
                ], className = "three columns gs-header gs-accent-header padded", style=dict(float='right')),

            ], className = "row gs-header gs-text-header")
    return header


def get_mylink():
    link = html.Div([
            'For Theory in Detail & Source Code:',
            html.A(['https://wenkaicui.com/2018/09/30/principle-component-analysis-in-finance/'],href='https://wenkaicui.com/2018/09/30/principle-component-analysis-in-finance/')
        ],style=dict(position="absolute", top=-20, left=0))
    return link

app.layout = html.Div([

    html.Div([ # page 1

        get_mylink(),
        html.A([ 'Print PDF' ],
           className="button no-print",
           style=dict(position="absolute", top=-40, right=0)),


        html.Div([ # subpage 1

            # Row 1 (Header)

            get_header(),

            html.Br([]),

            # Row 2

            html.Div([

                html.Div([
                    html.H6('Model Explained', className = "gs-header gs-text-header padded"),

                    html.Strong('Principle Component Analysis:'),
                    html.P([html.Img(src='/assets/1.png', height='12',className = 'latex')]),

                    html.Strong('Orthogonal Factor Model:'),
                    html.P('''The returns are driven by a constant mean and multiple factors and idiosyncratic random term. 
                    The factors are uncorrelated to each other, which means the returns are driven by independent factors. 
                    The  idiosyncratic terms could be related to each other. '''),
                    html.P([html.Img(src='/assets/2.png', height='13',className = 'latex')]),

                    html.P('The factor loadings are estimated by PCA, then a second pass regression is used to estimate factors.'),

                ], className = "six columns" ),

                html.Div([
                    html.H6(["Modern Portfolio Theory & Backtesting"],
                            className = "gs-header gs-table-header padded"),
                    html.P('''One thing about Modern Portfolio Theroy is the the estimation of covariance matrix. There
                    are too much noise and too less data.
                    The purpose of our factor model is to reduce the estimation error in covariance matrix. Calculate '''),
                    html.Ul([
                        html.Li('Sample Covariance Matrix '),
                        html.Li('Factor Constrained Covariance Matrix, by')
                    ]),
                    html.P([html.Img(src='/assets/3.png', height='13',className = 'latex')]),
                    html.P('''
                    Then apply Modern Portfolio Theory to find Mean-Variance efficient Porfolio. If factor constrained 
                    covariance matrix indeed outperform sample estimation covariance matrix, the factor model is proved to improve estimation accuracy.
                    ''')
                    
                ], className = "six columns" ),

            ], className = "row "),

            # row 3 BT1 title
            html.Div([
                html.Div([
                    html.H6('Backtesting Minimum Variance Portfolio (Short Sale Allowed)', className = "gs-header gs-text-header padded"),
                ],className = "twelve columns" ),
            ], className = "row "),

            # row 3 BT1 
            html.Div([
                html.Div([
                        html.P('Backtesting Parameters:',className = 'twelve columns second-title'),
                        html.Table( make_dash_table( df_backtest_parameters_table1)),
                        html.P('Performance Analysis:',className = 'twelve columns second-title'),
                        html.Table( make_dash_table( df_performance_analysis)),
                        html.P('Result Summary:',className = 'twelve columns second-title'),
                        html.Strong('''The goal of MVP is to minimize variance as much as possible, ignoring the cost of return.
                         EWMA shows that MVP construct by factor constrained covariance matrix exhibits significantly lower volatility 
                         than market portfolio, while unconstrained MVP doesn't outperform market. Interestingly, 
                         factor constrained portfolio doesn't show significant lower return than market portfolio, 
                         which is inconsistent with modern portfolio theory. ''',style={'line-height':'150%'})

                ],className = "five columns"),

                html.Div([
                    html.Iframe(src='https://plot.ly/~cuiwk0320/2.embed?modebar=false&link=false', \
                             style=dict(border=0), width="100%", height="250"),
                    html.Iframe(src='https://plot.ly/~cuiwk0320/4.embed?modebar=false&link=false', \
                             style=dict(border=0), width="100%", height="250")
                ],className = "seven columns")
            ], className = "row ")

        ], className = "subpage" ),

    ], className = "page" ),




    html.Div([ # page 2
        get_mylink(),
        html.A([ 'Print PDF' ],
           className="button no-print",
           style=dict(position="absolute", top=-40, right=0)),
        
        html.Div([# Row 1 (Header)
            get_header(),
            html.Br([]),

            html.Div([
                html.Div([
                    html.H6('Backtesting Tangency (No Short Sale)', className = "gs-header gs-text-header padded"),
                ],className = "twelve columns" ),
            ], className = "row "),

            html.Div([
                html.Div([
                    html.Div([
                        html.H6('Backtesting Parameters', className = "gs-header gs-table-header padded"),
                        html.Table( make_dash_table( df_backtest_parameters_table2)),

                        html.H6('Model Explained', className = "gs-header gs-table-header padded"),
                        html.P('''By Modern portfolio theory, the efficient frontier is a hyperbola. 
                        The tangency portfolio has the highest Sharpe Ratio. It can be calculated analytically:'''),
                        html.P([html.Img(src='/assets/4.png', height='24',className = 'latex')]),
                        html.P('''However, when backtesing, the weights tend to explode. Constraint must be imposed and 
                        weight can only be calculated by optimizer. In this backetst, short sale is not allowed.
                        ''')                                                       
                    ]),                             
                ],className = "five columns"),

                html.Div([
                    html.Iframe(src='https://plot.ly/~cuiwk0320/6.embed?modebar=false&link=false', \
                             style=dict(border=0), width="100%", height="300")
                ],className = "seven columns"),
            ], className = "row "),

            html.Div([
                html.Div([
                    html.Div([
                        html.H6('Results Summary', className = "gs-header gs-table-header padded"),
                        html.Strong('''
                            Both tangency portfolios consistently outperformed market portfolio with or without factor model constraint,
                            especially during the decade after financial crysis.
                            PCA factor constrained portfolio is better than unconstrained throughout the time, but the improvement is minor.
                            Tangency portfolios have betas very close to 1, which is partly consistent with CAPM''')
                    ])
                ],className = "five columns" ),

                html.Div([
                    html.H6('Performance Analysis', className = "gs-header gs-table-header padded"),
                    html.Table( make_dash_table( df_performance_analysis2))
                ],className = "seven columns" ),
            ], className = "row "),

            html.Div([
                html.Div([
                    html.H6('Summary', className = "gs-header gs-text-header padded"),
                    html.P('''Both backtests prove that, PCA factor model can effectively increase the accuracy of estimation of
                    covariance matrix. Then it helps construct more efficient portfolio following the theory of Modern Portfolio Theory.'''),
                    html.Strong('''
                    One thing that really interests me, is, because both factor loadings and factor prices are estimated from data, the historical 
                    factor prices are being updated once new data is incorporated into model. So, if simply pick a point in past, there is no
                    certain factor price. It's like the histroy is being changed because of today's information. This is also the 
                    biggest difference compared with other factor models.
                    ''')
                ],className = "twelve columns" ),
            ], className = "row "),

            html.Div([
                html.Div([
                    html.H6('Additional Information', className = "gs-header gs-text-header padded"),
                    html.P([
                        'Detailed explanation of how the PCA factor model is constructed from scratch can be found here:',
                        html.A(['https://wenkaicui.com/2018/09/30/principle-component-analysis-in-finance/'], \
                        href='https://wenkaicui.com/2018/09/30/principle-component-analysis-in-finance/')
                    ]),
                    html.P([html.P('Source Code can be found here:'),
                        html.A(['https://github.com/WenkaiCUi/PCA-and-Factor-Model'], \
                            href='https://github.com/WenkaiCUi/PCA-and-Factor-Model')
                    ]),
                    
                    html.P([html.P('Feel free to contact me at wkcui@bu.edu')])
                ],className = "twelve columns" ),
            ], className = "row ")

        ], className = "subpage" ),

    ], className = "page" )
])



external_css = [ "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({ "external_url": css })

external_js = [ "https://code.jquery.com/jquery-3.2.1.min.js",
        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js" ,
        'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=default']

for js in external_js:
    app.scripts.append_script({ "external_url": js })

if __name__ == '__main__':
	app.server.run(debug=True)
