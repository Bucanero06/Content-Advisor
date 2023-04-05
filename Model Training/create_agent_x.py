import re

import gradio as gr
import openai, os, subprocess
import json
from CREDENTIALS_DO_NOT_PUSH import OPENAI_API_KEY

# Use environment variables to store the API key securely
# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
DEFAULT_NAME_GENERATION_KEY = "g"

# Logger
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)





def init_and_launch_gradio(agent):
    """
    Launches a Gradio interface for the chatbot.

    Args:
        agent: An instance of the Agent class.
    """
    ui = gr.Interface(
        fn=agent.transcribe,
        inputs=gr.Audio(source="microphone", type="filepath"),
        outputs="text",
        title=agent.role_info["role"],
        description=agent.role_info["description"],
    ).launch()


def initialize_messages(system_message=None, intro_assistant_message=None, intro_user_message=None):
    """
    Initializes a list of messages for a chatbot conversation.

    Args:
        system_message: A string containing a system message.
        intro_assistant_message: A string containing an introductory message from the assistant.
        intro_user_message: A string containing an introductory message from the user.

    Returns:
        A list of dictionaries containing message information.
    """
    initial_messages = []
    if system_message:
        initial_messages.append({"role": "system", "content": system_message})
    if intro_assistant_message:
        initial_messages.append({"role": "assistant", "content": intro_assistant_message})
    if intro_user_message:
        initial_messages.append({"role": "user", "content": intro_user_message})
    return initial_messages


