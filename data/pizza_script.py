from dotenv import load_dotenv
import os

import openai

load_dotenv()


def pizza_prompt(pizza_labels: list[str]) -> list[dict[str, str]]:
    """OpenAI ChatCompletion prompt for pizza description creation.

    Parameters
    ----------
    pizza_labels: list[str]
        List of terms to add as context in the prompt.

    Returns
    -------
    list[dict[str, str]]
        Prompt with the context in the OpenAI ChatCompletion format.
    """
    prompt = [
        {
            "role": "system",
            "content": "You are an helpful assistant expert in pizza. "
        },
        {
            "role": "user",
            "content": "Write a text describing pizzas. The text must define a pizza, pizza kinds and well known pizzas with its ingredients. It must contains all the terms given."
        },
        {
            "role": "user",
            "content": "Terms:\n" + "\n".join(pizza_labels)
        }
    ]
    return prompt


def main() -> None:
    """Create pizza textual description from pizza ontology labels with GPT-4."""

    with open('data/pizza_onto_labels.txt', 'r', encoding="utf-8") as file:
        pizza_labels = file.readlines()
        
    pizza_labels = [label.rstrip("\n") for label in pizza_labels]

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
                model="gpt-4",
                temperature=0,
                messages=pizza_prompt(pizza_labels),
            )
    llm_output = response.choices[0].message.content

    text_file = open("data/pizza_description.txt", "w", encoding="utf-8")
    text_file.write(llm_output)
    text_file.close()


if __name__ == "__main__":
    main()
