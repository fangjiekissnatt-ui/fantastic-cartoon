#!/usr/bin/env python3
# 测试Hugging Face API连接

import requests
from config import Config

def test_api():
    """测试API连接"""
    
    print("🔍 测试Hugging Face API连接...")
    print("="*50)
    
    # 检查token
    if not Config.validate_token():
        print("❌ API Token未设置")
        return False
    
    print(f"✅ API Token已设置: {Config.HUGGINGFACE_TOKEN[:10]}...")
    
    # 测试简单的API调用
    headers = {
        "Authorization": f"Bearer {Config.HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 使用最简单的模型和请求
    test_model = "nlpconnect/vit-gpt2-image-captioning"  # 这个模型响应更快
    api_url = f"https://api-inference.huggingface.co/models/{test_model}"
    
    payload = {
        "inputs": "a photo of a cat"
    }
    
    try:
        print(f"🌐 测试连接到: {test_model}")
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        print(f"📡 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API连接正常!")
            return True
        elif response.status_code == 503:
            print("⏳ 模型正在加载中，这是正常的")
            print("💡 等待几分钟后再试")
            return True
        else:
            print(f"❌ API错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        return False

def test_image_generation():
    """测试图像生成"""
    
    print("\n🎨 测试图像生成API...")
    print("="*50)
    
    headers = {
        "Authorization": f"Bearer {Config.HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 使用简单的请求
    model = Config.DEFAULT_MODEL
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    payload = {
        "inputs": "a beautiful sunset over mountains"
    }
    
    try:
        print(f"🖼️  测试模型: {model}")
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        
        print(f"📡 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 图像生成API正常!")
            print(f"📊 响应大小: {len(response.content)} bytes")
            return True
        elif response.status_code == 503:
            print("⏳ 图像生成模型正在加载中")
            print("💡 第一次使用需要等待几分钟")
            return True
        else:
            print(f"❌ 图像生成失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Hugging Face API 诊断工具")
    print("="*50)
    
    # 基础连接测试
    basic_ok = test_api()
    
    if basic_ok:
        # 图像生成测试
        image_ok = test_image_generation()
        
        if image_ok:
            print("\n🎉 所有测试通过!")
            print("💡 你的API设置正确，可以正常使用")
        else:
            print("\n⚠️  基础连接正常，但图像生成有问题")
            print("💡 可能需要等待模型加载，或尝试其他模型")
    else:
        print("\n❌ API连接有问题")
        print("💡 请检查:")
        print("   1. 网络连接是否正常")
        print("   2. API Token是否正确")
        print("   3. Hugging Face服务是否可用")

