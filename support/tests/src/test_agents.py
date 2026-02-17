import pytest
from unittest.mock import Mock, patch
import os
os.environ["TESTING"] = "true"

# Mock OpenAI and langgraph dependencies before importing src.agents
with patch("langchain_openai.ChatOpenAI"), \
     patch("langgraph.prebuilt.create_react_agent"), \
     patch("langgraph_supervisor.create_supervisor"):
    from src.agents import model, balance_agent, workflow

def test_model_configuration():
    assert model is not None

def test_balance_agent_configuration():
    assert balance_agent is not None

def test_workflow_configuration():
    assert workflow is not None
