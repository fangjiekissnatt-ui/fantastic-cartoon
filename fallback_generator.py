#!/usr/bin/env python3
# 备用图片生成器
# 当Hugging Face API不可用时，生成示例图片

import os
import uuid
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import Config

class FallbackImageGenerator:
    """
    备用图片生成器
    当网络API不可用时，生成带有用户描述的示例图片
    """
    
    def __init__(self):
        # 确保生成文件夹存在
        if not os.path.exists(Config.GENERATED_FOLDER):
            os.makedirs(Config.GENERATED_FOLDER)
    
    def generate_image(self, prompt, style='realistic', reference_image_path=None):
        """
        生成示例图片
        
        参数:
            prompt: 用户输入的描述文字
            style: 选择的风格
            reference_image_path: 参考图片路径（如果存在会显示提示信息）
        
        返回:
            生成的图片文件路径
        """
        
        try:
            print("🎨 使用本地示例图片生成器...")
            print(f"   描述: {prompt}")
            print(f"   风格: {style}")
            print(f"   参考图: {'有' if reference_image_path and os.path.exists(reference_image_path) else '无'}")
            
            # 如果有参考图，在生成的图片上添加提示信息
            has_reference = reference_image_path and os.path.exists(reference_image_path)
            
            # 根据风格选择颜色主题（支持9种专业风格）
            color_themes = {
                'disney': {'bg': '#FFB6C1', 'text': '#8B4513', 'accent': '#FF69B4'},
                'anime': {'bg': '#FFA07A', 'text': '#FF4500', 'accent': '#FF1493'},
                'watercolor': {'bg': '#E6E6FA', 'text': '#4B0082', 'accent': '#9370DB'},
                'oilpainting': {'bg': '#DEB887', 'text': '#8B4513', 'accent': '#CD853F'},
                'pixel': {'bg': '#32CD32', 'text': '#006400', 'accent': '#00FF00'},
                'minimalist': {'bg': '#F5F5F5', 'text': '#2F2F2F', 'accent': '#808080'},
                'cyberpunk': {'bg': '#1E1E1E', 'text': '#00FFFF', 'accent': '#FF00FF'},
                'traditional_chinese': {'bg': '#F5F5DC', 'text': '#2F4F4F', 'accent': '#696969'},
                'photography': {'bg': '#87CEEB', 'text': '#2C3E50', 'accent': '#3498DB'}
            }
            
            theme = color_themes.get(style, color_themes['disney'])
            
            # 创建高质量图片
            width, height = 512, 512
            image = Image.new('RGB', (width, height), theme['bg'])
            draw = ImageDraw.Draw(image)
            
            # 添加渐变背景效果
            self.add_gradient_background(image, theme, style)
            
            # 尝试使用系统字体
            try:
                # macOS系统字体
                font_large = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 36)
                font_medium = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 24)
                font_small = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 18)
            except:
                # 如果找不到系统字体，使用默认字体
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # 绘制标题
            title = f"{self.get_style_name(style)}风格"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((width - title_width) // 2, 50), title, fill=theme['text'], font=font_large)
            
            # 绘制装饰元素
            self.draw_decorative_elements(draw, width, height, theme, style)
            
            # 如果有参考图，添加提示信息
            if has_reference:
                reference_text = "📸 参考图已加载"
                ref_bbox = draw.textbbox((0, 0), reference_text, font=font_medium)
                ref_width = ref_bbox[2] - ref_bbox[0]
                draw.text(((width - ref_width) // 2, 100), reference_text, fill=theme['accent'], font=font_medium)
            
            # 绘制用户描述（分行显示）
            words = prompt.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                bbox = draw.textbbox((0, 0), test_line, font=font_medium)
                if bbox[2] - bbox[0] < width - 40:  # 留40像素边距
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            # 显示描述文字
            start_y = (height // 2 - len(lines) * 15) + (50 if has_reference else 0)
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font_medium)
                line_width = bbox[2] - bbox[0]
                draw.text(((width - line_width) // 2, start_y + i * 30), line, fill=theme['text'], font=font_medium)
            
            # 绘制底部信息
            footer = "AI制图工作室 - 示例模式"
            footer_bbox = draw.textbbox((0, 0), footer, font=font_small)
            footer_width = footer_bbox[2] - footer_bbox[0]
            draw.text(((width - footer_width) // 2, height - 40), footer, fill=theme['accent'], font=font_small)
            
            # 保存图片
            filename = self.generate_filename(prompt)
            filepath = os.path.join(Config.GENERATED_FOLDER, filename)
            image.save(filepath, 'PNG')
            
            print(f"✅ 示例图片已生成: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ 示例图片生成失败: {str(e)}")
            return None
    
    def draw_decorative_elements(self, draw, width, height, theme, style):
        """绘制装饰元素（支持9种风格）"""
        
        if style == 'disney':
            # 绘制星星和魔法元素
            for i in range(15):
                x = (i * 73) % width
                y = (i * 37) % height
                draw.ellipse([x-3, y-3, x+3, y+3], fill=theme['accent'])
                
        elif style == 'anime':
            # 绘制樱花花瓣
            for i in range(12):
                x = (i * 89) % width
                y = (i * 43) % height
                draw.ellipse([x-4, y-2, x+4, y+6], fill=theme['accent'])
                
        elif style == 'watercolor':
            # 绘制水彩斑点
            for i in range(8):
                x = (i * 127) % width
                y = (i * 67) % height
                for j in range(3):
                    r = 8 + j * 3
                    draw.ellipse([x-r, y-r, x+r, y+r], outline=theme['accent'])
                    
        elif style == 'oilpainting':
            # 绘制厚重笔触效果
            for i in range(0, width, 80):
                for j in range(0, height, 80):
                    draw.rectangle([i, j, i+20, j+40], outline=theme['accent'], width=2)
                    
        elif style == 'pixel':
            # 绘制像素方块
            for i in range(0, width, 32):
                for j in range(0, height, 32):
                    if (i + j) % 64 == 0:
                        draw.rectangle([i, j, i+8, j+8], fill=theme['accent'])
                        
        elif style == 'minimalist':
            # 绘制极简几何
            draw.line([50, 50, width-50, 50], fill=theme['accent'], width=2)
            draw.line([50, height-50, width-50, height-50], fill=theme['accent'], width=2)
            
        elif style == 'cyberpunk':
            # 绘制霓虹线条
            for i in range(0, width, 60):
                draw.line([i, 0, i, height], fill=theme['accent'], width=1)
            for i in range(0, height, 40):
                draw.line([0, i, width, i], fill=theme['accent'], width=1)
                
        elif style == 'traditional_chinese':
            # 绘制山水元素
            for i in range(3):
                x = 100 + i * 150
                y = 200 + i * 20
                # 简化的山峰形状
                points = [(x, y), (x+30, y-30), (x+60, y)]
                draw.polygon(points, outline=theme['accent'])
                
        elif style == 'photography':
            # 绘制取景框
            draw.rectangle([30, 30, width-30, height-30], outline=theme['accent'], width=3)
            # 九宫格线
            draw.line([width//3, 30, width//3, height-30], fill=theme['accent'], width=1)
            draw.line([2*width//3, 30, 2*width//3, height-30], fill=theme['accent'], width=1)
            draw.line([30, height//3, width-30, height//3], fill=theme['accent'], width=1)
            draw.line([30, 2*height//3, width-30, 2*height//3], fill=theme['accent'], width=1)
    
    def add_gradient_background(self, image, theme, style):
        """添加渐变背景效果"""
        width, height = image.size
        pixels = image.load()
        
        # 根据风格选择渐变方向和效果
        if style in ['disney', 'anime']:
            # 从上到下的温暖渐变
            for y in range(height):
                ratio = y / height
                # 简化的渐变计算
                if y < height // 3:
                    # 上部分保持原色
                    continue
                elif y > 2 * height // 3:
                    # 下部分稍微暗一些
                    for x in range(width):
                        r, g, b = pixels[x, y]
                        pixels[x, y] = (max(0, r-20), max(0, g-20), max(0, b-20))
        
        elif style == 'cyberpunk':
            # 添加扫描线效果
            draw = ImageDraw.Draw(image)
            for y in range(0, height, 4):
                draw.line([0, y, width, y], fill=(0, 255, 255, 50), width=1)
    
    def get_style_name(self, style_code):
        """将风格代码转换为中文名称（支持9种风格）"""
        style_names = {
            'disney': '迪士尼动画',
            'anime': '日式动漫',
            'watercolor': '水彩画风',
            'oilpainting': '油画风格',
            'pixel': '像素艺术',
            'minimalist': '极简主义',
            'cyberpunk': '赛博朋克',
            'traditional_chinese': '中国山水画',
            'photography': '专业摄影'
        }
        return style_names.get(style_code, '专业创作')
    
    def generate_filename(self, prompt):
        """生成文件名"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        safe_prompt = "".join(c for c in prompt[:20] if c.isalnum() or c in (' ', '_')).rstrip()
        safe_prompt = safe_prompt.replace(' ', '_')
        return f"demo_{timestamp}_{unique_id}_{safe_prompt}.png"

# 全局函数供外部调用
def create_sample_image(prompt, style='realistic'):
    """
    创建示例图片的全局函数
    
    参数:
        prompt: 用户输入的描述文字
        style: 选择的风格
    
    返回:
        生成的图片文件路径
    """
    generator = FallbackImageGenerator()
    return generator.generate_image(prompt, style)
