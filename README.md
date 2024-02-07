# olaf-llm-eswc2024

LLM experiments for ontology learning with OLAF for ESWC 2024.

# Installation

```bash
git clone https://github.com/wikit-ai/olaf-llm-eswc2024
cd olaf-llm-eswc2024
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

``OPENAI_API_KEY`` must be defined in a ``.env`` file.

# Data

The text used to learn the ontology is created based on the Pizza Ontology labels ([Pizza Ontology tutorial](https://github.com/owlcs/pizza-ontology/tree/master)). 

The labels are extracted and grouped together in the ``data/pizza_onto_labels.txt`` file. 

A prompt is constructed to ask GPT-4 to create a text based on these labels. 

The script used is ``scripts/pizza_description_creation.py`` and can be ran with the following command:

```bash
python scripts/pizza_description_creation.py
```

The text obtained is stored in the ``data/pizza_description.txt`` file.

# Scripts

## LLM : text to OWL

Script to create an OWL ontology based on the pizza textual description with an LLM.

```bash
python scripts/llm_text_to_owl.py
```