import os
import configs

import argparse
import json
import random

import gradio as gr
import numpy as np
import utils as ut


def main(model_name, txt_path, reset=False):
    # print
    print("model_name:", model_name)
    print("txt_path:", txt_path)

    # vaiable
    path = "data/flash_cards.json"

    # crreate path
    if not os.path.exists("data"):
        os.mkdir("data")

    # read file
    with open(txt_path, "r") as f:
        text = f.read()

    # get model
    model = ut.get_model(model_name)

    if reset or not os.path.exists(path):
        # get flash card list
        flash_card_list = model.generate_flash_card(text, n_questions=5)
        # save flash cards as json
        with open("data/flash_cards.json", "w") as f:
            json.dump(flash_card_list, f)
    else:
        flash_card_list = json.load(open(path, "r"))

    # Gradio

    # Clean up the flash card list by rremoving anything preceding ':'
    for i in range(len(flash_card_list)):
        for key in flash_card_list[i].keys():
            if ":" in flash_card_list[i][key]:
                flash_card_list[i][key] = flash_card_list[i][key].split(":")[1].strip()

    index = 0
    answer_keys = ["true_answer", "wrong_answer_1", "wrong_answer_2", "wrong_answer_3"]
    # random permutations of size 4
    indices = np.random.permutation(4)

    answer_list = np.array([flash_card_list[index][a] for a in answer_keys])
    answer_id = np.where(indices == 0)[0][0]
    # randomly shuffle answer_list and return
    answer_list = list(answer_list[indices])

    def greet(name):
        if name == answer_list[answer_id]:
            return gr.update(value="Correct", visible=True)
        else:
            return gr.update(value="Wrong", visible=True)

    question = flash_card_list[index]["question"]
    with gr.Blocks() as demo:
        radio = gr.Radio(answer_list, value=answer_list[0], label=question)
        label = gr.Label(visible=False)
        greet_btn = gr.Button("Greet")
        greet_btn.click(fn=greet, inputs=radio, outputs=label, api_name="Submit")

    demo.launch()
    print("Experiment Completed")


# Entry point with parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--model", type=str, default="flash_agent", help="model name")
    parser.add_argument(
        "--txt_path",
        type=str,
        default="santa_wiki.txt",
        help="content to send to the model",
    )

    args = parser.parse_args()
    main(args.model, args.txt_path)
