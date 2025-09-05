#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试ARK API响应格式
查看豆包实际返回的内容
"""

import requests
import json
import os

def debug_ark_response():
    """测试并显示ARK API的详细响应"""
    
    # 使用环境变量中的API密钥
    api_key = "b122a8a1-da7b-4cbc-8304-0235a9e319a1"
    
    print("🔍 调试ARK API响应...")
    print("=" * 50)
    
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 测试数据
    data = {
        "model": "ep-20250904150244-tk8fb",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请生成一张可爱的卡通小猫图片"
                    }
                ]
            }
        ]
    }
    
    try:
        print("📡 发送请求...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("\n✅ JSON响应解析成功!")
                print("📄 完整响应内容:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                
                # 分析响应结构
                if 'choices' in result:
                    print(f"\n🔍 发现choices数组，长度: {len(result['choices'])}")
                    for i, choice in enumerate(result['choices']):
                        print(f"   选择 {i}: {choice}")
                        if 'message' in choice:
                            message = choice['message']
                            print(f"   消息角色: {message.get('role', '未知')}")
                            content = message.get('content', '')
                            print(f"   内容类型: {type(content)}")
                            print(f"   内容长度: {len(str(content))}")
                            print(f"   内容预览: {str(content)[:200]}...")
                
            except json.JSONDecodeError:
                print("❌ 响应不是有效的JSON格式")
                print(f"原始响应: {response.text}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    debug_ark_response()

