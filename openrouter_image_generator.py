#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenRouter AI图像生成器
使用OpenRouter聚合平台支持多种先进的AI图像生成模型
包括Flux、DALL-E 3、Midjourney、Stable Diffusion等
"""

import os
import uuid
import requests
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image
from config import Config

class OpenRouterImageGenerator:
    """OpenRouter AI图像生成器"""
    
    def __init__(self):
        """初始化OpenRouter图像生成器"""
        self.config = Config
        self.api_key = self.config.OPENROUTER_API_KEY
        self.base_url = self.config.OPENROUTER_BASE_URL
        self.models = self.config.OPENROUTER_IMAGE_MODELS
        self.default_model = self.config.DEFAULT_OPENROUTER_MODEL
        
        print("🤖 OpenRouter AI图像生成器初始化完成")
        if self.api_key and self.api_key.startswith('sk-or-v1-'):
            print("✅ OpenRouter API密钥已配置")
        else:
            print("⚠️ OpenRouter API密钥未设置或格式不正确")
    
    def generate_image(self, prompt, style=None, reference_image_path=None):
        """
        生成图像的主函数
        
        Args:
            prompt (str): 图像描述提示词
            style (str): 绘画风格
            reference_image_path (str): 参考图片路径
        
        Returns:
            str: 生成的图片文件路径，失败时返回None
        """
        
        print(f"🎨 开始使用OpenRouter生成图片...")
        print(f"   提示词: {prompt}")
        print(f"   风格: {style}")
        print(f"   参考图: {'有' if reference_image_path else '无'}")
        
        try:
            if not self.api_key or not self.api_key.startswith('sk-or-v1-'):
                print("⚠️ OpenRouter API密钥未配置，使用备用方案")
                return self._generate_fallback(prompt, style)
            
            # 使用OpenRouter生成图像
            return self._generate_with_openrouter(prompt, style, reference_image_path)
        
        except Exception as e:
            print(f"❌ OpenRouter图像生成失败: {e}")
            return self._generate_fallback(prompt, style)
    
    def _generate_with_openrouter(self, prompt, style, reference_image_path=None):
        """使用OpenRouter API生成图像"""
        
        try:
            # 获取风格配置
            style_config = self.config.get_style_config(style)
            
            # 构建完整的提示词
            full_prompt = self._build_full_prompt(prompt, style_config)
            
            # 选择合适的模型
            model = self._select_model(style)
            
            print(f"🤖 正在调用OpenRouter API...")
            print(f"📡 使用模型: {model}")
            print(f"📝 完整提示词: {full_prompt[:100]}...")
            
            # 准备请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:4000",  # 设置来源
                "X-Title": "AI Image Generation Website"
            }
            
            # 构建请求数据 - 针对图像生成模型
            if "gemini" in model and "image" in model:
                # Gemini图像生成模型的特殊处理
                content_parts = []

                # 添加文本提示
                content_parts.append({"type": "text", "text": full_prompt})

                # 如果有参考图片，添加到请求中
                if reference_image_path and os.path.exists(reference_image_path):
                    try:
                        with open(reference_image_path, 'rb') as img_file:
                            img_base64 = base64.b64encode(img_file.read()).decode()
                            content_parts.append({
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
                            })
                            print(f"📸 已添加参考图片到请求中")
                    except Exception as e:
                        print(f"⚠️ 处理参考图片失败: {e}")

                data = {
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": content_parts
                        }
                    ],
                    "modalities": ["image", "text"],  # 关键：指定输出模态
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            else:
                # 其他模型的标准处理
                data = {
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Generate an image: {full_prompt}"
                        }
                    ],
                    "modalities": ["image", "text"],  # 关键：指定输出模态
                    "max_tokens": 1000,
                    "temperature": 0.7
                }

                # 如果有参考图片，进行特殊处理
                if reference_image_path and os.path.exists(reference_image_path):
                    try:
                        with open(reference_image_path, 'rb') as img_file:
                            img_base64 = base64.b64encode(img_file.read()).decode()
                            data["messages"] = [
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": full_prompt},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                                    ]
                                }
                            ]
                            print(f"📸 已添加参考图片到请求中")
                    except Exception as e:
                        print(f"⚠️ 处理参考图片失败: {e}")

            # 调用OpenRouter API
            url = f"{self.base_url}/chat/completions"
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            print(f"📊 API响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ OpenRouter API响应成功")
                
                # 解析响应获取图像
                generated_image_path = self._parse_openrouter_response(result, prompt, style)
                
                if generated_image_path:
                    print(f"🎉 OpenRouter图像生成成功!")
                    return generated_image_path
                else:
                    print(f"⚠️ 未能从响应中提取图像，使用备用方案")
                    return self._generate_fallback(prompt, style)
            
            else:
                error_msg = f"API错误 {response.status_code}: {response.text}"
                print(f"❌ OpenRouter API调用失败: {error_msg}")
                return self._generate_fallback(prompt, style)
        
        except Exception as e:
            print(f"❌ OpenRouter API调用出错: {e}")
            return self._generate_fallback(prompt, style)
    
    def _select_model(self, style):
        """根据风格选择最适合的模型"""
        
        # 根据不同风格选择不同模型
        style_model_mapping = {
            'disney': 'dalle3',  # DALL-E 3适合卡通风格
            'anime': 'flux',     # Flux适合动漫风格
            'watercolor': 'midjourney',  # Midjourney适合艺术风格
            'oilpainting': 'midjourney',
            'pixel': 'stable_diffusion',  # Stable Diffusion适合像素艺术
            'cyberpunk': 'flux',
            'photography': 'dalle3',  # DALL-E 3适合写实风格
        }
        
        model_key = style_model_mapping.get(style, self.default_model)
        return self.models.get(model_key, self.models[self.default_model])
    
    def _build_full_prompt(self, prompt, style_config):
        """构建完整的提示词"""
        
        base_prompt = prompt
        
        # 添加风格描述
        if style_config:
            style_suffix = style_config.get('prompt_suffix', '')
            negative_prompt = style_config.get('negative_prompt', '')
            style_name = style_config.get('name', '')
            
            # 对于高保真3D卡通风格，专门针对写实到卡通的转换
            if 'reference_3d' in str(style_config) or '高保真3D卡通' in style_name:
                full_prompt = f"REALISTIC TO CARTOON TRANSFORMATION: Transform this realistic object/robot into cute cartoon version. {base_prompt}{style_suffix}. SPECIFIC CONVERSION RULES: 1) Round all sharp edges and corners, 2) Make proportions more chunky and toy-like, 3) Convert metallic/hard surfaces to soft plastic toy material, 4) Enlarge head/main features proportionally, 5) Add warmth and friendliness to the design, 6) Keep basic structure but make it adorable and approachable, 7) Apply C4D cartoon rendering with soft lighting."
            else:
                full_prompt = f"{base_prompt}{style_suffix}"
            
            # 为OpenRouter格式化负面提示词
            if negative_prompt:
                full_prompt += f". High quality, detailed, professional. Avoid: {negative_prompt}"
            else:
                full_prompt += ". High quality, detailed, professional artwork."
            
            return full_prompt
        
        return f"{base_prompt}. High quality, detailed, professional artwork."
    
    def _parse_openrouter_response(self, response_data, prompt, style):
        """解析OpenRouter API响应"""

        try:
            # OpenRouter的响应格式
            choices = response_data.get('choices', [])

            if not choices:
                print("❌ 响应中没有找到choices")
                return None

            choice = choices[0]
            message = choice.get('message', {})

            # 检查是否有图像数据
            images = message.get('images', [])
            if images:
                # 处理图像数据
                for image in images:
                    image_url = image.get('image_url', {}).get('url', '')
                    if image_url.startswith('data:image/'):
                        # Base64图像数据
                        print(f"🎨 找到Base64图像数据")
                        return self._save_base64_image(image_url, prompt, style)
                    elif image_url.startswith('http'):
                        # URL图像
                        print(f"🔗 找到图像URL: {image_url}")
                        return self._download_image_from_url(image_url, prompt, style)

            # 检查文本内容中是否有图像信息
            content = message.get('content', '')
            if 'http' in content:
                # 提取URL
                import re
                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                if urls:
                    image_url = urls[0]
                    print(f"🔗 从文本中找到图像URL: {image_url}")
                    return self._download_image_from_url(image_url, prompt, style)

            # 如果没有找到图像数据
            print(f"📋 OpenRouter响应内容: {content[:200]}...")
            
            # 生成一个示例图片作为备用
            return self._generate_fallback(prompt, style)
        
        except Exception as e:
            print(f"❌ 解析OpenRouter响应失败: {e}")
            return None
    
    def _download_image_from_url(self, image_url, prompt, style):
        """从URL下载图像"""
        
        try:
            print(f"📥 下载图像: {image_url}")
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                # 保存图像
                image = Image.open(BytesIO(response.content))
                return self._save_generated_image(image, prompt, style)
            else:
                print(f"❌ 下载图像失败: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ 下载图像出错: {e}")
            return None

    def _save_base64_image(self, base64_url, prompt, style):
        """保存Base64编码的图像"""

        try:
            # 解析Base64数据
            if base64_url.startswith('data:image/'):
                # 提取Base64数据部分
                header, data = base64_url.split(',', 1)
                image_data = base64.b64decode(data)

                # 创建PIL图像
                image = Image.open(BytesIO(image_data))
                return self._save_generated_image(image, prompt, style)
            else:
                print(f"❌ 无效的Base64图像格式")
                return None

        except Exception as e:
            print(f"❌ 处理Base64图像失败: {e}")
            return None

    def _save_generated_image(self, image, prompt, style):
        """保存生成的图像"""
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        safe_prompt = "".join(c for c in prompt[:20] if c.isalnum() or c in " ").strip()
        safe_prompt = safe_prompt.replace(" ", "_")
        
        filename = f"openrouter_{timestamp}_{unique_id}_{safe_prompt}.png"
        filepath = os.path.join(self.config.GENERATED_FOLDER, filename)
        
        # 确保目录存在
        os.makedirs(self.config.GENERATED_FOLDER, exist_ok=True)
        
        # 保存图像
        image.save(filepath, "PNG")
        
        return filepath
    
    def _generate_fallback(self, prompt, style):
        """备用图像生成方案"""
        
        # 导入并使用原有的fallback生成器
        try:
            from fallback_generator import create_sample_image
            return create_sample_image(prompt, style)
        except ImportError:
            print("❌ 备用生成器不可用")
            return None
    
    def test_connection(self):
        """测试OpenRouter API连接"""
        
        if not self.api_key or not self.api_key.startswith('sk-or-v1-'):
            return {
                'success': False,
                'error': 'OpenRouter API密钥未设置或格式不正确'
            }
        
        try:
            # 测试简单的文本生成
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:4000",
                "X-Title": "AI Image Generation Website"
            }
            
            data = {
                "model": "openai/gpt-3.5-turbo",  # 使用文本模型测试连接
                "messages": [{"role": "user", "content": "Hello, test connection"}],
                "max_tokens": 10
            }
            
            url = f"{self.base_url}/chat/completions"
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message': 'OpenRouter API连接正常',
                    'available_models': len(self.models),
                    'default_model': self.models[self.default_model]
                }
            else:
                return {
                    'success': False,
                    'error': f'API连接失败: {response.status_code} - {response.text[:100]}'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'连接测试失败: {str(e)}'
            }

# 全局实例
openrouter_generator = OpenRouterImageGenerator()
