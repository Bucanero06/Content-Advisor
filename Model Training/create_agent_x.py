import gradio as gr
import openai, os, subprocess
import json
import CREDENTIALS_DO_NOT_PUSH

# Use environment variables to store the API key securely
# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = str(CREDENTIALS_DO_NOT_PUSH.OPENAI_API_KEY)


class Agent:
    def __init__(self, role):
        self.role = role
        agent = self.get_agent_info()
        self.messages = [
            {"role": "system", "content": agent["system_message"], "welcome_message": agent["welcome_message"]}]

    def get_selected_role(self):
        available_roles = self.load_available_roles()
        for role_info in available_roles:
            if role_info["role"] == self.role:
                return role_info["system_message"], role_info["welcome_message"]
        return "Role not found.", "No welcome message."

    def get_agent_info(self):
        system_message, welcome_message = self.get_selected_role()
        agent = {"role": self.role, "system_message": system_message, "welcome_message": welcome_message}
        return agent

    @staticmethod
    def load_available_roles():
        try:
            with open("roles.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: roles.json not found.")
            return []

    def create_model_personality(self, role, system_message, welcome_message):
        available_roles = self.load_available_roles()
        new_role = {"role": role, "system_message": system_message, "welcome_message": welcome_message}
        available_roles.append(new_role)
        with open("roles.json", "w") as file:
            json.dump(available_roles, file)

    def transcribe(self, audio):
        if not audio:
            return "Error: No audio input received."

        audio_file = open(audio, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        if not transcript["text"]:
            return "Error: Unable to transcribe audio input."

        self.messages.append({"role": "user", "content": transcript["text"]})

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)

        system_message = response["choices"][0]["message"]
        self.messages.append(system_message)

        chat_transcript = ""
        for message in self.messages:
            if message['role'] != 'system':
                chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

        return chat_transcript


def launch_gradio(agent):
    ui = gr.Interface(fn=agent.transcribe,
                      inputs=gr.Audio(source="microphone", type="filepath"),
                      outputs="text",
                      title="Therapy Chatbot",
                      description="Speak to a virtual therapist about your thoughts and emotions.",
                      ).launch()


if __name__ == "__main__":
    therapist_agent = Agent(role="therapist")
    launch_gradio(therapist_agent)
