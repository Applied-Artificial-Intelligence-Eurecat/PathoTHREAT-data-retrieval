Code developed under the H2020 PathoCERT project: https://pathocert.eu/

# Getting started

```
pip install requirements.txt

Download models with format gguf.

Adapt configuration file params to your own path and model name. 
Example:
MODEL: 'mistral-7b-instruct-v0.2.Q8_0'
MODEL_PATH: 'models/mistral-7b-instruct-v0.2.Q8_0.gguf'


For full files reading
python main.py

or

For individual reading
python main.py "context"
```

Models used and download links:
- Llama 2 7b Q8 and Q4 chat: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main
- gemma 2b it: https://huggingface.co/google/gemma-2b-it/tree/main
- gemma 7b it Q8: https://huggingface.co/mlabonne/gemma-7b-it-GGUF/tree/main
- Mistral 7b it Q8: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/tree/main

