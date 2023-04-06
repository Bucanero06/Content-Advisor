from django.shortcuts import render
from django.http import JsonResponse
import openai
import sys
import os
# get the absolute path to the directory containing the module file
module_dir = os.path.abspath('../')

# add the directory to Python's search path
sys.path.append(module_dir)

# print the current directory to verify that the module directory has been added
print("Current Directory:", sys.path)

# import the module by its name
from create_agent_x import Agent
from CREDENTIALS_DO_NOT_PUSH import OPENAI_API_KEY


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
