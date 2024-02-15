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

Running the different scripts requires the followwing environment variables you can set in a `.env` file:

```Bash
OPENAI_API_KEY=you-openai-ai-key
DATA_PATH=/path/to/your/local/data/folder/
RESULTS_PATH=/path/to/your/local/results/folder/
JAVA_EXE=/path/to/your/local/java/folder/java.exe
ROBOT_JAR=C:/path/to/your/local/obo/robot/cli/tool/folder/robot.jar
```

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

Results are stored in `results/llm_text_to_owl/llm_owl_pizza_onto_eswc2024.ttl`

## LLM pipeline

Script to create an OWL ontology based on the pizza textual description with a pipeline made up with LLM components.

```bash
python scripts/llm_pipeline.py
```
Results are stored in `results/llm_pipeline/llm_pipeline_kr_rgf_graph_eswc2024.ttl` and `results/llm_pipeline/llm_pipeline_kr_eswc2024.json`.

## No LLM pipeline 

Script to create an OWL ontology based on the pizza textual description with a pipeline made up without LLM components.

```bash
python scripts/no_llm_pipeline.py
```

Results are stored in `results/no_llm_pipeline/no_llm_pipeline_kr_rgf_graph_eswc2024.ttl` and `results/no_llm_pipeline/no_llm_pipeline_kr_eswc2024.json`.

## Pipeline components

The `scripts/pipeline_components_analysis.ipynb` notebook compare available techniques in OLAF for each ontology learning pipeline component.

Results are stored in `results/pipeline_components`.

# Results

All results are stored in the folder corresponding to the ontology learning technique used. 

Results analysis are available in the `results/results_analysis.ipynb` notebook.

The folder `results/pipeline_components` contains materials to discuss the performances of pipeline components.
