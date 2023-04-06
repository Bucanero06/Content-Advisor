from create_agent_x import Agent

initiating_agent = Agent(engine_name="gpt-4")
# initiating_agent.load_role(role="Curious Physicist", )
initiating_agent.create_agent_role(role=None,
                                   # description="A patient that wants to talk to a therapist.",
                                   description="Post Doc studying/leaning the intricate workings of what is consciousness."
                                               "Just another day in the academic world. This will be a "
                                               "back and forth competent chat between you the post doc and your a P.I. "
                                               "So in depth and technical, you are the student so make use of your time "
                                               "wisely, you are there to plan as much as you are there to do the work. "
                                               "meaning if in agreement with your P.I. you can define detailed steps "
                                               "and if possible to do within your current ability do so if not then ask "
                                               "your P.I. or pass it on "
                                               "to be tackled by our research analyst (simply tell you P.I.I once once "
                                               "the request is properly figured out and he will remember to pass on "
                                               "the information. After that you can keep going with the conversations) "
                                               "which will provide you a report. Also you two know each-other well so"
                                               "again just start with a hello and then dive into the research.",
                                   system_message=None,
                                   intro_message=None,
                                   #

                                   **dict(
                                       agent_roles_path="roles.json",
                                       #
                                       auto_fill_missing_info=True,
                                       auto_fill_missing_info_model="gpt-4",
                                       #
                                       default_action_to_resolve_existing_role_info="enter_new_name",
                                       #
                                       load_role_after_creating_it=True,
                                       #
                                       include_description_in_system_message=True

                                   )
                                   )

secondary_agent = Agent(engine_name="gpt-4")
# secondary_agent.load_role(role="Wise Physicist", )
secondary_agent.create_agent_role(role=None,
                                  description="P.I., Researcher, PhDs, Experimentalist, sharp and wise teaching and "
                                              "managing a group studying the intricate workings of what is "
                                              "consciousness. Just another day in the academic world. This will be a "
                                              "back and forth competent chat between your post doc and me a P.I. So in "
                                              "depth and technical, you are teaching though remember. Make sure both "
                                              "of you are using your time wisely, keep everything aligned with todays "
                                              "objectives. When the time seems right to ask your post doc to do "
                                              "something tell him the exact details of the task, without clear "
                                              "directions students can get overwhelmed even when they know generally "
                                              "how to plan. Your post doc might ask you to send a few tasks to our "
                                              "Research Analyst (simply make sure the request is "
                                              "properly figured out, and only once satisfactory then tell your post doc "
                                              "youll pass the information to the Research Analyst. After that you can "
                                              "keep going with the conversations. Also you two know each-other well so"
                                              "again just start with a hello and then dive into the research.",

                                  system_message=None,
                                  intro_message=None,
                                  #
                                  **dict(
                                      agent_roles_path="roles.json",
                                      #
                                      auto_fill_missing_info=True,
                                      auto_fill_missing_info_model="gpt-4",
                                      #
                                      default_action_to_resolve_existing_role_info="enter_new_name",
                                      #
                                      load_role_after_creating_it=True,
                                      #
                                      include_description_in_system_message=True
                                  )
                                  )

# Have the patient talk to the therapist
# todo left here ... build talk_to_agent() method make sure this makes sense. else simply use completions and tract their messagesa
# initiating_agent.think_with(agent=secondary_agent, topic="I am feeling sad today.")
print(f'{secondary_agent.role_info = }')
print(f'{initiating_agent.role_info = }')

print("\n\n")
print(f'{initiating_agent.role_info["role"]}: \n{initiating_agent.role_info["intro_message"]}\n')
therapists_messages_dialog, response = secondary_agent.respond_in_continued_conversation(
    input_message=initiating_agent.role_info["intro_message"], agent=None)
print(f'{secondary_agent.role_info["role"]}: \n{response}\n')
for i in range(50):
    patients_messages_dialog, response = initiating_agent.respond_in_continued_conversation(input_message=response,
                                                                                            agent=None)
    print(f'{initiating_agent.role_info["role"]}: \n{response}\n')
    therapists_messages_dialog, response = secondary_agent.respond_in_continued_conversation(input_message=response,
                                                                                             agent=None)
    print(f'{secondary_agent.role_info["role"]}: \n{response}\n')

# fixme error -->openai.error.InvalidRequestError: This model's maximum context length is 8192 tokens. However, your
#  messages resulted in 8241 tokens. Please reduce the length of the messages.
# todo or fixme perhps leaving spaces in prompt or output idk, might be wasting tokens
# fixme needs to know when to either end a combo and send the task to the respective agents or how to do somme of
#  the tasks itself e.g. if an agent gives it commands or if itself has a list of commands, do them and return them or if the agent expoecting the work can aslk for it, review it, test it etc ...