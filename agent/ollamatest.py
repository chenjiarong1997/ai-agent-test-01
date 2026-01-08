# ollama_demo.py
import ollama

# 检查可用的本地模型
print("本地可用模型：")
models = ollama.list()
for model in models['models']:
    print(f"- {model['model']} (大小: {model['size'] / 1024**3:.1f}GB)")

def chat_with_ollama(model_name="gemma3:4b"):
    """使用 Ollama 进行对话"""
    
    conversation_history = []  # 用于存储对话历史

    while True:
        # conversation_history = [] # 重置对话历史以开始新对话
        user_input = input("你: ")  # 接收用户输入
        if user_input.lower() in ["exit", "quit"]:  # 退出条件
            print("对话结束。")
            break
        
        # 将当前用户输入加入历史
        conversation_history.append({
            'role': 'user',
            'content': user_input
        })

        # 发送对话历史给模型并获取响应
        # messages=[
        #     {
        #         'role': 'user',
        #         'content': '今天星期几?'
        #     }
        # ]
        response = ollama.chat(
            model=model_name,
            messages=conversation_history,  # 发送所有对话历史
            stream=True  # 启用流式响应 流式返回的response是迭代器， 非流式response是字符串
        )
        
        #print("\nAI 回复（流式）:")
        #说明：
        # for chunk in response：从生成器中逐一获取每一个块。
        # content = chunk['message']['content']：提取当前块中的内容。
        # print(content, end='', flush=True)：实时打印出当前块的内容，而不是等到整个响应完成后再一次性打印。end 参数用于指定打印完内容后要追加的字符。默认情况下，print 函数在输出内容后会追加一个换行符 \n，因此下一次调用 print 函数时会在新的一行开始输出。
        # flush 参数用于控制输出缓存的刷新行为。默认情况下，print 会将输出内容缓存在内部，这意味着文本会在缓冲区中暂时存储，可能在缓冲区填满或程序结束时才会被实际输出到终端。
        # 当你将 flush 设置为 True 时，print 函数会强制立即刷新输出缓存，确保内容被立即输出到终端。这在某些情况下非常有用，例如
        full_response = ""
        for chunk in response:
            # print(chunk.message.content, end='', flush=True)
            content = chunk['message']['content']
            print(content, end='', flush=True)
            full_response += content
            
        # 将AI的回复添加到历史
        conversation_history.append({
            'role': 'assistant',
            'content': full_response
        })

        #print("等待单次回复...:")
        # print(response.message.content)

if __name__ == "__main__":
    # 运行对话
    chat_with_ollama()