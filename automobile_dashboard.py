# =============================================================================
# Final Assignment: Part 2 - Create Dashboard with Plotly and Dash
# XYZAutomotives – Automobile Sales Dashboard
# =============================================================================

import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Generate / Load Dataset ──────────────────────────────────────────────────
np.random.seed(42)
years = list(range(1980, 2024))
recession_years = [1980, 1981, 1982, 1991, 2000, 2001, 2002, 2007, 2008, 2009, 2020]
vehicle_types   = ['Supperminicar', 'Small family car', 'Medium family car',
                   'Executive car', 'Sports', 'Luxury']

records = []
for year in years:
    is_recession = 1 if year in recession_years else 0
    for month in range(1, 13):
        base_sales = 35000 if not is_recession else 22000
        seasonal   = 5000 * np.sin((month - 3) * np.pi / 6)
        auto_sales = max(8000, base_sales + np.random.normal(0, 3000) + seasonal)
        gdp        = np.random.normal(2.5 if not is_recession else -1.2, 0.5)
        unemployment = np.random.normal(5.5 if not is_recession else 8.5, 0.8)

        for vtype in vehicle_types:
            vmult = {'Supperminicar': 1.2, 'Small family car': 1.0,
                     'Medium family car': 0.9, 'Executive car': 0.5,
                     'Sports': 0.4, 'Luxury': 0.3}[vtype]
            rec_impact = {'Supperminicar': 0.85, 'Small family car': 0.80,
                          'Medium family car': 0.75, 'Executive car': 0.50,
                          'Sports': 0.45, 'Luxury': 0.40}[vtype]
            v_sales = max(500, auto_sales * vmult * (rec_impact if is_recession else 1.0)
                          + np.random.normal(0, 500))
            price   = {'Supperminicar': 15000, 'Small family car': 22000,
                       'Medium family car': 30000, 'Executive car': 55000,
                       'Sports': 45000, 'Luxury': 80000}[vtype]
            price  += np.random.normal(0, price * 0.05)
            adv     = v_sales * price * np.random.uniform(0.01, 0.03)

            records.append({
                'Year': year, 'Month': month, 'Recession': is_recession,
                'Automobile_Sales': auto_sales, 'GDP': gdp,
                'Unemployment_Rate': unemployment, 'Vehicle_Type': vtype,
                'Vehicle_Sales': v_sales, 'Advertising_Expenditure': adv,
                'Price': price,
                'Seasonality_Weight': seasonal / 10000 + 1,
                'Consumer_Confidence': np.random.normal(90 if not is_recession else 60, 10),
            })

df = pd.DataFrame(records)

# ── 4.1  Create the Dash Application with a meaningful title ─────────────────
app = dash.Dash(__name__)
app.title = "XYZAutomotives – Automobile Sales Dashboard"

# ── Dropdown options ──────────────────────────────────────────────────────────
statistics_options = [
    {'label': 'Recession Report Statistics',  'value': 'Recession'},
    {'label': 'Yearly Report Statistics',     'value': 'Yearly'},
]

year_options = [{'label': str(y), 'value': y} for y in sorted(df['Year'].unique())]

