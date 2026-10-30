import os
from dotenv import load_dotenv
from anthropic import Anthropic
from duckduckgo_search import DDGS

load_dotenv()

client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def chat_with_character(character_name, character_prompt, conversation_history):
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in conversation_history
    ]

    system_prompt = f"""당신은 '{character_name}'라는 캐릭터입니다.

{character_prompt}

다음 캐릭터의 성격, 말투, 특성을 완벽하게 재현해서 대화해주세요.
친근하고 자연스럽게 응답하세요."""

    res = client.messages.create(
        model="claude-haiku",
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )
    return res.content[0].text


def search_character(character_name):
    prompt = f"""'{character_name}'라는 캐릭터에 대해 알고 있는 정보를 정리해주세요.
캐릭터의:
- 성격과 특징
- 주요 능력이나 스킬
- 대표적인 말투나 습관
- 배경 이야기

정확하고 자세하게 작성하세요."""

    res = client.messages.create(
        model="claude-haiku",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text


def search_character_image(character_name):
    try:
        results = DDGS().images(character_name, max_results=1)
        if results and len(results) > 0:
            image_url = results[0].get('image')
            if image_url:
                return image_url
    except Exception as e:
        print(f"이미지 검색 오류: {e}")
    return None
