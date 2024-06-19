from ray import serve
from ray.serve.handle import DeploymentHandle
import torch
from transformers import AutoTokenizer, pipeline
from starlette.requests import Request
from fastapi import FastAPI

app = FastAPI()

@serve.deployment(num_replicas=4, ray_actor_options={"num_cpus": 1, "num_gpus": 0.25})
@serve.ingress(app)
class commonFactorClassification:
    def __init__(self, model_id: str = "openai-community/gpt2"): # "openai-community/gpt2" "TinyLlama/TinyLlama-1.1B-Chat-v1.0" "meta-llama/Llama-2-7b-hf"
        self.model_id = model_id
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu' # Assume running on GPU
        print("Device: ", self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
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

    @app.post("/common_factors_classification")
    async def classify(self, http_request: Request) -> str:
        input_request: str = await http_request.json()
        #self.logger.info(input_request)
        input_text = input_request["input_text"]
        full_prompt = self.user_prompt.format(input=input_text)
        messages = [{"role": "system", "content": self.sys_prompt}, {"role": "user", "content": full_prompt}]
        #self.logger.info(messages)
        tokenized_chat = self.tokenizer.apply_chat_template(messages, tokenize=False)
        output = self.pipe(tokenized_chat, max_new_tokens=100, do_sample=True)
        return output[0]['generated_text']
    

common_factors_model = commonFactorClassification.bind()

# Start the Ray Serve instance
serve.start(http_options={"http_port": 8000})

# Deploy the model
handle = serve.run(common_factors_model)

# wait for ctrl-c

import time
try:
    print("Server is running. Press Ctrl-C to stop.")
    while True:
        # The sleep is not necessary but prevents this loop from consuming too much CPU
        time.sleep(1)
except KeyboardInterrupt:
    print("Server stopping...")
    serve.shutdown()
    print("Server stopped.")