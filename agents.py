from typing import Dict, Any, List
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from datetime import datetime

# Initialize clients
tavily_client = TavilyClient()
llm = ChatOpenAI(model="gpt-3.5-turbo-1106")

# Define agent states
class AgentState:
    def __init__(self):
        self.messages: List[Any] = []
        self.current_topic: str = ""
        self.articles: List[Dict] = []
        self.summaries: List[Dict] = []

# Browsing Agent Implementation
def browsing_agent(state: AgentState) -> Dict:
    # Use Tavily to search for articles based on the current topic
    search_results = tavily_client.search(
        query=state.current_topic,
        search_depth="advanced",
        max_results=5
    )
    
    # Process and store articles
    articles = []
    for result in search_results:
        article = {
            'title': result.get('title'),
            'url': result.get('url'),
            'content': result.get('content'),
            'published_date': result.get('published_date', datetime.now().isoformat())
        }
        articles.append(article)
    
    state.articles.extend(articles)
    return {"articles": articles}

# Writing Agent Implementation
def writing_agent(state: AgentState) -> Dict:
    summaries = []
    
    for article in state.articles:
        # Create prompt for summary generation
        prompt = f"Please provide a concise, single-paragraph summary of the following article:\n\nTitle: {article['title']}\n\nContent: {article['content']}"
        
        # Generate summary using LLM
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        
        summary = {
            'article_title': article['title'],
            'content': response.content,
            'created_at': datetime.now().isoformat()
        }
        summaries.append(summary)
    
    state.summaries.extend(summaries)
    return {"summaries": summaries}

# Configure the workflow
def create_workflow() -> Graph:
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("browse", browsing_agent)
    workflow.add_node("write", writing_agent)
    
    # Define edges
    workflow.add_edge("browse", "write")
    
    # Set entry and exit points
    workflow.set_entry_point("browse")
    workflow.set_finish_point("write")
    
    # Compile the graph
    return workflow.compile()

# Example usage
def process_topic(topic: str) -> Dict:
    # Initialize workflow
    workflow = create_workflow()
    
    # Create initial state
    initial_state = AgentState()
    initial_state.current_topic = topic
    
    # Run the workflow
    result = workflow.invoke(initial_state)
    
    return {
        "topic": topic,
        "articles": result.articles,
        "summaries": result.summaries
    }