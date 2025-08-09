import streamlit as st
from utils.helpers import load_data, plot_trend
import pandas as pd

st.set_page_config(page_title="Vahan Investor Dashboard", layout="wide")
st.title("🚗 Vahan Registration Dashboard")

tab1, tab2 = st.tabs(["By Vehicle Category", "By Manufacturer"])

with tab1:
    df = load_data("category")
    cats = st.multiselect("Select vehicle categories", df["category"].unique(), default=list(df["category"].unique()))
    rng = st.date_input("Date range", [df["date"].min(), df["date"].max()])
    rng = [pd.to_datetime(rng[0]), pd.to_datetime(rng[1])]
    filt = df[df["category"].isin(cats) & df["date"].between(*rng)]
    st.plotly_chart(plot_trend(filt,"date","registrations","category"), use_container_width=True)
    st.dataframe(filt.tail(20))

with tab2:
    df = load_data("manufacturer")
    if df.empty or "manufacturer" not in df.columns:
        st.warning("No manufacturer data available.")
    else:
        mfgs = st.multiselect("Select manufacturers", df["manufacturer"].unique()[:20],
                              default=df["manufacturer"].unique()[:5])
        rng = st.date_input("Date range ", [df["date"].min(), df["date"].max()], key="mfg_rng")
        rng = [pd.to_datetime(rng[0]), pd.to_datetime(rng[1])]
        filt = df[df["manufacturer"].isin(mfgs) & df["date"].between(*rng)]
        st.plotly_chart(plot_trend(filt,"date","registrations","manufacturer"), use_container_width=True)
        st.dataframe(filt.tail(20))