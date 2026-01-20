import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load the data
DATA_PATH = "./formatted_sales_data.csv"

try:
    data = pd.read_csv(DATA_PATH)
    print(f"✅ Data loaded: {len(data)} rows")
except FileNotFoundError:
    print(f"❌ Error: {DATA_PATH} not found!")
    exit(1)

# Convert date to datetime and sort
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(by="date")

# Initialize Dash app
app = Dash(__name__)

# Simple and clean CSS
app.layout = html.Div([
    # Header with styling
    html.H1(
        "Pink Morsel Sales Dashboard",
        style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'marginTop': '20px',
            'marginBottom': '10px'
        }
    ),
    
    # Subtitle
    html.P(
        "Filter by region to analyze sales before/after Jan 15, 2021 price increase",
        style={
            'textAlign': 'center',
            'color': '#7f8c8d',
            'marginBottom': '30px'
        }
    ),
    
    # Region filter in a nice box
    html.Div([
        html.H4("Select Region:", style={'marginBottom': '15px', 'color': '#2c3e50'}),
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': '🌍 All Regions', 'value': 'all'},
                {'label': '❄️ North', 'value': 'north'},
                {'label': '☀️ South', 'value': 'south'},
                {'label': '🌅 East', 'value': 'east'},
                {'label': '🌄 West', 'value': 'west'}
            ],
            value='all',
            inline=True,
            labelStyle={
                'marginRight': '20px',
                'padding': '10px 20px',
                'backgroundColor': '#f0f8ff',
                'borderRadius': '20px',
                'border': '2px solid #3498db',
                'cursor': 'pointer'
            }
        )
    ], style={
        'backgroundColor': '#e8f4f8',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px auto',
        'maxWidth': '800px'
    }),
    
    # Chart
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={'margin': '20px auto', 'maxWidth': '1000px'}),
    
    # Statistics
    html.Div([
        html.H4("📊 Statistics", style={'color': '#2c3e50', 'marginBottom': '15px'}),
        html.Div(id='stats-display', style={'fontSize': '16px'})
    ], style={
        'backgroundColor': '#f9f9f9',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px auto',
        'maxWidth': '1000px'
    }),
    
    # Conclusion
    html.Div([
        html.H4("💡 Business Insight", style={'color': '#27ae60', 'marginBottom': '15px'}),
        html.Div(id='conclusion-display', style={'fontSize': '18px', 'fontWeight': 'bold'})
    ], style={
        'backgroundColor': '#f1f8e9',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px auto',
        'maxWidth': '1000px'
    })
])

# Callback to update everything
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('stats-display', 'children'),
     Output('conclusion-display', 'children')],
    [Input('region-radio', 'value')]
)
def update_dashboard(selected_region):
    # Filter data
    if selected_region == 'all':
        filtered_data = data
        region_label = "All Regions"
    else:
        filtered_data = data[data['region'] == selected_region]
        region_label = selected_region.capitalize() + " Region"
    
    # Group by date
    daily_sales = filtered_data.groupby('date')['sales'].sum().reset_index()
    
    # Create simple line chart WITHOUT add_vline
    fig = px.line(
        daily_sales, 
        x='date', 
        y='sales',
        title=f'Pink Morsel Sales - {region_label}',
        labels={'sales': 'Sales ($)', 'date': 'Date'}
    )
    
    # Customize chart
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=450,
        xaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            tickprefix='$'
        ),
        hovermode='x unified'
    )
    
    # Make line thicker
    fig.update_traces(
        line=dict(color='#3498db', width=3)
    )
    
    # Calculate statistics
    price_increase_date = pd.Timestamp('2021-01-15')
    before_data = filtered_data[filtered_data['date'] < price_increase_date]
    after_data = filtered_data[filtered_data['date'] >= price_increase_date]
    
    total_sales = filtered_data['sales'].sum()
    avg_sale = filtered_data['sales'].mean()
    before_avg = before_data['sales'].mean() if len(before_data) > 0 else 0
    after_avg = after_data['sales'].mean() if len(after_data) > 0 else 0
    
    # Create statistics
    stats = [
        html.P(f"📈 Total Sales: ${total_sales:,.0f}"),
        html.P(f"📊 Average Sale: ${avg_sale:,.2f}"),
        html.P(f"🔍 Number of Transactions: {len(filtered_data):,}"),
        html.P(f"📅 Before Jan 15, 2021: ${before_data['sales'].sum():,.0f} (${before_avg:,.2f} avg)"),
        html.P(f"📅 After Jan 15, 2021: ${after_data['sales'].sum():,.0f} (${after_avg:,.2f} avg)")
    ]
    
    # Create conclusion
    if len(before_data) > 0 and len(after_data) > 0:
        if after_avg > before_avg:
            percent_change = ((after_avg / before_avg) - 1) * 100
            conclusion = f"✅ Sales INCREASED by {percent_change:.1f}% after the price increase in {region_label.lower()}!"
            color = '#27ae60'
        else:
            percent_change = (1 - (after_avg / before_avg)) * 100
            conclusion = f"❌ Sales DECREASED by {percent_change:.1f}% after the price increase in {region_label.lower()}."
            color = '#e74c3c'
    else:
        conclusion = "⚠️ Not enough data to compare before and after the price increase."
        color = '#f39c12'
    
    conclusion_display = html.P(conclusion, style={'color': color})
    
    return fig, stats, conclusion_display

# Run the app
if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Pink Morsel Sales Dashboard")
    print("=" * 50)
    print("✅ Data loaded successfully")
    print("✅ Starting server at: http://127.0.0.1:8050")
    print("=" * 50)
    
    app.run(debug=True, port=8050)