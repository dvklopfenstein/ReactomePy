"""Reactome Graph Database Data Schema."""
# https://reactome.org/content/schema/

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

ITEM2CHILDREN = {
    'DatabaseObject':set([
        'AbstractModifiedResidue',
        'Affiliation',
        'CatalystActivity',
        'ControlReference',
        'DatabaseIdentifier',
        'EntityFunctionalStatus',
        'Event',
        'EvidenceType',
        'ExternalOntology',
        'Figure',
        'FunctionalStatus',
        'FunctionalStatusType',
        'GO_Term',
        'InstanceEdit',
        'Interaction',
        'Person',
        'PhysicalEntity',
        'Publication',
        'ReferenceDatabase',
        'ReferenceEntity',
        'Regulation',
        'Summation',
        'Taxon',
    ]),

    'AbstractModifiedResidue':set([
        'GeneticallyModifiedResidue',
        'TranslationalModification',
    ]),

    'ControlReference':set([
        'CatalystActivityReference',
        'RegulationReference'
    ]),

    'GeneticallyModifiedResidue':set([
        'FragmentModification',
        'ReplacedResidue',
    ]),

    'FragmentModification':set([
        'FragmentDeletionModification',
        'FragmentInsertionModification',
        'FragmentReplacedModification',
    ]),

    'TranslationalModification':set([
        'CrosslinkedResidue',
        'GroupModifiedResidue',
        'ModifiedResidue',
    ]),

    'CrosslinkedResidue':set([
        'InterChainCrosslinkedResidue',
        'IntraChainCrosslinkedResidue',
    ]),

    'Event':set([
        'Pathway',
        'TopLevelPathway',  # DVK
        'ReactionLikeEvent',
    ]),

    # 'Pathway':set(['TopLevelPathway']),  # DVK

    'ReactionLikeEvent':set([
        'BlackBoxEvent',
        'Depolymerisation',
        'FailedReaction',
        'Polymerisation',
        'Reaction',
    ]),

    'ExternalOntology':set([
        'Disease',
        'PsiMod',
        'SequenceOntology',
    ]),

    'GO_Term':set([
        'GO_BiologicalProcess',
        'GO_CellularComponent',
        'GO_MolecularFunction',
    ]),

    'GO_CellularComponent':set(['Compartment']),
    'Interaction':set(['UndirectedInteraction']),

    'PhysicalEntity':set([
        'Complex',
        'Drug',
        'EntitySet',
        'GenomeEncodedEntity',
        'OtherEntity',
        'Polymer',
        'SimpleEntity',
    ]),

    'Drug':set([
        'ChemicalDrug',
        'ProteinDrug',
    ]),

    'EntitySet':set([
        'CandidateSet',
        'DefinedSet',
    ]),

    'Publication':set([
        'Book',
        'LiteratureReference',
        'URL',
    ]),

    'GenomeEncodedEntity':set(['EntityWithAccessionedSequence']),

    'ReferenceEntity':set([
        'ReferenceGroup',
        'ReferenceMolecule',
        'ReferenceSequence',
        'ReferenceTherapeutic',
    ]),

    'ReferenceSequence':set([
        'ReferenceDNASequence',
        'ReferenceGeneProduct',
        'ReferenceRNASequence',
    ]),

    'ReferenceGeneProduct':set(['ReferenceIsoform']),

    'Regulation':set([
        'NegativeRegulation',
        'PositiveRegulation',
    ]),

    'NegativeRegulation':set(['NegativeGeneExpressionRegulation']),

    'PositiveRegulation':set([
        'PositiveGeneExpressionRegulation',
        'Requirement',
    ]),

    'Taxon':set(['Species']),
}

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
