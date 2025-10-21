#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一参考图处理工具类
为所有模型提供统一的参考图参数格式
"""

import os
import base64
from typing import Optional, Dict, Any, List

class UnifiedReferenceHandler:
    """统一参考图处理器"""
    
    @staticmethod
    def image_to_base64(image_path: str) -> Optional[str]:
        """
        将图片文件转换为Base64编码
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            Base64编码的图片数据，失败时返回None
        """
        try:
            if not os.path.exists(image_path):
                print(f"⚠️ 图片文件不存在: {image_path}")
                return None
            
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                base64_data = base64.b64encode(img_data).decode('utf-8')
                print(f"✅ 图片Base64转换成功，数据长度: {len(base64_data)}")
                return base64_data
                
        except Exception as e:
            print(f"❌ 图片Base64转换失败: {e}")
            return None
    
    @staticmethod
    def build_openrouter_format(prompt: str, reference_image_path: Optional[str] = None, model: str = "default") -> Dict[str, Any]:
        """
        构建OpenRouter标准格式的请求数据
        
        Args:
            prompt: 文本提示词
            reference_image_path: 参考图片路径（可选）
            model: 模型标识
            
        Returns:
            符合OpenRouter格式的请求数据
        """
        # 基础请求结构
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": []
                }
            ],
            "modalities": ["image", "text"],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        # 添加文本提示
        data["messages"][0]["content"].append({
            "type": "text",
            "text": prompt
        })
        
        # 添加参考图片（如果提供）
        if reference_image_path:
            base64_data = UnifiedReferenceHandler.image_to_base64(reference_image_path)
            if base64_data:
                data["messages"][0]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"}
                })
                print(f"📸 已添加参考图片到OpenRouter格式请求中")
            else:
                print(f"⚠️ 参考图片处理失败，使用纯文本模式")
        
        return data
    
    @staticmethod
    def build_segmind_format(prompt: str, reference_image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        构建Segmind格式的请求数据
        
        Args:
            prompt: 文本提示词
            reference_image_path: 参考图片路径（必需）
            
        Returns:
            符合Segmind格式的请求数据
        """
        data = {
            'seed': None,
            'prompt': prompt,
            'aspect_ratio': "match_input_image",
            'output_format': "png",
            'safety_tolerance': 5,
            'guidance_scale': 7.5,
            'num_inference_steps': 20
        }
        
        # Segmind使用文件上传格式，不需要Base64
        if reference_image_path and os.path.exists(reference_image_path):
            print(f"📸 已准备参考图片用于Segmind格式请求: {reference_image_path}")
        else:
            print(f"⚠️ Segmind需要参考图片，但未提供或文件不存在")
        
        return data
    
    @staticmethod
    def get_openrouter_headers(api_key: str) -> Dict[str, str]:
        """
        获取OpenRouter标准请求头
        
        Args:
            api_key: API密钥
            
        Returns:
            标准化的请求头
        """
        return {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:4000',
            'X-Title': 'AI Image Generation Website'
        }
    
    @staticmethod
    def get_segmind_headers(api_key: str) -> Dict[str, str]:
        """
        获取Segmind标准请求头
        
        Args:
            api_key: API密钥
            
        Returns:
            标准化的请求头
        """
        return {
            'x-api-key': api_key
        }
    
    @staticmethod
    def validate_reference_image(image_path: Optional[str]) -> bool:
        """
        验证参考图片是否有效
        
        Args:
            image_path: 图片路径
            
        Returns:
            是否有效
        """
        if not image_path:
            return False
        
        if not os.path.exists(image_path):
            print(f"⚠️ 参考图片文件不存在: {image_path}")
            return False
        
        # 检查文件大小（限制为10MB）
        file_size = os.path.getsize(image_path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            print(f"⚠️ 参考图片文件过大: {file_size} bytes")
            return False
        
        # 检查文件扩展名
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext not in allowed_extensions:
            print(f"⚠️ 不支持的图片格式: {file_ext}")
            return False
        
        print(f"✅ 参考图片验证通过: {image_path}")
        return True
    
    @staticmethod
    def get_supported_formats() -> Dict[str, str]:
        """
        获取各模型支持的格式信息
        
        Returns:
            模型格式信息字典
        """
        return {
            "openrouter_standard": "统一OpenRouter格式 - 适用于Flux Kontext Pro, GPT-4o, Claude等",
            "segmind_native": "Segmind原生格式 - 适用于Flux Kontext Pro (直接文件上传)",
            "gpt_image1_legacy": "GPT Image 1传统格式 - 使用reference_images字段"
        }
    
    @staticmethod
    def format_compatibility_matrix() -> Dict[str, List[str]]:
        """
        获取格式兼容性矩阵
        
        Returns:
            格式兼容性信息
        """
        return {
            "openrouter_standard": [
                "Flux Kontext Pro (通过OpenRouter)",
                "GPT-4o",
                "Claude 3.5 Sonnet", 
                "Gemini 2.5 Flash",
                "GPT Image 1 (修改后)"
            ],
            "segmind_native": [
                "Flux Kontext Pro (直接调用)",
                "其他Segmind模型"
            ],
            "gpt_image1_legacy": [
                "GPT Image 1 (原始格式)"
            ]
        }

# 全局实例
unified_handler = UnifiedReferenceHandler()
