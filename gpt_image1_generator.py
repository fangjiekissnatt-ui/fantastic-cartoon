# GPT Image 1 图像生成器
# 这个模块负责调用Segmind的GPT Image 1 API来生成图片

import requests
import base64
import os
from config import Config

class GPTImage1Generator:
    """
    GPT Image 1 图像生成器类
    使用Segmind的GPT Image 1 API生成高质量图片
    """
    
    def __init__(self):
        """
        初始化GPT Image 1生成器
        从配置文件读取API密钥和基础URL
        """
        self.api_key = Config.GPT_IMAGE1_API_KEY
        self.base_url = Config.GPT_IMAGE1_BASE_URL
        self.timeout = 120  # 2分钟超时
    
    def test_connection(self):
        """
        测试API连接是否正常
        检查API密钥格式是否正确
        """
        try:
            if not self.api_key or self.api_key == "YOUR_API_KEY":
                return {
                    'success': False,
                    'error': 'GPT Image 1 API密钥未设置'
                }
            
            # 检查API密钥格式
            if not self.api_key.startswith('SG_'):
                return {
                    'success': False,
                    'error': 'GPT Image 1 API密钥格式不正确'
                }
            
            return {
                'success': True,
                'message': 'GPT Image 1 API配置正确'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'GPT Image 1 API连接测试失败: {str(e)}'
            }
    
    def image_file_to_base64(self, image_path):
        """
        将本地图片文件转换为base64编码
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            print(f"图片文件转换base64失败: {str(e)}")
            return None
    
    def image_url_to_base64(self, image_url):
        """
        从URL获取图片并转换为base64编码
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            image_data = response.content
            return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            print(f"图片URL转换base64失败: {str(e)}")
            return None
    
    def generate_image(self, prompt, style=None, reference_image_path=None):
        """
        使用GPT Image 1生成图片
        
        参数:
        - prompt: 图片描述文字
        - style: 风格（会添加到prompt中）
        - reference_image_path: 参考图片路径（会转换为base64并添加到请求中）
        
        返回:
        - 成功: 生成的图片文件路径
        - 失败: None
        """
        try:
            print(f"🎨 使用GPT Image 1生成图片...")
            print(f"   描述: {prompt}")
            print(f"   风格: {style if style else '默认'}")
            print(f"   参考图: {'有' if reference_image_path else '无'}")
            
            # 构建增强的prompt
            enhanced_prompt = prompt
            
            # 添加风格信息到prompt中
            if style:
                from config import Config
                style_config = Config.get_style_config(style)
                if style_config and 'prompt_suffix' in style_config:
                    enhanced_prompt += style_config['prompt_suffix']
                    print(f"   增强描述: {enhanced_prompt}")
            
            # 构建请求数据 - 恢复GPT Image 1原始格式
            data = {
                "prompt": enhanced_prompt,
                "size": "auto",
                "quality": "auto", 
                "moderation": "auto",
                "background": "opaque",
                "output_compression": 100,
                "output_format": "png"
            }
            
            # 处理参考图片 - 使用GPT Image 1的原始格式
            if reference_image_path:
                try:
                    # 将参考图片转换为base64
                    reference_image_base64 = self.image_file_to_base64(reference_image_path)
                    if reference_image_base64:
                        # 使用GPT Image 1的原始字段格式
                        data["reference_images"] = [reference_image_base64]
                        print(f"   已添加参考图片到请求中 (使用GPT Image 1原始格式)")
                    else:
                        print(f"   ⚠️ 参考图片转换失败，继续使用纯文本生成")
                except Exception as e:
                    print(f"   ⚠️ 处理参考图片时出错: {str(e)}，继续使用纯文本生成")
            
            # 设置请求头
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            print(f"📡 正在调用GPT Image 1 API...")
            
            # 发送API请求
            response = requests.post(
                self.base_url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            
            # 检查响应状态
            if response.status_code == 200:
                print("✅ GPT Image 1 API调用成功")
                
                # 保存生成的图片
                generated_image_path = self._save_generated_image(response.content)
                
                if generated_image_path:
                    print(f"💾 图片已保存到: {generated_image_path}")
                    return generated_image_path
                else:
                    print("❌ 图片保存失败")
                    return None
            else:
                print(f"❌ GPT Image 1 API调用失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("⏰ GPT Image 1 API请求超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"🌐 GPT Image 1 API网络错误: {str(e)}")
            return None
        except Exception as e:
            print(f"💥 GPT Image 1生成过程中出现错误: {str(e)}")
            return None
    
    def _save_generated_image(self, image_data):
        """
        保存生成的图片到本地文件
        
        参数:
        - image_data: 图片的二进制数据
        
        返回:
        - 成功: 保存的文件路径
        - 失败: None
        """
        try:
            import uuid
            from datetime import datetime
            
            # 确保生成图片目录存在
            generated_folder = Config.GENERATED_FOLDER
            if not os.path.exists(generated_folder):
                os.makedirs(generated_folder)
            
            # 生成唯一的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"gpt_image1_{timestamp}_{unique_id}.png"
            file_path = os.path.join(generated_folder, filename)
            
            # 保存图片文件
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            return file_path
            
        except Exception as e:
            print(f"💾 保存GPT Image 1生成图片失败: {str(e)}")
            return None

# 创建全局实例
gpt_image1_generator = GPTImage1Generator()
