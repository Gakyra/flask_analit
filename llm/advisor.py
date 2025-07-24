import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)

def generate_analysis(portfolio_data):
    stats = [f"{symbol}: кол-во {info['quantity']}, прибыль {info['profit']}" for symbol, info in portfolio_data.items()]
    prompt = f"""
    Ты — финансовый аналитик. Проанализируй крипто‑портфель: {', '.join(stats)}.
    Какие рекомендации ты можешь дать? Как оценить риск? Дай советы на русском языке, кратко и по делу.
    """

    try:
        response = client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Ошибка вызова модели: {e}"
