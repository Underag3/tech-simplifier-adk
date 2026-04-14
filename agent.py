import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# --- 1. Initial Setup ---
load_dotenv()
model_name = "gemini-2.5-flash" # Change it to gemini-3-flash-preview for newer model

# --- 2. Tool Definitions ---
def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    tool_context.state["PROMPT"] = prompt
    return {"status": "success"}

wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# --- 3. Multi-Agent Workflow (Professional English Version) ---

# Agent C: The Professional Explainer
explainer_agent = Agent(
    name="explainer",
    model=model_name,
    instruction="""You are a Senior Technical Consultant. 
    Your task is to synthesize the technical data provided by previous agents 
    into a concise, high-level executive summary. 
    Translate complex jargon into clear, professional English 
    that is easy to understand for business stakeholders, 
    focusing on core concepts and practical value."""
)

# Agent B: The Researcher
researcher_agent = Agent(
    name="researcher",
    model=model_name,
    instruction="""Search for the definition of the term in the PROMPT using Wikipedia. 
    DO NOT answer the user directly. After gathering the information, 
    you MUST TRANSFER the data to the 'explainer' agent for simplification.""",
    tools=[wikipedia_tool],
    sub_agents=[explainer_agent]
)

# Agent A: The Greeter
greeter_agent = Agent(
    name="greeter",
    model=model_name,
    instruction="""Greet the user and use the add_prompt_to_state tool to save their input. 
    Then, you MUST TRANSFER the task to the 'researcher' agent.""",
    tools=[add_prompt_to_state],
    sub_agents=[researcher_agent]
)

# --- 4. Workflow Manager ---
root_agent = SequentialAgent(
    name="tech_simplifier_workflow",
    sub_agents=[greeter_agent]
)

# ADK Entry Point
agent = root_agent
