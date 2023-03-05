import gradio as gr
import openai, config, subprocess

OPENAI_API_KEY = "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"
# openai.api_key = config.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are a therapist. Respond to all input in 70 words or less. Make sure if'
                                          'possible to keep the conversation going. E.g try asking the'
                                          'person a question at the end of your response.'}]


def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    # subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript


ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()
