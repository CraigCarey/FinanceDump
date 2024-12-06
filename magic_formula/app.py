import pandas as pd
import streamlit as st
import pickle

st.set_page_config(page_title="Magic Formula & Acquirer's Multiple Screener",
                   page_icon=":bar_chart:", layout="wide")


@st.cache_data
def load_data():
    mf_am_datafile = '../data/all_mf_am_230430_processed.pkl'
    with open(mf_am_datafile, 'rb') as file:
        mf_am_df = pickle.load(file)

    return mf_am_df


df = load_data()

all_exchanges = sorted(df["exchange"].unique())
all_symbols = sorted(df["symbol"].unique())

# ---- SIDEBAR ----
st.sidebar.header("Screening Options")
exchanges = st.sidebar.multiselect(
    label="Exchanges:",
    options=all_exchanges,
    default=all_exchanges
)

# exclude_industries = st.sidebar.multiselect(
#     label="Industries to exclude:",
#     options=["Banking", "Utilities"],
#     default=["Banking", "Utilities"],
# )

include_companies = st.sidebar.multiselect(
    label="Companies to include:",
    options=all_symbols,
    default=[],
)

exclude_companies = st.sidebar.multiselect(
    label="Companies to exclude:",
    options=all_symbols,
    default=[],
)

min_mc = st.sidebar.slider(
    label="Min Market Cap (m)",
    min_value=0,
    max_value=1000,
    value=200
) * 1e6

# df_selection = df.query(
#     "City == @city & Customer_type ==@customer_type & Gender == @gender"
# )

# ---- MAINPAGE ----
st.title("Magic Formula & Acquirer's Multiple Screener")
st.markdown("##")

if len(include_companies):
    df_selection = df.query(
        "market_cap > @min_mc & exchange in @exchanges & symbol in @include_companies"
    )
else:
    df_selection = df.query(
        "market_cap > @min_mc & exchange in @exchanges & symbol not in @exclude_companies"
    )

df_selection = df_selection.drop(
    'market_cap', axis=1).sort_values(by=['mf_am_rank']).reset_index(drop=True)
df_selection.index += 1

st.dataframe(
    # data=df.loc[(df['market_cap'] >= min_mc * 1e6)].reset_index(),
    data=df_selection,
    height=1200,
    use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
