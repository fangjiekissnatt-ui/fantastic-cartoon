# 文档处理生成器
# 这个模块负责处理文档上传和内容提取，使用豆包API

import requests
import os
import json
from config import Config

class DocumentProcessor:
    """
    文档处理生成器类
    使用豆包API处理各种文档格式并提取关键信息
    """
    
    def __init__(self):
        """
        初始化文档处理器
        从配置文件读取API密钥
        """
        self.api_key = Config.DOUBAO_DOCUMENT_API_KEY
        self.base_url = Config.DOUBAO_DOCUMENT_BASE_URL
        self.timeout = 60  # 1分钟超时
    
    def test_connection(self):
        """
        测试API连接是否正常
        """
        try:
            if not self.api_key or self.api_key == "YOUR_API_KEY":
                return {
                    'success': False,
                    'error': '豆包文档理解API密钥未设置'
                }
            
            # 检查API密钥格式
            if not self.api_key or len(self.api_key) < 10:
                return {
                    'success': False,
                    'error': '豆包API密钥格式不正确'
                }
            
            return {
                'success': True,
                'message': '豆包文档理解API配置正确'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'豆包API连接测试失败: {str(e)}'
            }
    
    def extract_text_from_file(self, file_path):
        """
        从文件中提取文本内容
        
        参数:
        - file_path: 文件路径
        
        返回:
        - 成功: 提取的文本内容
        - 失败: None
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                return self._extract_from_txt(file_path)
            elif file_extension == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_extension in ['.doc', '.docx']:
                return self._extract_from_doc(file_path)
            else:
                print(f"不支持的文件格式: {file_extension}")
                return None
                
        except Exception as e:
            print(f"文件文本提取失败: {str(e)}")
            return None
    
    def _extract_from_txt(self, file_path):
        """
        从TXT文件提取文本
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    return f.read()
            except:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
    
    def _extract_from_pdf(self, file_path):
        """
        从PDF文件提取文本
        """
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            print("需要安装PyPDF2: pip install PyPDF2")
            return None
        except Exception as e:
            print(f"PDF提取失败: {str(e)}")
            return None
    
    def _extract_from_doc(self, file_path):
        """
        从DOC/DOCX文件提取文本
        """
        try:
            import docx
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            print("需要安装python-docx: pip install python-docx")
            return None
        except Exception as e:
            print(f"DOC提取失败: {str(e)}")
            return None
    
    def process_document(self, file_path):
        """
        处理文档并提取关键信息用于图像生成
        
        参数:
        - file_path: 文档文件路径
        
        返回:
        - 成功: 处理后的提示词
        - 失败: None
        """
        try:
            print(f"📄 开始处理文档: {file_path}")
            
            # 提取文本内容
            text_content = self.extract_text_from_file(file_path)
            if not text_content:
                print("❌ 无法提取文档内容")
                return None
            
            print(f"✅ 成功提取文本，长度: {len(text_content)} 字符")
            
            # 如果文本太长，先截取前部分
            if len(text_content) > 8000:
                text_content = text_content[:8000] + "..."
                print("⚠️ 文本过长，已截取前8000字符")
            
            # 使用豆包分析文档内容
            analysis_result = self._analyze_with_doubao(text_content)
            
            if analysis_result:
                print("✅ 文档分析完成")
                return analysis_result
            else:
                print("❌ 豆包分析失败，使用本地分析")
                # 当豆包失败时，提供简单的本地分析
                return self._local_analysis(text_content)
                
        except Exception as e:
            print(f"💥 文档处理过程中出现错误: {str(e)}")
            return None
    
    def _analyze_with_doubao(self, text_content):
        """
        使用豆包分析文档内容
        
        参数:
        - text_content: 文档文本内容
        
        返回:
        - 成功: 分析结果
        - 失败: None
        """
        try:
            # 构建分析提示词
            analysis_prompt = f"""
请分析以下文档内容，提取关键信息并生成适合AI图像生成的描述：

文档内容：
{text_content}

请按照以下格式输出：
1. 文档主题/类型：
2. 关键概念/元素：
3. 视觉风格建议：
4. 图像生成提示词：

要求：
- 提取最重要的视觉元素
- 建议适合的艺术风格
- 生成简洁但富有创意的提示词
- 用中文回答
"""
            
            # 构建请求数据
            data = {
                "model": "deepseek-v3-1-250821",  # 豆包模型ID
                "messages": [
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # 设置请求头
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            print(f"📡 正在调用豆包API分析文档...")
            
            # 发送API请求
            response = requests.post(
                self.base_url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            
            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    analysis_text = result['choices'][0]['message']['content']
                    print("✅ 豆包分析成功")
                    return analysis_text
                else:
                    print("❌ 豆包响应格式错误")
                    return None
            else:
                print(f"❌ 豆包API调用失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("⏰ 豆包API请求超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"🌐 豆包API网络错误: {str(e)}")
            return None
        except Exception as e:
            print(f"💥 豆包分析过程中出现错误: {str(e)}")
            return None
    
    def _local_analysis(self, text_content):
        """
        本地文档分析（当豆包API不可用时使用）
        
        参数:
        - text_content: 文档文本内容
        
        返回:
        - 分析结果
        """
        try:
            print("🔍 开始本地文档分析...")
            
            # 简单的关键词提取和分析
            keywords = []
            visual_elements = []
            
            # 常见视觉元素关键词
            visual_keywords = {
                '动物': ['猫', '狗', '鸟', '鱼', '兔子', '熊', '老虎', '狮子', '大象', '马', '牛', '羊', '猪'],
                '自然': ['花', '树', '草', '山', '水', '海', '天空', '云', '太阳', '月亮', '星星', '森林', '花园'],
                '建筑': ['房子', '建筑', '城堡', '塔', '桥', '门', '窗', '屋顶', '墙'],
                '人物': ['人', '孩子', '女孩', '男孩', '女人', '男人', '老人', '朋友', '家人'],
                '物品': ['书', '笔', '桌子', '椅子', '车', '飞机', '船', '玩具', '食物', '衣服'],
                '颜色': ['红', '蓝', '绿', '黄', '紫', '橙', '粉', '黑', '白', '灰', '棕'],
                '情感': ['快乐', '悲伤', '愤怒', '惊讶', '害怕', '爱', '希望', '梦想', '温暖', '可爱']
            }
            
            # 分析文本内容
            for category, words in visual_keywords.items():
                for word in words:
                    if word in text_content:
                        if category not in [kw['category'] for kw in keywords]:
                            keywords.append({'category': category, 'word': word})
                        visual_elements.append(word)
            
            # 生成分析结果
            analysis = f"""📄 文档分析结果：

1. 文档主题/类型：创意描述文档
2. 关键概念/元素：{', '.join(set(visual_elements)) if visual_elements else '未识别到特定元素'}
3. 视觉风格建议：温馨可爱的插画风格
4. 图像生成提示词：{text_content}

💡 提示：基于文档内容，建议生成温馨、可爱的插画风格图像。"""
            
            print("✅ 本地分析完成")
            return analysis
            
        except Exception as e:
            print(f"💥 本地分析过程中出现错误: {str(e)}")
            return f"📄 文档内容：{text_content}\n\n💡 提示：请基于以上内容生成相应的图像。"
    
    def analyze_image(self, image_path):
        """
        分析图片内容，生成文字描述
        """
        try:
            print(f"🖼️ 开始分析图片: {image_path}")
            
            # 检查文件是否存在
            if not os.path.exists(image_path):
                raise Exception("图片文件不存在")
            
            # 尝试使用豆包API分析
            try:
                return self._analyze_image_with_doubao(image_path)
            except Exception as api_error:
                print(f"⚠️ 豆包API分析失败: {str(api_error)}")
                print("🔄 回退到本地分析...")
                return self._analyze_image_local(image_path)
                
        except Exception as e:
            print(f"💥 图片分析过程中出现错误: {str(e)}")
            # 返回基础的图片描述
            return f"📸 图片分析：一张图片\n\n💡 提示：请基于上传的图片内容生成相应的图像描述。"
    
    def _analyze_image_local(self, image_path):
        """
        智能本地图片分析功能 - 专业版
        """
        try:
            from PIL import Image
            import colorsys
            import numpy as np
            
            # 打开图片
            with Image.open(image_path) as img:
                # 转换为RGB模式进行分析
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 获取图片基本信息
                width, height = img.size
                format_name = img.format or "未知格式"
                
                # 智能分析图片内容
                analysis_result = self._deep_image_analysis(img)
                
                # 生成专业的描述
                description = f"📸 智能图片分析报告：\n\n"
                
                # 基础信息
                description += f"🔍 基础信息：\n"
                description += f"• 尺寸：{width} × {height} 像素\n"
                description += f"• 格式：{format_name}\n"
                description += f"• 宽高比：{width/height:.2f}\n\n"
                
                # 内容分析
                description += f"🎯 内容分析：\n"
                description += f"• 主要特征：{analysis_result['main_features']}\n"
                description += f"• 颜色特征：{analysis_result['color_analysis']}\n"
                description += f"• 构图特征：{analysis_result['composition']}\n\n"
                
                # 风格建议
                description += f"🎨 风格建议：\n"
                description += f"• 推荐风格：{analysis_result['recommended_styles']}\n"
                description += f"• 适合场景：{analysis_result['suitable_scenes']}\n\n"
                
                # 生成提示词
                description += f"💡 生成提示词：\n"
                description += f"{analysis_result['prompt_suggestion']}\n\n"
                
                description += f"✨ 基于以上分析，您可以调整描述文字来获得更好的生成效果！"
                
                print(f"✅ 智能本地图片分析成功")
                return description
                
        except Exception as e:
            print(f"❌ 本地图片分析失败: {str(e)}")
            raise e
    
    def _deep_image_analysis(self, img):
        """
        深度图片分析
        """
        try:
            # 转换为numpy数组进行分析
            img_array = np.array(img)
            width, height = img.size
            
            # 分析主要特征
            main_features = self._analyze_main_features(img_array, width, height)
            
            # 分析颜色特征
            color_analysis = self._analyze_color_features(img_array)
            
            # 分析构图特征
            composition = self._analyze_composition(width, height, img_array)
            
            # 生成风格建议
            recommended_styles = self._get_recommended_styles(main_features, color_analysis)
            
            # 生成场景建议
            suitable_scenes = self._get_suitable_scenes(main_features, composition)
            
            # 生成提示词建议
            prompt_suggestion = self._generate_smart_prompt(main_features, color_analysis, composition)
            
            return {
                'main_features': main_features,
                'color_analysis': color_analysis,
                'composition': composition,
                'recommended_styles': recommended_styles,
                'suitable_scenes': suitable_scenes,
                'prompt_suggestion': prompt_suggestion
            }
            
        except Exception as e:
            print(f"❌ 深度分析失败: {str(e)}")
            return {
                'main_features': "图片内容",
                'color_analysis': "颜色特征",
                'composition': "构图特征",
                'recommended_styles': "多种风格",
                'suitable_scenes': "通用场景",
                'prompt_suggestion': "请描述图片内容"
            }
    
    def _analyze_main_features(self, img_array, width, height):
        """分析主要特征"""
        try:
            # 分析图片的复杂度
            gray = np.mean(img_array, axis=2)
            edges = np.abs(np.diff(gray, axis=1)).sum() + np.abs(np.diff(gray, axis=0)).sum()
            complexity = edges / (width * height)
            
            if complexity > 1000:
                return "高细节复杂图片"
            elif complexity > 500:
                return "中等细节图片"
            else:
                return "简洁风格图片"
                
        except:
            return "图片内容"
    
    def _analyze_color_features(self, img_array):
        """分析颜色特征"""
        try:
            # 计算平均颜色
            avg_color = np.mean(img_array, axis=(0, 1))
            
            # 分析颜色分布
            color_std = np.std(img_array, axis=(0, 1))
            
            # 判断主要颜色
            if avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]:
                main_color = "暖色调"
            elif avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:
                main_color = "中性色调"
            else:
                main_color = "冷色调"
            
            # 判断饱和度
            saturation = np.mean(color_std)
            if saturation > 50:
                saturation_desc = "高饱和度"
            elif saturation > 25:
                saturation_desc = "中等饱和度"
            else:
                saturation_desc = "低饱和度"
            
            return f"{main_color}, {saturation_desc}"
            
        except:
            return "颜色特征"
    
    def _analyze_composition(self, width, height, img_array):
        """分析构图特征"""
        try:
            aspect_ratio = width / height
            
            if aspect_ratio > 1.5:
                return "宽屏横向构图"
            elif aspect_ratio > 1.2:
                return "横向构图"
            elif aspect_ratio < 0.67:
                return "竖屏竖向构图"
            elif aspect_ratio < 0.83:
                return "竖向构图"
            else:
                return "正方形构图"
                
        except:
            return "构图特征"
    
    def _get_recommended_styles(self, main_features, color_analysis):
        """获取推荐风格"""
        styles = []
        
        if "高细节" in main_features:
            styles.append("逼真摄影")
            styles.append("高清写实")
        elif "简洁" in main_features:
            styles.append("扁平风格")
            styles.append("简约设计")
        
        if "暖色调" in color_analysis:
            styles.append("温馨风格")
        elif "冷色调" in color_analysis:
            styles.append("清新风格")
        
        return ", ".join(styles) if styles else "多种风格可选"
    
    def _get_suitable_scenes(self, main_features, composition):
        """获取适合场景"""
        scenes = []
        
        if "横向构图" in composition:
            scenes.append("风景场景")
            scenes.append("建筑场景")
        elif "竖向构图" in composition:
            scenes.append("人像场景")
            scenes.append("物品特写")
        else:
            scenes.append("通用场景")
        
        return ", ".join(scenes)
    
    def _generate_smart_prompt(self, main_features, color_analysis, composition):
        """生成智能提示词"""
        prompt_parts = []
        
        # 基于特征生成提示词
        if "高细节" in main_features:
            prompt_parts.append("high quality, detailed")
        elif "简洁" in main_features:
            prompt_parts.append("simple, clean")
        
        # 基于颜色生成提示词
        if "暖色调" in color_analysis:
            prompt_parts.append("warm colors")
        elif "冷色调" in color_analysis:
            prompt_parts.append("cool colors")
        
        # 基于构图生成提示词
        if "横向构图" in composition:
            prompt_parts.append("landscape")
        elif "竖向构图" in composition:
            prompt_parts.append("portrait")
        
        # 添加通用质量提示词
        prompt_parts.append("professional, artistic")
        
        return ", ".join(prompt_parts)
    
    def _generate_style_suggestions(self, aspect_ratio, total_pixels):
        """生成风格建议"""
        suggestions = []
        
        if aspect_ratio > 1.5:
            suggestions.append("宽屏风景图")
        elif aspect_ratio < 0.67:
            suggestions.append("竖屏人像图")
        
        if total_pixels > 2000000:
            suggestions.append("高清细节图")
        
        return ", ".join(suggestions) if suggestions else "通用图片"
    
    def _suggest_art_styles(self, features):
        """推荐艺术风格"""
        if "高清图片" in features or "超高清图片" in features:
            return "逼真摄影, 高清写实"
        elif "正方形图片" in features:
            return "卡通风格, 扁平设计"
        else:
            return "多种风格可选"
    
    def _generate_prompt_suggestions(self, features):
        """生成提示词建议"""
        suggestions = []
        
        if "横向图片" in features:
            suggestions.append("landscape")
        if "竖向图片" in features:
            suggestions.append("portrait")
        if "高清图片" in features:
            suggestions.append("high quality, detailed")
        
        return ", ".join(suggestions) if suggestions else "根据内容描述"
    
    def _analyze_image_with_doubao(self, image_path):
        """
        使用豆包API分析图片 - 修复版
        """
        try:
            # 读取图片并转换为base64
            import base64
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
            
            # 构建分析提示词
            analysis_prompt = """请详细分析这张图片的内容，生成适合AI图像生成的描述文字。请包含以下信息：

1. 主体对象：图片中的主要人物、动物、物体等
2. 外观特征：颜色、形状、大小、材质等
3. 动作姿态：人物的动作、表情、姿态等
4. 环境背景：场景、背景、环境等
5. 风格特征：艺术风格、色调、氛围等

请用简洁明了的中文描述，适合作为AI图像生成的提示词。"""
            
            # 尝试多种API调用方式
            
            # 方式1: 使用通用模型
            try:
                data = {
                    "model": "doubao-pro-32k",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": analysis_prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                print(f"📡 尝试方式1: 使用doubao-pro-32k模型...")
                response = requests.post(self.base_url, json=data, headers=headers, timeout=self.timeout)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        description = result['choices'][0]['message']['content'].strip()
                        print(f"✅ 豆包API图片分析成功")
                        return description
                
            except Exception as e:
                print(f"⚠️ 方式1失败: {str(e)}")
            
            # 方式2: 使用doubao-lite模型
            try:
                data = {
                    "model": "doubao-lite-32k",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": analysis_prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                
                print(f"📡 尝试方式2: 使用doubao-lite-32k模型...")
                response = requests.post(self.base_url, json=data, headers=headers, timeout=self.timeout)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        description = result['choices'][0]['message']['content'].strip()
                        print(f"✅ 豆包API图片分析成功")
                        return description
                
            except Exception as e:
                print(f"⚠️ 方式2失败: {str(e)}")
            
            # 方式3: 使用doubao-pro-4k模型
            try:
                data = {
                    "model": "doubao-pro-4k",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": analysis_prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                
                print(f"📡 尝试方式3: 使用doubao-pro-4k模型...")
                response = requests.post(self.base_url, json=data, headers=headers, timeout=self.timeout)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        description = result['choices'][0]['message']['content'].strip()
                        print(f"✅ 豆包API图片分析成功")
                        return description
                
            except Exception as e:
                print(f"⚠️ 方式3失败: {str(e)}")
            
            # 所有方式都失败
            raise Exception("所有豆包API模型都无法使用")
                
        except Exception as e:
            print(f"❌ 豆包API图片分析失败: {str(e)}")
            raise e

# 创建全局实例
document_processor = DocumentProcessor()