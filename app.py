# AI制图网站的Python后端程序
# 这个程序负责接收用户的请求，处理图片生成任务

# 导入需要的Python库
from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import uuid

# 导入我们自己的AI图像生成模块
from ai_image_generator import AIImageGenerator
from gemini_image_generator import gemini_generator
from ai_video_generator import video_generator
from segmind_image_generator import segmind_generator
from config import Config

# 创建Flask应用 - Flask是一个简单易用的Python网站框架
app = Flask(__name__)

# 使用配置文件中的设置
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
GENERATED_FOLDER = Config.GENERATED_FOLDER
ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS

# 如果文件夹不存在，就创建它们
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)

# 创建AI图像生成器实例
ai_generator = AIImageGenerator()

def allowed_file(filename):
    """
    检查文件名是否符合要求
    这个函数检查用户上传的文件是否是允许的图片格式
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 网站首页路由 - 当用户访问网站时显示HTML页面
@app.route('/')
def index():
    """
    显示主页 - Canvas版本界面
    当用户在浏览器中打开网站时，这个函数会运行
    """
    return send_from_directory('.', 'index_canvas.html')

# 处理图片生成请求的路由
@app.route('/generate', methods=['POST'])
def generate_image():
    """
    处理AI图片生成请求
    这个函数接收用户的描述文字、风格选择和参考图片，然后生成新图片
    """
    try:
        # 获取用户输入的描述文字
        prompt = request.form.get('prompt', '').strip()
        # 获取用户选择的风格
        style = request.form.get('style', '')
        # 获取用户选择的AI模型
        selected_model = request.form.get('model', 'auto')
        
        # 检查必填信息是否完整
        if not prompt:
            return jsonify({
                'success': False,
                'error': '请输入图片描述'
            })
        
        if not style:
            return jsonify({
                'success': False,
                'error': '请选择绘画风格'
            })
        
        # 处理用户上传的参考图片（如果有的话）
        reference_image_path = None
        if 'reference_image' in request.files:
            file = request.files['reference_image']
            # 检查文件是否有效
            if file and file.filename and allowed_file(file.filename):
                # 生成唯一的文件名，避免文件名冲突
                filename = f"{uuid.uuid4().hex}_{file.filename}"
                reference_image_path = os.path.join(UPLOAD_FOLDER, filename)
                # 保存上传的图片
                file.save(reference_image_path)
                print(f"参考图片已保存到: {reference_image_path}")
        
        # 创建任务记录 - 记录用户的生成请求
        task_data = {
            'id': str(uuid.uuid4()),  # 生成唯一的任务ID
            'prompt': prompt,  # 用户的描述文字
            'style': style,  # 选择的风格
            'reference_image': reference_image_path,  # 参考图片路径
            'timestamp': datetime.now().isoformat(),  # 创建时间
            'status': 'processing'  # 任务状态
        }
        
        # 打印任务信息到控制台，方便查看
        print(f"收到新的图片生成任务:")
        print(f"  描述: {prompt}")
        print(f"  风格: {get_style_name(style)}")
        print(f"  模型: {get_model_name(selected_model)}")
        print(f"  参考图: {'有' if reference_image_path else '无'}")
        
        # 根据用户选择的模型进行图片生成
        generated_image_path = generate_with_selected_model(
            prompt=prompt,
            style=style,
            selected_model=selected_model,
            reference_image_path=reference_image_path
        )
        
        if not generated_image_path:
            return jsonify({
                'success': False,
                'error': '图片生成失败，请检查API设置或稍后重试'
            })
        
        # 生成访问URL
        filename = os.path.basename(generated_image_path)
        generated_image_url = f'/generated/{filename}'
        
        # 返回成功结果给前端
        return jsonify({
            'success': True,
            'task_id': task_data['id'],
            'image_url': generated_image_url,
            'message': '图片生成成功！'
        })
        
    except Exception as e:
        # 如果出现错误，返回错误信息
        print(f"图片生成过程中出现错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'生成过程中出现错误: {str(e)}'
        })

@app.route('/generate_video', methods=['POST'])
def generate_video():
    """
    处理图生视频请求
    将用户生成的图片转换为动态视频
    """
    try:
        # 获取请求参数
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '请求数据无效'
            })
        
        image_url = data.get('image_url')
        prompt = data.get('prompt', '生成动态视频')
        video_style = data.get('video_style', 'cinematic')
        resolution = data.get('resolution', Config.DEFAULT_VIDEO_RESOLUTION)
        duration = data.get('duration', Config.DEFAULT_VIDEO_DURATION)
        
        if not image_url:
            return jsonify({
                'success': False,
                'error': '请提供图片URL'
            })
        
        print(f"收到视频生成请求:")
        print(f"  图片: {image_url}")
        print(f"  描述: {prompt}")
        print(f"  风格: {video_style}")
        print(f"  参数: {resolution}, {duration}秒")
        
        # 构建完整的图片URL（如果是相对路径）
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
                'estimated_time': f'{duration * 2}-{duration * 3}分钟'  # 估算时间
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            })
    
    except Exception as e:
        print(f"视频生成请求处理错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'视频生成失败: {str(e)}'
        })

@app.route('/check_video_task/<task_id>')
def check_video_task(task_id):
    """
    查询视频生成任务状态
    """
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
            
            # 如果任务完成，尝试获取视频URL
            if status == 'completed':
                # 这里需要根据实际API响应格式调整
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
            return jsonify({
                'success': False,
                'error': result['error']
            })
    
    except Exception as e:
        print(f"查询视频任务状态错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'查询失败: {str(e)}'
        })

@app.route('/video_styles')
def get_video_styles():
    """
    获取可用的视频风格列表
    """
    try:
        styles = video_generator.get_video_styles()
        return jsonify({
            'success': True,
            'styles': styles
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def get_style_name(style_code):
    """
    将风格代码转换为中文名称
    基于AI大模型优化后的美术风格体系
    """
    style_names = {
        'disney': '迪士尼动画',
        'anime': '日式动漫',
        'watercolor': '水彩画风',
        'oilpainting': '油画风格',
        'pixel': '像素艺术',
        'minimalist': '极简主义',
        'cyberpunk': '赛博朋克',
        'traditional_chinese': '中国山水画',
        'photography': '专业摄影',
        'realistic_transform': '真实照片转换'
    }
    return style_names.get(style_code, '未知风格')

def get_model_name(model_code):
    """
    将模型代码转换为中文名称
    """
    model_names = {
        'auto': '智能选择',
        'segmind': 'Segmind (真实照片转换)',
        'gemini': 'Google Gemini (多功能)',
        'openrouter': 'OpenRouter (高质量)',
        'fallback': '备用生成器'
    }
    return model_names.get(model_code, '未知模型')

def generate_with_selected_model(prompt, style, selected_model, reference_image_path=None):
    """
    根据用户选择的模型生成图片
    """
    generated_image_path = None
    
    # 智能选择模式 - 根据风格和条件自动选择最佳模型
    if selected_model == 'auto':
        print("🧠 使用智能选择模式...")
        
        # 如果选择了真实照片转换风格，并且有参考图片，优先使用Segmind
        if style == 'realistic_transform' and reference_image_path:
            print("🎯 智能选择：使用Segmind进行真实照片转换...")
            generated_image_path = segmind_generator.generate_image(
                prompt=prompt,
                style=style, 
                reference_image_path=reference_image_path
            )
        
        # 如果Segmind失败或不适用，使用Google Gemini
        if not generated_image_path:
            print("🤖 智能选择：使用Google Gemini AI图片生成...")
            generated_image_path = gemini_generator.generate_image(
                prompt=prompt,
                style=style, 
                reference_image_path=reference_image_path
            )
        
        # 如果Gemini也失败，回退到原有生成器
        if not generated_image_path:
            print("⚠️ 智能选择：Gemini生成失败，使用备用生成器...")
            generated_image_path = ai_generator.generate_image(
                prompt=prompt,
                style=style, 
                reference_image_path=reference_image_path
            )
    
    # 用户指定使用Segmind模型
    elif selected_model == 'segmind':
        print("🎯 用户指定：使用Segmind模型...")
        if not reference_image_path:
            print("⚠️ Segmind需要参考图片，自动回退到其他模型...")
            generated_image_path = gemini_generator.generate_image(
                prompt=prompt,
                style=style, 
                reference_image_path=reference_image_path
            )
        else:
            generated_image_path = segmind_generator.generate_image(
                prompt=prompt,
                style=style, 
                reference_image_path=reference_image_path
            )
    
    # 用户指定使用Gemini模型
    elif selected_model == 'gemini':
        print("🤖 用户指定：使用Google Gemini模型...")
        generated_image_path = gemini_generator.generate_image(
            prompt=prompt,
            style=style, 
            reference_image_path=reference_image_path
        )
    
    # 用户指定使用OpenRouter模型
    elif selected_model == 'openrouter':
        print("🚀 用户指定：使用OpenRouter模型...")
        generated_image_path = ai_generator.generate_image(
            prompt=prompt,
            style=style, 
            reference_image_path=reference_image_path
        )
    
    # 用户指定使用备用生成器
    elif selected_model == 'fallback':
        print("🎨 用户指定：使用备用生成器...")
        from fallback_generator import FallbackImageGenerator
        fallback = FallbackImageGenerator()
        generated_image_path = fallback.generate_image(
            prompt=prompt,
            style=style, 
            reference_image_path=reference_image_path
        )
    
    return generated_image_path

def simulate_image_generation(task_data):
    """
    模拟AI图片生成过程
    在真实项目中，这里会调用实际的AI图片生成API，比如：
    - OpenAI的DALL-E
    - Stability AI的Stable Diffusion
    - Midjourney API
    等等
    
    现在我们先返回一个模拟的结果
    """
    
    # 根据不同风格返回不同的模拟图片URL
    # 在实际项目中，这些会是真正生成的图片
    style_sample_images = {
        'realistic': 'https://via.placeholder.com/512x512/4CAF50/white?text=真实摄影风格',
        'disney': 'https://via.placeholder.com/512x512/FF9800/white?text=迪士尼风格',
        'flat': 'https://via.placeholder.com/512x512/2196F3/white?text=扁平风格',
        'c4d': 'https://via.placeholder.com/512x512/9C27B0/white?text=C4D渲染',
        'hyperrealistic': 'https://via.placeholder.com/512x512/F44336/white?text=超写实CG'
    }
    
    # 模拟处理时间
    import time
    time.sleep(1)  # 等待1秒，模拟AI生成时间
    
    # 返回对应风格的示例图片
    return style_sample_images.get(task_data['style'], 'https://via.placeholder.com/512x512/666/white?text=生成完成')

# 提供静态文件服务 - 让浏览器能够访问CSS、JS、图片等文件
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    提供上传文件的访问服务
    用户上传的参考图片可以通过这个路径访问
    """
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/generated/<filename>')
def generated_file(filename):
    """
    提供生成图片的访问服务
    AI生成的图片可以通过这个路径访问
    """
    return send_from_directory(GENERATED_FOLDER, filename)

