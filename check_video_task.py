#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
查询字节跳动图生视频任务状态
"""

import requests
import json
import time
from config import Config

def check_task_status(task_id):
    """查询视频生成任务状态"""
    
    print(f"🔍 查询视频任务状态...")
    print(f"📋 任务ID: {task_id}")
    print("=" * 50)
    
    # 查询任务状态的端点（推测）
    url = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Config.ARK_API_KEY}"
    }
    
    try:
        print(f"📡 发送查询请求...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 查询成功")
            print(f"📋 任务状态: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查任务状态
            status = result.get('status', '未知')
            print(f"🎯 当前状态: {status}")
            
            if status == 'completed':
                print("🎬 视频生成完成！")
                video_url = result.get('video_url') or result.get('result', {}).get('video_url')
                if video_url:
                    print(f"🔗 视频下载链接: {video_url}")
            elif status == 'processing':
                print("⏳ 视频正在生成中...")
            elif status == 'failed':
                print("❌ 视频生成失败")
                error = result.get('error_message')
                if error:
                    print(f"   错误信息: {error}")
            
        else:
            error_text = response.text
            print(f"❌ 查询失败: {response.status_code}")
            try:
                error_json = response.json()
                print(f"   错误详情: {error_json}")
            except:
                print(f"   错误详情: {error_text}")
    
    except Exception as e:
        print(f"💥 查询出错: {str(e)}")

def main():
    """主函数"""
    # 使用刚才测试创建的任务ID
    task_id = "cgt-20250904160603-4lhm5"
    
    print("🎬 字节跳动图生视频任务查询工具")
    print("=" * 50)
    
    # 查询任务状态
    check_task_status(task_id)
    
    print("\n💡 提示:")
    print("- 如果状态是processing，说明视频正在生成")
    print("- 通常需要几分钟到十几分钟完成")
    print("- 可以定期运行此脚本查看进度")

if __name__ == "__main__":
    main()

