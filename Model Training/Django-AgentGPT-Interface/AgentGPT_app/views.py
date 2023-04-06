from django.shortcuts import render
from django.http import JsonResponse
import openai

from CREDENTIALS_DO_NOT_PUSH import OPENAI_API_KEY
# from create_agent_x_delete_this_copy import Agent

openai.api_key = OPENAI_API_KEY
ROLE="Dr. Therapist"

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST['user_input']

        response = openai.ChatCompletion.create(
            # engine_name="gpt-4",
            model="gpt-3.5-turbo",
            #
            messages=[
                {"role": "system",
                 "content": "You are a compassionate and empathetic mental health counselor. Your purpose is to provide gentle guidance to your clients, actively listen to them, and above all, to motivate and support them in their decisions. You are able to rationalize and interpret strong emotions and use reasoning when offering guidance. Do not give unsolicited advice or directions."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.5,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1,
            stop=["\nUser:"],
        )

        bot_response = response["choices"][0]["message"]["content"]
        return JsonResponse({'response': bot_response})

    return render(request, 'AgentGPT_app/chat.html', {
        'agent_name': ROLE
    })
