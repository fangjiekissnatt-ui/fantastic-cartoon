#!/usr/bin/env python3
# 检查服务器状态

import requests
import socket

def check_port(port):
    """检查端口是否可用"""
    try:
        response = requests.get(f'http://localhost:{port}', timeout=2)
        return response.status_code == 200
    except:
        return False

def find_server():
    """找到运行中的服务器"""
    for port in [4000, 4001, 4002, 4003, 4004, 4005, 5000, 8000, 3000]:
        if check_port(port):
            print(f"✅ 找到运行中的服务器: http://localhost:{port}")
            return port
    return None

if __name__ == "__main__":
    print("🔍 检查AI制图网站服务器状态...")
    
    port = find_server()
    if port:
        print(f"🎉 服务器正常运行！")
        print(f"🌐 访问地址: http://localhost:{port}")
        print(f"📱 请在浏览器中打开这个地址")
    else:
        print("❌ 没有找到运行中的服务器")
        print("请运行: python3 start_server.py")

