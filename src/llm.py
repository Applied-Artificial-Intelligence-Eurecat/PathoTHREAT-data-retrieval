'''
===========================================
        Module: Open-source LLM Setup
===========================================
'''
from langchain_community.llms import LlamaCpp
from dotenv import find_dotenv, load_dotenv
import box
import yaml

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def build_llm():
    # Local Llamacpp model
    llm = LlamaCpp(
        model_path=cfg.MODEL_PATH,
        n_gpu_layers=cfg.GPU_LAYERS,
        temperature=cfg.TEMPERATURE,
        max_tokens=cfg.MAX_NEW_TOKENS,
        n_batch=1024,
        n_ctx=cfg.CONTEXT_LENGTH,
        verbose=False,
    )

    return llm
