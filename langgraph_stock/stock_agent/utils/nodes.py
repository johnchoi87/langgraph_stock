from langchain_community.tools import TavilySearchResults
from langchain_core.output_parsers import PydanticOutputParser
from langchain_teddynote.tools import GoogleNews
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph_stock.stock_agent.utils.state import ServiceState, StockRecommendations
from datetime import datetime, timedelta
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()
# LLM 정의
llm = ChatOpenAI(model="gpt-4o", temperature=0)
google_search = GoogleNews()
tavily_search = TavilySearchResults(
    max_results=100,
    include_answer=True,
    include_raw_content=True,
    # include_images=True,
    # search_depth="advanced", # or "basic"
    include_domains=["finance.yahoo.com", "www.etftrends.com", "www.marketwatch.com", "money.cnn.com",
                     "www.bloomberg.com"]
    # exclude_domains = []
)


# 이슈에 대한 검색 키워드 생성 함수 정의
def generate_keyword_query(state: ServiceState):
    if messages := state.get("messages", []):
        # 최근 메시지
        ai_message = messages[-1]
    else:
        #
        raise ValueError("No messages found in the state.")

    print(f'Called generate_keyword_query {ai_message}')
    prompt_template = """
    Based on the following sentences, please make the best English search terms to search in the news. Please make a sentence centered on keywords for your search. 
    Sentence: "{issue}"
    Format: keyword1 keyword2 keyword3 ...
    """
    prompt = PromptTemplate(
        input_variables=["issue"],
        template=prompt_template,
    )
    chain = prompt | llm
    result = chain.invoke({"issue": ai_message})
    query = result.content.strip()
    return {"messages": [query]}


# 구글 검색 함수 정의
def search_google(state: ServiceState):
    if messages := state.get("messages", []):
        # 최근 메시지
        ai_message = messages[-1]
    else:
        #
        raise ValueError("No messages found in the state.")
    print(f'Called search_google {ai_message}')
    search_keyword = google_search.search_by_keyword(ai_message.content, k=20)
    return {"blog_posts": [search_keyword.invoke(f"{ai_message.content}")]}


# 뉴스 검색 함수 정의
def search_news(state: ServiceState):
    if messages := state.get("messages", []):
        # 최근 메시지
        ai_message = messages[-1]
    else:
        #
        raise ValueError("No messages found in the state.")
    # print(f'Called search_news {ai_message}')
    return {"news_articles": [tavily_search.invoke(f"{ai_message} stock news")]}


# 주식 추천 함수 정의
def recommend_stocks(state: ServiceState):
    if news_articles := state.get("news_articles", []):
        # 최근 메시지
        related_articles = news_articles[-1]
    else:
        #
        raise ValueError("No messages found in the state.")
    print(f'Called recommend_stocks {related_articles}')

    parser = PydanticOutputParser(pydantic_object=StockRecommendations)
    prompt = PromptTemplate(
        template="Based on the following news, we recommend relevant US stock tickers. Please translate the explanation into Korean:\n{news}\n{format_instructions}\nRecommendations:",
        input_variables=["news"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    # return parser.parse(result)
    # print(parser.get_format_instructions())
    result = chain.invoke(related_articles)
    # print(result)
    return {"related_stocks": result.recommendations}


# 주식 데이터 다운로드 함수 정의
def download_stock_prices(state: ServiceState):
    if related_stocks := state.get("related_stocks", []):
        # 최근 메시지
        stocks = related_stocks
    else:
        #
        raise ValueError("No messages found in the state.")
    # 1. 티커 리스트 정의
    # tickers = ["AAPL", "MSFT", "GOOG"]  # 가져올 티커 리스트
    # print(stocks)
    tickers = [stock.ticker for stock in stocks]
    # 2. 날짜 범위 설정 (최근 1년)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # 3. 데이터 다운로드
    data = yf.download(tickers, start=start_date, end=end_date)

    # 4. 종가(Close) 데이터만 추출
    close_prices = data['Close']
    # 5. 데이터프레임 확인
    # print(close_prices.head())  # 상위 5개 행 출력
    return {"stock_data": data}


# 키워드 관련 주식 종목 요약
def summarize_related_stocks(state: ServiceState):
    print("=============================================")
    print(f"summary : {state}")
    print("=============================================")
    return state
