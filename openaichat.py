import openai
import os
import json

class OpenAIChat:
    def __init__(self, model = "gpt-4-0613"):
        self.model = model
        self.functions = {}
        self.functions_descrition = []
        self.messages = []
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def completion(self, messages):
        if len(self.functions) == 0:
            return openai.ChatCompletion.create(model=self.model,messages=messages)
        return openai.ChatCompletion.create(model=self.model,messages=messages,functions=self.functions_descrition)
    
    def treat_completion_response(self, completion):
        response_message = completion["choices"][0]["message"]
        if response_message.get("function_call"):
            print("--- FUNCTION CALL ---")
            print(response_message["function_call"])

            function_name = response_message["function_call"]["name"]
            function_to_call = self.functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(**function_args)

            self.messages.append(response_message)
            self.messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )
            return self.chat(self.messages)
        print("--- MESSAGE ---------")
        print(self.messages)
        print("---------------------")
        return response_message

    def chat(self, messages):
        self.messages = messages
        completion = self.completion(messages)
        return self.treat_completion_response(completion)
    
    def add_function(self, function, description):
        self.functions[function.__name__] = function
        self.functions_descrition.append(description)
        return self.functions