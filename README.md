# olaf-llm-eswc2024

LLM experiments for ontology learning with OLAF for ESWC 2024

# Installation

```bash
git clone https://github.com/wikit-ai/olaf-llm-eswc2024
cd olaf-llm-eswc2024
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

# Data

The text used to learn the ontology is created based on the Pizza Ontology labels. 

The labels are extracted and group together in the ``data/pizza_onto_labels.txt`` file. 

A prompt is constructed to ask GPT-4 to create a text based on these labels. 

The script used is ``scripts/pizza_description_creation.py`` and can be run with the following command:

```bash
python3 scripts/pizza_description_creation.py
```

The text obtained is stored in the ``data/pizza_description.txt`` file.