# 健康检查接口 - 检查服务器是否正常运行
@app.route('/health')
def health_check():
    """
    健康检查接口
    可以用来测试服务器是否正常工作
    """
    return jsonify({
        'status': 'healthy',
        'message': 'AI制图服务运行正常',
        'timestamp': datetime.now().isoformat()
    })

# API状态检查接口
@app.route('/api-status')
def api_status():
    """
    检查AI API是否配置正确
    包括Gemini图像生成和ByteDance视频生成
    """
    try:
        # 检查Gemini API状态
        gemini_status = gemini_generator.test_connection()
        
        # 检查ByteDance API状态
        ark_token_valid = Config.validate_token()
        
        # 检查Segmind API状态
        segmind_status = segmind_generator.test_connection()
        
        # 检查Gemini API密钥
        gemini_key_set = bool(getattr(Config, 'GEMINI_API_KEY', ''))
        
        # 检查Segmind API密钥
        segmind_key_set = bool(getattr(Config, 'SEGMIND_API_KEY', ''))
        
        return jsonify({
            'gemini': {
                'configured': gemini_status['success'],
                'api_key_set': gemini_key_set,
                'status': 'OK' if gemini_status['success'] else 'ERROR',
                'message': gemini_status.get('message', gemini_status.get('error', ''))
            },
            'segmind': {
                'configured': segmind_status['success'],
                'api_key_set': segmind_key_set,
                'status': 'OK' if segmind_status['success'] else 'ERROR',
                'message': segmind_status.get('message', segmind_status.get('error', ''))
            },
            'bytedance': {
                'configured': ark_token_valid,
                'api_key_set': ark_token_valid,
                'status': 'OK' if ark_token_valid else 'ERROR',
                'message': 'ByteDance ARK API已配置' if ark_token_valid else '需要设置ByteDance API密钥'
            },
            'overall_status': 'ready' if (gemini_status['success'] or segmind_status['success'] or ark_token_valid) else 'fallback',
            'message': '所有功能正常运行，智能回退机制确保服务可用',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'overall_status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    """
    程序入口
    当直接运行这个Python文件时，会启动网站服务器
    """
    print("="*50)
    print("🎨 AI智能制图工作室 启动中...")
    print("="*50)
    print("📱 打开浏览器访问: http://localhost:4000")
    print("🛠️  按 Ctrl+C 停止服务器")
    print("="*50)
    
    # 启动Flask开发服务器
    # debug=True 表示开启调试模式，代码修改后会自动重启
    # host='0.0.0.0' 表示允许所有IP地址访问
    # port=4000 表示使用4000端口（避免VS Code Live Preview冲突）
    app.run(debug=True, host='0.0.0.0', port=4000)