class Agent:
    """
    The Agent class represents an AI agent with a specific role, description, system message, and initial message.
    It can load or create roles, transcribe audio input, interact with OpenAI API, and launch a Gradio interface.
    """

    def __init__(self):
        """
        Initializes an Agent instance with default attributes.
        """
        self.role_info = None
        self.messages = None

    def load_role(self, role):
        """
       Loads the specified role and initializes the messages attribute.

       Args:
           role (str): The role to be loaded.

       Returns:
           bool: True if the role is loaded successfully, otherwise False.
       """
        assert role, "Please provide a role to be loaded."

        self.role_info = self.get_agent_info(role)

        if not self.role_info:
            print("Role not found. Create a new one?")
            # if input("Enter 'y' to create a new role: ").lower() == "y":
            #     self.update_role_info_attribute(role=role)
            #     self.create_agent_role(
            #
            #     )
            # todo create new role
            return False
        else:
            assert self.role_info["role"] == role, "Role name mismatch."
            self.messages = initialize_messages(
                system_message=self.role_info["system_message"],
                intro_assistant_message=self.role_info["intro_message"]
            )

    def get_agent_info(self, role):
        """
        Retrieves the role information from the available roles.

        Args:
            role (str): The role to get the information for.

        Returns:
            dict: The role information if the role exists, otherwise None.
        """
        available_roles = self.load_available_roles()
        if role in available_roles:
            return available_roles[role]

    def update_role_info_agent_class_attribute(self, role=None, description=None, system_message=None,
                                               intro_message=None):
        """
        Updates the role_info attribute of the Agent class with the provided information.

        Args:
            role (str, optional): The role name.
            description (str, optional): The role description.
            system_message (str, optional): The system message for the role.
            intro_message (str, optional): The initial/welcome message for the role.
        """
        print(f'\nUpdating role info agent class attribute  ---> json dump')
        self.role_info = {
            "role": role,
            "description": description,
            "system_message": system_message,
            "intro_message": intro_message
        }
        print(f'    {json.dumps(self.role_info, indent=4)}\n')

    @staticmethod
    def load_available_roles(agent_roles_path="roles.json"):
        """
        Loads available agent roles from a JSON file.

        Args:
            agent_roles_path (str, optional): The path to the JSON file containing the agent roles.
                Defaults to "roles.json".

        Returns:
            dict: A dictionary containing the available agent roles. Returns an empty dictionary if the file is not found.
        """

        try:
            with open(agent_roles_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {agent_roles_path} not found.")
            return {}

    @staticmethod
    def write_json_to_agent_roles_path(agent_roles_path="roles.json", available_roles=None):
        """
        Writes available agent roles to a JSON file.

        Args:
            agent_roles_path (str, optional): The path to the JSON file for storing the agent roles.
                Defaults to "roles.json".
            available_roles (list, optional): The list of available agent roles.
                Defaults to None.
        """

        available_roles = available_roles or []
        with open(agent_roles_path, "w") as file:
            json.dump(available_roles, file, indent=4)

    @staticmethod
    def legacy_complete(prompt, engine="davinci", max_tokens=100, stop=None, temperature=0.9, top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0, n=1, stream=False, logprobs=None, echo=True):
        """
            Calls the OpenAI API to generate text based on the given prompt and parameters.

            Args:
                prompt (str): The text prompt to send to the OpenAI API.
                engine (str, optional): The OpenAI engine to use for text generation. Defaults to "davinci".
                max_tokens (int, optional): The maximum number of tokens in the generated text. Defaults to 100.
                stop (list, optional): A list of strings that indicate the end of the generated text. Defaults to None.
                temperature (float, optional): Controls the randomness of the generated text. Defaults to 0.9.
                top_p (float, optional): Controls the nucleus sampling to limit the token set. Defaults to 1.
                frequency_penalty (float, optional): Controls the penalty for token frequency. Defaults to 0.
                presence_penalty (float, optional): Controls the penalty for new tokens. Defaults to 0.
                n (int, optional): The number of generated responses. Defaults to 1.
                stream (bool, optional): Controls whether to stream the response. Defaults to False.
                logprobs (int, optional): The number of log probabilities to return. Defaults to None.
                echo (bool, optional): Controls whether to include the input prompt in the response. Defaults to True.

            Returns:
                str: The generated text from the OpenAI API.
            """
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            n=n,
            stream=stream,
            logprobs=logprobs,
            echo=echo,
        )
        # Can use token information to estimate costs
        # print(f"OpenAI response: {response}")

        # Return the text from the first response
        return response.choices[0].text

    @staticmethod
    def complete(model="gpt-3.5-turbo", system_message=None, intro_assistant_message=None, user_prompt=None,
                 formatted_messages=None):
        """Uses OpenAI's text generation API to generate text based on a prompt."""

        return openai.ChatCompletion.create(
            model=model,
            messages=initialize_messages(
                system_message=system_message,
                intro_assistant_message=intro_assistant_message,
                intro_user_message=user_prompt
            ) if not formatted_messages else formatted_messages,
        )

    def transcribe(self, audio):
        """
        Transcribes an audio input and generates a chat transcript with the assistant's response.

        Args:
            self: An instance of the Agent class.
            audio: A file path to the audio input.

        Returns:
            A string containing the chat transcript.
        """
        if not audio:
            return "Error: No audio input received."

        audio_file = open(audio, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        if not transcript["text"]:
            return "Error: Unable to transcribe audio input."

        self.messages.append({"role": "user", "content": transcript["text"]})

        print(self.messages)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)

        system_message = response["choices"][0]["message"]
        self.messages.append(system_message)

        chat_transcript = ""
        for message in self.messages:
            if message['role'] != 'system':
                chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

        return chat_transcript

    def resolve_existing_role_info(self,
                                   role,
                                   description=None,
                                   system_message=None,
                                   intro_message=None,
                                   **kwargs):
        print(f"Warning: Role '{role}' already exists.")
        action = input(
            "Enter:"
            "\n 'o' to overwrite with passed and autofill the rest,"
            "\n 'n' to just type a new name as to not disturb the already created agent, "
            "use the passed values and autofill the rest,"
            "\n"
        ).lower()

        if not action:
            action = kwargs.get("default_action_to_resolve_existing_role_info", "n")
        if action in ["o", "overwrite"]:
            self.update_role_info_agent_class_attribute(role, description, system_message, intro_message)
        elif action in ["n", "enter_new_name"]:
            role = input("Enter a new name for the role: ")
            self.update_role_info_agent_class_attribute(role, description, system_message, intro_message)
        else:
            print("Invalid input. Try again.")
            self.resolve_existing_role_info(role, description, system_message, intro_message, **kwargs)

    def get_available_context_from_role_info_attribute(self):
        """
        Retrieves the available context from the role_info attribute and formats it as a string.

        Returns:
            str: A string containing the available context from the role_info attribute.
        """

        context_keys = {
            "role": "Role name",
            "description": "Description",
            "system_message": "System message",
            "intro_message": "Initial/Welcome message"
        }

        # Append available context elements from the role_info attribute
        context = [f"{key_label}: {self.role_info[key]}" for key, key_label in context_keys.items() if
                   self.role_info[key]]

        # Join the context elements into a single string
        return " ".join(context)

    def fill_role_info_attribute_based_on_context(self, **kwargs):
        """
        Uses OpenAI's text generation API to generate any missing information with every available context object.
        """

        # Ensure at least one value in the role_info attribute is not None
        if not any(self.role_info.values()):
            raise ValueError("No context available. Please provide at least one value for the role_info attribute.")

        print('... auto-filling missing information based on context available ...')

        # Construct the prompt to generate missing information based on the available context
        beginning_of_prompt = f'Using the provided context, which includes a role name, description, system message, ' \
                              f'and initial message, create a complete and vibrant output that aligns with user ' \
                              f'expectations. Generate new content as needed, be aware that some inputs might be None. ' \
                              f'Remember to craft each element with attention to detail, engaging language, and ' \
                              f'high-quality content: ' \
                              f'Role name: A title or position that defines a persons function or expertise.' \
                              f'Role description: A comprehensive summary of the roles tasks and responsibilities.' \
                              f'System message: A message that establishes the AIs persons, tone, and communication ' \
                              f'style, considering that the roles might desire a more human-like behavior or ' \
                              f'interaction.Initial message: A tailored, welcoming, and informative message from the ' \
                              f'AI to the user, reflecting a communication style that may not feel like a typical ' \
                              f'AI interaction. ' \
                              f'1.I dont want values that are passed to be changed in the outcome. ' \
                              f'2.i want something like what the description currently outputted to be in the ' \
                              f'system_message since it really brings the personality, traits and theme needed. ' \
                              f'The only difference is that description should be shorter and more aimed at an end user ' \
                              f'who is looking to quickly understand the role while system_message is more in depth. ' \
                              f'3. Since some roles might not be desired to behave like a machine/ai, and might ' \
                              f'require a more human touch, so keep that in mind' \
                              f'Please adhere to the following output format:' \
                              f'{{' \
                              f'"role": original_or_generated_role_name, ' \
                              f'"description": original_or_generated_role_description, ' \
                              f'"system_message": original_or_generated_system_message,' \
                              f'"intro_message": original_or_generated_initial_message' \
                              f'}} Based on the following context: '

        context = self.get_available_context_from_role_info_attribute()
        end_of_prompt = 'Returning Dictionary:'
        beginning_of_output = '{"role"'
        prompt = f'{beginning_of_prompt} {context} {end_of_prompt} {beginning_of_output}'

        # Call the text generation API
        response = self.complete(
            model=kwargs.get("auto_fill_missing_info_model", "gpt-3.5-turbo"),
            system_message=self.role_info["system_message"],
            intro_assistant_message=self.role_info["intro_message"],
            user_prompt=prompt
        )

        print(f"Model's Inference Response: {response}")

        # Extract and format the output from the API response
        output = f'{beginning_of_output} {response.choices[0].message.content}'
        print(f"Output: {output}")

        # Update the role_info dictionary with the generated output
        self.role_info = dict(json.loads(output))

    def create_agent_role(self, role, description=None, system_message=None, intro_message=None, **kwargs):
        """High level function to create a new agent role and handle all the necessary steps to take.

        role: str
            The name of the role to be created.
        description: str
            A short description of the role.
        system_message: str
            A message that will be used by the assistant to inform itself of its role.
        intro_message: str
            A message that will be sent to the user when they join the server.
        **kwargs: dict
            Any additional keyword arguments to pass to the function.
            auto_fill_missing_info: bool (default: False)
                If True, then the function will attempt to fill in any missing information with the OpenAI API.
            default_action_to_resolve_existing_role_info: str (default: "n")
                The default action to take if the user does not provide an input when asked to resolve an existing role.
                Options are "o" for overwrite or "n" for enter a new name

        Returns:
            self.role_info: dict
                A dictionary containing the role information that was just created.
        """

        available_roles = self.load_available_roles()
        agent_roles_path = kwargs.get("agent_roles_path", "roles.json")

        '''* Check if role is already made, if so then resolve_existing_role_name
                or 
            * If role does not exist, then create a new role. Else, ask user if they want to overwrite, 
                pick a new name, or generate a new name based on the system and welcome messages.'''
        if role in available_roles:
            self.resolve_existing_role_info(role=role, description=description,
                                            system_message=system_message, intro_message=intro_message, **kwargs)

        else:
            print("Since we are creating a new agent role we are going to use the provided "
                  "information to fill in the blanks of those settings which were not provide")
            assert role, "Role name is required"
            self.update_role_info_agent_class_attribute(role, description, system_message, intro_message)
            assert self.role_info["role"] not in available_roles, "Role exists ... error handling didnt catch this"

        if kwargs.get("auto_fill_missing_info", False): self.fill_role_info_attribute_based_on_context(**kwargs)
        available_roles[role] = self.role_info
        self.write_json_to_agent_roles_path(agent_roles_path=agent_roles_path, available_roles=available_roles)

        if kwargs.get("load_role_after_creating_it", False): self.load_role(role=role)
        return self.role_info


if __name__ == "__main__":
    LOAD_ROLE = True

    # todo update this module
    therapist_agent = Agent()
    if LOAD_ROLE:
        therapist_agent.load_role(role="Therapy Chatbot")
    else:
        therapist_agent.create_agent_role(
            role="Therapy Chatbot",
            # description="A therapist that listens to your thoughts and emotions.",
            description=None,
            system_message=None,
            intro_message=None,
            #
            **dict(
                agent_roles_path="roles.json",
                #
                auto_fill_missing_info=True,
                auto_fill_missing_info_model="gpt-3.5-turbo",
                #
                default_action_to_resolve_existing_role_info="enter_new_name",
                #
                load_role_after_creating_it=True
            )
        )

    print(f'{therapist_agent.role_info = }')
    init_and_launch_gradio(therapist_agent)
