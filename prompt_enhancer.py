#!/usr/bin/env python3
"""
智能提示词增强器
将用户的简短输入转换为详细的AI绘图提示词
"""

class PromptEnhancer:
    def __init__(self):
        # 简短关键词映射表
        self.keyword_mappings = {
            # 动物类
            '猫': 'cute cat, fluffy fur, big round eyes, adorable expression',
            '狗': 'cute dog, friendly face, wagging tail, loyal companion',
            '熊猫': 'adorable panda, black and white fur, round belly, cute expression',
            '兔子': 'cute rabbit, long ears, fluffy tail, innocent eyes',
            '鸟': 'colorful bird, beautiful feathers, flying pose, nature scene',
            
            # 人物类
            '机器人': 'robot, high tech,futuristic style, futuristic aesthetic, neon light, cute, screen head, no fingers, no legs, no headset, no earphones, round shape, friendly smile, chassis model',
            '女孩': 'beautiful girl, 10 years old, tailed girl, colorful skirt, cute smile',
            '女人': 'beautiful woman, 25 years old, long hair, elegant dress, gentle smile',
            '男人': 'handsome man,25 years old, confident pose, casual outfit, friendly expression',
            '男孩': 'handsome boy, 10 years old, confident pose, casual outfit, friendly expression',
            '宝宝': 'cute baby, chubby cheeks, innocent eyes, adorable expression',
            '老人': 'wise elderly person, kind face, gentle expression, experienced look',
            
            # 场景类
            '森林': 'enchanted forest, tall trees, dappled sunlight, magical atmosphere',
            '海洋': 'crystal clear ocean, blue waves, underwater scene, marine life',
            '城堡': 'majestic castle, medieval architecture, stone towers, royal atmosphere',
            '花园': 'beautiful garden, colorful flowers, green grass, peaceful atmosphere',
            '城市': 'modern city, skyscrapers, busy streets, urban landscape',
            
            # 情绪类
            '开心': 'happy expression, bright smile, cheerful mood, positive energy',
            '大笑': 'laughing loudly, wide open mouth, joyful expression, hearty laugh',
            '悲伤': 'sad expression, gentle tears, melancholic mood, emotional depth',
            '惊喜': 'surprised expression, open mouth, laugh, wide eyes, amazed look, unexpected moment',
            '惊讶': 'surprised expression, wide eyes, amazed look, unexpected moment',
            '愤怒': 'angry expression, intense emotion, powerful stance, dramatic mood',
            
            # 风格类
            '科技': 'futuristic style, high tech design, glowing elements, futuristic aesthetic, neon light' ,
            '可爱': 'kawaii style, super cute, adorable features, sweet expression',
            '酷炫': 'cool style, edgy design, modern aesthetic, stylish look',
            '梦幻': 'dreamy atmosphere, ethereal beauty, magical elements, fantasy world',
            '复古': 'vintage style, classic design, nostalgic feeling, retro aesthetic',
            
            # 材质类
            '毛绒': 'fluffy texture, soft fur, plush material, cozy feeling',
            '金属': 'metallic surface, shiny material, industrial look, modern design',
            '玻璃': 'transparent glass, crystal clear, reflective surface, elegant material',
            '木头': 'wooden texture, natural grain, warm color, rustic charm'
        }
        
        # 组合词规则
        self.combination_rules = {
            '颜色': {
                '红色': 'vibrant red color',
                '蓝色': 'beautiful blue color', 
                '绿色': 'natural green color',
                '黄色': 'bright yellow color',
                '粉色': 'soft pink color',
                '紫色': 'royal purple color'
            },
            '数量': {
                '一只': 'single',
                '两只': 'pair of',
                '一群': 'group of',
                '很多': 'many'
            },
            '动作': {
                '坐着': 'sitting pose',
                '双手打开': 'hands open, open arms, wide open hands, open hands pose',
                '站着': 'standing pose', 
                '跑着': 'running pose',
                '飞着': 'flying pose',
                '睡觉': 'sleeping pose'
            }
        }
        
        # 质量增强词
        self.quality_enhancers = [
            'high quality', 'detailed', 'beautiful', 'stunning', 'amazing',
            'perfect lighting', 'sharp focus', 'professional', 'artistic'
        ]

    def enhance_prompt(self, user_input, style=None):
        """
        增强用户输入的提示词
        
        Args:
            user_input (str): 用户输入的简短描述
            style (str): 选择的艺术风格
            
        Returns:
            str: 增强后的详细提示词
        """
        # 1. 基础文本处理
        enhanced = user_input.strip()
        
        # 2. 关键词替换
        enhanced = self._replace_keywords(enhanced)
        
        # 3. 组合词处理
        enhanced = self._apply_combination_rules(enhanced)
        
        # 4. 风格特定增强
        if style:
            enhanced = self._apply_style_enhancement(enhanced, style)
        
        # 5. 质量增强
        enhanced = self._add_quality_enhancers(enhanced)
        
        # 6. 智能补全
        enhanced = self._intelligent_completion(enhanced)
        
        # 7. 添加特征保持增强词
        enhanced = self._add_character_preservation_enhancers(enhanced)
        
        return enhanced

    def _replace_keywords(self, text):
        """替换关键词"""
        for keyword, replacement in self.keyword_mappings.items():
            if keyword in text:
                text = text.replace(keyword, replacement)
        return text

    def _apply_combination_rules(self, text):
        """应用组合词规则"""
        # 颜色组合
        for color_cn, color_en in self.combination_rules['颜色'].items():
            if color_cn in text:
                text = text.replace(color_cn, color_en)
        
        # 数量组合
        for num_cn, num_en in self.combination_rules['数量'].items():
            if num_en in text:
                text = text.replace(num_cn, num_en)
        
        # 动作组合
        for action_cn, action_en in self.combination_rules['动作'].items():
            if action_cn in text:
                text = text.replace(action_cn, action_en)
        
        return text

    def _apply_style_enhancement(self, text, style):
        """应用风格特定增强"""
        from config import Config
        style_config = Config.get_style_config(style)
        if style_config and 'prompt_suffix' in style_config:
            text += style_config['prompt_suffix']
        return text

    def _add_quality_enhancers(self, text):
        """添加质量增强词"""
        # 随机选择1-2个质量增强词
        import random
        selected_enhancers = random.sample(self.quality_enhancers, 2)
        text += ', ' + ', '.join(selected_enhancers)
        return text

    def _intelligent_completion(self, text):
        """智能补全缺失的描述"""
        # 如果没有明确的主体，添加通用描述
        if not any(keyword in text for keyword in ['cat', 'dog', 'person', 'character', 'object']):
            text = 'cute character, ' + text
        
        # 如果没有环境描述，添加通用环境
        if not any(keyword in text for keyword in ['background', 'scene', 'environment', 'setting']):
            text += ', clean background, studio lighting'
        
        return text

    def _add_character_preservation_enhancers(self, text):
        """添加特征保持增强词"""
        # 检查是否包含需要特征保持的关键词
        character_keywords = ['机器人', '机械', 'robot', 'machine', '设备', '产品', '物体', '建筑', '车辆']
        
        for keyword in character_keywords:
            if keyword in text.lower():
                # 添加特征保持增强词
                preservation_enhancers = [
                    'maintain original character features',
                    'cartoonize proportions', 
                    'make more rounded and adorable',
                    'preserve distinctive characteristics',
                    'enhance cuteness while keeping identity'
                ]
                text += ', ' + ', '.join(preservation_enhancers)
                break
        
        return text

    def get_prompt_suggestions(self, partial_input):
        """
        根据部分输入提供智能建议
        
        Args:
            partial_input (str): 用户的部分输入
            
        Returns:
            list: 建议的完整提示词列表
        """
        suggestions = []
        
        # 基于关键词匹配建议
        for keyword in self.keyword_mappings.keys():
            if keyword in partial_input:
                # 生成相关的建议
                base_prompt = self.enhance_prompt(partial_input)
                suggestions.append(base_prompt)
                
                # 添加变化版本
                variations = self._generate_variations(base_prompt)
                suggestions.extend(variations)
        
        return suggestions[:5]  # 返回前5个建议

    def _generate_variations(self, base_prompt):
        """生成提示词的变化版本"""
        variations = []
        
        # 添加不同的情绪
        emotions = ['happy', 'serious', 'mysterious', 'playful']
        for emotion in emotions:
            variation = base_prompt.replace('cute', f'{emotion} and cute')
            variations.append(variation)
        
        return variations

# 创建全局实例
prompt_enhancer = PromptEnhancer()
