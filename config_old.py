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
    
    # 基于AI大模型能力优化的美术风格配置
    # 每个风格都包含详细的特征描述和专业的AI绘图提示词
    STYLE_CONFIGS = {
        'disney': {
            'name': '迪士尼动画',
            'description': '经典迪士尼动画风格：大眼睛、柔和线条、温暖色彩',
            'prompt_suffix': ', Disney Pixar animation style, big expressive eyes, soft rounded features, warm lighting, magical atmosphere, cute and friendly, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'realistic, dark, scary, angular, harsh lighting, losing original features, too realistic',
            'ai_description': '具有大而富有表现力的眼睛，柔和圆润的特征，温暖的色彩和魔法般的氛围',
            'keywords': ['迪士尼', 'disney', '迪斯尼', 'pixar', '皮克斯', '动画', '卡通', '可爱', '圆润', '大眼睛']
        },
        '3d_cartoon': {
            'name': '3D卡通',
            'description': '立体3D卡通风格：C4D渲染、立体质感、圆润造型',
            'prompt_suffix': ', 3D cartoon style, C4D rendering, volumetric lighting, cute 3D character, rounded shapes, plastic toy aesthetic, bright colors, glossy surface, maintain original features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'flat, 2D, realistic, dark, angular, low quality, losing original features, too realistic',
            'ai_description': '3D渲染的卡通角色，具有立体质感、圆润造型和明亮色彩',
            'keywords': ['3d', '3D', '立体', '卡通', 'cartoon', 'c4d', '圆润', '可爱', '玩具', '立体感']
        },
        'reference_3d': {
            'name': '高保真3D卡通',
            'description': '写实转卡通：圆润化机械体、温暖质感、可爱比例重构',
            'prompt_suffix': ', transform realistic robot/machine into cute cartoon version, Cinema 4D style, C4D render, 3D illustration, make proportions rounder and chunkier, enlarge head proportionally, soften all edges and corners, convert metallic surfaces to soft matte plastic toy material, warm friendly lighting, pastel color palette, kawaii aesthetic, adorable character design, smooth volumetric lighting, clean studio background, octane render, high detail, ultra detailed, toy-like finish, approachable and friendly appearance, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'realistic metallic surfaces, sharp edges, technical details, screws, mechanical joints, cold industrial look, dark lighting, harsh shadows, realistic proportions, thin parts, angular design, professional product photography, complex technical features, losing original features, too realistic',
            'ai_description': '将写实机械体转换为圆润可爱的卡通玩具质感，温暖友好的C4D渲染风格',
            'keywords': ['高保真', '3d', '卡通', '圆润', '可爱', '机械', '机器人', '玩具', 'c4d', '立体', '比例', '重构']
        },
        'anime': {
            'name': '日式动漫',
            'description': '日本动漫风格：精致细腻、色彩鲜艳、情感丰富',
            'prompt_suffix': ', anime style, manga, cel shading, vibrant colors, detailed hair, expressive emotions, Japanese animation, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'realistic, western cartoon, dull colors, losing original features, too realistic',
            'ai_description': '赛璐璐着色技术，鲜艳色彩，精致的头发细节，丰富的情感表达',
            'keywords': ['动漫', 'anime', '日漫', 'manga', '日式', '二次元', '可爱', '圆润', '细腻', '色彩']
        },
        'watercolor': {
            'name': '水彩画风',
            'description': '水彩绘画风格：柔和渐变、透明质感、艺术气息',
            'prompt_suffix': ', watercolor painting, soft gradients, transparent layers, artistic brush strokes, flowing colors, paper texture, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'digital, sharp edges, solid colors, geometric, losing original features, too realistic',
            'ai_description': '柔和的色彩渐变，透明的颜料层次，流动的色彩效果',
            'keywords': ['水彩', 'watercolor', '水墨', '渐变', '透明', '艺术', '柔和', '流动', '画笔', '质感']
        },
        'oilpainting': {
            'name': '油画风格',
            'description': '经典油画：厚重质感、丰富层次、古典美感',
            'prompt_suffix': ', oil painting, thick brush strokes, rich textures, classical art, warm tones, museum quality, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'digital, flat, modern, cartoon, losing original features, too realistic',
            'ai_description': '厚重的笔触，丰富的纹理层次，经典的艺术风格',
            'keywords': ['油画', 'oil', 'painting', '古典', '厚重', '质感', '笔触', '艺术', '层次', '温暖']
        },
        'pixel': {
            'name': '像素艺术',
            'description': '8位像素风格：复古游戏、方块像素、怀旧色彩',
            'prompt_suffix': ', pixel art, 8-bit, retro game style, blocky pixels, limited color palette, nostalgic, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'smooth, high resolution, realistic, modern, losing original features, too realistic',
            'ai_description': '8位游戏风格，方块状像素，有限的调色板，复古怀旧感',
            'keywords': ['像素', 'pixel', '8bit', '8-bit', '复古', '游戏', '方块', '怀旧', '像素化', '经典']
        },
        'minimalist': {
            'name': '极简主义',
            'description': '简约设计：干净线条、留白空间、几何形状',
            'prompt_suffix': ', minimalist design, clean lines, negative space, geometric shapes, simple composition, modern, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'cluttered, complex, detailed, ornate, losing original features, too realistic',
            'ai_description': '简洁的线条，大量留白，几何图形，现代简约美学',
            'keywords': ['极简', 'minimal', '简约', '简洁', '线条', '留白', '几何', '现代', '干净', '简单']
        },
        'cyberpunk': {
            'name': '赛博朋克',
            'description': '未来科幻：霓虹色彩、科技感、城市夜景',
            'prompt_suffix': ', cyberpunk style, neon lights, futuristic, sci-fi, urban night scene, high tech, glowing effects, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'natural, pastoral, vintage, low tech, losing original features, too realistic',
            'ai_description': '霓虹灯光效果，未来科技感，城市夜景氛围',
            'keywords': ['赛博', 'cyber', '朋克', 'punk', '未来', '科幻', '霓虹', '科技', '夜景', '发光']
        },
        'traditional_chinese': {
            'name': '中国山水画',
            'description': '传统国画：水墨晕染、意境深远、诗意美感',
            'prompt_suffix': ', Chinese traditional painting, ink wash, misty mountains, flowing water, poetic atmosphere, ancient style, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'western style, bright colors, modern, geometric, losing original features, too realistic',
            'ai_description': '水墨晕染效果，山水意境，诗意的传统美学',
            'keywords': ['中国', '山水', '水墨', '国画', '传统', '意境', '诗意', '晕染', '古典', '东方']
        },
        'photography': {
            'name': '专业摄影',
            'description': '真实摄影：高清细节、专业光影、写实质感',
            'prompt_suffix': ', professional photography, high resolution, realistic lighting, detailed textures, DSLR quality, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'cartoon, anime, painting, sketch, artificial, losing original features, too realistic',
            'ai_description': '专业相机级别的真实效果，精确的光影和细节',
            'keywords': ['摄影', 'photography', '专业', '真实', '高清', '细节', '光影', '相机', '写实', '质感']
        },
        'realistic_transform': {
            'name': '真实照片转换',
            'description': '使用Segmind技术将任何图片转换为真实照片风格',
            'prompt_suffix': ', make this a real photograph, photorealistic, high quality, natural lighting, maintain original character features, cartoonize proportions, make more rounded and adorable, preserve distinctive characteristics, enhance cuteness while keeping identity',
            'negative_prompt': 'cartoon, anime, artistic, painted, artificial, losing original features, too realistic',
            'ai_description': '专门将卡通、绘画等转换为逼真的照片效果',
            'keywords': ['真实', '照片', 'photorealistic', '转换', '写实', '自然', '逼真', '摄影', 'segmind', '高质量']
        }
    }
    
    # 文件上传设置
    UPLOAD_FOLDER = 'uploads'
    GENERATED_FOLDER = 'generated'
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    @classmethod
    def get_style_config(cls, style):
        """
        获取指定风格的配置
        如果风格不存在，返回默认配置
        """
        return cls.STYLE_CONFIGS.get(style, cls.STYLE_CONFIGS['disney'])
    
    @classmethod
    def validate_token(cls):
        """
        检查ARK API密钥是否已设置
        """
        return bool(cls.ARK_API_KEY)
