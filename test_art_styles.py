#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试豆包对各种美术风格的理解能力
生成新的风格配置
"""

import requests
import json

def test_art_style(style_name, description):
    """测试豆包对特定美术风格的理解"""
    
    api_key = "b122a8a1-da7b-4cbc-8304-0235a9e319a1"
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = f"""请详细描述{style_name}的特点，包括：
1. 核心视觉特征
2. 色彩搭配
3. 构图特点
4. 适合的AI绘图提示词（中英文各一个）
5. 代表性的元素

描述对象：{description}"""
    
    data = {
        "model": "ep-20250904150244-tk8fb",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return content
        else:
            return f"API错误: {response.status_code}"
    except Exception as e:
        return f"请求异常: {e}"

def main():
    """测试多种美术风格"""
    print("🎨 测试豆包大模型的美术风格理解能力")
    print("=" * 50)
    
    # 定义要测试的风格
    styles = [
        ("迪士尼动画风格", "一只可爱的小狐狸"),
        ("日式动漫风格", "一个年轻的武士"),
        ("水彩画风格", "一座山间小屋"),
        ("油画风格", "一片向日葵田"),
        ("像素艺术风格", "一个8位游戏角色"),
        ("极简主义风格", "一个现代建筑"),
        ("赛博朋克风格", "一个未来城市"),
        ("中国山水画风格", "山间云雾缭绕"),
    ]
    
    results = {}
    
    for style_name, description in styles:
        print(f"\n🔍 测试风格: {style_name}")
        print(f"📝 描述对象: {description}")
        print("-" * 30)
        
        result = test_art_style(style_name, description)
        results[style_name] = result
        
        # 显示结果预览
        print(f"📋 结果预览: {result[:200]}...")
        print()
    
    # 保存完整结果
    with open("美术风格分析结果.txt", "w", encoding="utf-8") as f:
        f.write("🎨 豆包大模型美术风格分析结果\n")
        f.write("=" * 50 + "\n\n")
        
        for style_name, result in results.items():
            f.write(f"## {style_name}\n")
            f.write("-" * 30 + "\n")
            f.write(result)
            f.write("\n\n" + "=" * 50 + "\n\n")
    
    print("✅ 测试完成！结果已保存到 美术风格分析结果.txt")

if __name__ == "__main__":
    main()

