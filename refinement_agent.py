from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from datetime import datetime

class RefinementAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo-1106"):
        self.llm = ChatOpenAI(model=model_name)

    def refine_summary(self, original_summary: str, critique: str, raw_content: str) -> Dict[str, Any]:
        """
        Generate an improved summary based on critique feedback.
        
        Args:
            original_summary: The initial summary
            critique: Feedback from the Reflection Agent
            raw_content: The original article content for reference
            
        Returns:
            Dictionary containing the refined summary and metadata
        """
        # Construct the prompt for refinement
        prompt = f"""As an expert editor, improve the following summary based on the provided critique 
        while referring to the original content. Address all identified issues and maintain accuracy.

        Original Content:
        {raw_content}

        Original Summary:
        {original_summary}

        Critique to Address:
        {critique}

        Instructions:
        1. Address each point from the critique
        2. Ensure factual accuracy with the original content
        3. Maintain clarity and coherence
        4. Keep the summary concise but comprehensive

        Please provide an improved version of the summary."""

        # Generate the refined summary
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            "refined_summary": response.content,
            "original_summary": original_summary,
            "refinement_timestamp": datetime.utcnow().isoformat(),
            "improvements_based_on": critique
        }

# LangGraph node implementation
def refinement_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node for summary refinement based on critique.
    
    Expected state keys:
    - summary: The original summary text
    - critique_result: The critique from Reflection Agent
    - raw_content: The original article content
    
    Returns:
    - Dictionary with refined summary added to state
    """
    agent = RefinementAgent()
    
    # Validate required inputs
    required_fields = ["summary", "critique_result", "raw_content"]
    missing_fields = [field for field in required_fields if field not in state]
    
    if missing_fields:
        return {
            "error": "Missing required fields in state",
            "missing_fields": missing_fields
        }
    
    try:
        # Extract critique text from critique_result
        critique = state['critique_result'].get('critique', '')
        
        # Generate refined summary
        refinement_result = agent.refine_summary(
            original_summary=state['summary'],
            critique=critique,
            raw_content=state['raw_content']
        )
        
        # Update state with refined summary
        return {
            "refinement_result": refinement_result,
            "final_summary": refinement_result['refined_summary'],
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }

# Example usage in a graph
def add_refinement_to_graph(workflow):
    """
    Add refinement node to an existing LangGraph workflow.
    
    Args:
        workflow: The LangGraph StateGraph instance
    """
    # Add the refinement node
    workflow.add_node("refine", refinement_node)
    
    # Example edge configuration
    workflow.add_edge("reflect", "refine")