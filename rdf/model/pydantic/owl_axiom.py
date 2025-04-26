from rdflib.namespace import (RDF,
                              RDFS,
                              OWL,
                              SKOS,
                              DC)

CLASS_AXIOMS = {
    RDFS.subClassOf,
    OWL.equivalentClass,
    OWL.disjointWith,
    OWL.disjointUnionOf,
    # Complex Axioms
    OWL.intersectionOf,
    OWL.unionOf,
    OWL.oneOf,
    OWL.Restriction

}
PROPERTY_AXIOMS = {
    OWL.FunctionalProperty,
    OWL.TransitiveProperty,
    OWL.SymmetricProperty,
    OWL.AsymmetricProperty,
    OWL.TransitiveProperty
}

INDIVIDUAL_AXIOMS = {
    OWL.NamedIndividual,
}

