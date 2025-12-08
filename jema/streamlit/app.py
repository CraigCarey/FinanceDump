import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="JEMA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# Force light theme
st.markdown(
    """
    <script>
        var stApp = window.parent.document.querySelector('.stApp');
        if (stApp) {
            stApp.classList.remove('dark');
            stApp.classList.add('light');
        }
    </script>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Column definitions
description_col = "Security Description"
security_col = "Security No."
symbol_col = "Symbol"
holding_col = "Holding"
market_value_col = "Market Value"
percent_col = "% of Fund"
exchange_col = "Exchange"
currency_col = "Currency"
conversion_col = "Conv Rate"
sp_lc_col = "SP LC"
sp_gbp_col = "SP GBP"
holding_gbp_col = "Holding GBP"
nav_gbp_col = "NAV GBP"


# Load data
@st.cache_data
def load_data():
    json_filename = "jema_data.json"
    with open(json_filename, "r") as json_file:
        data = json.load(json_file)

    df = pd.read_csv("jema_holdings.csv")
    df = df.drop(
        columns=[security_col, conversion_col, market_value_col], errors="ignore"
    )

    return data, df


data, df = load_data()

# Header
st.markdown('<h1 class="main-header">JEMA NAV Dashboard</h1>', unsafe_allow_html=True)

# Parse timestamp
try:
    data_timestamp = datetime.fromisoformat(data["data_timestamp"])
    st.caption(f"Data last updated: {data_timestamp.strftime('%B %d, %Y at %H:%M:%S')}")
except:
    st.caption(f"Data last updated: {data.get('data_timestamp', 'N/A')}")

st.divider()

# Key Metrics Section
st.subheader("Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total NAV ", value=f"£{data['total_nav_gbp']:.2f}", delta=None)

with col2:
    st.metric(label="Equity NAV ", value=f"£{data['equity_nav_gbp']:.2f}", delta=None)

with col3:
    st.metric(
        label="S Account per Share",
        value=f"£{data['s_account_divs_per_share']:.2f}",
        delta=None,
    )

with col4:
    st.metric(label="JEMA Price", value=f"£{data['jema_price']:.2f}", delta=None)

st.divider()

# Holdings breakdown
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        label="Total Holdings + Divs ",
        value=f"£{data['total_holding_gbp'] + data['s_account_divs_now_gbp']:,.0f}",
        delta=None,
    )

with col6:
    st.metric(
        label="Russian Holdings",
        value=f"£{data['total_holding_rus']:,.0f}",
        delta=None,
    )

with col7:
    st.metric(
        label="Non-Russian Holdings",
        value=f"£{data['total_holding_non']:,.0f}",
        delta=None,
    )

with col8:
    st.metric(
        label="S Account Dividends ",
        value=f"£{data['s_account_divs_now_gbp']:,.0f}",
        delta=None,
    )


st.divider()

# Visualizations
st.subheader("📈 Portfolio Analytics")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Holdings Breakdown",
        "Currency Distribution",
        "Exchange Distribution",
        "Top Holdings",
    ]
)

with tab1:
    # Holdings pie chart
    holdings_data = pd.DataFrame(
        {
            "Category": [
                "Russian Holdings",
                "Non-Russian Holdings",
                "S Account Dividends",
            ],
            "Value": [
                data["total_holding_rus"],
                data["total_holding_non"],
                data["s_account_divs_now_gbp"],
            ],
        }
    )

    fig_pie = px.pie(
        holdings_data,
        values="Value",
        names="Category",
        title="Portfolio Holdings Distribution",
        color_discrete_sequence=["#FF6B6B", "#4ECDC4"],
        hole=0.4,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(font=dict(size=14), showlegend=True, height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    # Currency distribution
    currency_dist = df.groupby(currency_col)[holding_gbp_col].sum().reset_index()
    currency_dist = currency_dist.sort_values(holding_gbp_col, ascending=False)

    fig_currency = px.bar(
        currency_dist,
        x=currency_col,
        y=holding_gbp_col,
        title="Holdings by Currency ",
        labels={holding_gbp_col: "Holdings ", currency_col: "Currency"},
        color=holding_gbp_col,
        color_continuous_scale="Viridis",
    )
    fig_currency.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_currency, use_container_width=True)

with tab3:
    # Exchange distribution
    exchange_dist = df.groupby(exchange_col)[holding_gbp_col].sum().reset_index()
    exchange_dist = exchange_dist.sort_values(holding_gbp_col, ascending=False)

    fig_exchange = px.bar(
        exchange_dist,
        x=exchange_col,
        y=holding_gbp_col,
        title="Holdings by Exchange ",
        labels={holding_gbp_col: "Holdings ", exchange_col: "Exchange"},
        color=holding_gbp_col,
        color_continuous_scale="Blues",
    )
    fig_exchange.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_exchange, use_container_width=True)

with tab4:
    # Top 10 holdings
    top_holdings = df.nlargest(10, holding_gbp_col)[
        [description_col, symbol_col, holding_gbp_col, currency_col, exchange_col]
    ]

    fig_top = px.bar(
        top_holdings,
        x=holding_gbp_col,
        y=description_col,
        orientation="h",
        title="Top 10 Holdings by Value ",
        labels={holding_gbp_col: "Holdings ", description_col: "Security"},
        color=holding_gbp_col,
        color_continuous_scale="Reds",
    )
    fig_top.update_layout(
        showlegend=False, height=500, yaxis={"categoryorder": "total ascending"}
    )
    st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# Detailed Holdings Table
st.subheader("📋 Detailed Holdings")

# Add search and filter options in sidebar
with st.sidebar:
    st.header("🔍 Filters")

    # Currency filter
    currencies = ["All"] + sorted(df[currency_col].unique().tolist())
    selected_currency = st.selectbox("Currency", currencies)

    # Exchange filter
    exchanges = ["All"] + sorted(df[exchange_col].unique().tolist())
    selected_exchange = st.selectbox("Exchange", exchanges)

    # Search box
    search_term = st.text_input("Search Securities", "")

    # Sort by
    sort_by = st.selectbox(
        "Sort by", [holding_gbp_col, sp_gbp_col, holding_col, description_col], index=0
    )
    sort_order = st.radio("Order", ["Descending", "Ascending"])

# Apply filters
filtered_df = df.copy()

if selected_currency != "All":
    filtered_df = filtered_df[filtered_df[currency_col] == selected_currency]

if selected_exchange != "All":
    filtered_df = filtered_df[filtered_df[exchange_col] == selected_exchange]

if search_term:
    filtered_df = filtered_df[
        filtered_df[description_col].str.contains(search_term, case=False, na=False)
        | filtered_df[symbol_col].str.contains(search_term, case=False, na=False)
    ]

# Sort
ascending = sort_order == "Ascending"
filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

# Format numeric columns for display
display_df = filtered_df.copy()
for col in [holding_gbp_col, sp_gbp_col, sp_lc_col]:
    if col in display_df.columns:
        display_df[col] = display_df[col].apply(
            lambda x: f"£{x:,.2f}" if pd.notna(x) else "N/A"
        )

if holding_col in display_df.columns:
    display_df[holding_col] = display_df[holding_col].apply(
        lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"
    )

# Display metrics about filtered data
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Total Securities", len(filtered_df))
with col_b:
    total_value = filtered_df[holding_gbp_col].sum()
    st.metric("Total Value ", f"£{total_value:,.2f}")
with col_c:
    if len(df) > 0:
        percentage = (len(filtered_df) / len(df)) * 100
        st.metric("% of Portfolio", f"{percentage:.1f}%")

# Display the dataframe
st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)

# Download button
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name=f"jema_holdings_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)
