from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
# 1.简单提示模版
# # 方法1：直接实例化
# template = "请把以下内容翻译成英文：{text}"
# prompt = PromptTemplate(input_variables=["text"], template=template)

# # 方法2：使用from_template（更简洁）
# prompt = PromptTemplate.from_template("请把以下内容翻译成英文：{text}")

# # 格式化提示词
# formatted_prompt = prompt.format(text="你好，世界！")
# print(formatted_prompt)
# # 输出: 请把以下内容翻译成英文：你好，世界！

# 2.包含多个变量的模板
# template = """
# 作为一位{role}，请用{style}的风格回答以下问题：
# 问题：{question}
# 回答：
# """
# prompt = PromptTemplate(
#     input_variables=["role", "style", "question"],
#     template=template
# )

# # 格式化
# result = prompt.format(
#     role="资深软件工程师",
#     style="专业且简洁",
#     question="如何优化Python代码的性能？"
# )
# print(result)


# 3.创建系统消息和用户消息模板
# system_template = "你是一个{domain}专家，请用{language}回答用户的问题。"
# system_prompt = SystemMessagePromptTemplate.from_template(system_template)

# human_template = "我的问题是：{question}"
# human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# # 组合成聊天提示模板
# chat_prompt = ChatPromptTemplate.from_messages([
#     system_prompt,
#     human_prompt
# ])

# # 格式化
# messages = chat_prompt.format_messages(
#     domain="人工智能",
#     language="中文",
#     question="什么是机器学习？"
# )

# # 与模型结合使用
# from langchain_community.chat_models import ChatTongyi
# import os
# os.environ["DASHSCOPE_API_KEY"] = "sk-5e542da025fd4f05902320081e15e0d9"
# model = ChatTongyi(model="qwen-plus")
# response = model.invoke(messages)
# print(response.content)

# 4.创建LCEL链
# from langchain_community.chat_models import ChatTongyi
# import os
# from langchain_core.output_parsers import StrOutputParser
# os.environ["DASHSCOPE_API_KEY"] = "sk-5e542da025fd4f05902320081e15e0d9"
# prompt = ChatPromptTemplate.from_template(
#     "你是一位{profession}，请回答：{query}"
# )

# chain = prompt | ChatTongyi() | StrOutputParser()

# # 执行链
# result = chain.invoke({
#     "profession": "历史学家",
#     "query": "简述第二次世界大战的主要原因"
# })
# print(result)


# 5.RAG专用提示模板
# rag_template = """
# 根据以下上下文信息，回答问题。如果上下文不包含相关信息，请回答"根据已知信息无法回答"。

# 上下文：
# {context}

# 问题：{question}

# 请基于上下文提供准确、完整的答案：
# """

# rag_prompt = PromptTemplate(
#     input_variables=["context", "question"],
#     template=rag_template
# )

# # 使用示例
# context = """
# 人工智能是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。
# 机器学习是人工智能的一个子领域，它使计算机能够在没有明确编程的情况下学习。
# 深度学习是机器学习的一个分支，使用神经网络模拟人脑的工作方式。
# """

# question = "什么是深度学习？"

# formatted = rag_prompt.format(context=context, question=question)
# print(formatted)

# 6.分步提示模板
# template = """
# 请按以下步骤思考并回答问题：

# 原始问题：{question}

# 第一步：分析问题的关键要素
# 关键要素：{step1_thinking}

# 第二步：查找相关知识
# 相关知识：{step2_knowledge}

# 第三步：综合信息给出最终答案
# 最终答案：
# """

# prompt = PromptTemplate(
#     input_variables=["question", "step1_thinking", "step2_knowledge"],
#     template=template
# )

# # 可以分步填充
# partial_prompt = prompt.partial(
#     step1_thinking="这是一个关于技术定义的问题，需要明确术语和范畴。",
#     step2_knowledge="深度学习是机器学习的分支，基于神经网络。"
# )

# final_prompt = partial_prompt.format(question="解释深度学习的概念")
# print(final_prompt)

# 7.少样本提示模板
# from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# # 定义示例
# examples = [
#     {
#         "input": "太阳是什么颜色的？",
#         "output": "太阳在可见光波段呈现白色，但由于大气散射，我们常看到它是黄色或橙红色。"
#     },
#     {
#         "input": "水在100摄氏度时是什么状态？",
#         "output": "在标准大气压下，水在100摄氏度时沸腾，从液态变为气态（水蒸气）。"
#     }
# ]

# # 定义单个示例的格式
# example_template = """
# 输入：{input}
# 输出：{output}
# """
# example_prompt = PromptTemplate(
#     input_variables=["input", "output"],
#     template=example_template
# )

# # 创建FewShotPromptTemplate
# few_shot_prompt = FewShotPromptTemplate(
#     examples=examples,
#     example_prompt=example_prompt,
#     prefix="请根据以下示例的格式回答问题：",
#     suffix="输入：{user_input}\n输出：",
#     input_variables=["user_input"],
#     example_separator="\n\n"
# )

# # 使用
# result = few_shot_prompt.format(user_input="冰的熔点是多少？")
# print(result)

# 8.模板的管理与重用
# 将模板存储在字典中便于管理
# TEMPLATE_REGISTRY = {
#     "translation": "将以下{source_lang}文本翻译成{target_lang}：\n{text}",
#     "summarization": "请用{length}字总结以下文本：\n{text}",
#     "code_explanation": "解释以下{language}代码的功能：\n```{code}```"
# }

# def get_prompt(template_name, **kwargs):
#     """获取预定义模板"""
#     if template_name not in TEMPLATE_REGISTRY:
#         raise ValueError(f"模板 '{template_name}' 不存在")
    
#     template = TEMPLATE_REGISTRY[template_name]
#     return PromptTemplate.from_template(template).format(**kwargs)

# # 使用
# summary_prompt = get_prompt(
#     "summarization",
#     length="100",
#     text="这里是一段很长的文本内容..."
# )
# print(summary_prompt)

# 9.模版验证和调试
# 检查模板变量
# prompt = PromptTemplate.from_template("你好，{name}！你今天感觉怎么样？")

# print("输入变量:", prompt.input_variables)  # 输出: ['name']
# print("模板文本:", prompt.template)

# # 验证变量是否匹配
# try:
#     # 缺少必要变量会报错
#     prompt.format()  # 会抛出KeyError
# except KeyError as e:
#     print(f"缺少变量: {e}")

# # 正确使用
# formatted = prompt.format(name="小明")
# print(formatted)

# 设置DashScope API Key
# from langchain_community.chat_models import ChatTongyi
# import os
# os.environ["DASHSCOPE_API_KEY"] = "sk-5e542da025fd4f05902320081e15e0d9"

# # 创建专业领域的提示模板
# template = ChatPromptTemplate.from_messages([
#     ("system", "你是{domain}领域的资深专家，拥有10年以上经验。"),
#     ("human", "请以{style}的方式回答以下问题：\n\n问题：{question}"),
#     ("ai", "好的，我将以{style}的方式为您解答。")
# ])

# # 创建LCEL链
# chain = template | ChatTongyi(model_name="qwen-plus") | StrOutputParser()

# # 执行
# response = chain.invoke({
#     "domain": "人工智能与机器学习",
#     "style": "专业、详细且举例说明",
#     "question": "Transformer模型在自然语言处理中的核心创新是什么？"
# })

# print("千问AI的回答：")
# print(response)