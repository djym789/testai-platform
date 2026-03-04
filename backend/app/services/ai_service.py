"""
Kimi (Moonshot) AI 服务 - 同步版本（简单稳定）
"""
import os
from dotenv import load_dotenv
import requests  # 使用同步的 requests

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY 未设置")
        
        self.base_url = "https://api.moonshot.cn/v1"
        self.model = "moonshot-v1-8k"
    
    def generate_test_case(self, requirement: str) -> dict:
        """
        调用 Kimi 生成测试用例（同步版本）
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": """你是一位资深软件测试工程师，擅长设计全面的测试用例。
请根据用户需求，生成结构化的测试用例，包含：
1. 用例标题
2. 前置条件  
3. 测试步骤（详细编号）
4. 预期结果
5. 优先级（高/中/低）

请用中文回答，格式清晰。"""
                    },
                    {
                        "role": "user",
                        "content": f"请为以下需求生成测试用例：\n\n{requirement}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }
            
            # 使用同步 requests
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            result = response.json()
            
            if response.status_code != 200:
                error_msg = result.get('error', {}).get('message', 'Unknown error')
                return {
                    "success": False,
                    "error": f"API Error: {error_msg}",
                    "requirement": requirement
                }
            
            content = result['choices'][0]['message']['content']
            
            return {
                "success": True,
                "content": content,
                "requirement": requirement,
                "model": self.model
            }
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "requirement": requirement
            }
