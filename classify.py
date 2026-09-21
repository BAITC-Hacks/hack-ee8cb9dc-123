"""Классификатор обращений: категория + черновик ответа. Без зависимостей."""
import re
import sys

COMPLAINT = ("очеред", "холодн", "грязн", "пропал", "не работает", "сломал",
             "хамств", "жалоб", "отвратит", "плох", "шум", "долго жду")
REQUEST = ("как ", "где ", "когда ", "какой", "какие", "куда ", "можно ли",
           "справк", "документ", "график", "расписан")

REPLIES = {
    "жалоба": "Здравствуйте! Спасибо за обращение, приносим извинения за неудобства. "
              "Передали вопрос в ответственную службу, вернёмся с ответом в течение 1 рабочего дня.",
    "справка": "Здравствуйте! Спасибо за вопрос. Подготовим для вас информацию и ответим "
               "в течение 1 рабочего дня. Уточнить детали можно в деканате или по e-mail поддержки.",
    "другое": "Здравствуйте! Обращение получено и передано профильному сотруднику. "
              "Свяжемся с вами для уточнения деталей.",
}


def classify(text: str) -> str:
    t = text.lower().replace("‑", "-")
    if any(k in t for k in COMPLAINT):
        return "жалоба"
    if any(k in t for k in REQUEST):
        return "справка"
    return "другое"


def draft(text: str) -> str:
    return REPLIES[classify(text)]


def load(path: str):
    with open(path, encoding="utf-8") as f:
        return [re.sub(r"^\d+\)\s*", "", ln).strip() for ln in f if ln.strip()]


def demo():
    assert classify("В столовой очередь, еда холодная.") == "жалоба"
    assert classify("Как получить справку о месте учёбы?") == "справка"
    assert classify("Хочу записаться на консультацию завтра.") == "другое"
    assert classify("Пропал Wi-Fi в корпусе B.") == "жалоба"
    print("self-check ok")


if __name__ == "__main__":
    if "--test" in sys.argv:
        demo()
    else:
        path = sys.argv[1] if len(sys.argv) > 1 else "messages.txt"
        for i, msg in enumerate(load(path), 1):
            print(f"{i}. {msg}\n   Категория: {classify(msg)}\n   Ответ: {draft(msg)}\n")