# ── 4.2 / 4.3  Layout: dropdowns + output divisions ──────────────────────────
app.layout = html.Div(
    className='main-container',
    children=[

        # ── Header ────────────────────────────────────────────────────────────
        html.Div(
            className='header',
            children=[
                html.H1(
                    "XYZAutomotives – Automobile Sales Dashboard",
                    style={'color': '#FFFFFF', 'textAlign': 'center',
                           'margin': '0', 'padding': '20px 0',
                           'fontFamily': 'Arial, sans-serif', 'fontSize': '26px'}
                ),
                html.P(
                    "Explore how recessions, GDP, unemployment, and seasonality affect automobile sales (1980–2023)",
                    style={'color': '#AECBFA', 'textAlign': 'center',
                           'margin': '0 0 10px 0', 'fontFamily': 'Arial, sans-serif',
                           'fontSize': '14px'}
                ),
            ],
            style={'backgroundColor': '#0B1D3A', 'padding': '10px 20px'}
        ),

        # ── Controls Row ───────────────────────────────────────────────────────
        html.Div(
            className='controls-row',
            children=[

                # 4.2a: Statistics type dropdown
                html.Div([
                    html.Label("Select Statistics Type",
                               style={'fontWeight': 'bold', 'color': '#0B1D3A',
                                      'fontFamily': 'Arial', 'marginBottom': '6px',
                                      'display': 'block'}),
                    dcc.Dropdown(
                        id='dropdown-statistics',
                        options=statistics_options,
                        value='Recession',
                        placeholder='Select a report type',
                        clearable=False,
                        style={'fontFamily': 'Arial', 'fontSize': '14px'}
                    ),
                ], style={'width': '40%', 'marginRight': '20px'}),

                # 4.2b: Year dropdown (enabled only for Yearly report)
                html.Div([
                    html.Label("Select Year  (Yearly Report only)",
                               style={'fontWeight': 'bold', 'color': '#0B1D3A',
                                      'fontFamily': 'Arial', 'marginBottom': '6px',
                                      'display': 'block'}),
                    dcc.Dropdown(
                        id='select-year',
                        options=year_options,
                        value=2008,
                        placeholder='Select a year',
                        clearable=False,
                        style={'fontFamily': 'Arial', 'fontSize': '14px'}
                    ),
                ], style={'width': '30%'}),

            ],
            style={'display': 'flex', 'alignItems': 'flex-end',
                   'padding': '20px 30px', 'backgroundColor': '#F4F7FF',
                   'borderBottom': '2px solid #D1D5DB'}
        ),

        # ── 4.3  Output division ───────────────────────────────────────────────
        html.Div(
            id='output-container',
            className='output-container',
            children=[],
            style={'padding': '20px 30px', 'backgroundColor': '#FFFFFF',
                   'minHeight': '600px'}
        ),

        # ── Footer ─────────────────────────────────────────────────────────────
        html.Div(
            children=[
                html.P("XYZAutomotives Data Science Dashboard  |  IBM Data Science Capstone  |  2024–2025",
                       style={'textAlign': 'center', 'color': '#6B8DD6',
                              'fontFamily': 'Arial', 'fontSize': '12px', 'margin': '0'})
            ],
            style={'backgroundColor': '#0B1D3A', 'padding': '12px'}
        ),
    ]
)


# ── 4.4  Callback: enable/disable year dropdown based on selected statistic ───
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    """
    4.4 – Update the input container (year dropdown) based on the selected
    statistics type. Year selector is only relevant for the Yearly report.
    """
    if selected_statistics == 'Yearly':
        return False   # enable
    return True        # disable for Recession report


