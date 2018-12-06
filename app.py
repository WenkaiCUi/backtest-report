import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html


df_backtest_parameters_table1 = pd.read_csv('data/backtest_parameters_table1.csv')





app = dash.Dash(__name__)
server = app.server


def make_dash_table( df ):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for _, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append( html.Td([ row[i] ]) )
        table.append( html.Tr( html_row ) )
    return table




app.layout = html.Div([

    html.Div([ # page 1

        html.Div([
            'For Theory in Detail & Source Code:',
            html.A(['https://wenkaicui.com/2018/09/30/principle-component-analysis-in-finance/'],href='https://wenkaicui.com/2018/09/30/principle-component-analysis-in-finance/')
        ],style=dict(position="absolute", top=-20, left=0)),

        html.A([ 'Print PDF' ],
           className="button no-print",
           style=dict(position="absolute", top=-40, right=0)),


        html.Div([ # subpage 1

            # Row 1 (Header)

            html.Div([

                html.Div([
                    html.H5('Principle Component Analysis Factor Model Backtesting Report'),
                    html.H6('Based on Modern Portfolio Theory', style=dict(color='#7F90AC')),
                    ], className = "nine columns padded" ),

                html.Div([
                    html.H1([html.Span('12', style=dict(opacity=0.5)), html.Span('05')]),
                    html.H6('Wenkai Cui')
                ], className = "three columns gs-header gs-accent-header padded", style=dict(float='right') ),

            ], className = "row gs-header gs-text-header"),

            html.Br([]),

            # Row 2

            html.Div([

                html.Div([
                    html.H6('Model Explained', className = "gs-header gs-text-header padded"),

                    html.Strong('Principle Component Analysis:'),
                    html.P(r'''
                    $$ \Omega = P\Lambda P^{T} = P\Lambda^{0.5} \Lambda^{0.5}  (P)^{T} = \beta \beta ^T  $$
                    ''',style={'font-size':'7px'}),

                    html.Strong('Orthogonal Factor Model:'),
                    html.P('''The returns are driven by a constant mean and multiple factors and idiosyncratic random term. 
                    The factors are uncorrelated to each other, which means the returns are driven by independent factors. 
                    The  idiosyncratic terms could be related to each other. '''),
                    html.P(r'''
                    $$ R_i = \alpha_i + \sum_{j=1}^m \beta_{ij}F_j + \epsilon_i \hspace{0.5cm} \Omega=\beta E(FF^T) \beta^T+ E(\epsilon \epsilon^T) = \beta \beta^T + D $$
                    ''',style={'font-size':'7px'}),

                    html.P('The factor loadings are estimated by PCA, then a second pass regression is used to estimate factors.'),

                ], className = "six columns" ),

                html.Div([
                    html.H6(["Modern Portfolio Theory & Backtesting"],
                            className = "gs-header gs-table-header padded"),
                    html.P('''The purpose of our factor model is to reduce the estimation error in covariance matrix. Calculate '''),

                    html.Li('Sample Covariance Matrix '),
                    html.Li('Factor Constrained Covariance Matrix, by'),

                    html.P(r'$$ \Omega_{FC} = \hat\beta \Omega_F \hat\beta^T + D $$',style={'font-size':'7px'}),
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
                        html.Strong('Backtesting Parameters:'),
                        html.Table( make_dash_table( df_backtest_parameters_table1)),
                        html.Strong('Result Summary:'),
                        html.P('The goal of MVP is to minimize variance as much as possible, ignoring the cost of return. ')

                ],className = "four columns"),

                html.Div([
                    html.Iframe(src='https://plot.ly/~cuiwk0320/2.embed?modebar=false&link=false', \
                             style=dict(border=0), width="100%", height="250"),
                    html.Iframe(src='https://plot.ly/~cuiwk0320/4.embed?modebar=false&link=false', \
                             style=dict(border=0), width="100%", height="250")
                ],className = "eight columns")
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
