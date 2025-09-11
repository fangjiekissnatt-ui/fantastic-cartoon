#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI图像生成器基础类
整合多个图像生成服务，提供统一的接口
"""

import os
from openrouter_image_generator import openrouter_generator
from fallback_generator import FallbackImageGenerator

class AIImageGenerator:
    """
    AI图像生成器主类
    这个类整合了多个不同的AI图像生成服务
    """
    
    def __init__(self):
        """初始化AI图像生成器"""
        print("🤖 AI图像生成器初始化完成")
        
        # 初始化备用生成器
        self.fallback_generator = FallbackImageGenerator()
        
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
        
        print(f"🎨 开始生成图片...")
        print(f"   提示词: {prompt}")
        print(f"   风格: {style}")
        print(f"   参考图: {'有' if reference_image_path else '无'}")
        
        try:
            # 优先使用OpenRouter生成器
            generated_image_path = openrouter_generator.generate_image(
                prompt=prompt,
                style=style,
                reference_image_path=reference_image_path
            )
            
            # 如果OpenRouter失败，使用备用生成器
            if not generated_image_path:
                print("⚠️ OpenRouter生成失败，使用备用生成器...")
                generated_image_path = self.fallback_generator.generate_image(
                    prompt=prompt,
                    style=style,
                    reference_image_path=reference_image_path
                )
            
            return generated_image_path
        
        except Exception as e:
            print(f"❌ AI图像生成失败: {e}")
            # 最后的回退方案
            return self.fallback_generator.generate_image(
                prompt=prompt,
                style=style,
                reference_image_path=reference_image_path
            )
    
    def test_connection(self):
        """测试API连接"""
        return openrouter_generator.test_connection()

# 全局实例
ai_generator = AIImageGenerator()


