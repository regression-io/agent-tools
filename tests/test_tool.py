import sys
from unittest.mock import Mock, patch

import pytest

from agenttools import agent_tool


# Test function to decorate
@agent_tool
def sample_tool(query: str, limit: int = 10) -> list:
    """Search for something

    Args:
        query: The search query
        limit: Max results to return

    Returns:
        List of results
    """
    return ["result"]


# SmolAgents Tests
def test_smolagents_tool_creation():
    with patch.dict('sys.modules', {
        'smolagents': Mock(),
        'crewai': None,
        'langgraph': None
    }):
        mock_tool = Mock()
        sys.modules['smolagents'].tools.tool = mock_tool

        @agent_tool
        def test_func(): pass

        mock_tool.assert_called_once()


# CrewAI Tests
def test_crewai_tool_creation():
    with patch.dict('sys.modules', {
        'smolagents': None,
        'crewai': Mock(),
        'langgraph': None
    }):
        mock_tool = Mock()
        sys.modules['crewai'].Tool = mock_tool

        @agent_tool
        def test_func():
            """Test function"""
            pass

        mock_tool.assert_called_once_with(
            name='test_func',
            description='Test function',
            func=test_func
        )


# Langgraph Tests
def test_langgraph_tool_creation():
    with patch.dict('sys.modules', {
        'smolagents': None,
        'crewai': None,
        'langgraph': Mock()
    }):
        mock_tool = Mock()
        sys.modules['langgraph'].prebuilt.ToolNode = mock_tool

        @agent_tool
        def test_func():
            """Test function"""
            pass

        mock_tool.assert_called_once_with(
            test_func,
            name='test_func',
            description='Test function'
        )


# Error case
def test_no_framework_error():
    with patch.dict('sys.modules', {
        'smolagents': None,
        'crewai': None,
        'langgraph': None
    }):
        with pytest.raises(ImportError) as exc:
            @agent_tool
            def test_func(): pass

        assert "No supported framework" in str(exc.value)
