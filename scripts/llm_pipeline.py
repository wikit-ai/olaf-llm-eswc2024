import os

import openai
import spacy

from olaf import Pipeline
from olaf.commons.errors import MissingEnvironmentVariable
from olaf.commons.llm_tools import LLMGenerator
from olaf.commons.logging_config import logger
from olaf.commons.prompts import (
    openai_prompt_concept_term_extraction, 
    openai_prompt_concept_extraction,
    openai_prompt_hierarchisation,
    openai_prompt_owl_axiom_extraction,
    openai_prompt_relation_extraction,
    openai_prompt_relation_term_extraction,
    openai_prompt_term_enrichment
)
from olaf.pipeline.pipeline_component.axiom_extraction import LLMBasedOWLAxiomExtraction
from olaf.pipeline.pipeline_component.candidate_term_enrichment import LLMBasedTermEnrichment
from olaf.pipeline.pipeline_component.concept_relation_extraction import(
    LLMBasedConceptExtraction,
    LLMBasedRelationExtraction
)
from olaf.pipeline.pipeline_component.concept_relation_hierarchy import LLMBasedHierarchisation
from olaf.pipeline.pipeline_component.term_extraction import LLMTermExtraction
from olaf.repository.corpus_loader import TextCorpusLoader
from olaf.repository.serialiser import KRJSONSerialiser


class CustomLLMGenerator(LLMGenerator):
    """Text generator based on the new version of OpenAI gpt-3.5-turbo model."""

    def check_resources(self) -> None:
        """Check that the resources needed to use the custom generator are available."""
        if "OPENAI_API_KEY" not in os.environ:
            raise MissingEnvironmentVariable(self.__class__, "OPENAI_API_KEY")

    def generate_text(self, prompt: list[dict[str, str]]) -> str:
        """Generate text based on a chat completion prompt for the OpenAI gtp-3.5-turbo-0125 model.

        Parameters
        ----------
        prompt: list[dict[str, str]]
            The prompt to use for text generation.

        Returns
        -------
        str
            The output generated by the LLM.
        """
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        llm_output = ""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                temperature=0,
                max_tokens=10000,
                messages=prompt,
            )
            llm_output = response.choices[0].message.content
        except Exception as e:
            logger.error(
                """Exception %s still occurred after retries on OpenAI API.
                         Skipping document %s...""",
                e,
                prompt[-1]["content"][5:100],
            )
        return llm_output


def create_pipeline() -> Pipeline:
    """Initialise a pipeline.

    Returns
    -------
    Pipeline
        The new pipeline created.
    """
    spacy_model = spacy.load("en_core_web_lg")
    corpus_loader = TextCorpusLoader(
        corpus_path=f"{os.getenv('DATA_PATH')}/pizza_description.txt"
    )
    pipeline = Pipeline(
        spacy_model=spacy_model,
        corpus_loader=corpus_loader
    )
    return pipeline


def add_pipeline_components(pipeline: Pipeline) -> Pipeline:
    """Create pipeline with LLM components.

    Parameters
    ----------
    pipeline: Pipeline
        The pipeline into which the components are to be added. 

    Returns
    -------
    Pipeline
        The pipeline updated with new components.
    """

    openai_generator = CustomLLMGenerator()
    llm_cterm_extraction = LLMTermExtraction(
        prompt_template=openai_prompt_concept_term_extraction,
        llm_generator=openai_generator
    )
    pipeline.add_pipeline_component(llm_cterm_extraction)

    llm_cterm_enrichment = LLMBasedTermEnrichment(
        openai_prompt_term_enrichment, openai_generator)
    pipeline.add_pipeline_component(llm_cterm_enrichment)

    llm_concept_extraction = LLMBasedConceptExtraction(
        openai_prompt_concept_extraction, openai_generator)
    pipeline.add_pipeline_component(llm_concept_extraction)

    llm_hierarchisation = LLMBasedHierarchisation(
        openai_prompt_hierarchisation, openai_generator)
    pipeline.add_pipeline_component(llm_hierarchisation)

    llm_rterm_extraction = LLMTermExtraction(
        prompt_template=openai_prompt_relation_term_extraction,
        llm_generator=openai_generator
    )
    pipeline.add_pipeline_component(llm_rterm_extraction)

    llm_rterm_enrichment = LLMBasedTermEnrichment(
        openai_prompt_term_enrichment, openai_generator)
    pipeline.add_pipeline_component(llm_rterm_enrichment)

    llm_relation_extraction = LLMBasedRelationExtraction(
        openai_prompt_relation_extraction, openai_generator)
    pipeline.add_pipeline_component(llm_relation_extraction)

    llm_axiom_extraction = LLMBasedOWLAxiomExtraction(
        openai_prompt_owl_axiom_extraction,
        openai_generator,
        namespace="https://github.com/wikit-ai/olaf-llm-eswc2024/o/example#"
    )
    pipeline.add_pipeline_component(llm_axiom_extraction)

    return pipeline


def main() -> None:
    """LLM pipeline execution."""
    pipeline = create_pipeline()
    pipeline = add_pipeline_components(pipeline)
    pipeline.run()

    kr_serialiser = KRJSONSerialiser()
    kr_serialisation_path = os.path.join(
        os.getenv("RESULTS_PATH"), "llm_pipeline", "llm_pipeline_kr.json")
    kr_serialiser.serialise(kr=pipeline.kr, file_path=kr_serialisation_path)

    kr_rdf_graph_path = os.path.join(
        os.getenv("RESULTS_PATH"), "llm_pipeline", "llm_pipeline_kr_rdf_graph.ttl")
    pipeline.kr.rdf_graph.serialize(kr_rdf_graph_path, format="ttl")

    print(f"Nb concepts: {len(pipeline.kr.concepts)}")
    print(f"Nb relations: {len(pipeline.kr.relations)}")
    print(f"Nb metarelations: {len(pipeline.kr.metarelations)}")
    print(f"The KR object has been JSON serialised in : {kr_serialisation_path}")
    print(f"The KR RDF graph has been serialised in : {kr_rdf_graph_path}")


if __name__ == "__main__":
    main()
