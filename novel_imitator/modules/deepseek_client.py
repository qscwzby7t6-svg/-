"""
DeepSeek V4 Pro 集成模块 - 负责与DeepSeek API交互
支持低成本替代方案，使用本地模板生成
"""
import os
import json
import time
import logging
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GenerationRequest:
    """生成请求"""
    prompt: str
    system_prompt: str
    max_tokens: int
    temperature: float
    context: Optional[Dict[str, Any]] = None

@dataclass
class GenerationResponse:
    """生成响应"""
    content: str
    usage: Dict[str, int]
    finish_reason: str
    cached: bool = False

class DeepSeekClient:
    """DeepSeek API 客户端"""
    
    def __init__(self, api_key: str = "", base_url: str = "https://api.deepseek.com/v4", 
                 model: str = "deepseek-v4-pro", config: Optional[Any] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = base_url
        self.model = model
        self.config = config
        
        self.request_timeout = 120
        self.max_retries = 3
        self.retry_delay = 2
        
        self.use_local_fallback = not self.api_key
        self.local_templates = self._init_local_templates()
        
        if self.use_local_fallback:
            logger.warning("未提供API密钥，将使用本地模板生成")
    
    def _init_local_templates(self) -> Dict[str, Any]:
        """初始化本地模板"""
        return {
            'chapter_intro': [
                "清晨的阳光透过云层，洒落在{location}上。",
                "夜色笼罩着{location}，显得格外寂静。",
                "这一日，{protagonist}来到了{location}。",
                "{time}，{protagonist}独自站在{location}。",
                "只见{location}中，{protagonist}缓步走来。"
            ],
            'dialogue_start': [
                '"{dialogue}"',
                '{speaker}道："{dialogue}"',
                '{speaker}不由得{action}："{dialogue}"',
                '{speaker}冷笑一声："{dialogue}"',
                '{speaker}沉吟片刻，道："{dialogue}"'
            ],
            'action_scene': [
                '{protagonist}{action}，{action_detail}。',
                '只见{protagonist}{action}，{reaction}。',
                '{protagonist}猛地{action}，{consequence}。'
            ],
            'emotion_concrete': {
                '紧张': [
                    '手足无措地站在那里，双手紧紧地拧着衣角',
                    '额头渗出细密的汗珠，眼神飘忽不定',
                    '声音微微发颤，嘴唇不自觉地抿紧'
                ],
                '愤怒': [
                    '脸色铁青，双拳紧握，指关节泛白',
                    '眼中闪过一丝狠厉，嘴角不停地抽搐',
                    '胸膛剧烈起伏，鼻息粗重如牛'
                ],
                '高兴': [
                    '眉开眼笑，嘴角都快咧到耳根',
                    '脸上洋溢着藏不住的喜悦',
                    '一蹦三尺高，兴奋得手舞足蹈'
                ],
                '悲伤': [
                    '眼眶泛红，泪水在眼眶里打转',
                    '身体微微颤抖，肩膀不停地耸动',
                    '声音哽咽，说不出话来'
                ],
                '惊讶': [
                    '瞪大了眼睛，嘴巴张成了O形',
                    '倒吸一口凉气，整个人僵在原地',
                    '脸色瞬间变得煞白'
                ]
            },
            'fight_sequence': [
                '{attacker}猛地出拳，带着呼啸的风声直取{defender}面门。',
                '{defender}侧身一闪，顺势一脚踢向{attacker}。',
                '两人你来我往，招招凶狠，式式致命。',
                '电光火石间，{attacker}已经攻出七八招。',
                '{defender}挡下{attacker}的攻击，冷笑一声。'
            ],
            'transition': [
                '就在此时，',
                '就在这时，',
                '忽然，',
                '突然，',
                '蓦然，'
            ],
            'cliffhanger': [
                '然而，事情并没有这么简单...',
                '但他不知道的是，一场更大的危机正在悄然逼近...',
                '谁也没有想到，意外就这样发生了...',
                '就在他准备离开的时候，',
                '而这一切，才刚刚开始...'
            ]
        }
    
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """生成文本"""
        if self.use_local_fallback:
            return await self._generate_local(request)
        
        return await self._generate_api(request)
    
    async def _generate_api(self, request: GenerationRequest) -> GenerationResponse:
        """通过API生成"""
        import aiohttp
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.prompt}
            ],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": False
        }
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=headers, 
                                           timeout=aiohttp.ClientTimeout(total=self.request_timeout)) as response:
                        if response.status == 200:
                            data = await response.json()
                            content = data['choices'][0]['message']['content']
                            usage = data.get('usage', {})
                            
                            return GenerationResponse(
                                content=content,
                                usage={
                                    'prompt_tokens': usage.get('prompt_tokens', 0),
                                    'completion_tokens': usage.get('completion_tokens', 0),
                                    'total_tokens': usage.get('total_tokens', 0)
                                },
                                finish_reason=data['choices'][0].get('finish_reason', 'stop')
                            )
                        elif response.status == 429:
                            logger.warning(f"API限流，等待重试...")
                            await self._wait_with_backoff(attempt)
                        else:
                            error_text = await response.text()
                            logger.error(f"API错误 {response.status}: {error_text}")
                            if attempt < self.max_retries - 1:
                                await self._wait_with_backoff(attempt)
                            else:
                                return await self._generate_local(request)
            except Exception as e:
                logger.error(f"API请求失败: {e}")
                if attempt < self.max_retries - 1:
                    await self._wait_with_backoff(attempt)
                else:
                    return await self._generate_local(request)
        
        return await self._generate_local(request)
    
    async def _wait_with_backoff(self, attempt: int):
        """退避等待"""
        delay = self.retry_delay * (2 ** attempt)
        await asyncio.sleep(delay) if 'asyncio' in dir() else time.sleep(delay)
    
    async def _generate_local(self, request: GenerationRequest) -> GenerationResponse:
        """本地模板生成"""
        logger.info("使用本地模板生成")
        
        templates = self.local_templates
        context = request.context or {}
        
        content_parts = []
        
        if 'context' in request.prompt.lower():
            location = context.get('location', '某处')
            protagonist = context.get('protagonist', '主角')
            content_parts.append(self._select_template(templates['chapter_intro']).format(
                location=location, protagonist=protagonist
            ))
        
        if 'dialogue' in request.prompt.lower():
            dialogue = context.get('dialogue', '对话内容')
            speaker = context.get('speaker', '某人')
            action = context.get('action', '说道')
            content_parts.append(self._select_template(templates['dialogue_start']).format(
                dialogue=dialogue, speaker=speaker, action=action
            ))
        
        if 'action' in request.prompt.lower():
            protagonist = context.get('protagonist', '主角')
            action = context.get('action', '行动')
            content_parts.append(self._select_template(templates['action_scene']).format(
                protagonist=protagonist, action=action,
                action_detail='动作细节', reaction='反应'
            ))
        
        if not content_parts:
            content_parts.append(self._generate_from_style(request.system_prompt))
        
        content = '\n\n'.join(content_parts)
        
        return GenerationResponse(
            content=content,
            usage={'prompt_tokens': 0, 'completion_tokens': len(content), 'total_tokens': len(content)},
            finish_reason='local_template',
            cached=True
        )
    
    def _select_template(self, templates: List[str]) -> str:
        """选择模板"""
        import random
        return random.choice(templates)
    
    def _generate_from_style(self, system_prompt: str) -> str:
        """根据风格生成"""
        templates = self.local_templates
        
        intro = self._select_template(templates['chapter_intro']).format(
            location='某处', protagonist='主角'
        )
        
        transition = self._select_template(templates['transition'])
        action = self._select_template(templates['action_scene']).format(
            protagonist='主角', action='行动', action_detail='动作', reaction='反应'
        )
        
        return f"{intro}\n\n{transition}{action}"
    
    def generate_chapter(self, outline: str, style_guide: str, 
                        target_length: int, context: Dict[str, Any]) -> str:
        """生成章节"""
        system_prompt = f"""你是一个专业的小说作家，需要仿写小说章节。

风格要求：
{style_guide}

重要规则：
1. 避免AI特征词（首先、其次、最后、综上所述等）
2. 使用具体动作和场景描写，少用抽象描述
3. 适当使用口语化表达
4. 保持章节字数在{target_length}字左右
5. 确保情节连贯，人物性格一致
"""
        
        prompt = f"""根据以下大纲生成章节内容：

{outline}

要求：
- 字数：约{target_length}字
- 保持原文风格
- 避免AI化表达
- 使用具体场景和动作描写
"""
        
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        request = GenerationRequest(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=4000,
            temperature=0.7,
            context=context
        )
        
        response = loop.run_until_complete(self.generate(request))
        return response.content
    
    def batch_generate(self, requests: List[GenerationRequest]) -> List[GenerationResponse]:
        """批量生成"""
        responses = []
        
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        async def generate_all():
            tasks = [self.generate(req) for req in requests]
            return await asyncio.gather(*tasks)
        
        return loop.run_until_complete(generate_all())
    
    def check_health(self) -> Tuple[bool, str]:
        """检查API健康状态"""
        if self.use_local_fallback:
            return True, "使用本地模板模式"
        
        try:
            import aiohttp
            url = f"{self.base_url}/models"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def check():
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                        return response.status == 200
            
            is_healthy = loop.run_until_complete(check())
            
            if is_healthy:
                return True, "API连接正常"
            else:
                return False, "API连接失败"
        except Exception as e:
            return False, f"健康检查失败: {str(e)}"


