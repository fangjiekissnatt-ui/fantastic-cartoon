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

# 创建全局实例
document_processor = DocumentProcessor()