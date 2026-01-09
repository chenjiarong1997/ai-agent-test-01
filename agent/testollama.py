from langchain_ollama import ChatOllama
import json

def test_qwen3_function_calling():
    """测试qwen3:4b是否支持function calling"""
    print("正在测试 qwen3:4b 是否支持function calling...")
    
    llm = ChatOllama(
        model="qwen3:4b",
        temperature=0.3,
        base_url="http://localhost:11434"
    )
    
    # 测试function calling能力
    test_prompt = """你是一个助手。如果用户询问天气，请调用get_weather函数。

函数定义：
- name: get_weather
- description: 获取城市天气
- parameters:
  - city: string, 城市名称

用户：北京天气怎么样？

请严格按照以下JSON格式回复函数调用：
{
  "function": "get_weather",
  "arguments": {"city": "北京"}
}

如果不需要函数，直接回答。"""
    
    try:
        response = llm.invoke(test_prompt)
        print(f"模型响应:\n{response.content}\n")
        
        # 尝试解析JSON
        try:
            data = json.loads(response.content.strip())
            if "function" in data:
                print("✅ qwen3:4b 支持function calling!")
                print(f"函数调用: {data}")
                return True
        except json.JSONDecodeError:
            # 检查是否有类似的JSON结构
            if "get_weather" in response.content and "北京" in response.content:
                print("⚠️ 可能支持，但格式不标准")
                print("响应内容:", response.content[:200])
                return "maybe"
            else:
                print("❌ qwen3:4b 不支持标准function calling")
                print("返回的是普通文本")
                return False
                
    except Exception as e:
        print(f"测试出错: {e}")
        return False

# 运行测试
result = test_qwen3_function_calling()
print(f"\n测试结果: {result}")