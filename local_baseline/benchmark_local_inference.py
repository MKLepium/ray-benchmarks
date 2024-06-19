import time
import torch
from transformers import AutoTokenizer, pipeline

def setup_model():
    model_id = "openai-community/gpt2"
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Setup the pipeline
    pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer, device=device)
    return tokenizer, pipe

tokenizer, pipe = setup_model()

def generate_prediction(input_text: str):
    sys_prompt = """Your task is to classify text inputs. You'll be given a text input and a set of classes to choose from."""
    user_prompt = f"""Classify the input into one of the following classes: Low-Tech-Savviness, Stressful Life Events, Alliance Rupture, Low Usability, Demoralisation, Fear to Change, Extrinsic Motivation, Loneliness / Lack of Social Support, Amotivation, Perceived Lack of Fit, Self-Depreciation / Learned helplessness and Ambivalence. Below are the definitions of each of the classes available at this level

Rank the top three classes in descending order. That is the most likely class should be ranked first, the second most likely class should be ranked second, and the third most likely class should be ranked third. Assign confidence scores to each of the predicted classes.

input: {input_text}"""

    messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}]
    tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=False)
    
    # Generate prediction
    output = pipe(tokenized_chat, max_length=500)
    return output[0]['generated_text']


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
    
    prediction = generate_prediction(test_input)
    
    elapsed_time = time.time() - start_time
    times.append(elapsed_time)
    
    #print(prediction)
    print(f"Time taken: {elapsed_time} seconds")
    print("iteration: ", i+1, "out of 1000")

average_time = sum(times) / len(times)

# write times to file

with open("local_call_times.txt", "w") as f:
    for time in times:
        f.write(f"{time}\n")


print(f"Average time per prediction: {average_time} seconds")