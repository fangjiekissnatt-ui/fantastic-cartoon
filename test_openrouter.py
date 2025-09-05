#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试OpenRouter API功能
"""

import os
from openrouter_image_generator import openrouter_generator

def test_openrouter():
    """测试OpenRouter设置和连接"""
    
    print("🧪 测试OpenRouter AI图像生成...")
    print("=" * 60)
    
    # 1. 测试API连接
    print("🔗 1. 测试API连接...")
    connection_result = openrouter_generator.test_connection()
    
    if connection_result['success']:
        print(f"✅ OpenRouter API连接成功")
        print(f"📋 连接信息: {connection_result.get('message', '')}")
        print(f"🎯 可用模型数量: {connection_result.get('available_models', 0)}")
        print(f"🤖 默认模型: {connection_result.get('default_model', '')}")
    else:
        print(f"❌ OpenRouter API连接失败: {connection_result['error']}")
        print("💡 可能的原因:")
        print("   1. API密钥无效或已过期")
        print("   2. 网络连接问题")
        print("   3. OpenRouter服务暂时不可用")
    
    print("\n" + "-" * 60)
    
    # 2. 测试图像生成（如果API可用）
    if connection_result['success']:
        print("🎨 2. 测试图像生成...")
        
        test_cases = [
            {
                'prompt': '一只可爱的卡通猫咪坐在彩虹上',
                'style': 'disney',
                'description': 'Disney风格测试'
            },
            {
                'prompt': '赛博朋克城市夜景，霓虹灯闪烁',
                'style': 'cyberpunk', 
                'description': '赛博朋克风格测试'
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 测试案例 {i}: {test_case['description']}")
            print(f"📋 提示词: {test_case['prompt']}")
            print(f"🎨 风格: {test_case['style']}")
            
            try:
                result_path = openrouter_generator.generate_image(
                    prompt=test_case['prompt'],
                    style=test_case['style']
                )
                
                if result_path and os.path.exists(result_path):
                    print(f"✅ 图像生成成功!")
                    print(f"📁 文件路径: {result_path}")
                    
                    # 获取文件大小
                    file_size = os.path.getsize(result_path)
                    print(f"📊 文件大小: {file_size / 1024:.1f} KB")
                else:
                    print(f"❌ 图像生成失败或文件不存在")
            
            except Exception as e:
                print(f"❌ 图像生成过程出错: {e}")
    
    else:
        print("⏭️ 2. 跳过图像生成测试（API不可用）")
    
    print("\n" + "=" * 60)
    print("💡 OpenRouter集成说明:")
    print("1. OpenRouter是AI模型聚合平台，支持多种先进模型")
    print("2. 支持Flux、DALL-E 3、Midjourney、Stable Diffusion等")
    print("3. 根据不同风格自动选择最合适的模型")
    print("4. 智能回退机制确保服务始终可用")
    print("5. 高质量图像生成，支持多种艺术风格")

if __name__ == "__main__":
    test_openrouter()

