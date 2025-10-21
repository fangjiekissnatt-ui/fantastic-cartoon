#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成失败诊断脚本
检查各个组件的状态和可能的错误原因
"""

import sys
import os
import traceback
from PIL import Image, ImageDraw

# 添加项目路径
sys.path.append('.')

def create_test_image():
    """创建测试图片"""
    img = Image.new('RGB', (100, 100), color='red')
    draw = ImageDraw.Draw(img)
    draw.text((20, 40), "TEST", fill='white')
    
    filename = "test_diagnosis.png"
    img.save(filename)
    print(f"✅ 创建测试图片: {filename}")
    return filename

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入")
    print("=" * 50)
    
    modules_to_test = [
        'config',
        'unified_reference_handler',
        'gpt_image1_generator',
        'openrouter_image_generator',
        'segmind_image_generator',
        'gemini_image_generator',
        'fallback_generator',
        'prompt_enhancer',
        'document_processor'
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name}: 导入成功")
        except Exception as e:
            print(f"❌ {module_name}: 导入失败 - {e}")
            failed_imports.append(module_name)
    
    print(f"\n📊 导入结果: {len(modules_to_test) - len(failed_imports)}/{len(modules_to_test)} 成功")
    if failed_imports:
        print(f"❌ 失败的模块: {failed_imports}")
    
    return len(failed_imports) == 0

def test_config():
    """测试配置"""
    print("\n🔧 测试配置")
    print("=" * 50)
    
    try:
        from config import Config
        
        # 测试API密钥
        api_keys = {
            'OpenRouter': Config.OPENROUTER_API_KEY,
            'GPT Image 1': Config.GPT_IMAGE1_API_KEY,
            'Segmind': 'SG_d0d17371e4b1a360',  # 硬编码的密钥
            'Doubao': Config.DOUBAO_DOCUMENT_API_KEY
        }
        
        for name, key in api_keys.items():
            if key and len(key) > 10:
                print(f"✅ {name}: API密钥已配置")
            else:
                print(f"⚠️ {name}: API密钥未配置或格式不正确")
        
        # 测试模型配置
        models = Config.OPENROUTER_IMAGE_MODELS
        print(f"✅ OpenRouter模型数量: {len(models)}")
        
        # 测试风格配置
        styles = Config.STYLE_CONFIGS
        print(f"✅ 风格配置数量: {len(styles)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_generators():
    """测试生成器"""
    print("\n🎨 测试生成器")
    print("=" * 50)
    
    test_image = create_test_image()
    
    generators_to_test = [
        ('GPT Image 1', 'gpt_image1_generator', 'GPTImage1Generator'),
        ('OpenRouter', 'openrouter_image_generator', 'OpenRouterImageGenerator'),
        ('Segmind', 'segmind_image_generator', 'SegmindImageGenerator'),
        ('Gemini', 'gemini_image_generator', 'GeminiImageGenerator'),
        ('Fallback', 'fallback_generator', 'FallbackImageGenerator')
    ]
    
    results = {}
    
    for name, module_name, class_name in generators_to_test:
        try:
            module = __import__(module_name)
            generator_class = getattr(module, class_name)
            generator = generator_class()
            
            print(f"✅ {name}: 初始化成功")
            
            # 测试生成方法
            try:
                result = generator.generate_image(
                    prompt="测试提示词",
                    style="cyberpunk",
                    reference_image_path=test_image
                )
                
                if result:
                    print(f"   ✅ {name}: 生成成功 - {result}")
                    results[name] = "成功"
                else:
                    print(f"   ⚠️ {name}: 生成返回None")
                    results[name] = "返回None"
                    
            except Exception as e:
                print(f"   ❌ {name}: 生成失败 - {e}")
                results[name] = f"失败: {e}"
                
        except Exception as e:
            print(f"❌ {name}: 初始化失败 - {e}")
            results[name] = f"初始化失败: {e}"
    
    # 清理测试文件
    if os.path.exists(test_image):
        os.remove(test_image)
    
    return results

def test_unified_handler():
    """测试统一处理器"""
    print("\n🔧 测试统一处理器")
    print("=" * 50)
    
    try:
        from unified_reference_handler import unified_handler
        
        test_image = create_test_image()
        
        # 测试OpenRouter格式
        openrouter_data = unified_handler.build_openrouter_format(
            prompt="测试提示词",
            reference_image_path=test_image,
            model="test-model"
        )
        
        print(f"✅ OpenRouter格式构建成功")
        print(f"   📊 数据大小: {len(str(openrouter_data))} 字符")
        
        # 测试Segmind格式
        segmind_data = unified_handler.build_segmind_format(
            prompt="测试提示词",
            reference_image_path=test_image
        )
        
        print(f"✅ Segmind格式构建成功")
        print(f"   📊 数据大小: {len(str(segmind_data))} 字符")
        
        # 测试图片验证
        is_valid = unified_handler.validate_reference_image(test_image)
        print(f"✅ 图片验证: {'通过' if is_valid else '失败'}")
        
        # 清理测试文件
        if os.path.exists(test_image):
            os.remove(test_image)
        
        return True
        
    except Exception as e:
        print(f"❌ 统一处理器测试失败: {e}")
        traceback.print_exc()
        return False

def test_app_routes():
    """测试应用路由"""
    print("\n🌐 测试应用路由")
    print("=" * 50)
    
    try:
        import requests
        
        # 测试健康检查
        response = requests.get('http://localhost:4000/health', timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查: 正常")
        else:
            print(f"⚠️ 健康检查: 状态码 {response.status_code}")
        
        # 测试生成接口（不实际生成）
        try:
            response = requests.post('http://localhost:4000/generate', 
                                   data={'prompt': 'test', 'model': 'auto'},
                                   timeout=5)
            print(f"✅ 生成接口: 可访问 (状态码: {response.status_code})")
        except requests.exceptions.Timeout:
            print("⚠️ 生成接口: 请求超时")
        except Exception as e:
            print(f"⚠️ 生成接口: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 应用路由测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始生成失败诊断")
    print("=" * 80)
    
    # 测试1: 模块导入
    imports_ok = test_imports()
    
    # 测试2: 配置
    config_ok = test_config()
    
    # 测试3: 统一处理器
    handler_ok = test_unified_handler()
    
    # 测试4: 生成器
    generator_results = test_generators()
    
    # 测试5: 应用路由
    routes_ok = test_app_routes()
    
    print("\n" + "=" * 80)
    print("📊 诊断总结")
    print("=" * 80)
    
    print(f"✅ 模块导入: {'正常' if imports_ok else '异常'}")
    print(f"✅ 配置检查: {'正常' if config_ok else '异常'}")
    print(f"✅ 统一处理器: {'正常' if handler_ok else '异常'}")
    print(f"✅ 应用路由: {'正常' if routes_ok else '异常'}")
    
    print("\n🎨 生成器状态:")
    for name, status in generator_results.items():
        print(f"   {name}: {status}")
    
    print("\n💡 建议:")
    if not imports_ok:
        print("   - 检查模块导入错误，修复依赖问题")
    if not config_ok:
        print("   - 检查配置文件，确保API密钥正确")
    if not handler_ok:
        print("   - 检查统一处理器实现")
    if not routes_ok:
        print("   - 检查应用是否正常运行")
    
    # 检查是否有生成器完全失败
    failed_generators = [name for name, status in generator_results.items() 
                        if "失败" in status or "初始化失败" in status]
    
    if failed_generators:
        print(f"   - 重点关注失败的生成器: {failed_generators}")
    else:
        print("   - 所有生成器基本正常，可能是网络或API问题")

if __name__ == "__main__":
    main()
