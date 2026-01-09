from langchain.tools import tool
from langchain.agents import create_agent
import langchain_community.llms as llms
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
import os

os.environ["DASHSCOPE_API_KEY"] = "sk-5e542da025fd4f05902320081e15e0d9"
model = ChatTongyi(model="qwen-plus")
# model = ChatOllama(model="gemma3:4b", temperature=0.7)
# model = ChatOllama(model="qwen3:4b", temperature=0.7)

# result = model.invoke("你好")
# print(result)
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

@tool
def get_stock(code: str) -> str:
    """"search stock information by code"""
    return f"{code} up 2% today..."

agent = create_agent(model, tools=[search, get_weather, get_stock])

result = agent.invoke({"messages": [HumanMessage("search stock 600231'.")]})

for msg in result["messages"]:
    print(f"{msg.__class__.__name__}:{msg.content}\n")

print("=== 方法1：提取最后一个AI消息 ===")
if 'messages' in result:
    messages = result['messages']
    # 从后往前找第一个有内容的AI消息
    for msg in reversed(messages):
        if hasattr(msg, 'content') and msg.content and msg.content.strip():
            print(f"最终回答: {msg.content}")
            break