import openai
import json
import os
from webai.browser import Browser
import webai.prompt_lib as prompt_lib

class GPTV_Actor:
    def __init__(self):
        self.client = openai.Client()
        self.last_response = None
        self.chat_history = []
        self.agent_memory = []

    def _call_api(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=400,
        )
        return response.choices[0].message.content
    
    def start(self, start_link="https://www.google.com", auto=False):
        self.browser = Browser(start_link, resolution=(768, 768))
        self.auto = auto
        if not self.auto:
            input("After each step, you will need to press ENTER to confirm agent's action or type the message you want to send to the agent. Press ENTER to start...")
        goal = input("What can I help you with? ")
        self.chat_history.append({"role": "user", "content": f"Goal: {goal}"})
        while True:
            self.act()

    def start_browser(self, start_link="https://www.google.com", resolution=(768, 768)):
        self.browser = Browser(start_link, resolution=(768, 768))
    
    def act(self):
        self.browser.save_current_view()
        if not hasattr(self, 'browser'):
            raise Exception("Please start browser first!")
        obs_msg = self.browser.get_obs_msg()
        msgs = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_lib.sys_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_lib.get_context_prompt(self.last_response, self.agent_memory, self.chat_history)
                    },
                    obs_msg
                ]
            }
        ]
        response = self._call_api(msgs)
        print(f"🤔: {response}")
        response_json = json.loads(response)
        self.last_response = response_json
        action = response_json['next_action']
        if action =="<STOP>":
            input("Session terminated by agent. Press ENTER to quit...")
            exit(0)
        if 'memorize' in response_json:
            self.agent_memory.append(response_json['memorize'])
        if 'user_response' in response_json:
            print(f"💬: {response_json['user_response']}")
            self.chat_history.append({"role": "agent", "content": response_json['user_response']})
        print(f"🤖: {action}")
        if not self.auto:
            user_msg = input("You:")
            if user_msg != "":
                self.chat_history.append({"role": "user", "content": user_msg})
        self.browser.step(action)

