import os
import openai
import time

os.environ["OPENAI_API_KEY"] = 'YOUR API KEY'
openai.api_key = os.getenv("OPENAI_API_KEY")

def createResponse(mesg, context=[
            {"role": "system", "content": "You are a helpful assistant."},
        ]):
    collected_events = []
    completion_text = []
    speed = 0.05 #smaller is faster
    start_time = time.time()

    currentContext = context
    currentContext.append({"role": "user", "content": mesg})

    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=currentContext,
        temperature=0,
        stream=True
    )

    for i in reponse:
        if (i['choices'][0]['finish_reason'] != 'stop'):
            event_time = time.time() - start_time  # calculate the time delay of the event
            collected_events.append(i)  # save the event response
            event_text = i['choices'][0]['delta']['content']  # extract the text
            completion_text += event_text  # append the text
            time.sleep(speed)
            print(f"{event_text}", end="", flush=True)
        else:
         print('\n')

    resp = ''.join(completion_text)
    currentContext.append({"role": "system", "content": resp})
    return currentContext



mesg = 'Hello chatGPT'
conversationContext = createResponse(mesg, [
            {"role": "system", "content": "You are a helpful assistant."},
        ])
mesg = input()
while (mesg != 'q'):
    conversationContext = createResponse(mesg, conversationContext)
    print(conversationContext)
    mesg = input()