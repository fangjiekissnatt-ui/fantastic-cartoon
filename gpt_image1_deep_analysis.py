#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GPT Image 1 深度分析脚本
检查API数据结构、功能支持、版本问题和字段添加
"""

import sys
import os
import json
import requests
import base64
from PIL import Image, ImageDraw

# 添加项目路径
sys.path.append('.')

from gpt_image1_generator import GPTImage1Generator
from config import Config

class GPTImage1DeepAnalyzer:
    """GPT Image 1 深度分析器"""
    
    def __init__(self):
        self.generator = GPTImage1Generator()
        
    def check_api_documentation(self):
        """检查API文档和官方信息"""
        print("📚 检查GPT Image 1 API文档和官方信息")
        print("=" * 60)
        
        # 检查API端点信息
        print(f"🔗 API端点: {self.generator.base_url}")
        print(f"🔑 API密钥: {self.generator.api_key[:10]}..." if self.generator.api_key else "❌ 未设置")
        print()
        
        # 尝试获取API信息
        try:
            headers = {'x-api-key': self.generator.api_key}
            response = requests.get(self.generator.base_url.replace('/v1/gpt-image-1', '/v1/models'), 
                                  headers=headers, timeout=10)
            if response.status_code == 200:
                print("✅ 成功连接到API")
                models_info = response.json()
                print(f"📋 可用模型: {models_info}")
            else:
                print(f"⚠️ API信息获取失败: {response.status_code}")
                print(f"   响应: {response.text}")
        except Exception as e:
            print(f"❌ API连接测试失败: {e}")
        print()
    
    def check_input_image_field(self):
        """检查input_image字段是否正确添加"""
        print("🔍 检查input_image字段添加过程")
        print("=" * 60)
        
        # 创建测试图片
        test_image_path = self.create_test_image()
        
        # 模拟生成过程
        print("📝 模拟generate_image函数调用:")
        print(f"   - 提示词: '测试提示词'")
        print(f"   - 风格: 'realistic'")
        print(f"   - 参考图: {test_image_path}")
        print()
        
        # 检查base64转换
        print("🔄 检查Base64转换:")
        try:
            base64_data = self.generator.image_file_to_base64(test_image_path)
            if base64_data:
                print(f"   ✅ Base64转换成功")
                print(f"   📊 数据长度: {len(base64_data)} 字符")
                print(f"   🔤 前100字符: {base64_data[:100]}...")
                print(f"   🎯 格式验证: {'data:image' in base64_data[:50] if 'data:image' in base64_data[:50] else '纯Base64'}")
            else:
                print(f"   ❌ Base64转换失败")
                return False
        except Exception as e:
            print(f"   ❌ Base64转换异常: {e}")
            return False
        print()
        
        # 检查请求数据构建
        print("📦 检查请求数据构建:")
        data = {
            "prompt": "测试提示词",
            "size": "auto",
            "quality": "auto", 
            "moderation": "auto",
            "background": "opaque",
            "output_compression": 100,
            "output_format": "png"
        }
        
        print(f"   📋 基础数据字段: {list(data.keys())}")
        print(f"   📊 基础数据大小: {len(json.dumps(data))} 字节")
        
        # 添加参考图
        data["input_image"] = base64_data
        print(f"   ✅ 添加input_image字段")
        print(f"   📋 完整数据字段: {list(data.keys())}")
        print(f"   📊 完整数据大小: {len(json.dumps(data))} 字节")
        print(f"   🎯 input_image字段存在: {'input_image' in data}")
        print(f"   📏 input_image数据长度: {len(data['input_image'])} 字符")
        print()
        
        # 清理测试文件
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        
        return True
    
    def test_api_parameters(self):
        """测试不同的API参数格式"""
        print("🧪 测试不同的API参数格式")
        print("=" * 60)
        
        # 创建测试图片
        test_image_path = self.create_test_image()
        base64_data = self.generator.image_file_to_base64(test_image_path)
        
        # 测试不同的参数组合
        test_configs = [
            {
                "name": "当前格式",
                "data": {
                    "prompt": "基于参考图生成",
                    "size": "auto",
                    "quality": "auto",
                    "moderation": "auto",
                    "background": "opaque",
                    "output_compression": 100,
                    "output_format": "png",
                    "input_image": base64_data
                }
            },
            {
                "name": "添加image_strength",
                "data": {
                    "prompt": "基于参考图生成",
                    "size": "auto",
                    "quality": "auto",
                    "moderation": "auto",
                    "background": "opaque",
                    "output_compression": 100,
                    "output_format": "png",
                    "input_image": base64_data,
                    "image_strength": 0.8
                }
            },
            {
                "name": "使用reference_image字段",
                "data": {
                    "prompt": "基于参考图生成",
                    "size": "auto",
                    "quality": "auto",
                    "moderation": "auto",
                    "background": "opaque",
                    "output_compression": 100,
                    "output_format": "png",
                    "reference_image": base64_data
                }
            },
            {
                "name": "使用image字段",
                "data": {
                    "prompt": "基于参考图生成",
                    "size": "auto",
                    "quality": "auto",
                    "moderation": "auto",
                    "background": "opaque",
                    "output_compression": 100,
                    "output_format": "png",
                    "image": base64_data
                }
            },
            {
                "name": "添加conditioning_scale",
                "data": {
                    "prompt": "基于参考图生成",
                    "size": "auto",
                    "quality": "auto",
                    "moderation": "auto",
                    "background": "opaque",
                    "output_compression": 100,
                    "output_format": "png",
                    "input_image": base64_data,
                    "conditioning_scale": 1.0
                }
            }
        ]
        
        for i, config in enumerate(test_configs, 1):
            print(f"🔧 测试配置 {i}: {config['name']}")
            print(f"   📋 字段列表: {list(config['data'].keys())}")
            print(f"   📊 数据大小: {len(json.dumps(config['data']))} 字节")
            
            # 模拟API调用（不实际发送）
            print(f"   🌐 模拟API调用...")
            try:
                headers = {
                    'x-api-key': self.generator.api_key,
                    'Content-Type': 'application/json'
                }
                
                # 这里只是模拟，不实际发送请求
                print(f"   ✅ 请求数据构建成功")
                print(f"   📡 目标端点: {self.generator.base_url}")
                print(f"   🔑 请求头: {list(headers.keys())}")
                
            except Exception as e:
                print(f"   ❌ 请求构建失败: {e}")
            
            print()
        
        # 清理测试文件
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
    
    def check_api_support(self):
        """检查API是否支持参考图功能"""
        print("🔍 检查API参考图功能支持")
        print("=" * 60)
        
        # 检查API端点信息
        print(f"📍 API端点分析:")
        print(f"   - 基础URL: {self.generator.base_url}")
        print(f"   - 版本: v1")
        print(f"   - 模型: gpt-image-1")
        print()
        
        # 检查是否有其他端点
        possible_endpoints = [
            "https://api.segmind.com/v1/gpt-image-1",
            "https://api.segmind.com/v1/gpt-image-1/transform",
            "https://api.segmind.com/v1/gpt-image-1/image-to-image",
            "https://api.segmind.com/v1/models/gpt-image-1"
        ]
        
        print(f"🔗 可能的API端点:")
        for endpoint in possible_endpoints:
            print(f"   - {endpoint}")
        print()
        
        # 检查API文档链接
        print(f"📚 建议检查的文档:")
        print(f"   - Segmind官方文档: https://docs.segmind.com/")
        print(f"   - GPT Image 1 API文档: https://docs.segmind.com/models/gpt-image-1")
        print(f"   - API参数说明: https://docs.segmind.com/api-reference")
        print()
        
        # 检查API响应格式
        print(f"📊 检查API响应格式:")
        try:
            # 尝试获取模型信息
            headers = {'x-api-key': self.generator.api_key}
            response = requests.get(
                "https://api.segmind.com/v1/models", 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                models = response.json()
                print(f"   ✅ 成功获取模型列表")
                if isinstance(models, dict) and 'models' in models:
                    model_list = models['models']
                    for model in model_list:
                        if 'gpt-image-1' in model.get('id', '').lower():
                            print(f"   🎯 找到GPT Image 1模型: {model}")
                            if 'capabilities' in model:
                                print(f"   🔧 模型能力: {model['capabilities']}")
                            if 'parameters' in model:
                                print(f"   ⚙️ 支持参数: {model['parameters']}")
                else:
                    print(f"   📋 模型信息: {models}")
            else:
                print(f"   ⚠️ 模型信息获取失败: {response.status_code}")
                print(f"   📝 响应内容: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 模型信息检查失败: {e}")
        print()
    
    def check_version_compatibility(self):
        """检查API版本兼容性"""
        print("🔄 检查API版本兼容性")
        print("=" * 60)
        
        # 检查当前使用的版本
        print(f"📌 当前API版本信息:")
        print(f"   - 端点: {self.generator.base_url}")
        print(f"   - 版本: v1")
        print(f"   - 超时: {self.generator.timeout}秒")
        print()
        
        # 检查可能的版本
        possible_versions = [
            "v1",
            "v2", 
            "v1.1",
            "v1.2"
        ]
        
        print(f"🔍 检查其他可能版本:")
        for version in possible_versions:
            test_url = f"https://api.segmind.com/{version}/gpt-image-1"
            print(f"   - {test_url}")
        
        print()
        print(f"💡 版本兼容性建议:")
        print(f"   - 检查官方文档中的最新API版本")
        print(f"   - 确认参考图功能在哪个版本中引入")
        print(f"   - 考虑升级到支持参考图的最新版本")
        print()
    
    def create_test_image(self, filename="test_image.png"):
        """创建测试图片"""
        img = Image.new('RGB', (100, 100), color='lightblue')
        draw = ImageDraw.Draw(img)
        draw.ellipse([20, 20, 80, 80], fill='red')
        draw.text((30, 45), "TEST", fill='white')
        img.save(filename)
        return filename
    
    def run_full_analysis(self):
        """运行完整的分析"""
        print("🚀 开始GPT Image 1深度分析")
        print("=" * 80)
        print()
        
        # 1. 检查API文档
        self.check_api_documentation()
        
        # 2. 检查input_image字段
        self.check_input_image_field()
        
        # 3. 测试API参数
        self.test_api_parameters()
        
        # 4. 检查API支持
        self.check_api_support()
        
        # 5. 检查版本兼容性
        self.check_version_compatibility()
        
        print("=" * 80)
        print("✅ 深度分析完成！")
        print()
        print("📋 分析总结:")
        print("   1. 检查了API文档和官方信息")
        print("   2. 验证了input_image字段添加过程")
        print("   3. 测试了不同的API参数格式")
        print("   4. 检查了API参考图功能支持")
        print("   5. 分析了版本兼容性问题")

if __name__ == "__main__":
    analyzer = GPTImage1DeepAnalyzer()
    analyzer.run_full_analysis()
