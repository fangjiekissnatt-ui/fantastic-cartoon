# AI制图网站配置文件
# 这个文件用来管理API密钥和参数设置

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """
    配置管理类
    用来统一管理所有的设置和API密钥
    """
    
    # 字节跳动视觉API设置（用于视频生成）
    ARK_API_KEY = os.getenv('ARK_API_KEY', 'b122a8a1-da7b-4cbc-8304-0235a9e319a1')
    
    # OpenRouter API设置（支持多种AI模型的聚合平台）
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    
    # Segmind API设置（专门用于图片转真实照片）
    SEGMIND_API_KEY = os.getenv('SEGMIND_API_KEY', 'SG_d0d17371e4b1a360')
    SEGMIND_BASE_URL = "https://api.segmind.com/v1/flux-kontext-pro"
    
    # GPT Image 1 API设置（高质量图像生成）
    GPT_IMAGE1_API_KEY = os.getenv('GPT_IMAGE1_API_KEY', 'SG_d0d17371e4b1a360')
    GPT_IMAGE1_BASE_URL = "https://api.segmind.com/v1/gpt-image-1"
    
    # 豆包文档理解API设置（文档处理和文本分析）
    DOUBAO_DOCUMENT_API_KEY = os.getenv('DOUBAO_DOCUMENT_API_KEY', 'b122a8a1-da7b-4cbc-8304-0235a9e319a1')
    DOUBAO_DOCUMENT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    # OpenRouter支持的图像生成模型（使用正确的模型ID）
    OPENROUTER_IMAGE_MODELS = {
        'gemini_image': 'google/gemini-2.5-flash-image-preview',  # Gemini 2.5 Flash 图像生成
        'gpt4o': 'openai/gpt-4o-2024-08-06',  # GPT-4o - 支持图像生成
        'claude': 'anthropic/claude-3.5-sonnet',  # Claude 3.5 Sonnet
        'deepseek': 'deepseek/deepseek-chat-v3.1:free',  # DeepSeek V3.1 - 免费
    }
    DEFAULT_OPENROUTER_MODEL = 'gemini_image'  # 默认使用免费的Gemini图像生成模型
    
    # 图片生成参数
    IMAGE_WIDTH = 512        # 生成图片的宽度
    IMAGE_HEIGHT = 512       # 生成图片的高度  
    INFERENCE_STEPS = 20     # 推理步数（更多步数=更好质量，但更慢）
    GUIDANCE_SCALE = 7.5     # 引导强度（控制AI对提示词的遵循程度）
    
    # 视频生成参数
    VIDEO_MODEL = "ep-20250904152826-dxz7p"  # 字节跳动图生视频模型
    VIDEO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
    DEFAULT_VIDEO_RESOLUTION = "1080p"
    DEFAULT_VIDEO_DURATION = 5
    DEFAULT_CAMERA_FIXED = False
    DEFAULT_WATERMARK = True
    
    # 精简优化的美术风格配置 - 只保留7个核心风格
    # 每个风格都经过重新设计，确保更好的AI生成效果
    STYLE_CONFIGS = {
        'disney': {
            'name': '迪士尼卡通',
            'description': '经典迪士尼动画风格：大眼睛、柔和线条、温暖色彩',
            'prompt_suffix': ', Disney Pixar style, big expressive eyes, soft rounded features, warm lighting, magical atmosphere, cute and friendly character design, high quality animation art',
            'negative_prompt': 'realistic, dark, scary, angular, harsh lighting, anime style, manga',
            'ai_description': '具有大而富有表现力的眼睛，柔和圆润的特征，温暖的色彩和魔法般的氛围',
            'keywords': ['迪士尼', 'disney', 'pixar', '动画', '卡通', '可爱', '圆润', '大眼睛']
        },
        '3d_cartoon': {
            'name': '3D卡通',
            'description': '立体3D卡通风格：C4D渲染、立体质感、圆润造型',
            'prompt_suffix': ', 3D cartoon style, Cinema 4D render, volumetric lighting, cute 3D character, rounded shapes, plastic toy aesthetic, bright colors, glossy surface, high quality 3D art',
            'negative_prompt': 'flat, 2D, realistic, dark, angular, low quality, anime style',
            'ai_description': '3D渲染的卡通角色，具有立体质感、圆润造型和明亮色彩',
            'keywords': ['3d', '3D', '立体', '卡通', 'cartoon', 'c4d', '圆润', '可爱', '玩具']
        },
        'anime': {
            'name': '日系漫画',
            'description': '日本动漫风格：精致细腻、色彩鲜艳、情感丰富',
            'prompt_suffix': ', anime style, manga art, cel shading, vibrant colors, detailed character design, expressive emotions, Japanese animation style, high quality anime art',
            'negative_prompt': 'realistic, western cartoon, Disney style, dull colors, 3D style',
            'ai_description': '赛璐璐着色技术，鲜艳色彩，精致的角色设计，丰富的情感表达',
            'keywords': ['动漫', 'anime', '日漫', 'manga', '日式', '二次元', '可爱', '细腻', '色彩']
        },
        'flat': {
            'name': '扁平风格',
            'description': '现代扁平设计：简洁线条、几何形状、明亮色彩',
            'prompt_suffix': ', flat design style, clean lines, geometric shapes, bright colors, minimalist illustration, modern design, vector art style, simple and elegant',
            'negative_prompt': 'realistic, 3D, detailed, complex, dark, anime style, Disney style',
            'ai_description': '简洁的线条设计，几何图形，明亮的色彩，现代简约美学',
            'keywords': ['扁平', 'flat', '简洁', '几何', '现代', '简约', '线条', '明亮', '设计']
        },
        'watercolor': {
            'name': '水彩风格',
            'description': '水彩绘画风格：柔和渐变、透明质感、艺术气息',
            'prompt_suffix': ', watercolor painting style, soft gradients, transparent layers, artistic brush strokes, flowing colors, paper texture, beautiful watercolor art',
            'negative_prompt': 'digital, sharp edges, solid colors, geometric, anime style, Disney style, 3D',
            'ai_description': '柔和的色彩渐变，透明的颜料层次，流动的色彩效果',
            'keywords': ['水彩', 'watercolor', '水墨', '渐变', '透明', '艺术', '柔和', '流动', '画笔']
        },
        'cyberpunk': {
            'name': '赛博酷炫',
            'description': '未来科幻风格：霓虹色彩、科技感、酷炫氛围',
            'prompt_suffix': ', cyberpunk style, neon lights, futuristic design, sci-fi aesthetic, urban night scene, high tech atmosphere, glowing effects, cool cyberpunk art',
            'negative_prompt': 'natural, pastoral, vintage, low tech, Disney style, anime style, cute',
            'ai_description': '霓虹灯光效果，未来科技感，酷炫的城市夜景氛围',
            'keywords': ['赛博', 'cyber', '朋克', 'punk', '未来', '科幻', '霓虹', '科技', '夜景', '酷炫']
        },
        'photography': {
            'name': '逼真摄影',
            'description': '真实摄影风格：高清细节、专业光影、写实质感',
            'prompt_suffix': ', professional photography, high resolution, realistic lighting, detailed textures, DSLR quality, photorealistic, natural lighting, high quality photograph',
            'negative_prompt': 'cartoon, anime, painting, sketch, artificial, Disney style, flat design, watercolor',
            'ai_description': '专业相机级别的真实效果，精确的光影和细节',
            'keywords': ['摄影', 'photography', '专业', '真实', '高清', '细节', '光影', '相机', '写实', '逼真']
        }
    }
    
    # 文件上传设置
    UPLOAD_FOLDER = 'uploads'
    GENERATED_FOLDER = 'generated'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'pdf', 'txt', 'doc', 'docx'}
    
    # 文档处理设置
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
    SUPPORTED_DOCUMENT_TYPES = ['pdf', 'txt', 'doc', 'docx']
    
    @staticmethod
    def get_style_config(style_key):
        """获取指定风格的配置"""
        return Config.STYLE_CONFIGS.get(style_key)
    
    @staticmethod
    def get_all_styles():
        """获取所有可用的风格"""
        return Config.STYLE_CONFIGS
    
    @staticmethod
    def get_style_name(style_key):
        """获取风格的显示名称"""
        config = Config.get_style_config(style_key)
        return config['name'] if config else '未知风格'
    
    @staticmethod
    def get_model_name(model_key):
        """获取模型的显示名称"""
        model_names = {
            'auto': '智能选择',
            'segmind': 'Segmind (真实照片转换)',
            'gpt_image1': 'GPT Image 1 (高质量生成)',
            'gemini': 'Google Gemini (免费)',
            'openrouter': 'OpenRouter (多模型)',
            'fallback': '备用生成器'
        }
        return model_names.get(model_key, '未知模型')
