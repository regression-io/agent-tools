import importlib
import inspect
from typing import Callable, Any
from docstring_parser import parse as parse_docstring


def agent_tool(func: Callable) -> Any:
    """Decorator to convert a function into a Tool object for SmolAgents, CrewAI, and Langgraph.
    Returns a concrete Tool instance based on the detected framework.
    """
    # Infer description from docstring
    doc = parse_docstring(func.__doc__ or "")
    inferred_description = doc.short_description or func.__name__

    # Infer input schema from type hints and docstring
    type_hints = inspect.get_annotations(func)
    params = inspect.signature(func).parameters
    local_input_schema = {}

    for param in params.values():
        param_doc = next((p for p in doc.params if p.arg_name == param.name), None)

        # Get type from annotation or default to string
        param_type = type_hints.get(param.name, str)
        param_info = {
            "type": (
                param_type.__name__
                if hasattr(param_type, "__name__")
                else str(param_type)
            )
        }
        # Get description from docstring
        if param_doc and param_doc.description:
            param_info["description"] = param_doc.description

        # Handle default values
        if param.default != inspect.Parameter.empty:
            param_info["default"] = param.default

        local_input_schema[param.name] = param_info

    # Dynamically detect and import the framework
    if importlib.util.find_spec("smolagents"):
        smol = importlib.import_module("smolagents")
        return smol.tools.tool(func)
    elif importlib.util.find_spec("crewai"):
        crewai = importlib.import_module("crewai")
        return crewai.Tool(name=func.__name__, description=inferred_description, func=func)
    elif importlib.util.find_spec("langgraph"):
        langgraph = importlib.import_module("langgraph.prebuilt")
        return langgraph.ToolNode(func, name=func.__name__, description=inferred_description)
    else:
        raise ImportError("No supported framework (SmolAgents, CrewAI, Langgraph) found.")
