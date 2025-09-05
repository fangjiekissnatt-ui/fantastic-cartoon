#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试字节跳动视觉API
验证图像生成功能
"""

import requests
import json
from config import Config

def test_visual_api():
    """测试字节跳动视觉API"""
    print("🔍 测试字节跳动视觉API...")
    print("=" * 50)
    
    # 检查配置
    if not Config.ARK_API_KEY:
        print("❌ API密钥未配置")
        return False
    
    print(f"🔑 API密钥: {Config.ARK_API_KEY[:10]}...")
    print(f"🌐 API地址: {Config.VISUAL_API_BASE_URL}")
    print(f"🤖 模型: {Config.VISUAL_IMAGE_MODEL}")
    
    # 测试API连接
    print("\n📡 测试图像生成API...")
    
    # 尝试将Action参数放在URL中
    url = f"{Config.VISUAL_API_BASE_URL}/?Action=CVprocess&Version=2018-08-01"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Config.ARK_API_KEY}"
    }
    
    # 请求体只包含具体的服务参数
    test_data = {
        "ServiceId": "text2image",
        "Req": {
            "prompt": "a cute cartoon cat",
            "model_version": Config.VISUAL_IMAGE_MODEL,
            "width": 512,
            "height": 512,
            "scale": 7.5,
            "ddim_steps": 20,
            "return_url": True
        }
    }
    
    print(f"🔗 测试字节跳动视觉API端点")
    print(f"📋 请求数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=test_data, timeout=60)
        
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API连接成功!")
            try:
                result = response.json()
                print("📄 响应格式正确")
                print(f"📋 响应内容: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
                return True
            except json.JSONDecodeError:
                print("⚠️ 响应不是有效的JSON格式")
                print(f"📄 原始响应: {response.text[:200]}...")
                return False
        elif response.status_code == 401:
            print("❌ API密钥无效或过期")
            return False
        elif response.status_code == 403:
            print("❌ 没有访问权限")
            return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            try:
                error_info = response.json()
                print(f"   错误详情: {error_info}")
            except:
                print(f"   错误文本: {response.text[:200]}...")
            return False
                
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败")
        return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    success = test_visual_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 字节跳动视觉API配置成功!")
        print("🚀 现在可以生成真实的AI图片了!")
    else:
        print("💡 视觉API配置有问题，建议:")
        print("1. 检查API密钥是否正确")
        print("2. 确认API端点地址") 
        print("3. 检查网络连接")
        print("4. 验证账号权限和余额")
        print("5. 当前使用本地示例生成，功能正常")
