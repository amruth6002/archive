import os 

from dotenv import load_dotenv

load_dotenv(os.path.join("..",".env"),override=True)

from typing  import Annotated,List,Literal,Union

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.agents import create_agent

from utils import format_messages

@tool
def caluclator(
    operation: Literal["add","subtract","multiply","divide"],
    a: Union[int,float],
    b: Union[int,float],
) -> Union[int,float]:
    """Define a two-input calculator tool that returns precise answers.

    Arg:
        operation (str): The operation to perform ('add', 'subtract', 'multiply', 'divide').
        a (float or int): The first number.
        b (float or int): The second number.
        
    Returns:
        result (float or int): the result of the operation
    Example
        Divide: result   = a / b
        Subtract: result = a - b
    """
    
    if operation == 'divide' and b == 0:
        return {"error": "Division by zero is not allowed."}

    # Perform calculation
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        result = a / b
    else: 
        result = "unknown operation"
    return result

SYSTEM_PROMPT="""
You are a helpful arithmetic assistant who is an expert at using a calculator. 
Return all text as plain text without Markdown math delimiters.
"""

model = init_chat_model(model="google_genai:gemini-2.5-flash", temperature=0.0)
tools = [caluclator]

# Create agent
agent = create_agent(             # updated for 1.0
    model,
    tools,
    system_prompt=SYSTEM_PROMPT,  # updated for 1.0
    #state_schema=AgentState,  # default
).with_config({"recursion_limit": 20})


# Example usage
result1 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is 3.1 * 4.2?",
            }
        ],
    }
)

format_messages(result1["messages"])



