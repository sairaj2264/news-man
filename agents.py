from typing import Dict, Any, List
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from datetime import datetime

# Import custom agents
from reflection_agent import reflection_node
from refinement_agent import refinement_node
from headline_agent import headline_node

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
        self.current_article: Dict = {}
        self.current_summary: str = ""
        self.critique_result: Dict = {}
        self.refinement_result: Dict = {}
        self.headline: str = ""

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
            'raw_content': result.get('content'),  # Store raw content for reflection
            'published_date': result.get('published_date', datetime.now().isoformat())
        }
        articles.append(article)
    
    state.articles.extend(articles)
    if articles:
        state.current_article = articles[0]  # Process one article at a time
    
    return {"articles": articles, "current_article": state.current_article}

# Writing Agent Implementation
def writing_agent(state: AgentState) -> Dict:
    if not state.current_article:
        return {"error": "No article to process"}
    
    # Create prompt for summary generation
    prompt = f"""Please provide a concise, single-paragraph summary of the following article:

Title: {state.current_article['title']}

Content: {state.current_article['content']}

Generate a clear, accurate, and engaging summary."""
    
    # Generate summary using LLM
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    summary = response.content
    state.current_summary = summary
    
    return {
        "summary": summary,
        "raw_content": state.current_article['raw_content']
    }

# Configure the workflow
def create_workflow() -> Graph:
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("browse", browsing_agent)
    workflow.add_node("write", writing_agent)
    workflow.add_node("reflect", reflection_node)
    workflow.add_node("refine", refinement_node)
    workflow.add_node("headline", headline_node)
    
    # Define edges - sequential flow
    workflow.add_edge("browse", "write")
    workflow.add_edge("write", "reflect")
    workflow.add_edge("reflect", "refine")
    workflow.add_edge("refine", "headline")
    
    # Set entry and exit points
    workflow.set_entry_point("browse")
    workflow.set_finish_point("headline")
    
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
        "article": result.current_article,
        "initial_summary": result.current_summary,
        "critique": result.critique_result,
        "refined_summary": result.refinement_result.get('refined_summary'),
        "headline": result.headline
    }