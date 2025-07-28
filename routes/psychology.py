from flask import Blueprint, jsonify, render_template, request
import random

psychology = Blueprint("psychology", __name__)

advice_by_category = {
    "мышление": [
        "Долгосрочное мышление побеждает краткосрочную суету.",
        "Настоящий анализ — это спокойный взгляд на факты.",
        "Холодный рассудок важнее горячих новостей.",
        "Оцени ошибки не по убыткам, а по урокам.",
    ],
    "дисциплина": [
        "Не торгуй на эмоциях — они стоят дорого.",
        "Финансовая дисциплина — залог спокойствия.",
        "Тренируй терпение, как мышцу.",
        "Не цепляйся за каждый тик — выгоранию привет.",
    ],
    "страх": [
        "Страх мешает росту — управляй рисками.",
        "Если страшно — подыши, но не продавай.",
        "Страх потерь не должен перекрывать возможности.",
        "Психологически устойчивый инвестор — якорь в шторм.",
    ],
    "мотивация": [
        "Трейдинг — марафон, не спринт.",
        "Развивай себя, а не только счёт.",
        "Выход за эмоции — шаг к зрелости.",
        "Фокус на улучшение — лучше фокуса на результат.",
    ],
}

def generate_svg_card(text):
    return f"""
    <svg width="500" height="120" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" rx="10" ry="10" fill="#f2f6fc" stroke="#c3d3e8" stroke-width="2"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
            font-family="Verdana" font-size="16" fill="#223344">{text}</text>
    </svg>
    """

@psychology.route("/api/advice")
def get_advice():
    category = request.args.get("category")
    advice_list = advice_by_category.get(category) if category else sum(advice_by_category.values(), [])
    advice = random.choice(advice_list)
    svg = generate_svg_card(advice)

    with open("advice_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{category or 'случайно'} → {advice}\n")

    return jsonify({"advice": advice, "svg": svg})

@psychology.route("/psychology")
def psychology_page():
    return render_template("psychology.html")
