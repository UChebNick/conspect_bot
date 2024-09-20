import asyncio

import httpx
import requests


def send_request(links, text, user_text, gpt, max_tokens):
    content = {
                "type": "text",
                "text": f'составь конспект по тексту с моей лекции - "{text}" {user_text}'
              }

    # if user_text:
    #     text.append({
    #             "type": "text",
    #             "text": user_text
    #         })
    # if links:
    #     images = [{
    #             "type": "image_url",
    #             "image_url": {
    #               "url": link
    #             }} for link in links]
    #     content.extend(images)

    url = "https://api.proxyapi.ru/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-VheRX9HvvbtrTxarsbb3JRwU9sUAKVBU"
    }
    print(max_tokens)
    if gpt in ['gpt-3.5-turbo-1106', 'gpt-3.5-turbo-0125', 'gpt-4']:
        data = {
            "model": gpt,
            "messages": [{"role": "user", "content": [content]}],
            "temperature": 0.5,
            "max_completion_tokens": max_tokens // 1}
    else:
        data = {
            "model": gpt,
            "messages": [{"role": "user", "content": [content]}],
            "max_completion_tokens": max_tokens // 1}
    print(data)

    response = httpx.post(url, headers=headers, json=data)
    print(response.json())
    return response.json()