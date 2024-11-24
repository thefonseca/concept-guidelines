#!/bin/bash

# Open-source LLMs
# Model names: llama-7b-chat, llama-13b-chat, llama-70b-chat, tiiuae/falcon-180B-chat
# For llama-70b-chat, use two A100 80G GPUs
# For tiiuae/falcon-180B-chat, use 4 A100 80G GPUs

python run_guidelines.py \
--model_name llama-2-7b-chat \
--model_checkpoint_path /path/to/llama2-7b-chat/ \
--model_dtype float16

# OpenAI LLMs
# Model names: gpt-3.5-turbo-0613, gpt-4-0613
# (gpt-3.5-turbo-0613 is now deprecated)

python run_guidelines.py \
--domain financial \
--model_name gpt-4-0613 \
--ignore_errors \
--model_request_interval 3