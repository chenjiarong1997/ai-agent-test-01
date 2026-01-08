import os
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

os.environ["DASHSCOPE_API_KEY"] = "sk-5e542da025fd4f05902320081e15e0d9"
model = ChatTongyi(model="qwen-plus")
# messages = [
#     SystemMessage(content="Translate the following from English into Italian"),
#     HumanMessage(content="hi!"),
# ]
parser = StrOutputParser()
# result = model.invoke(messages)
# result = parser.invoke(result)
# chain = model | parser
# result = chain.invoke(messages)
# print(result)

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
result = prompt_template.invoke({"language": "italian", "text": "hi"})

# print(result)
chain = prompt_template | model | parser
result = chain.invoke({"language": "chinese", "text": "hi"})
print(result)