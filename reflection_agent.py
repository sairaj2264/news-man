from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from datetime import datetime

class ReflectionAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo-1106"):
        self.llm = ChatOpenAI(model=model_name)

    def analyze_summary(self, summary: str, raw_content: str) -> Dict[str, Any]:
        """
        Analyze a summary for factual correctness and coherence against the original content.
        
        Args:
            summary: The generated summary to analyze
            raw_content: The original article content
            
        Returns:
            Dictionary containing the critique and metadata
        """
        # Construct the prompt for analysis
        prompt = f"""As a critical reviewer, analyze the following summary for factual accuracy and coherence. 
        Compare it with the original content and identify any:
        1. Factual errors or misrepresentations
        2. Missing key information
        3. Coherence and flow issues
        4. Potential biases or misinterpretations

        Original Content:
        {raw_content}

        Summary to Analyze:
        {summary}

        Provide a detailed critique focusing on these aspects."""

        # Generate the critique
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)

        # Structure the output
        return {
            "critique": response.content,
            "timestamp": datetime.utcnow().isoformat(),
            "summary_length": len(summary),
            "content_length": len(raw_content)
        }

# LangGraph node implementation
def reflection_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node for reflection and critique of summaries.
    
    Expected state keys:
    - summary: The generated summary text
    - raw_content: The original article content
    
    Returns:
    - Dictionary with critique results added to state
    """
    agent = ReflectionAgent()
    
    # Validate input
    if 'summary' not in state or 'raw_content' not in state:
        return {
            "error": "Missing required fields in state",
            "required_fields": ["summary", "raw_content"]
        }
    
    try:
        # Perform the analysis
        critique_result = agent.analyze_summary(
            summary=state['summary'],
            raw_content=state['raw_content']
        )
        
        # Update state with results
        return {
            "critique_result": critique_result,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }

# Example usage in a graph
def add_reflection_to_graph(workflow):
    """
    Add reflection node to an existing LangGraph workflow.
    
    Args:
        workflow: The LangGraph StateGraph instance
    """
    # Add the reflection node
    workflow.add_node("reflect", reflection_node)
    
    # Example edge configuration (to be modified based on specific workflow)
    workflow.add_edge("write", "reflect")