# ── 4.4 / 4.5 / 4.6  Main callback: render charts into output container ──────
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    """
    4.4 – Main callback that updates the output container with the appropriate
          charts based on the selected statistics type and year.
    4.5 – Displays Recession Report Statistics graphs.
    4.6 – Displays Yearly Report Statistics graphs.
    """

    # ── Common colour palette ────────────────────────────────────────────────
    COLORS = ['#1A56DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C']
    CHART_BG = '#F8FAFF'

    def chart_title_style():
        return {'textAlign': 'center', 'color': '#0B1D3A',
                'fontFamily': 'Arial', 'fontSize': '15px',
                'fontWeight': 'bold', 'marginBottom': '4px'}

    def section_heading(text):
        return html.H3(text, style={'color': '#1A56DB', 'fontFamily': 'Arial',
                                    'fontSize': '20px', 'borderBottom': '2px solid #1A56DB',
                                    'paddingBottom': '6px', 'marginTop': '10px'})

    # ════════════════════════════════════════════════════════════════════════
    # 4.5  RECESSION REPORT STATISTICS
    # ════════════════════════════════════════════════════════════════════════
    if selected_statistics == 'Recession':

        rec_df = df[df['Recession'] == 1]

        # ── Chart R1: Average Automobile Sales by Year (Recession) ────────────
        r1_data = rec_df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig_r1 = px.line(
            r1_data, x='Year', y='Automobile_Sales',
            title='Average Automobile Sales During Recession Years',
            markers=True, color_discrete_sequence=['#E74C3C']
        )
        fig_r1.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Year', yaxis_title='Avg Automobile Sales',
            font=dict(family='Arial', size=12)
        )

        # ── Chart R2: Average Vehicles Sold by Vehicle Type (Recession) ───────
        r2_data = rec_df.groupby('Vehicle_Type')['Vehicle_Sales'].mean().reset_index()
        fig_r2 = px.bar(
            r2_data, x='Vehicle_Type', y='Vehicle_Sales',
            title='Average Vehicles Sold by Type During Recessions',
            color='Vehicle_Type', color_discrete_sequence=COLORS,
            text_auto='.0f'
        )
        fig_r2.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Vehicle Type', yaxis_title='Avg Sales',
            showlegend=False, font=dict(family='Arial', size=12)
        )
        fig_r2.update_xaxes(tickangle=-20)

        # ── Chart R3: Pie – Overall Automobile Sales Share by Vehicle Type ────
        r3_data = rec_df.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
        fig_r3 = px.pie(
            r3_data, names='Vehicle_Type', values='Automobile_Sales',
            title='Share of Total Sales by Vehicle Type (Recession)',
            color_discrete_sequence=COLORS, hole=0.35
        )
        fig_r3.update_layout(font=dict(family='Arial', size=12))
        fig_r3.update_traces(textposition='inside', textinfo='percent+label')

        # ── Chart R4: Bar – Effect of Unemployment on Vehicle Sales ───────────
        r4_data = rec_df.groupby('Vehicle_Type').agg(
            Unemployment_Rate=('Unemployment_Rate', 'mean'),
            Vehicle_Sales=('Vehicle_Sales', 'mean')
        ).reset_index()
        fig_r4 = px.bar(
            r4_data, x='Vehicle_Type', y='Unemployment_Rate',
            title='Avg Unemployment Rate by Vehicle Type During Recessions',
            color='Vehicle_Sales', color_continuous_scale='RdYlGn',
            text_auto='.2f'
        )
        fig_r4.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Vehicle Type', yaxis_title='Avg Unemployment Rate (%)',
            coloraxis_colorbar=dict(title='Avg Sales'),
            font=dict(family='Arial', size=12)
        )
        fig_r4.update_xaxes(tickangle=-20)

        # ── Chart R5: Scatter – Vehicle Price vs Sales During Recession ───────
        r5_data = rec_df.groupby('Vehicle_Type').agg(
            Avg_Price=('Price', 'mean'),
            Avg_Sales=('Vehicle_Sales', 'mean')
        ).reset_index()
        fig_r5 = px.scatter(
            r5_data, x='Avg_Price', y='Avg_Sales',
            color='Vehicle_Type', size='Avg_Sales',
            title='Vehicle Price vs Sales Volume (Recession Periods)',
            color_discrete_sequence=COLORS, trendline='ols'
        )
        fig_r5.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Average Price ($)', yaxis_title='Average Sales',
            font=dict(family='Arial', size=12)
        )

        # ── Chart R6: Line – GDP Trend During Recession Years ─────────────────
        r6_data = rec_df.groupby('Year')['GDP'].mean().reset_index()
        fig_r6 = px.line(
            r6_data, x='Year', y='GDP',
            title='GDP Growth Rate During Recession Years',
            markers=True, color_discrete_sequence=['#9B59B6']
        )
        fig_r6.add_hline(y=0, line_dash='dash', line_color='black', opacity=0.5)
        fig_r6.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Year', yaxis_title='GDP Growth Rate (%)',
            font=dict(family='Arial', size=12)
        )

        # ── Assemble Recession layout ─────────────────────────────────────────
        return [
            section_heading("📉 Recession Report Statistics"),

            html.Div([
                html.Div([html.P("Avg Automobile Sales by Year", style=chart_title_style()),
                          dcc.Graph(figure=fig_r1)],
                         style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([html.P("Avg Sales by Vehicle Type", style=chart_title_style()),
                          dcc.Graph(figure=fig_r2)],
                         style={'width': '48%', 'display': 'inline-block',
                                'verticalAlign': 'top', 'marginLeft': '3%'}),
            ]),

            html.Div([
                html.Div([html.P("Sales Share by Vehicle Type", style=chart_title_style()),
                          dcc.Graph(figure=fig_r3)],
                         style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([html.P("Unemployment Rate Effect on Sales", style=chart_title_style()),
                          dcc.Graph(figure=fig_r4)],
                         style={'width': '48%', 'display': 'inline-block',
                                'verticalAlign': 'top', 'marginLeft': '3%'}),
            ]),

            html.Div([
                html.Div([html.P("Vehicle Price vs Sales (Recession)", style=chart_title_style()),
                          dcc.Graph(figure=fig_r5)],
                         style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([html.P("GDP Growth During Recession Years", style=chart_title_style()),
                          dcc.Graph(figure=fig_r6)],
                         style={'width': '48%', 'display': 'inline-block',
                                'verticalAlign': 'top', 'marginLeft': '3%'}),
            ]),
        ]

    # ════════════════════════════════════════════════════════════════════════
    # 4.6  YEARLY REPORT STATISTICS
    # ════════════════════════════════════════════════════════════════════════
    elif selected_statistics == 'Yearly':

        if input_year is None:
            return [html.P("Please select a year from the dropdown above.",
                           style={'color': '#E74C3C', 'fontFamily': 'Arial',
                                  'fontSize': '16px', 'textAlign': 'center',
                                  'marginTop': '60px'})]

        year_df = df[df['Year'] == input_year]
        is_rec  = year_df['Recession'].iloc[0] == 1
        rec_tag = "⚠️ Recession Year" if is_rec else "✅ Non-Recession Year"
        tag_col = '#E74C3C' if is_rec else '#27AE60'

        # ── Chart Y1: Line – Monthly Automobile Sales for Selected Year ───────
        y1_data = year_df.groupby('Month')['Automobile_Sales'].mean().reset_index()
        month_names = ['Jan','Feb','Mar','Apr','May','Jun',
                       'Jul','Aug','Sep','Oct','Nov','Dec']
        y1_data['Month_Name'] = y1_data['Month'].apply(lambda x: month_names[x-1])
        fig_y1 = px.line(
            y1_data, x='Month_Name', y='Automobile_Sales',
            title=f'Monthly Automobile Sales – {input_year}',
            markers=True,
            color_discrete_sequence=['#1A56DB' if not is_rec else '#E74C3C']
        )
        fig_y1.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Month', yaxis_title='Automobile Sales',
            font=dict(family='Arial', size=12)
        )

        # ── Chart Y2: Bar – Monthly Advertising Expenditure ───────────────────
        y2_data = year_df.groupby('Month')['Advertising_Expenditure'].sum().reset_index()
        y2_data['Month_Name'] = y2_data['Month'].apply(lambda x: month_names[x-1])
        fig_y2 = px.bar(
            y2_data, x='Month_Name', y='Advertising_Expenditure',
            title=f'Total Monthly Advertising Expenditure – {input_year}',
            color_discrete_sequence=['#2ECC71']
        )
        fig_y2.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Month', yaxis_title='Advertising Spend ($)',
            showlegend=False, font=dict(family='Arial', size=12)
        )

        # ── Chart Y3: Pie – Vehicle Sales Distribution by Type ────────────────
        y3_data = year_df.groupby('Vehicle_Type')['Vehicle_Sales'].sum().reset_index()
        fig_y3 = px.pie(
            y3_data, names='Vehicle_Type', values='Vehicle_Sales',
            title=f'Vehicle Sales Distribution by Type – {input_year}',
            color_discrete_sequence=COLORS, hole=0.3
        )
        fig_y3.update_layout(font=dict(family='Arial', size=12))
        fig_y3.update_traces(textposition='inside', textinfo='percent+label')

        # ── Chart Y4: Bar – Total Ad Expenditure by Vehicle Type ──────────────
        y4_data = year_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig_y4 = px.bar(
            y4_data, x='Vehicle_Type', y='Advertising_Expenditure',
            title=f'Total Advertising Expenditure by Vehicle Type – {input_year}',
            color='Vehicle_Type', color_discrete_sequence=COLORS,
            text_auto='.2s'
        )
        fig_y4.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Vehicle Type', yaxis_title='Ad Expenditure ($)',
            showlegend=False, font=dict(family='Arial', size=12)
        )
        fig_y4.update_xaxes(tickangle=-20)

        # ── Chart Y5: Line – GDP for Selected Year across Months ──────────────
        y5_data = year_df.groupby('Month')['GDP'].mean().reset_index()
        y5_data['Month_Name'] = y5_data['Month'].apply(lambda x: month_names[x-1])
        fig_y5 = px.line(
            y5_data, x='Month_Name', y='GDP',
            title=f'Monthly GDP Growth Rate – {input_year}',
            markers=True, color_discrete_sequence=['#F39C12']
        )
        fig_y5.add_hline(y=0, line_dash='dash', line_color='black', opacity=0.4)
        fig_y5.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Month', yaxis_title='GDP Growth Rate (%)',
            font=dict(family='Arial', size=12)
        )

        # ── Chart Y6: Line – Unemployment Rate across Months ──────────────────
        y6_data = year_df.groupby('Month')['Unemployment_Rate'].mean().reset_index()
        y6_data['Month_Name'] = y6_data['Month'].apply(lambda x: month_names[x-1])
        fig_y6 = px.line(
            y6_data, x='Month_Name', y='Unemployment_Rate',
            title=f'Monthly Unemployment Rate – {input_year}',
            markers=True, color_discrete_sequence=['#9B59B6']
        )
        fig_y6.update_layout(
            plot_bgcolor=CHART_BG, paper_bgcolor='white',
            xaxis_title='Month', yaxis_title='Unemployment Rate (%)',
            font=dict(family='Arial', size=12)
        )

        # ── Assemble Yearly layout ────────────────────────────────────────────
        return [
            section_heading(f"📊 Yearly Report Statistics – {input_year}"),

            html.Div([
                html.Span(rec_tag, style={'backgroundColor': tag_col,
                                          'color': 'white', 'padding': '5px 14px',
                                          'borderRadius': '12px', 'fontFamily': 'Arial',
                                          'fontSize': '13px', 'fontWeight': 'bold'})
            ], style={'marginBottom': '16px'}),

            html.Div([
                html.Div([html.P(f"Monthly Auto Sales – {input_year}", style=chart_title_style()),
                          dcc.Graph(figure=fig_y1)],
                         style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([html.P(f"Monthly Ad Expenditure – {input_year}", style=chart_title_style()),
                          dcc.Graph(figure=fig_y2)],
                         style={'width': '48%', 'display': 'inline-block',
                                'verticalAlign': 'top', 'marginLeft': '3%'}),
            ]),

            html.Div([
                html.Div([html.P(f"Sales by Vehicle Type – {input_year}", style=chart_title_style()),
                          dcc.Graph(figure=fig_y3)],
                         style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([html.P(f"Ad Spend by Vehicle Type – {input_year}", style=chart_title_style()),
                          dcc.Graph(figure=fig_y4)],
                         style={'width': '48%', 'display': 'inline-block',
                                'verticalAlign': 'top', 'marginLeft': '3%'}),
            ]),

            html.Div([
                html.Div([html.P(f"Monthly GDP – {input_year}", style=chart_title_style()),
                          dcc.Graph(figure=fig_y5)],
                         style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([html.P(f"Monthly Unemployment – {input_year}", style=chart_title_style()),
                          dcc.Graph(figure=fig_y6)],
                         style={'width': '48%', 'display': 'inline-block',
                                'verticalAlign': 'top', 'marginLeft': '3%'}),
            ]),
        ]

    return [html.P("Please select a statistics type from the dropdown.",
                   style={'textAlign': 'center', 'fontFamily': 'Arial',
                          'color': '#64748B', 'marginTop': '60px'})]


# ── Run the app ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=8050)
