from openai import OpenAI
import configs


def get_model(model_name):
    if model_name == "flash_agent":
        return FlashAgent()


class FlashAgent:
    def __init__(self) -> None:
        pass

    # Create the Respond Function
    def forward(self, content):
        """
        From Content to GPT Respond
        """
        client = OpenAI(api_key=configs.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}]
        )
        return response.choices[0].message.content

    def generate_flash_card(self, text, n_questions=5):
        """
        LLM is only used here

        Input: the actual text

        Output: a list of 10 questions each with the keys "Question", "True Answer", "Wrong Answer List", which has 3 wrong answers
        """
        past_question_list = []
        flash_card_list = []

        def get_flash_card_w_history(past_question_list):
            # print(past_question_list)
            text_input = f"""
            You are a Trivia Master

            Extract a question, its 1 true answer, and generate 3 wrong answers
            in the following format from the 'Text' below.

            Make sure the question is not in this list {past_question_list}

            Question:
            True Answer:
            Wrong Answer 1:
            Wrong Answer 2:
            Wrong Answer 3:


            Text
            ====
            {text}
            """
            output = self.forward(text_input)
            # print(text_input)
            flash_card_dict = parse_raw_text(output)
            return flash_card_dict

        for i in range(n_questions):
            flash_card_dict = get_flash_card_w_history(
                past_question_list=str(past_question_list)
            )

            past_question_list += [flash_card_dict["question"]]
            flash_card_list += [flash_card_dict]
            print(i)
            print(flash_card_dict)
            print("=============")

        return flash_card_list


import re


def parse_raw_text(raw_text):
    data = []

    # Split the raw text into lines
    lines = raw_text.split("\n")

    # Initialize variables to store question and answers
    question = None
    true_answer = None
    wrong_answers = []
    data = {}
    for line in lines:
        line = line.strip()
        # print(line)
        if line.startswith("Question:"):
            data["question"] = line.replace("Question:", "").strip()
        elif line.startswith("True Answer:"):
            data["true_answer"] = line.replace("True Answer:", "").strip()
        elif line.startswith("Wrong Answer 1:"):
            data["wrong_answer_1"] = line.replace("Wrong Answer 1:", "").strip()
        elif line.startswith("Wrong Answer 2:"):
            data["wrong_answer_2"] = line.replace("Wrong Answer 2:", "").strip()
        elif line.startswith("Wrong Answer 3:"):
            data["wrong_answer_3"] = line.replace("Wrong Answer:", "").strip()

    return data


# Get the Flash Cards


# Loop over the Flash cards and pompt the user to choose the answers as 1, 2, 3, or 4
def prompt_user(flash_card_list):
    for f in flash_card_list:
        pass
    # prompt user with the question

    # ask the user to input the answer

    # show the user the score and display the right answer

    return total_score, pred_answers, gt_answers
