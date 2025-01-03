import time
from Tinder import Tinder

import time

from openai import OpenAI



AUTH_TOKEN = '' #Your Tinder token here
chat_TOKEN = '' #Your chatGPT token here

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=chat_TOKEN,
)

def chatBOT(api_key = "", message = ""):
    
    
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      max_tokens=128,
      temperature=0.5,
      messages=[
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content


def send_message():
    while True:
        TinderAcc = Tinder(AUTH_TOKEN)
        all_messages = TinderAcc.find_matches()
        #print(all_messages)
        keys = list(all_messages.keys())
        values = list(all_messages.values())
        
        for i in range(len(keys)):
            print(keys[i], " : ", values[i])
            resp = chatBOT(chat_TOKEN,values[i])
            print(resp)
            TinderAcc.send_message(sendID = keys[i], message = resp)
        #TinderAcc.send_message(sendID = key[0], message = "test.")
        print("Rest for 10 min...")
        time.sleep(600)
        
      
if __name__ == "__main__":
    send_message()
