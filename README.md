# Can Large Language Models Follow Concept Annotation Guidelines?

Resources for the paper [Can Large Language Models Follow Concept Annotation Guidelines? A Case Study on Scientific and Financial Domains](https://aclanthology.org/2024.findings-acl.478/)

## Requirements

It is recommended to setup a Python 3.12 environment. Using [Miniconda](https://docs.anaconda.com/miniconda/), the environment is created as follows:
```
conda create -n concept-guidelines python=3.12
```

Then, activate the environment, clone this repository, and install the dependencies:
```
conda activate concept-guidelines
git clone https://github.com/thefonseca/concept-guidelines.git
cd concept-guidelines
pip install -r requirements.txt
```

## Classification with guidelines

The classification experiments (Figure 2 in the paper) use the following command for open-source LLMs (e.g., Llama-7B):
```sh
# Open-source LLMs
# Model names: llama-7b-chat, llama-13b-chat, llama-70b-chat, tiiuae/falcon-180B-chat
# For llama-70b-chat, use two A100 80G GPUs
# For tiiuae/falcon-180B-chat, use 4 A100 80G GPUs

python run_guidelines.py \
--model_name llama-2-7b-chat \
--model_checkpoint_path /path/to/llama-7b-chat/ \
--model_dtype float16
```

And for OpenAI LLMs:
```sh
# Model names: gpt-3.5-turbo-0613, gpt-4-0613
# (gpt-3.5-turbo-0613 is now deprecated)
# Please set the OPENAI_API_KEY environment variable accordingly

python run_guidelines.py \
--model_name gpt-4-0613 \
--ignore_errors \
--model_request_interval 3
```

## Guideline factuality level

To evaluate guidelines with different levels of factuality (Figure 3 in the paper), use the following command for open-source LLMs:

```sh
python run_factuality_level.py \
--model_name llama-2-7b-chat \
--model_checkpoint_path /path/to/llama-7b-chat/ \
--model_dtype float16
```

And for OpenAI LLMs:

```sh
python run_factuality_level.py \
--model_name gpt-4-0613 \
--ignore_errors \
--model_request_interval 3
```

## Adherence to guidelines

To generate the guideline adherence plots shown in Figure 4:
```sh
python run_guideline_adherence.py
```

## Citation
```
@inproceedings{fonseca-cohen-2024-large,
    title = "Can Large Language Models Follow Concept Annotation Guidelines? A Case Study on Scientific and Financial Domains",
    author = "Fonseca, Marcio  and
      Cohen, Shay",
    editor = "Ku, Lun-Wei  and
      Martins, Andre  and
      Srikumar, Vivek",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2024",
    month = aug,
    year = "2024",
    address = "Bangkok, Thailand",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-acl.478",
    doi = "10.18653/v1/2024.findings-acl.478",
    pages = "8027--8042",
    abstract = "Although large language models (LLMs) exhibit remarkable capacity to leverage in-context demonstrations, it is still unclear to what extent they can learn new facts or concept definitions via prompts. To address this question, we examine the capacity of instruction-tuned LLMs to follow in-context concept annotation guidelines for zero-shot sentence labeling tasks. We design guidelines that present different types of factual and counterfactual concept definitions, which are used as prompts for zero-shot sentence classification tasks. Our results show that although concept definitions consistently help in task performance, only the larger models (with 70B parameters or more) have limited ability to work under counterfactual contexts. Importantly, only proprietary models such as GPT-3.5 can recognize nonsensical guidelines, which we hypothesize is due to more sophisticated alignment methods. Finally, we find that Falcon-180B-chat is outperformed by Llama-2-70B-chat is most cases, which indicates that increasing model scale does not guarantee better adherence to guidelines. Altogether, our simple evaluation method reveals significant gaps in concept understanding between the most capable open-source language models and the leading proprietary APIs.",
}
```