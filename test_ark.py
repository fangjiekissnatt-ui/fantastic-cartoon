#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包ARK API测试工具
用于测试ARK API是否配置正确
"""

import requests
import json
from config import Config

def test_ark_api():
    """测试豆包ARK API"""
    print("🔍 测试豆包ARK API...")
    print("=" * 50)
    
    # 检查配置
    if not Config.validate_token():
        print("❌ ARK API密钥未配置")
        print("💡 请运行: python3 setup_ark.py")
        return False
    
    print(f"🔑 当前API密钥: {Config.ARK_API_KEY[:10]}...")
    print(f"🌐 API地址: {Config.ARK_BASE_URL}")
    print(f"🤖 模型ID: {Config.ARK_IMAGE_MODEL}")
    
    # 测试API连接
    print("\n📡 测试API连接...")
    
    url = f"{Config.ARK_BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Config.ARK_API_KEY}"
    }
    
    # 简单的测试请求
    test_data = {
        "model": Config.ARK_IMAGE_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "测试连接"
                    }
                ]
            }
        ],
        "stream": False
    }
    
    try:
        print("⏳ 发送测试请求...")
        response = requests.post(url, headers=headers, json=test_data, timeout=30)
        
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API连接成功!")
            try:
                result = response.json()
                print("📄 响应格式正确")
                return True
            except json.JSONDecodeError:
                print("⚠️ 响应不是有效的JSON格式")
                return False
        elif response.status_code == 401:
            print("❌ API密钥无效或过期")
            print("💡 请检查ARK API密钥是否正确")
            return False
        elif response.status_code == 403:
            print("❌ 没有访问权限")
            print("💡 请检查ARK API权限设置")
            return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            try:
                error_info = response.json()
                print(f"   错误详情: {error_info}")
            except:
                print(f"   错误文本: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("💡 请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败")
        print("💡 请检查网络连接和API地址")
        return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    success = test_ark_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 豆包ARK API配置成功!")
        print("🚀 现在可以重启服务器测试图片生成:")
        print("   python3 start_server.py")
    else:
        print("💡 ARK API配置有问题，请检查:")
        print("1. API密钥是否正确")
        print("2. 网络连接是否正常") 
        print("3. 模型ID是否有效")
        print("4. 运行 python3 setup_ark.py 重新配置")

