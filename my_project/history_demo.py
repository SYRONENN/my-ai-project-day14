import os
from gigachat.models import ChatMessage
from prompts import SYSTEM_PROMPT

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

messages.append(ChatMessage(role="user", content="посоветуй фантастику"))
messages.append(ChatMessage(role="assistant", content="Рекомендую фильм Интерстеллар"))

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

    print("\nОтправляем запрос...")
    
    answer = "Отличный выбор, я запомнил ваши предпочтения."
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
