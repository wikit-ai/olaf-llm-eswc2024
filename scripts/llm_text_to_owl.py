from dotenv import load_dotenv
import os

import openai

load_dotenv()


def text_to_llm_prompt(pizza_description: str) -> list[dict[str, str]]:
    """OpenAI ChatCompletion prompt for creating an OWL ontology based on the pizza description.

    Parameters
    ----------
    pizza_description: str
        Text describing the pizza ontology used as context in the prompt.

    Returns
    -------
    list[dict[str, str]]
        Prompt with the context in the OpenAI ChatCompletion format.
    """
    prompt = [
        {
            "role": "system",
            "content": "You are a helpful assistant in building an ontology. You are fluent in the W3C Semantic Web stack and in the RDF, RDFS, and OWL languages."
        },
        {
            "role": "user",
            "content": "Use the given text to construct an OWL ontology in the Turtle format. Use this namespace: https://github.com/wikit-ai/olaf-llm-eswc2024/o/example#. Return only the turtle file."
        },
        {
            "role": "user",
            "content": f"Text:\n{pizza_description}"
        }
    ]
    return prompt


def main() -> None:
    """Create OWL ontology from pizza textual description with OpenAI GPT-3.5 turbo 16k model."""

    text_file = open("data/pizza_description.txt", "r")
    pizza_description = text_file.read()
    text_file.close()

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                temperature=0,
                max_tokens=13300,
                messages=text_to_llm_prompt(pizza_description),
            )
    llm_output = response.choices[0].message.content

    text_file = open("results/llm_text_to_owl/llm_owl_pizza_onto.ttl", "w", encoding="utf-8")
    text_file.write(llm_output)
    text_file.close()


if __name__ == "__main__":
    main()
