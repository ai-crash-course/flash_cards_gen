import os
import configs
import argparse

import utils as ut

os.environ["OPENAI_API_KEY"] = configs.OPENAI_API_KEY


def main(model_name, txt_path):
    # print
    print("model_name:", model_name)
    print("txt_path:", txt_path)

    # read file
    with open(txt_path, "r") as f:
        text = f.read()

    # get model
    model = ut.get_model(model_name)

    # get flash card list
    flash_card_list = model.generate_flash_card(text)

    print("Experiment Completed")

    


# Entry point with parser
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--model', type=str, default="flash_agent",
                        help='model name')
    parser.add_argument('--txt_path', type=str, default="santa_wiki.txt",
                        help='content to send to the model')
    
    args = parser.parse_args()
    main(args.model, args.txt_path)

