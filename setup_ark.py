#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包ARK API设置工具
帮助用户轻松设置ARK API密钥
"""

import os
import sys

def setup_ark_api():
    """设置豆包ARK API密钥"""
    print("🔧 豆包ARK API设置工具")
    print("=" * 50)
    
    # 获取用户输入的API密钥
    api_key = input("请输入你的ARK API密钥: ").strip()
    
    if not api_key:
        print("❌ API密钥不能为空")
        return False
    
    # 读取当前配置文件
    config_file = "config.py"
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换API密钥
        old_line = "ARK_API_KEY = os.getenv('ARK_API_KEY', '')"
        new_line = f"ARK_API_KEY = os.getenv('ARK_API_KEY', '{api_key}')"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            # 写回文件
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ ARK API密钥设置成功!")
            print(f"🔑 密钥: {api_key[:10]}...")
            print("\n💡 现在可以运行以下命令测试:")
            print("   python3 test_ark.py")
            return True
        else:
            print("❌ 配置文件格式异常，请检查config.py")
            return False
            
    except FileNotFoundError:
        print("❌ 找不到config.py文件")
        return False
    except Exception as e:
        print(f"❌ 设置失败: {e}")
        return False

if __name__ == "__main__":
    setup_ark_api()

