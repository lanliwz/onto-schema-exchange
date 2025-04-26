from rdflib.namespace import (RDFS,
                              RDF,
                              OWL,
                              SKOS,
                              DC)
from pydantic import BaseModel
from typing import List, Optional
TITLE_ANNOTATIONS = {
    RDFS.label,
    SKOS.prefLabel,
    SKOS.altLabel,
    DC.title,
}

CREATION_ANNOTATIONS = {
    RDFS.isDefinedBy,
    OWL.versionInfo,
    OWL.priorVersion,
    OWL.deprecated,
    DC.creator,
    DC.contributor,

}

EXPLANATION_ANNOTATIONS = {
    RDFS.comment,
    RDFS.seeAlso,
    SKOS.definition,
    SKOS.example,
    SKOS.note,
    SKOS.notation,
    SKOS.scopeNote,
    # part of a broader metadata standard often used in digital libraries and archives.
    DC.description,
}


