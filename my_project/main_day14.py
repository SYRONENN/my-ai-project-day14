import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions
from prompts import SYSTEM_PROMPT

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")
print("Помощник по выбору фильмов")
print("Команды управления")
print("'выход' - завершить работу")
print("'очистить' - начать новый разговор (сбросить историю)")
print("'история' - посмотреть текущее состояние памяти чата\n")

messages = [
    ChatMessage(
        role="system",
        content=SYSTEM_PROMPT,
    )
]

with GigaChat(
    credentials=key,
    scope=scope,
    model="GigaChat-2",
    ca_bundle_file="certs/Russian_Trusted_Root_CA.cer",
    timeout=60,
) as client:
    while True:
        raw_input = input("\nНапишите ваши предпочтения и я выберу фильм специально для вас или введите команду: ")
        command_candidate = raw_input.strip().lower()

        if command_candidate == "выход":
            print("До свидания")
            break

        if command_candidate == "очистить":
            messages = [messages[0]]
            print("\n[История диалога очищена.]")
            continue

        if command_candidate == "история":
            print(f"\nКоличество сообщений в истории: {len(messages)}")
            print("Роли сообщений по порядку:")
            for msg in messages:
                print(f"роль: {msg.role}")
            continue

        if not raw_input.strip():
            print("\nошибка: пустое сообщение")
            continue

        messages.append(
            ChatMessage(
                role="user",
                content=raw_input.strip(),
            )
        )
        request = ChatCompletionRequest(
            model="GigaChat-2",
            messages=messages,
            model_options=ChatModelOptions(
                temperature=0.2,
                max_tokens=300
            )
        )

        print("\nОтправляем запрос...")

        try:
            response = client.chat.create(request)
            answer = response.messages[0].content[0].text

            print("\nОтвет от ИИ-помощника:")
            print(answer)
            messages.append(
                ChatMessage(
                    role="assistant",
                    content=answer,
                )
            )

            print(f"Длина истории сообщений: {len(messages)}")

            if len(messages) > 7:
                messages = [messages[0]] + messages[-6:]

        except Exception as e:
            print(f"ошибка при обращении к API{e}")