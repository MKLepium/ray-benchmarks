import ray
import torch
import time
from transformers import AutoTokenizer, pipeline
from starlette.requests import Request

from fastapi import FastAPI

ray.init()

@ray.remote(num_cpus=1, num_gpus=1)
class CommonFactorClassification:
    def __init__(self, model_id: str = "openai-community/gpt2"): # "openai-community/gpt2" "TinyLlama/TinyLlama-1.1B-Chat-v1.0" "meta-llama/Llama-2-7b-hf"
        print("initializing", flush=True)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu' # Assume running on GPU
        print(f"Using device: {self.device}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        self.model_id = model_id
        self.pipe = pipeline("text-generation", model=self.model_id, tokenizer=self.tokenizer, device=self.device)
        self.sys_prompt = """
Your task is to classify text inputs. You'll be given a text input and a set of classes to choose from.

Output the results as a JSON in the following format:
{"Final_prediction": {
        "first_place_prediction": {
            "class_name": <The class with the highest confidence score>,
            "confidence_score": <The confidence score for that class>  
        },
        "second_place_prediction": {
            "class_name": <The class with the second-highest confidence score>,
            "confidence_score": <The confidence score for that class>  
        },
        "third_place_prediction": {
            "class_name": <The class with the third-highest confidence score>,
            "confidence_score": <The confidence score for that class>  
        }
    }
}"""    

        self.user_prompt = """
Classify the input into one of the following classes: Low-Tech-Savviness, Stressful Life Events, Alliance Rupture, Low Usability, Demoralisation, Fear to Change, Extrinsic Motivation, Loneliness / Lack of Social Support, Amotivation, Perceived Lack of Fit, Self-Depreciation / Learned helplessness and Ambivalence. Below are the definitions of each of the classes available at this level

Rank the top three classes in descending order. That is the most likely class should be ranked first, the second most likely class should be ranked second, and the third most likely class should be ranked third. Assign confidence scores to each of the predicted classes.

input: {input}"""


    def classify(self, classify) -> str:
        input_request: str = classify
        input_text = input_request["input_text"]
        full_prompt = self.user_prompt.format(input=input_text)
        messages = [{"role": "system", "content": self.sys_prompt}, {"role": "user", "content": full_prompt}]
        #self.logger.info(messages)
        tokenized_chat = self.tokenizer.apply_chat_template(messages, tokenize=False)
        output = self.pipe(tokenized_chat, max_new_tokens=100, do_sample=True)
        return output
    

classification_actor = CommonFactorClassification.remote()

times = []
for i in range(1000):
    test_input = """Dear Journal,

Today was a bit of a struggle on the iCBT platform. I found myself getting really frustrated with the whole thing. It felt like no matter how hard I tried, I just couldn't seem to navigate the app and website properly. It's like I'm just not as tech-savvy as I should be. It's like I was speaking a whole different language!

I mean, I know I'm not the most tech-savvy person out there, but today really made me feel like I was falling behind. The whole user interface and navigation just felt so overwhelming and confusing. It made me question whether or not I was even capable of using this platform to its fullest potential.

It's like I struggled so much trying to understand how to use the features and tools that were available. It felt like this barrier between me and actually getting the help that I needed. I wish the platform was a little bit more user-friendly for people like me who aren't super tech-savvy.

On a completely unrelated note, I did manage to go for a walk at the park today. It was nice to get some fresh air and clear my mind, even if only for a little while.

Anyway, I'll have to make sure to bring this up to my therapist next time. Maybe they can offer some tips or resources to help me navigate the digital platform a bit better.

Until next time,
[Your Name]"""
    start_time = time.time()
    
    prediction = ray.get(classification_actor.classify.remote({"input_text": test_input}))
    
    elapsed_time = time.time() - start_time
    times.append(elapsed_time)
    
    #print(prediction)
    print(f"Time taken: {elapsed_time} seconds")
    print("iteration: ", i+1, "out of 1000")

average_time = sum(times) / len(times)

# write times to file

with open("ray_actor_call_times.txt", "w") as f:
    for time in times:
        f.write(f"{time}\n")


print(f"Average time per prediction: {average_time} seconds")