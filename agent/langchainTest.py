import langchain_community.llms as llms
from langchain_core.prompts import PromptTemplate
import json

# 连接Ollama
llm = llms.Ollama(model="gemma3:4b")

# # 简单问答
# question = "你好，请介绍一下你自己"
# print(f"问: {question}")

# answer = llm.invoke(question)
# print(f"答: {answer}")
# 1. 基本示例：创建一个带变量的模板
template = "请帮我将以下文本翻译成{target_language}：{text}"
prompt = PromptTemplate.from_template(template)

# 填充变量，生成完整提示词
full_prompt = prompt.invoke({"target_language": "法语", "text": "你好，世界"})
print(full_prompt.text)
