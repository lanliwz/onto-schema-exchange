from rdflib import Graph
from model.pydantic.owl_annotation import TITLE_ANNOTATIONS,EXPLANATION_ANNOTATIONS, CREATION_ANNOTATIONS
from model.pydantic.owl_axiom import CLASS_AXIOMS, PROPERTY_AXIOMS

# load ontology
def loadOntology(g: Graph, ontofile: str, format: str = "xml"):
    g.parse(ontofile, format=format)

