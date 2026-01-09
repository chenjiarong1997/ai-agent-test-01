from langchain_core.tools import tool
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 定义工具
@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        return str(eval(expression))
    except:
        return "计算错误"

# 连接Ollama
llm = Ollama(model="gemma3:4b")

# 创建提示模板，告诉LLM可以使用工具
prompt = PromptTemplate.from_template("""
你是一个智能助手，可以使用工具来帮助用户。

可用的工具：
1. calculator - 计算数学表达式，输入格式：数学表达式，例如：3*4+5

用户的问题：{question}

请分析是否需要使用工具：
1. 如果需要使用工具，请回复：TOOL:calculator 表达式: [这里写表达式]
2. 如果不需要工具，直接回答。

示例：
用户：计算3乘以4
助手：TOOL:calculator 表达式: 3*4
""")

# 创建链
chain = prompt | llm | StrOutputParser()

# 获取响应
question = "计算3乘以4再加上5等于多少？"
response = chain.invoke({"question": question})
print("原始响应:", response)

# 解析响应并调用工具
if "TOOL:calculator" in response:
    # 提取表达式
    import re
    match = re.search(r'表达式:\s*(.+)', response)
    if match:
        expression = match.group(1).strip()
        print(f"提取的表达式: {expression}")
        # 调用工具
        result = calculator.invoke({"expression": expression})
        print(f"计算结果: {result}")
        
        # 将结果反馈给LLM
        follow_up_prompt = PromptTemplate.from_template("""
        根据计算结果回答用户问题：
        
        用户问题：{question}
        计算过程：{expression} = {result}
        
        请给出最终回答：
        """)
        
        final_response = (follow_up_prompt | llm | StrOutputParser()).invoke({
            "question": question,
            "expression": expression,
            "result": result
        })
        print(f"最终回答: {final_response}")
else:
    print(f"LLM直接回答: {response}")