from pathlib import Path
import pandas as pd
from pandas import DataFrame
import streamlit as st


if __name__ == "__main__":
    data_path = Path('/home/malaarabiou/Programming_Projects/Pycharm_Projects/ArXiv_Papers_Matching/results/xrl/data.csv')
    data: DataFrame = pd.read_csv(data_path)
    st.dataframe(data)
