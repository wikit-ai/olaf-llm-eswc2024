import os

import spacy

from olaf import Pipeline
from olaf.data_container import CandidateTerm
from olaf.commons.spacy_processing_tools import is_not_punct, is_not_stopword
from olaf.pipeline.pipeline_component.candidate_term_enrichment import KnowledgeBasedCTermEnrichment
from olaf.pipeline.pipeline_component.concept_relation_extraction import(
    AgglomerativeClusteringConceptExtraction,
    AgglomerativeClusteringRelationExtraction
)
from olaf.pipeline.pipeline_component.concept_relation_hierarchy import SubsumptionHierarchisation
from olaf.pipeline.pipeline_component.term_extraction import (
    POSTermExtraction,
    TFIDFTermExtraction
)
from olaf.repository.corpus_loader import TextCorpusLoader
from olaf.repository.knowledge_source import WordNetKnowledgeResource


def create_pipeline() -> Pipeline:
    spacy_model = spacy.load("en_core_web_lg")
    corpus_loader = TextCorpusLoader(
        corpus_path=f"{os.getenv('DATA_PATH')}/pizza_description.txt"
    )
    pipeline = Pipeline(
        spacy_model=spacy_model,
        corpus_loader=corpus_loader
    )
    return pipeline


def cts_post_processing(cts: set[CandidateTerm]) -> set[CandidateTerm]:
    existing_cts = []
    new_cts = set()
    for ct in cts:
        keep = True
        if len(ct.corpus_occurrences) > 0:
            for co in ct.corpus_occurrences:
                for token in co:
                    if (not (is_not_punct(token)) or not (is_not_stopword(token)) or (token.pos_ == "VERB")):
                        keep = False
                        break
        else:
            keep = False
        if keep and ct.label not in existing_cts:
            new_cts.add(ct)
            existing_cts.append(ct.label)
    return new_cts


def add_pipeline_components(pipeline: Pipeline) -> Pipeline:

    tfidf_option = {"max_term_token_length": 3, "threshold": 0.05}
    tfidf_term_extraction = TFIDFTermExtraction(
        cts_post_processing_functions=[cts_post_processing],
        options=tfidf_option
    )
    pipeline.add_pipeline_component(tfidf_term_extraction)

    params = {
        "use_domains": True,
        "wordnet_domains_path": "wordnet_domains.txt",
        "enrichment_domains": set(["gastronomy"])
    }
    wn_kr = WordNetKnowledgeResource(params)
    wn_term_enrichment = KnowledgeBasedCTermEnrichment(wn_kr)
    pipeline.add_pipeline_component(wn_term_enrichment)

    ac_param = {"embedding_model": "sentence-transformers/sentence-t5-base"}
    ac_options = {"distance_threshold": 0.1}
    ac_concept_extraction = AgglomerativeClusteringConceptExtraction(
        parameters=ac_param, options=ac_options)
    pipeline.add_pipeline_component(ac_concept_extraction)

    sub_options = {"threshold": 0.99}
    sub_hierarchisation = SubsumptionHierarchisation(options=sub_options)

    pipeline.add_pipeline_component(sub_hierarchisation)

    param = {"pos_selection": ["VERB"]}
    pos_term_extraction = POSTermExtraction(parameters=param)
    pipeline.add_pipeline_component(pos_term_extraction)

    pipeline.add_pipeline_component(wn_term_enrichment)

    ac_relation_extraction = AgglomerativeClusteringRelationExtraction(
        parameters=ac_param, options=ac_options)
    pipeline.add_pipeline_component(ac_relation_extraction)

    return pipeline


def main() -> Pipeline:
    pipeline = create_pipeline()
    pipeline = add_pipeline_components(pipeline)
    pipeline.run()
    print(f"Nb concepts: {len(pipeline.kr.concepts)}")
    print(f"Nb relations: {len(pipeline.kr.relations)}")
    print(f"Nb metarelations: {len(pipeline.kr.metarelations)}")


if __name__ == "__main__":
    main()
