#services.py
#1. OpenAI의 ChatGPT API 호출하는 로직
import openai

# OpenAI API 키 설정
openai.api_key = "your-openai-api-key"

def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"
