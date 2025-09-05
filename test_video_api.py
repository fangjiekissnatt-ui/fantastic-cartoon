#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试字节跳动图生视频API
基于用户提供的API端点和参数
"""

import requests
import json
import os
from config import Config

def test_video_generation():
    """测试图生视频API"""
    
    print("🎬 测试字节跳动图生视频API...")
    print("=" * 50)
    print(f"🔑 API密钥: {Config.ARK_API_KEY[:12]}...")
    print(f"🌐 API地址: https://ark.cn-beijing.volces.com")
    print(f"🎯 功能: 图像转视频生成")
    
    # 测试图生视频API
    print("\n📡 测试图像转视频API...")
    
    # 使用用户提供的API端点
    url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Config.ARK_API_KEY}"
    }
    
    # 使用用户提供的请求格式
    test_data = {
        "model": "ep-20250904152826-dxz7p",  # 用户提供的图生视频模型
        "content": [
            {
                "type": "text",
                "text": "一只可爱的卡通猫在花园里玩耍，阳光透过树叶洒下，温馨治愈的场景 --resolution 1080p --duration 5 --camerafixed false --watermark true"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/seepro_i2v.png"
                }
            }
        ]
    }
    
    print(f"🔗 测试字节跳动图生视频API端点")
    print(f"📋 请求数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        print(f"📡 发送请求到API...")
        response = requests.post(url, headers=headers, json=test_data, timeout=30)
        
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API响应成功")
            print(f"📋 API响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查是否包含任务ID
            if 'task_id' in result or 'id' in result:
                task_id = result.get('task_id') or result.get('id')
                print(f"🎯 视频生成任务已创建: {task_id}")
                print(f"💡 这是一个异步任务，需要轮询状态获取最终结果")
            
        else:
            error_text = response.text
            print(f"❌ API请求失败: {response.status_code}")
            try:
                error_json = response.json()
                print(f"   错误详情: {error_json}")
            except:
                print(f"   错误详情: {error_text}")
    
    except requests.exceptions.Timeout:
        print("⏰ 请求超时 - API响应较慢")
    except requests.exceptions.ConnectionError:
        print("🔌 连接失败 - 请检查网络连接")
    except Exception as e:
        print(f"💥 意外错误: {str(e)}")
    
    print("\n" + "=" * 50)
    print("💡 图生视频API测试总结:")
    print("1. 这是一个异步任务API")
    print("2. 成功调用会返回task_id")
    print("3. 需要轮询任务状态获取视频结果")
    print("4. 适合集成到我们的AI制图网站")
    print("5. 可以实现图片→视频的完整工作流")

if __name__ == "__main__":
    test_video_generation()

