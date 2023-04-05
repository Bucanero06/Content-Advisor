from create_agent_x import Agent

therapist_agent = Agent()
therapist_agent.create_agent_role(role="Dr. Therapist",
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

patient_agent = Agent()
patient_agent.create_agent_role(role="Patient",
                                # description="A patient that wants to talk to a therapist.",
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

# Have the patient talk to the therapist
# todo left here ... build talk_to_agent() method make sure this makes sense. else simply use completions and tract their messagesa
patient_agent.talk_to_agent(agent=therapist_agent)
