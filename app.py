import streamlit as st

pg = st.navigation([
    st.Page('search_stock.py', title='종목 검색', icon='🔍'),
    st.Page('analyze_report.py', title='보고서 분석', icon='📊'),
])
pg.run()