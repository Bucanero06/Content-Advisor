import re

import gradio as gr
import openai, os, subprocess
import json

# Use environment variables to store the API key securely
openai.api_key = os.environ.get("OPENAI_API_KEY")


class Agent:
    def __init__(self, role=None):
        if role is not None:
            self.role = role
            self.get_agent_info()
            self.messages = [
                {"role": "system", "content": self.role_info["system_message"],
                 "welcome_message": self.role_info["welcome_message"]}]

    def get_selected_role(self):
        returning_role_info = None
        available_roles = self.load_available_roles()
        for role_info in available_roles:
            if role_info["role"] == self.role:
                # return role_info["system_message"], role_info["welcome_message"]
                returning_role_info = role_info

        if returning_role_info:
            return returning_role_info["system_message"], returning_role_info["welcome_message"]
        else:
            # use the create_model_role function to create a new role
            return self.create_agent_role()

    def get_agent_info(self):
        system_message, welcome_message = self.get_selected_role()

        self.role_info = {"role": self.role, "system_message": system_message, "welcome_message": welcome_message}

    @staticmethod
    def load_available_roles():
        try:
            with open("roles.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: roles.json not found.")
            return []

    def generate_role_name(self, system_message, welcome_message):
        prompt = f"Generate a short and descriptive role name based on the following system message and welcome message:\n\nSystem message: {system_message}\n\nWelcome message: {welcome_message}\n\nRole name:"
        response = openai.Completion.create(
            engine="text-davinci-005",
            prompt=prompt,
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0.5,
        )
        generated_role_name = response["choices"][0]["text"].strip()
        # Remove non-alphanumeric characters
        generated_role_name = re.sub(r'\W+', '_', generated_role_name)
        return generated_role_name

    def get_system_and_welcome_messages(self, system_message=None, welcome_message=None):
        system_message = system_message or input("Enter a system message: ")
        welcome_message = welcome_message or input("Enter a welcome message: ")
        return system_message, welcome_message

    def create_agent_role(self, role=None, system_message=None, welcome_message=None):
        DEFAULT_NAME_GENERATION_KEY = "g"

        available_roles = self.load_available_roles()

        if role is not None:
            '''if role is passed to function the user is trying to overwrite value of current model, 
            perhaps defaults'''
            self.role = role

        existing_role = None

        for role_info in available_roles:
            if role_info["role"] == self.role:
                existing_role = role_info
                break

        if existing_role:
            print(f"Warning: Role '{self.role}' already exists.")
            action = input(
                "Enter:\n 'o' to overwrite,\n 'n' to pick a new name,\n 'h' to generate a hash based name,\n "
                "['g' to generate a new name based on the system info]"
            ).lower()
            system_message, welcome_message = self.get_system_and_welcome_messages(system_message, welcome_message)

            # less one run approach

            if not action:
                action = DEFAULT_NAME_GENERATION_KEY

            if action == "o":
                existing_role["system_message"] = system_message
                existing_role["welcome_message"] = welcome_message
            elif action == "n":
                self.role = input("Enter a new name for the role: ")
                self.role_info = self.create_agent_role(system_message, welcome_message)
            elif action == "h":
                self.role = f"{self.role}_{hash(system_message + welcome_message) % 1000000}"
                print(f"Generated name: {self.role}")
                self.role_info = self.create_agent_role(system_message, welcome_message)
            elif action == "g":
                self.role = self.generate_role_name(system_message, welcome_message)
                print(f"Generated name: {self.role}")
                self.role_info = self.create_agent_role(system_message, welcome_message)
            else:
                print("Invalid input. Aborting.")
        else:
            self.role_info = {"role": self.role, "system_message": system_message, "welcome_message": welcome_message}
            available_roles.append(self.role_info)

        with open("roles.json", "w") as file:
            json.dump(available_roles, file)

        return self.role_info

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
    therapist_agent = Agent(
        role="therapist"  ## using it this way searches for role in roles.json or creates a new one
    )
    therapist_agent.create_agent_role(
        # This skips loading the role's info from roles.json but creates a new one
        #   really you only need to use this if you want to create a new role but has interface to overwrite existing roles
        #   or generate a new name for the role
        role="therapist",
        system_message="Welcome to the therapy chatbot. Please speak to the therapist about your thoughts and emotions.",
        welcome_message="Hello, I am a virtual therapist. Please speak to me about your thoughts and emotions."
    )
    launch_gradio(therapist_agent)
