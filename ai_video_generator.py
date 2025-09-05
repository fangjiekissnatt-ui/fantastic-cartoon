#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI视频生成器
专门处理图片转视频功能
使用字节跳动ARK图生视频API
"""

import requests
import json
import time
import os
from config import Config

class AIVideoGenerator:
    """AI视频生成器"""
    
    def __init__(self):
        """初始化视频生成器"""
        self.config = Config
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
        print("🎬 豆包ARK AI视频生成器初始化完成")
    
    def create_video_task(self, image_url, prompt, **kwargs):
        """
        创建图生视频任务
        
        Args:
            image_url (str): 参考图片的URL
            prompt (str): 视频描述提示词
            **kwargs: 额外参数
                - resolution: 分辨率 (默认1080p)
                - duration: 时长秒数 (默认5)
                - camera_fixed: 镜头是否固定 (默认False)
                - watermark: 是否添加水印 (默认True)
        
        Returns:
            dict: 包含任务ID或错误信息
        """
        
        # 获取视频参数
        resolution = kwargs.get('resolution', '1080p')
        duration = kwargs.get('duration', 5)
        camera_fixed = kwargs.get('camera_fixed', False)
        watermark = kwargs.get('watermark', True)
        
        # 构建完整的提示词
        full_prompt = f"{prompt} --resolution {resolution} --duration {duration} --camerafixed {str(camera_fixed).lower()} --watermark {str(watermark).lower()}"
        
        print(f"🎬 开始创建视频生成任务...")
        print(f"   图片: {image_url}")
        print(f"   描述: {prompt}")
        print(f"   参数: {resolution}, {duration}s, 镜头{'固定' if camera_fixed else '动态'}, {'有' if watermark else '无'}水印")
        
        # 构建请求数据
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.ARK_API_KEY}"
        }
        
        data = {
            "model": "ep-20250904152826-dxz7p",  # 图生视频模型
            "content": [
                {
                    "type": "text",
                    "text": full_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        }
        
        try:
            print(f"📡 发送视频生成请求...")
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                print(f"✅ 视频任务创建成功: {task_id}")
                
                return {
                    'success': True,
                    'task_id': task_id,
                    'message': '视频生成任务已创建，正在处理中...'
                }
            else:
                error_msg = f"API错误: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', error_msg)
                except:
                    pass
                
                print(f"❌ 视频任务创建失败: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
        
        except Exception as e:
            error_msg = f"请求失败: {str(e)}"
            print(f"❌ 视频任务创建出错: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def check_task_status(self, task_id):
        """
        查询视频生成任务状态
        
        Args:
            task_id (str): 任务ID
        
        Returns:
            dict: 任务状态信息
        """
        
        url = f"{self.base_url}/{task_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.ARK_API_KEY}"
        }
        
        try:
            print(f"🔍 查询任务状态: {task_id}")
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', 'unknown')
                
                print(f"📊 任务状态: {status}")
                
                return {
                    'success': True,
                    'status': status,
                    'data': result
                }
            else:
                error_msg = f"查询失败: {response.status_code}"
                print(f"❌ {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
        
        except Exception as e:
            error_msg = f"查询出错: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def wait_for_completion(self, task_id, max_wait_time=300, check_interval=10):
        """
        等待视频生成完成
        
        Args:
            task_id (str): 任务ID
            max_wait_time (int): 最大等待时间(秒)
            check_interval (int): 查询间隔(秒)
        
        Returns:
            dict: 最终结果
        """
        
        print(f"⏳ 等待视频生成完成...")
        print(f"   最大等待时间: {max_wait_time}秒")
        print(f"   查询间隔: {check_interval}秒")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            result = self.check_task_status(task_id)
            
            if not result['success']:
                return result
            
            status = result['status']
            
            if status == 'completed':
                print(f"🎉 视频生成完成！")
                return result
            elif status == 'failed':
                print(f"❌ 视频生成失败")
                return {
                    'success': False,
                    'error': '视频生成失败',
                    'data': result['data']
                }
            elif status in ['running', 'processing', 'pending']:
                elapsed = int(time.time() - start_time)
                print(f"⏳ 生成中... (已等待 {elapsed}秒)")
                time.sleep(check_interval)
            else:
                print(f"🤔 未知状态: {status}")
                time.sleep(check_interval)
        
        # 超时
        print(f"⏰ 等待超时，但任务可能仍在继续")
        return {
            'success': False,
            'error': '等待超时，请稍后手动查询任务状态',
            'task_id': task_id
        }
    
    def get_video_styles(self):
        """
        获取可用的视频风格列表
        
        Returns:
            dict: 视频风格配置
        """
        
        return {
            'cinematic': {
                'name': '电影级运镜',
                'description': '专业电影级镜头运动，平滑推拉摇移',
                'prompt_suffix': ', cinematic camera movement, smooth tracking shot, professional cinematography'
            },
            'drone': {
                'name': '无人机飞行',
                'description': '无人机视角的飞行镜头，鸟瞰或穿越',
                'prompt_suffix': ', drone flight perspective, aerial view, smooth flying movement through scene'
            },
            'rotate': {
                'name': '360度旋转',
                'description': '围绕主体的圆周运动，展示全貌',
                'prompt_suffix': ', 360 degree rotation around subject, orbital camera movement'
            },
            'zoom': {
                'name': '缩放聚焦',
                'description': '镜头推进或拉远，突出细节或展现全景',
                'prompt_suffix': ', smooth zoom in/out, dynamic focus change'
            },
            'parallax': {
                'name': '视差滚动',
                'description': '前后景分层运动，营造深度感',
                'prompt_suffix': ', parallax scrolling effect, layered depth movement'
            },
            'static': {
                'name': '静态镜头',
                'description': '固定镜头，只有元素内部动画',
                'prompt_suffix': ', static camera, subtle element animation only --camerafixed true'
            }
        }

# 全局视频生成器实例
video_generator = AIVideoGenerator()

