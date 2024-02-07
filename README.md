# olaf-llm-eswc2024

LLM experiments for ontology learning with OLAF for ESWC 2024

# Data

The text used to learn the ontology is created based on the Pizza Ontology labels. 

The labels are extracted and group together in the _data/pizza_onto_labels.txt_ file. 

A prompt is constructed to ask GPT-4 to create a text based on these labels. 

The script used is ``data/pizza_script.py`` and can be run with the following command:

```bash
python3 data/pizza_script.py
```

The text obtained is stored in the _data/pizza_description.txt_ file.