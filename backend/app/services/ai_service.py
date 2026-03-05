"""
Kimi (Moonshot) AI 服务 - 同步版本（简单稳定）
"""
import os
from dotenv import load_dotenv
import requests  # 使用同步的 requests，无需 C 编译

# 导入数据库模型
from app.models.database import SessionLocal, TestCase

# 加载环境变量
load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY 未设置，请在 .env 文件中配置")
        
        # Kimi API endpoint
        self.base_url = "https://api.moonshot.cn/v1"
        # 使用的模型
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
            
            # 使用 requests 发送同步请求（无需 C 编译）
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
            
            # 生成成功，保存到数据库
            try:
                # 提取标题（第一行或前50个字符）
                title = content.split('\n')[0][:50] if '\n' in content else content[:50]
                title = title.replace('#', '').strip()  # 去掉markdown标记
                
                # 创建数据库会话
                db = SessionLocal()
                db_test_case = TestCase(
                    title=title,
                    requirement=requirement,
                    content=content,
                    ai_model=self.model
                )
                db.add(db_test_case)
                db.commit()
                db.refresh(db_test_case)
                
                # 返回结果包含数据库ID
                result_data = {
                    "success": True,
                    "content": content,
                    "requirement": requirement,
                    "model": self.model,
                    "saved_to_db": True,
                    "db_id": db_test_case.id
                }
                
                db.close()
                return result_data
                
            except Exception as db_error:
                # 数据库保存失败不影响主流程，仍然返回生成结果
                print(f"保存到数据库失败: {db_error}")
                return {
                    "success": True,
                    "content": content,
                    "requirement": requirement,
                    "model": self.model,
                    "saved_to_db": False,
                    "save_error": str(db_error)
                }
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "requirement": requirement
            }
