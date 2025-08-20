from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

class HeadlineAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo-1106"):
        self.llm = ChatOpenAI(model=model_name)

    def generate_headline(self, summary: str) -> str:
        """
        Generate a concise and compelling headline from a summary.
        
        Args:
            summary: The refined article summary
            
        Returns:
            A string containing the generated headline
        """
        prompt = f"""As a skilled news editor, create a concise and compelling headline 
        for the following article summary. The headline should be attention-grabbing 
        while maintaining accuracy and journalistic integrity.

        Summary:
        {summary}

        Requirements:
        1. Maximum 10-12 words
        2. Capture the main point or most newsworthy aspect
        3. Use active voice and strong verbs
        4. Avoid clickbait or sensationalism
        5. Return only the headline text

        Generate the headline:"""

        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        
        # Clean and format the headline
        headline = response.content.strip().strip('"').strip()
        
        return headline

# LangGraph node implementation
def headline_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node for generating headlines from refined summaries.
    
    Expected state keys:
    - final_summary: The refined article summary
    
    Returns:
    - Dictionary with generated headline added to state
    """
    agent = HeadlineAgent()
    
    # Validate required input
    if "final_summary" not in state:
        return {
            "error": "Missing final_summary in state",
            "status": "failed"
        }
    
    try:
        # Generate headline
        headline = agent.generate_headline(state['final_summary'])
        
        # Update state with headline
        return {
            "headline": headline,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }

# Example usage in a graph
def add_headline_to_graph(workflow):
    """
    Add headline generation node to an existing LangGraph workflow.
    
    Args:
        workflow: The LangGraph StateGraph instance
    """
    # Add the headline node
    workflow.add_node("headline", headline_node)
    
    # Example edge configuration - connect after refinement
    workflow.add_edge("refine", "headline")