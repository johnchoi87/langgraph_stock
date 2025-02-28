# 그래프 생성
from langgraph.graph import StateGraph, START, END
from stock_agent.utils.nodes import search_news, recommend_stocks, download_stock_prices, summarize_related_stocks, \
    generate_keyword_query, search_google
from stock_agent.utils.state import ServiceState

def call_search_stock():
    graph_builder = StateGraph(ServiceState)

    # 노드 이름, 함수 혹은 callable 객체를 인자로 받아 노드를 추가
    graph_builder.add_node("generate_keyword_query", generate_keyword_query)
    graph_builder.add_node("search_news", search_news)
    #graph_builder.add_node("search_google", search_google)
    graph_builder.add_node("recommend_stocks", recommend_stocks)
    graph_builder.add_node("download_stock_prices", download_stock_prices)
    graph_builder.add_node("summarize_related_stocks", summarize_related_stocks)
    #
    graph_builder.add_edge("generate_keyword_query", "search_news")
    #graph_builder.add_edge("generate_keyword_query", "search_google")
    graph_builder.add_edge("search_news", "recommend_stocks")
    #graph_builder.add_edge("search_google", "recommend_stocks")
    graph_builder.add_edge("recommend_stocks", "download_stock_prices")
    graph_builder.add_edge("recommend_stocks", "summarize_related_stocks")
    graph_builder.add_edge("download_stock_prices", "summarize_related_stocks")


    # 시작 노드에서 챗봇 노드로의 엣지 추가
    graph_builder.add_edge(START, "generate_keyword_query")

    # 그래프에 엣지 추가
    graph_builder.add_edge("summarize_related_stocks", END)

    # 그래프 컴파일
    graph = graph_builder.compile()
    return graph
'''
    inputs = {"messages": [input]}
    result = graph.invoke(inputs)

    print("Related stocks:")
    print("---------------")
    print(result["related_stocks"])
    tickers = [stock.ticker for stock in result["related_stocks"]]
    for stock in result["related_stocks"]:
        print(f'[{stock.ticker}] {stock.name}: {stock.description}')
        '''
