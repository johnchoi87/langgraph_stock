from pprint import pprint

import streamlit as st

from stock_agent.agent import call_search_stock
from langchain_community.callbacks import StreamlitCallbackHandler
import matplotlib.pyplot as plt

st.title('종목 검색')

prompt = st.chat_input("이슈나 키워드를 입력하면 종목을 찾아드립니다.")
if prompt:
    graph = call_search_stock()
    print(prompt)
    inputs = {"messages": [("human", prompt)]}

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # StreamlitCallbackHandler 설정
        st_callback = StreamlitCallbackHandler(st.container())

        output_container = st.empty()

        # 그래프 실행
        with st.spinner("Processing..."):
            response = graph.invoke(inputs, {"callback": st_callback})

            # 최종 응답 표시
            print("=============== response ===============")
            pprint(response)
            print("=============== response ===============")
            related_stocks = response["related_stocks"]
            message_placeholder.markdown("연관 종목 결과")
            full_message = ""
            tickers = [stock.ticker for stock in related_stocks]
            for stock in related_stocks:
                stock_mesage = f'[{stock.ticker}] {stock.name}: {stock.description}'
                st.write(stock_mesage)

            # 4. 종가(Close) 데이터만 추출
            data = response["stock_data"]
            close_prices = data['Close']

            # 5. 데이터프레임 확인
            print(close_prices.head())  # 상위 5개 행 출력

            # 6. 그래프 그리기
            plt.figure(figsize=(12, 6))
            for ticker in tickers:
                plt.plot(close_prices.index, close_prices[ticker], label=ticker)

            plt.title("Stock Price Fluctuations Over the Last Year")
            plt.xlabel("Date")
            plt.ylabel("Stock Price (USD)")
            plt.legend()
            plt.grid()
            st.pyplot(plt)