def test_deepseek_client():
    """测试DeepSeek客户端"""
    print("=" * 60)
    print("DeepSeek V4 Pro 集成模块测试")
    print("=" * 60)
    
    client = DeepSeekClient()
    
    print("\n测试1: 本地模板生成")
    try:
        request = GenerationRequest(
            prompt="生成一段描写主角来到新地点的场景",
            system_prompt="使用古典武侠风格",
            max_tokens=500,
            temperature=0.7,
            context={'location': '天元城', 'protagonist': '李云', 'time': '清晨'}
        )
        
        response = asyncio.run(client.generate(request)) if 'asyncio' in dir() else client.generate(request)
        print(f"✓ 生成成功")
        print(f"内容：\n{response.content}")
        print(f"字数：{len(response.content)}")
        print(f"是否本地：{response.cached}")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试2: 模板选择")
    try:
        templates = client.local_templates['emotion_concrete']['紧张']
        selected = client._select_template(templates)
        print(f"✓ 选择成功: {selected}")
    except Exception as e:
        print(f"✗ 选择失败: {e}")
    
    print("\n测试3: 健康检查")
    try:
        is_healthy, message = client.check_health()
        print(f"✓ 健康检查: {is_healthy} - {message}")
    except Exception as e:
        print(f"✗ 健康检查失败: {e}")
    
    print("\n" + "=" * 60)
    print("DeepSeek V4 Pro 集成模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    test_deepseek_client()
