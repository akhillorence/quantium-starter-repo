import pandas as pd
from dash import Dash, html, dcc
from plotly.express import line

# Load the data
DATA_PATH = "./formatted_sales_data.csv"  # Changed from formatted_data.csv to your actual filename

try:
    data = pd.read_csv(DATA_PATH)
    print(f"✅ Data loaded successfully: {len(data)} rows")
except FileNotFoundError:
    print(f"❌ Error: {DATA_PATH} not found!")
    print("Please make sure formatted_sales_data.csv exists in the same directory.")
    print("If you need to generate it, run: python process_data.py")
    exit(1)

# Sort by date
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(by="date")

# Initialize dash app
dash_app = Dash(__name__)

# Create the line chart
line_chart = line(
    data, 
    x="date", 
    y="sales", 
    title="Pink Morsel Sales",
    labels={"sales": "Sales ($)", "date": "Date"}
)

# Update layout for better appearance
line_chart.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    plot_bgcolor='white',
    height=500
)

# Create the visualization
visualization = dcc.Graph(
    id="visualization",
    figure=line_chart
)

# Create the header
header = html.H1(
    "Pink Morsel Sales Visualizer",
    id="header",
    style={
        'textAlign': 'center',
        'color': '#2c3e50',
        'fontFamily': 'Arial, sans-serif',
        'marginTop': '20px',
        'marginBottom': '30px'
    }
)

# Add a description
description = html.P(
    "Sales data visualization to analyze the impact of price increase on January 15, 2021",
    style={
        'textAlign': 'center',
        'color': '#7f8c8d',
        'fontFamily': 'Arial, sans-serif',
        'marginBottom': '30px'
    }
)

# Add a simple answer to the business question
# Calculate average sales before and after Jan 15, 2021
price_increase_date = pd.Timestamp('2021-01-15')
before_sales = data[data['date'] < price_increase_date]['sales'].mean()
after_sales = data[data['date'] >= price_increase_date]['sales'].mean()

if after_sales > before_sales:
    conclusion_text = f"✅ Sales were HIGHER after the price increase on January 15, 2021."
else:
    conclusion_text = f"❌ Sales were LOWER after the price increase on January 15, 2021."

conclusion = html.P(
    conclusion_text,
    style={
        'textAlign': 'center',
        'color': '#27ae60' if after_sales > before_sales else '#e74c3c',
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '18px',
        'fontWeight': 'bold',
        'marginTop': '30px',
        'padding': '15px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '8px',
        'width': '80%',
        'margin': '0 auto'
    }
)

# Define the app layout
dash_app.layout = html.Div(
    [
        header,
        description,
        visualization,
        conclusion
    ],
    style={'padding': '20px'}
)

# Run the app
if __name__ == '__main__':
    print("🚀 Starting Pink Morsel Sales Visualizer...")
    print("🌐 Open your browser and go to: http://127.0.0.1:8050")
    dash_app.run(debug=True)