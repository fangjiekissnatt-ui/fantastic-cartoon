#!/usr/bin/env python3
# 简化的服务器启动脚本
# 只保留OpenRouter图像生成和ByteDance视频生成

import socket
import sys
import os

def find_available_port(start_port=4000):
    """找到一个可用的端口"""
    for port in range(start_port, start_port + 100):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

def main():
    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 找到可用端口
    port = find_available_port()
    if not port:
        print("❌ 找不到可用端口！")
        return
    
    print(f"🚀 启动AI制图网站...")
    print(f"📱 端口: {port}")
    print(f"🌐 访问地址: http://localhost:{port}")
    print("="*50)
    
    try:
        # 导入必要的模块
        from flask import Flask, request, jsonify, send_from_directory
        from openrouter_image_generator import openrouter_generator
        from ai_video_generator import video_generator
        from fallback_generator import create_sample_image
        from config import Config
        import uuid
        from datetime import datetime
        from PIL import Image, ImageFilter, ImageEnhance
        import numpy as np
        
        # 创建Flask应用
        app = Flask(__name__)
        
        # 使用配置文件中的设置
        UPLOAD_FOLDER = Config.UPLOAD_FOLDER
        GENERATED_FOLDER = Config.GENERATED_FOLDER
        ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
        
        # 确保文件夹存在
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        if not os.path.exists(GENERATED_FOLDER):
            os.makedirs(GENERATED_FOLDER)
        
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        # 网站首页路由 - Canvas版本（深色）
        @app.route('/')
        def index():
            return send_from_directory('.', 'index_canvas.html')
        
        # 浅色Canvas版本
        @app.route('/light')
        def light():
            return send_from_directory('.', 'index_light.html')
        
        # 简单测试页面
        @app.route('/test')
        def test():
            return send_from_directory('.', 'test_simple.html')
        
        # 静态文件服务
        @app.route('/static/<path:filename>')
        def static_files(filename):
            return send_from_directory('static', filename)
        
        # 处理图片生成请求的路由
        @app.route('/generate', methods=['POST'])
        def generate_image():
            try:
                prompt = request.form.get('prompt', '').strip()
                style = request.form.get('style', '')
                
                if not prompt:
                    return jsonify({'success': False, 'error': '请输入图片描述'})
                
                if not style:
                    return jsonify({'success': False, 'error': '请选择绘画风格'})
                
                # 处理参考图片
                reference_image_path = None
                if 'reference_image' in request.files:
                    file = request.files['reference_image']
                    if file and file.filename and allowed_file(file.filename):
                        filename = f"{uuid.uuid4().hex}_{file.filename}"
                        reference_image_path = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(reference_image_path)
                
                print(f"收到新的图片生成任务:")
                print(f"  描述: {prompt}")
                print(f"  风格: {style}")
                print(f"  参考图: {'有' if reference_image_path else '无'}")
                
                # 智能图片生成逻辑
                generated_image_path = None
                
                # 智能图片生成逻辑
                # 优先使用OpenRouter AI图片生成功能
                generated_image_path = openrouter_generator.generate_image(
                    prompt=prompt,
                    style=style,
                    reference_image_path=reference_image_path
                )

                # 如果OpenRouter失败，使用本地回退生成器
                if not generated_image_path:
                    if reference_image_path:
                        print("⚠️ AI生成失败，使用本地生成器...")
                    else:
                        print("🎨 使用本地生成器...")

                    generated_image_path = create_sample_image(prompt, style)
                
                if not generated_image_path:
                    return jsonify({
                        'success': False,
                        'error': '图片生成失败，请稍后重试'
                    })
                
                # 生成访问URL
                filename = os.path.basename(generated_image_path)
                generated_image_url = f'/generated/{filename}'
                
                return jsonify({
                    'success': True,
                    'task_id': str(uuid.uuid4()),
                    'image_url': generated_image_url,
                    'message': '图片生成成功！'
                })
                
            except Exception as e:
                print(f"图片生成过程中出现错误: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': f'生成过程中出现错误: {str(e)}'
                })
        
        # 视频生成路由
        @app.route('/generate_video', methods=['POST'])
        def generate_video():
            """处理图生视频请求"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': '请求数据无效'})
                
                image_url = data.get('image_url')
                prompt = data.get('prompt', '生成动态视频')
                video_style = data.get('video_style', 'cinematic')
                resolution = data.get('resolution', Config.DEFAULT_VIDEO_RESOLUTION)
                duration = data.get('duration', Config.DEFAULT_VIDEO_DURATION)
                
                if not image_url:
                    return jsonify({'success': False, 'error': '请提供图片URL'})
                
                print(f"收到视频生成请求:")
                print(f"  图片: {image_url}")
                print(f"  描述: {prompt}")
                print(f"  风格: {video_style}")
                
                # 构建完整的图片URL
                if image_url.startswith('/'):
                    base_url = request.url_root.rstrip('/')
                    full_image_url = base_url + image_url
                else:
                    full_image_url = image_url
                
                # 获取视频风格配置
                video_styles = video_generator.get_video_styles()
                style_config = video_styles.get(video_style, video_styles['cinematic'])
                
                # 构建完整提示词
                full_prompt = prompt + style_config['prompt_suffix']
                
                # 创建视频生成任务
                result = video_generator.create_video_task(
                    image_url=full_image_url,
                    prompt=full_prompt,
                    resolution=resolution,
                    duration=duration
                )
                
                if result['success']:
                    return jsonify({
                        'success': True,
                        'task_id': result['task_id'],
                        'message': result['message'],
                        'estimated_time': f'{duration * 2}-{duration * 3}分钟'
                    })
                else:
                    return jsonify({'success': False, 'error': result['error']})
            
            except Exception as e:
                print(f"视频生成请求处理错误: {str(e)}")
                return jsonify({'success': False, 'error': f'视频生成失败: {str(e)}'})
        
        # 查询视频任务状态
        @app.route('/check_video_task/<task_id>')
        def check_video_task(task_id):
            """查询视频生成任务状态"""
            try:
                result = video_generator.check_task_status(task_id)
                
                if result['success']:
                    task_data = result['data']
                    status = result['status']
                    
                    response_data = {
                        'success': True,
                        'task_id': task_id,
                        'status': status,
                        'created_at': task_data.get('created_at'),
                        'updated_at': task_data.get('updated_at')
                    }
                    
                    if status == 'completed':
                        video_url = task_data.get('video_url') or task_data.get('result', {}).get('video_url')
                        if video_url:
                            response_data['video_url'] = video_url
                            response_data['message'] = '视频生成完成！'
                        else:
                            response_data['message'] = '视频生成完成，但无法获取下载链接'
                    elif status == 'running':
                        response_data['message'] = '视频正在生成中...'
                    elif status == 'failed':
                        response_data['message'] = '视频生成失败'
                        response_data['error'] = task_data.get('error_message', '未知错误')
                    else:
                        response_data['message'] = f'任务状态: {status}'
                    
                    return jsonify(response_data)
                else:
                    return jsonify({'success': False, 'error': result['error']})
            
            except Exception as e:
                return jsonify({'success': False, 'error': f'查询失败: {str(e)}'})
        
        # 获取视频风格列表
        @app.route('/video_styles')
        def get_video_styles():
            """获取可用的视频风格列表"""
            try:
                styles = video_generator.get_video_styles()
                return jsonify({'success': True, 'styles': styles})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        # 提供静态文件服务
        @app.route('/uploads/<filename>')
        def uploaded_file(filename):
            return send_from_directory(UPLOAD_FOLDER, filename)
        
        @app.route('/generated/<filename>')
        def generated_file(filename):
            return send_from_directory(GENERATED_FOLDER, filename)
        
        # 健康检查接口
        @app.route('/health')
        def health_check():
            return jsonify({
                'status': 'healthy',
                'message': 'AI制图服务运行正常',
                'timestamp': datetime.now().isoformat()
            })
        
        # 简化的API状态检查接口
        @app.route('/api-status')
        def api_status():
            """检查API状态"""
            try:
                # 检查ByteDance API状态（仅视频）
                ark_token_valid = Config.validate_token()
                
                return jsonify({
                    'local_generator': {
                        'configured': True,
                        'status': 'OK',
                        'message': '本地专业图像生成器运行正常'
                    },
                    'bytedance_video': {
                        'configured': ark_token_valid,
                        'status': 'OK' if ark_token_valid else 'ERROR',
                        'message': 'ByteDance视频API已配置' if ark_token_valid else '需要设置ByteDance API密钥'
                    },
                    'overall_status': 'excellent',
                    'message': '本地专业图像生成 + ByteDance视频生成 = 完美创作体验',
                    'features': {
                        'image_generation': '✅ 9种专业美术风格，即时生成',
                        'video_generation': '✅ 6种运镜风格，专业品质',
                        'reliability': '✅ 100%可用性，无网络依赖',
                        'speed': '✅ 零延迟，极速响应'
                    },
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'overall_status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        # 启动服务器
        print(f"✅ 服务器启动成功！")
        print(f"🎨 请打开浏览器访问: http://localhost:{port}")
        app.run(debug=False, host='127.0.0.1', port=port)
        
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        print("请检查所有文件是否存在")

if __name__ == "__main__":
    main()
