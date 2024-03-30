import discord 
import os
import openai
with open("chat.txt" ,"r") as f:
    chat = f.read()
chat=" "
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

token = os.getenv("SECRET_KEY")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        chat += f"{message.author}:{message.content} \n " 
        print(f'Message from {message.author}: {message.content}')
        print(message.mentions)
        if self.user != message.author:
            if self.user in message.mentions:
                print(chat)
                response = openai.completions.create(  
                    model="gpt-3.5-turbo-instruct",
                    prompt=f"{chat}\n HarriniGpt: ",
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                print(response)  # Print response from OpenAI for debugging
                if response.choices:
                    channel = message.channel
                    message_to_send = response.choices[0].text.strip()
                    await channel.send(message_to_send)
                else:
                    print("No response received from OpenAI.")
            else:
                print("Bot not mentioned in the message.")
        else:
            print("Ignoring message from bot.")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token or "")

