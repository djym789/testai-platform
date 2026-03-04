"""
Kimi (Moonshot) AI 服务
用于生成测试用例
"""
import os
from dotenv import load_dotenv
import httpx

# 加载环境变量
load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY 未设置")
        
        self.base_url = "https://api.moonshot.cn/v1"
        self.model = "moonshot-v1-8k"
    
    async def generate_test_case(self, requirement: str) -> dict:
        """
        调用 Kimi 生成测试用例
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位资深软件测试工程师..."
                },
                {
                    "role": "user",
                    "content": f"请生成测试用例：{requirement}"
                }
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0
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
