# agent-tools

A universal tool decorator that automatically adapts to popular agent frameworks including SmolAgents, CrewAI, and Langgraph.

## Installation

```bash
pip install agent-tools
```

## Features
* Single decorator that works across multiple agent frameworks
* Automatic framework detection
* Preserves docstrings and type hints
* Zero configuration required

## Usage
```python
from agenttools import agent_tool

@agent_tool
def search_web(query: str, max_results: int = 5) -> list:
    """Search the web for information
    
    Args:
        query: The search query to execute
        max_results: Maximum number of results to return
        
    Returns:
        List of search results
    """
    # Your implementation here
    pass
```

The @agent_tool decorator will automatically:

- Convert your function into the appropriate Tool format based on your installed framework
- Use docstrings for tool descriptions
- Preserve type hints and parameter information
- Framework Detection
- Work seamlessly with:
  * SmolAgents
  * CrewAI
  * Langgraph

## Compatibility

The decorator automatically detects which framework you're using:

* With SmolAgents installed: Returns a SmolAgents Tool
* With CrewAI installed: Returns a CrewAI Tool
* With Langgraph installed: Returns a Langgraph ToolNode

## Requirements
* Python 3.8+
* docstring-parser
* One of: SmolAgents, CrewAI, or Langgraph

## License
Apache 2.0

