# Generating Flash Cards from Text

## Quick Start

1. Create `configs.py` with the variable `OPENAI_API_KEY = 'key here'` where you would instantiate your key (Note that this file will not be pushed to the repo and is private)

2. Run `python main.py --text_path santa_wiki.txt --model_name flash_agent`

## Goal

Running `python main.py` should prompt the user with flash card multiple choice quiz for a given text