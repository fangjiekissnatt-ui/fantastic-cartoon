#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建风格预览图片占位符
为每个美术风格生成对应的预览图片
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_style_preview(style_name, style_color, emoji, filename):
    """创建风格预览图片"""
    
    # 创建80x80的图片
    size = (80, 80)
    image = Image.new('RGB', size, color=style_color)
    draw = ImageDraw.Draw(image)
    
    # 尝试使用系统字体
    try:
        # macOS 系统字体
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 10)
    except:
        try:
            # 备用字体
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 10)
        except:
            # 使用默认字体
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # 添加emoji (如果支持的话)
    try:
        # 计算emoji位置（居中上方）
        bbox = draw.textbbox((0, 0), emoji, font=font_large)
        emoji_width = bbox[2] - bbox[0]
        emoji_height = bbox[3] - bbox[1]
        emoji_x = (size[0] - emoji_width) // 2
        emoji_y = 15
        
        draw.text((emoji_x, emoji_y), emoji, font=font_large, fill='white')
    except:
        # 如果emoji不支持，画一个简单的形状
        draw.ellipse([25, 15, 55, 45], fill='white', outline='lightgray')
    
    # 添加风格名称
    try:
        bbox = draw.textbbox((0, 0), style_name, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x = (size[0] - text_width) // 2
        text_y = 55
        
        draw.text((text_x, text_y), style_name, font=font_small, fill='white')
    except:
        pass
    
    # 保存图片
    output_path = f"static/styles/{filename}"
    image.save(output_path, 'JPEG', quality=85)
    print(f"✅ 创建风格预览: {output_path}")

def main():
    """创建所有风格预览图片"""
    print("🎨 开始创建风格预览图片...")
    
    # 确保目录存在
    os.makedirs("static/styles", exist_ok=True)
    
    # 定义所有风格
    styles = [
        ("迪士尼", "#FF6B9D", "🏰", "disney.jpg"),
        ("动漫", "#FF8A80", "🎌", "anime.jpg"), 
        ("水彩", "#81C784", "🎨", "watercolor.jpg"),
        ("油画", "#8D6E63", "🖼️", "oilpainting.jpg"),
        ("像素", "#64B5F6", "🕹️", "pixel.jpg"),
        ("极简", "#E0E0E0", "⭕", "minimalist.jpg"),
        ("赛博", "#AB47BC", "🌃", "cyberpunk.jpg"),
        ("山水", "#4DB6AC", "🏔️", "traditional_chinese.jpg"),
        ("摄影", "#FFB74D", "📸", "photography.jpg")
    ]
    
    # 创建每个风格的预览图
    for style_name, color, emoji, filename in styles:
        create_style_preview(style_name, color, emoji, filename)
    
    print(f"\n✅ 成功创建 {len(styles)} 个风格预览图片！")
    print("📁 图片保存在: static/styles/ 目录")

if __name__ == "__main__":
    main()

