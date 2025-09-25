from nicegui import ui
import pandas as pd
import plotly.express as px
import random

# --- SAMPLE DATA ---
def create_data():
    categories = ['A', 'B', 'C', 'D']
    data = {
        'Category': [random.choice(categories) for _ in range(100)],  # Random category
        'Value': [random.randint(10, 100) for _ in range(100)],       # Random value
    }
    return pd.DataFrame(data)

df = create_data()

# --- DASHBOARD HEADER ---
with ui.header().classes('items-center justify-between bg-blue-500 text-white p-2'):
    ui.label('📊 Interactive Data Dashboard').classes('text-xl font-bold')

# --- LAYOUT WITH SIDEBAR ---
with ui.row().classes('w-full h-screen'):
    # Sidebar column
    with ui.column().classes('w-1/5 bg-gray-100 p-3 space-y-3'):
        ui.label('⚙️ Filters').classes('text-lg font-semibold')

        # Dropdown filter (full width)
        category_filter = ui.select(
            options=['All'] + sorted(df['Category'].unique().tolist()),  # Options: All + categories
            value='All',  # Default selection
            label='Select Category'
        ).classes('w-full')

    # Main content column
    with ui.column().classes('w-4/5 p-5 space-y-5'):
        # Display initial chart with all data
        chart_area = ui.plotly(px.histogram(df, x='Category', y='Value')).classes('w-full h-96')
        # Display initial table with all data
        table_area = ui.table(
            columns=[{'name': c, 'label': c, 'field': c} for c in df.columns],
            rows=df.to_dict('records')
        ).classes('w-full')

# --- INTERACTIVITY FUNCTION ---
def update_dashboard():
    filtered = df.copy()

    # Apply category filter
    if category_filter.value != 'All':
        filtered = filtered[filtered['Category'] == category_filter.value]

    # Update chart
    fig = px.histogram(
        filtered, x='Category', y='Value',
        color='Category', title='Category Value Distribution'
    )
    chart_area.figure = fig  # Assign new figure
    chart_area.update()      # Refresh chart

    # Update table → show only filtered data
    table_area.rows = filtered.to_dict('records')
    table_area.update()

# Bind dropdown change to update function
category_filter.on('update:model-value', lambda e: update_dashboard())

# Run the NiceGUI app
ui.run()
