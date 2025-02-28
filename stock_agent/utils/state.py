from typing import List, Dict, Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pandas import DataFrame
from pydantic import BaseModel, Field


# Pydantic 모델 정의
class StockRecommendation(BaseModel):
    name: str = Field(description="The full name of the company")
    ticker: str = Field(description="The stock ticker symbol")
    description: str = Field(description="A brief description of why this stock is relevant")


class StockRecommendations(BaseModel):
    recommendations: List[StockRecommendation] = Field(description="List of stock recommendations")


class ServiceState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages] = Field(default_factory=list)
    issue: str = ""
    news_articles: List[Dict[str, str]] = Field(default_factory=list)
    blog_posts: List[Dict[str, str]] = Field(default_factory=list)
    related_stocks: List[StockRecommendation] = Field(default_factory=list, description="List of stock recommendations")
    stock_data: DataFrame = Field(default_factory=DataFrame, description="Stock data for plotting")
