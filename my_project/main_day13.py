import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions
from prompts import SYSTEM_PROMPT

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")
print("Помощник по выбору фильмов и сериалов")
genre = input("Введите предпочитаемый жанр фильма (обязательно):").strip()
mood = input("Введите желаемое настроение, например: расслабиться, посмеяться (обязательно):").strip()
duration = input("Введите желаемую длительность (необязательно, нажмите Enter, если не важно):").strip()

print("\nВыберите формат ответа:")
print("1 Краткий ответ")
print("2 Подробный ответ")
format_choice = input("Введите цифру 1 или 2:").strip()
if not genre or not mood:
    print("\nОшибка: «жанр» и «настроение» обязательны для заполнения")
else:
    if not duration:
        duration = "не указано"
    if format_choice == "1":
        format_description = "формат: дай краткий ответ."
    elif format_choice == "2":
        format_description = "формат: дай подробный ответ."
    else:
        format_description = "Формат стандартный"

    user_prompt = f"""
    Помоги подобрать фильм по следующим параметрам:
    жанр: {genre}
    настроение: {mood}
    длительность: {duration}
    {format_description}
    """

    print("\nСформированный запрос к модели:")
    print(user_prompt)

    request = ChatCompletionRequest(
        model="GigaChat-2",
        messages=[
            ChatMessage(
                role="system",
                content=SYSTEM_PROMPT,
            ),
            ChatMessage(
                role="user",
                content=user_prompt,
            )
        ],
        model_options=ChatModelOptions(
            temperature=1.0,
            max_tokens=80
        )
    )

    print("\nОтправляем запрос...")

    with GigaChat(
        credentials=key,
        scope=scope,
        model="GigaChat-2",
        ca_bundle_file="certs/Russian_Trusted_Root_CA.cer",
        timeout=60,
    ) as client:
        response = client.chat.create(request)
        answer = response.messages[0].content[0].text
        
        print("\nОтвет от ИИ-помощника:")
        print(answer)