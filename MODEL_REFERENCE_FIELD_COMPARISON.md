# 各模型参考图参数字段对比

## 📊 模型参考图参数详细对比

### 1. **Flux Kontext Pro Image** (通过OpenRouter)

#### **参考图参数字段**
```json
{
  "model": "black-forest-labs/flux-kontext-pro-image",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "基于参考图生成Flux风格图片"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,{base64_data}"
          }
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### **字段说明**
- **字段名称**: `messages[0].content[1].image_url.url`
- **数据格式**: Base64编码的图片数据
- **数据前缀**: `data:image/jpeg;base64,`
- **支持格式**: JPEG, PNG等
- **API端点**: `/chat/completions`
- **请求方式**: POST JSON

---

### 2. **GPT Image 1** (通过Segmind)

#### **参考图参数字段**
```json
{
  "prompt": "基于参考图生成图片",
  "size": "auto",
  "quality": "auto",
  "moderation": "auto",
  "background": "opaque",
  "output_compression": 100,
  "output_format": "png",
  "reference_images": ["base64_encoded_string"]
}
```

#### **字段说明**
- **字段名称**: `reference_images`
- **数据格式**: 字符串数组 `[base64_string]`
- **数据前缀**: 无前缀，直接Base64数据
- **支持格式**: 多种图片格式
- **API端点**: `/v1/gpt-image-1`
- **请求方式**: POST JSON

---

### 3. **Nano Banana** (通过OpenRouter)

#### **参考图参数字段**
```json
{
  "model": "nano-banana/flux-kontext-pro",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "基于参考图生成图片"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,{base64_data}"
          }
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### **字段说明**
- **字段名称**: `messages[0].content[1].image_url.url`
- **数据格式**: Base64编码的图片数据
- **数据前缀**: `data:image/jpeg;base64,`
- **支持格式**: JPEG, PNG等
- **API端点**: `/chat/completions`
- **请求方式**: POST JSON

---

### 4. **OpenRouter其他模型** (Gemini, GPT-4o, Claude等)

#### **参考图参数字段**
```json
{
  "model": "google/gemini-2.5-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "基于参考图生成图片"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,{base64_data}"
          }
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### **字段说明**
- **字段名称**: `messages[0].content[1].image_url.url`
- **数据格式**: Base64编码的图片数据
- **数据前缀**: `data:image/jpeg;base64,`
- **支持格式**: JPEG, PNG等
- **API端点**: `/chat/completions`
- **请求方式**: POST JSON

---

## 📋 对比总结表

| 模型 | 字段名称 | 数据格式 | 数据前缀 | API端点 | 请求方式 | 支持状态 |
|------|----------|----------|----------|---------|----------|----------|
| **Flux Kontext Pro** | `messages[0].content[1].image_url.url` | Base64字符串 | `data:image/jpeg;base64,` | `/chat/completions` | POST JSON | ✅ 支持 |
| **GPT Image 1** | `reference_images` | 字符串数组 | 无前缀 | `/v1/gpt-image-1` | POST JSON | ✅ 支持 |
| **Nano Banana** | `messages[0].content[1].image_url.url` | Base64字符串 | `data:image/jpeg;base64,` | `/chat/completions` | POST JSON | ✅ 支持 |
| **OpenRouter其他模型** | `messages[0].content[1].image_url.url` | Base64字符串 | `data:image/jpeg;base64,` | `/chat/completions` | POST JSON | ✅ 支持 |

---

## 🔍 详细分析

### **1. Flux Kontext Pro Image**
- **特点**: 专门设计用于参考图像输入的模型
- **优势**: 对参考图像的识别和处理能力强
- **适用场景**: 风格迁移、角色一致性保持
- **提示词要求**: 需要具体的动作动词+目标对象+效果描述

### **2. GPT Image 1**
- **特点**: 使用独特的`reference_images`字段
- **优势**: 字段名称直观，支持多张参考图
- **适用场景**: 通用图像生成和转换
- **注意事项**: 需要数组格式，即使只有一张图片

### **3. Nano Banana**
- **特点**: 基于Flux Kontext Pro的托管版本
- **优势**: 通过OpenRouter平台，使用简单
- **适用场景**: 与Flux Kontext Pro类似
- **注意事项**: 使用OpenRouter的标准格式

### **4. OpenRouter其他模型**
- **特点**: 统一的OpenRouter格式
- **优势**: 格式标准化，易于维护
- **适用场景**: 多模态对话和图像生成
- **注意事项**: 需要设置正确的modalities参数

---

## 🚀 使用建议

### **选择模型的原则**
1. **Flux Kontext Pro**: 最适合需要强参考图像关联的场景
2. **GPT Image 1**: 适合通用图像生成，支持多张参考图
3. **Nano Banana**: Flux Kontext Pro的简化版本
4. **OpenRouter其他模型**: 适合多模态对话场景

### **参考图像处理建议**
1. **图片格式**: 优先使用JPEG格式，兼容性最好
2. **图片大小**: 建议控制在2MB以内
3. **Base64编码**: 确保编码正确，包含正确的数据前缀
4. **提示词**: 明确描述要基于参考图做什么操作

### **错误排查**
1. **字段名称**: 检查字段名称是否正确
2. **数据格式**: 确认Base64编码格式
3. **数据前缀**: 检查是否包含正确的数据前缀
4. **API端点**: 确认使用正确的API端点
5. **请求方式**: 确认使用正确的HTTP方法和Content-Type

---

*最后更新: 2025-10-21 12:30*
