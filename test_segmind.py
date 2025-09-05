#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试Segmind API功能
这个脚本用来测试我们新添加的Segmind图片生成器是否正常工作
"""

import os
import sys
from segmind_image_generator import segmind_generator

def test_segmind_connection():
    """
    测试Segmind API连接
    """
    print("🔧 测试Segmind API连接...")
    print("="*50)
    
    # 测试API连接
    result = segmind_generator.test_connection()
    
    print(f"✅ 连接测试结果:")
    print(f"   成功: {result['success']}")
    if result['success']:
        print(f"   消息: {result['message']}")
        print(f"   模型: {result.get('model', '未知')}")
    else:
        print(f"   错误: {result['error']}")
    
    return result['success']

def test_segmind_generation():
    """
    测试Segmind图片生成功能
    需要一个测试图片作为输入
    """
    print("\n🎨 测试Segmind图片生成...")
    print("="*50)
    
    # 查找测试用的图片文件
    test_image_dirs = [
        'uploads',  # 上传文件夹
        'generated',  # 生成文件夹
        'static/styles'  # 静态文件夹
    ]
    
    test_image_path = None
    for dir_path in test_image_dirs:
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    test_image_path = os.path.join(dir_path, filename)
                    break
            if test_image_path:
                break
    
    if not test_image_path:
        print("⚠️ 没有找到测试图片，跳过生成测试")
        print("📝 提示：你可以在uploads文件夹中放一张图片来测试")
        return False
    
    print(f"📸 使用测试图片: {test_image_path}")
    
    # 测试生成图片
    try:
        result_path = segmind_generator.generate_image(
            prompt="transform this into a beautiful realistic photograph",
            style="realistic_transform",
            reference_image_path=test_image_path
        )
        
        if result_path:
            print(f"🎉 图片生成成功!")
            print(f"📁 保存位置: {result_path}")
            return True
        else:
            print("❌ 图片生成失败")
            return False
    
    except Exception as e:
        print(f"❌ 测试生成时出错: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("🚀 Segmind API 测试程序")
    print("="*50)
    print("这个程序会测试新添加的Segmind图片生成功能")
    print()
    
    # 测试连接
    connection_ok = test_segmind_connection()
    
    if connection_ok:
        print("\n✅ API连接正常，可以继续测试生成功能")
        # 测试生成
        generation_ok = test_segmind_generation()
        
        if generation_ok:
            print("\n🎊 所有测试通过！Segmind功能正常工作")
        else:
            print("\n⚠️ 生成测试失败，可能需要检查API密钥或网络连接")
    else:
        print("\n❌ API连接失败，请检查API密钥设置")
        print("💡 确保config.py中的SEGMIND_API_KEY设置正确")
    
    print("\n" + "="*50)
    print("测试完成")

if __name__ == "__main__":
    main()
