import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def load_data(kind="category"):
    fn = "processed_vehicle_type.csv" if kind == "category" else "processed_manufacturer.csv"
    path = f"data/{fn}"
    if not os.path.exists(path):
        return pd.DataFrame()  # Return empty DataFrame if file missing
    df = pd.read_csv(path, parse_dates=["date"])
    df["date"] = pd.to_datetime(df["date"])  # Ensure pandas datetime64[ns]
    return df

def plot_trend(df, x, y, color):
    if df.empty:
        return go.Figure()  # Return empty figure if no data
    fig = px.line(df, x=x, y=y, color=color, markers=True,
                  title="Registrations & Growth")
    fig.update_layout(hovermode="x unified")
    return fig