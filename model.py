from huggingface_hub import InferenceApi
import time
import os

TOKEN = os.environ.get("HF_TOKEN")
inference = InferenceApi("bigscience/bloom",token=TOKEN)

def infer(prompt,
          max_length = 32,
          top_k = 0,
          num_beams = 0,
          no_repeat_ngram_size = 2,
          top_p = 0.9,
          seed=42,
          temperature=0.7,
          greedy_decoding = False,
          return_full_text = False):
    

    top_k = None if top_k == 0 else top_k
    do_sample = False if num_beams > 0 else not greedy_decoding
    num_beams = None if (greedy_decoding or num_beams == 0) else num_beams
    no_repeat_ngram_size = None if num_beams is None else no_repeat_ngram_size
    top_p = None if num_beams else top_p
    early_stopping = None if num_beams is None else num_beams > 0

    params = {
        "max_new_tokens": max_length,
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "do_sample": do_sample,
        "seed": seed,
        "early_stopping":early_stopping,
        "no_repeat_ngram_size":no_repeat_ngram_size,
        "num_beams":num_beams,
        "return_full_text":return_full_text
    }
    
    s = time.time()
    response = inference(prompt, params=params)

    proc_time = time.time()-s
    print(f"Processing time was {proc_time} seconds")

    return response[0]['generated_text']

# prompt = "Bon dia al matí!"

# print("Generating output...")
# generated_text = infer(prompt, max_length=64)

# print("Output:")
# print(generated_text.replace(prompt, ""))