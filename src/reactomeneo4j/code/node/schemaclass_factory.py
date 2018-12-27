"""Given a schemaClass string, return the associated class instance."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# pylint: disable=line-too-long
from collections import OrderedDict
from reactomeneo4j.code.node.databaseobject import DatabaseObject
from reactomeneo4j.code.node.instanceedit import InstanceEdit
from reactomeneo4j.code.node.physicalentity import PhysicalEntity
from reactomeneo4j.code.node.entityset import EntitySet
from reactomeneo4j.code.node.candidateset import CandidateSet
from reactomeneo4j.code.node.definedset import DefinedSet
from reactomeneo4j.code.node.openset import OpenSet
from reactomeneo4j.code.node.drug import Drug
from reactomeneo4j.code.node.chemicaldrug import ChemicalDrug
from reactomeneo4j.code.node.genomeencodedentity import GenomeEncodedEntity
from reactomeneo4j.code.node.entitywithaccessionedsequence import EntityWithAccessionedSequence
from reactomeneo4j.code.node.complex import Complex
from reactomeneo4j.code.node.otherentity import OtherEntity
from reactomeneo4j.code.node.polymer import Polymer
from reactomeneo4j.code.node.simpleentity import SimpleEntity
from reactomeneo4j.code.node.event import Event
from reactomeneo4j.code.node.depolymerisation import Depolymerisation
from reactomeneo4j.code.node.polymerisation import Polymerisation
from reactomeneo4j.code.node.blackboxevent import BlackBoxEvent
from reactomeneo4j.code.node.reaction import Reaction
from reactomeneo4j.code.node.failedreaction import FailedReaction
from reactomeneo4j.code.node.pathway import Pathway
from reactomeneo4j.code.node.toplevelpathway import TopLevelPathway
from reactomeneo4j.code.node.positiveregulation import PositiveRegulation
from reactomeneo4j.code.node.positivegeneexpressionregulation import PositiveGeneExpressionRegulation
from reactomeneo4j.code.node.requirement import Requirement
from reactomeneo4j.code.node.negativeregulation import NegativeRegulation
from reactomeneo4j.code.node.negativegeneexpressionregulation import NegativeGeneExpressionRegulation
from reactomeneo4j.code.node.referenceentity import ReferenceEntity
from reactomeneo4j.code.node.referencesequence import ReferenceSequence
from reactomeneo4j.code.node.referencegeneproduct import ReferenceGeneProduct
from reactomeneo4j.code.node.referenceisoform import ReferenceIsoform
from reactomeneo4j.code.node.referencednasequence import ReferenceDNASequence
# from reactomeneo4j.code.node.referencernasequence import ReferenceRNASequence
from reactomeneo4j.code.node.referencegroup import ReferenceGroup
from reactomeneo4j.code.node.referencemolecule import ReferenceMolecule
from reactomeneo4j.code.node.referencetherapeutic import ReferenceTherapeutic
from reactomeneo4j.code.node.referencedatabase import ReferenceDatabase
from reactomeneo4j.code.node.catalystactivity import CatalystActivity
from reactomeneo4j.code.node.entityfunctionalstatus import EntityFunctionalStatus
from reactomeneo4j.code.node.literaturereference import LiteratureReference
from reactomeneo4j.code.node.book import Book
from reactomeneo4j.code.node.url import URL
from reactomeneo4j.code.node.compartment import Compartment
from reactomeneo4j.code.node.go_cellularcomponent import GO_CellularComponent
from reactomeneo4j.code.node.go_biologicalprocess import GO_BiologicalProcess
from reactomeneo4j.code.node.go_molecularfunction import GO_MolecularFunction
from reactomeneo4j.code.node.externalontology import ExternalOntology
from reactomeneo4j.code.node.abstractmodifiedresidue import AbstractModifiedResidue
from reactomeneo4j.code.node.fragmentdeletionmodification import FragmentDeletionModification
from reactomeneo4j.code.node.fragmentinsertionmodification import FragmentInsertionModification
from reactomeneo4j.code.node.fragmentreplacedmodification import FragmentReplacedModification
from reactomeneo4j.code.node.replacedresidue import ReplacedResidue
from reactomeneo4j.code.node.interchaincrosslinkedresidue import InterChainCrosslinkedResidue
from reactomeneo4j.code.node.intrachaincrosslinkedresidue import IntraChainCrosslinkedResidue
from reactomeneo4j.code.node.groupmodifiedresidue import GroupModifiedResidue
from reactomeneo4j.code.node.modifiedresidue import ModifiedResidue
from reactomeneo4j.code.node.undirectedinteraction import UndirectedInteraction
from reactomeneo4j.code.node.taxon import Taxon
from reactomeneo4j.code.node.species import Species
from reactomeneo4j.code.node.databaseidentifier import DatabaseIdentifier
from reactomeneo4j.code.node.person import Person
from reactomeneo4j.code.node.summation import Summation
from reactomeneo4j.code.node.functionalstatus import FunctionalStatus
from reactomeneo4j.code.node.affiliation import Affiliation
from reactomeneo4j.code.node.figure import Figure
from reactomeneo4j.code.node.functionalstatustype import FunctionalStatusType


SCHEMACLASS2CLS = OrderedDict([
    ('InstanceEdit', InstanceEdit),

    #   - PhysicalEntity (dcnt=13)
    #   -- EntitySet (dcnt=3)
    # > --- CandidateSet (dcnt=0)
    # > --- DefinedSet (dcnt=0)
    # > --- OpenSet (dcnt=0)
    #   -- Drug (dcnt=2)
    # > --- ChemicalDrug (dcnt=0)
    # > --- ProteinDrug (dcnt=0)
    # > -- GenomeEncodedEntity (dcnt=1)
    # > --- EntityWithAccessionedSequence (dcnt=0)
    # > -- Complex (dcnt=0)
    # > -- OtherEntity (dcnt=0)
    # > -- Polymer (dcnt=0)
    # > -- SimpleEntity (dcnt=0)
    ('PhysicalEntity', PhysicalEntity),
    ('EntitySet', EntitySet),
    ('CandidateSet', CandidateSet),
    ('DefinedSet', DefinedSet),
    ('OpenSet', OpenSet),
    ('Drug', Drug),
    ('ChemicalDrug', ChemicalDrug),
    ('ProteinDrug', Drug),
    ('GenomeEncodedEntity', GenomeEncodedEntity),
    ('EntityWithAccessionedSequence', EntityWithAccessionedSequence),
    ('Complex', Complex),
    ('OtherEntity', OtherEntity),
    ('Polymer', Polymer),
    ('SimpleEntity', SimpleEntity),

    #   - Event (dcnt=8)
    #   -- ReactionLikeEvent (dcnt=5)
    # > --- BlackBoxEvent (dcnt=0)
    # > --- Depolymerisation (dcnt=0)
    # > --- FailedReaction (dcnt=0)
    # > --- Polymerisation (dcnt=0)
    # > --- Reaction (dcnt=0)
    # > -- Pathway (dcnt=1)
    # > --- TopLevelPathway (dcnt=0)
    ('Event', Event),
    ('BlackBoxEvent', BlackBoxEvent),
    ('Depolymerisation', Depolymerisation),
    ('FailedReaction', FailedReaction),
    ('Polymerisation', Polymerisation),
    ('Reaction', Reaction),
    ('Pathway', Pathway),
    ('TopLevelPathway', TopLevelPathway),

    #   - Regulation (dcnt=5)
    # > -- PositiveRegulation (dcnt=2)
    # > --- PositiveGeneExpressionRegulation (dcnt=0)
    # > --- Requirement (dcnt=0)
    # > -- NegativeRegulation (dcnt=1)
    # > --- NegativeGeneExpressionRegulation (dcnt=0)
    ('PositiveRegulation', PositiveRegulation),
    ('PositiveGeneExpressionRegulation', PositiveGeneExpressionRegulation),
    ('Requirement', Requirement),
    ('NegativeRegulation', NegativeRegulation),
    ('NegativeGeneExpressionRegulation', NegativeGeneExpressionRegulation),

    #   - AbstractModifiedResidue (dcnt=12)
    #   -- GeneticallyModifiedResidue (dcnt=5)
    #   --- FragmentModification (dcnt=3)
    # > ---- FragmentDeletionModification (dcnt=0)
    # > ---- FragmentInsertionModification (dcnt=0)
    # > ---- FragmentReplacedModification (dcnt=0)
    # > --- ReplacedResidue (dcnt=0)
    #   -- TranslationalModification (dcnt=5)
    #   --- CrosslinkedResidue (dcnt=2)
    # > ---- InterChainCrosslinkedResidue (dcnt=0)
    # > ---- IntraChainCrosslinkedResidue (dcnt=0)
    # > --- GroupModifiedResidue (dcnt=0)
    # > --- ModifiedResidue (dcnt=0)
    ('AbstractModifiedResidue', AbstractModifiedResidue),
    ('FragmentDeletionModification', FragmentDeletionModification),
    ('FragmentInsertionModification', FragmentInsertionModification),
    ('FragmentReplacedModification', FragmentReplacedModification),
    ('ReplacedResidue', ReplacedResidue),
    ('InterChainCrosslinkedResidue', InterChainCrosslinkedResidue),
    ('IntraChainCrosslinkedResidue', IntraChainCrosslinkedResidue),
    ('GroupModifiedResidue', GroupModifiedResidue),
    ('ModifiedResidue', ModifiedResidue),

    #   - Interaction (dcnt=1)
    # > -- UndirectedInteraction (dcnt=0)
    ('UndirectedInteraction', UndirectedInteraction),

    #   - ReferenceEntity (dcnt=8)
    #   -- ReferenceSequence (dcnt=4)
    # > --- ReferenceGeneProduct (dcnt=1)
    # > ---- ReferenceIsoform (dcnt=0)
    # > --- ReferenceDNASequence (dcnt=0)
    # > --- ReferenceRNASequence (dcnt=0)
    # > -- ReferenceGroup (dcnt=0)
    # > -- ReferenceMolecule (dcnt=0)
    # > -- ReferenceTherapeutic (dcnt=0)
    ('ReferenceEntity', ReferenceEntity),
    ('ReferenceGeneProduct', ReferenceGeneProduct),
    ('ReferenceIsoform', ReferenceIsoform),
    ('ReferenceDNASequence', ReferenceDNASequence),
    ('ReferenceRNASequence', ReferenceSequence),
    ('ReferenceGroup', ReferenceGroup),
    ('ReferenceMolecule', ReferenceMolecule),
    ('ReferenceTherapeutic', ReferenceTherapeutic),

    #   - Publication (dcnt=3)
    # > -- LiteratureReference (dcnt=0)
    # > -- Book (dcnt=0)
    # > -- URL  (dcnt=0)
    ('LiteratureReference', LiteratureReference),
    ('Book', Book),
    ('URL', URL),

    #   - GO_Term (dcnt=4)
    # > -- GO_CellularComponent (dcnt=1)
    # > --- Compartment (dcnt=0)
    # > -- GO_BiologicalProcess (dcnt=0)
    # > -- GO_MolecularFunction (dcnt=0)
    ('GO_CellularComponent', GO_CellularComponent),
    ('Compartment', Compartment),
    ('GO_BiologicalProcess', GO_BiologicalProcess),
    ('GO_MolecularFunction', GO_MolecularFunction),

    #   - ExternalOntology (dcnt=3)
    # > -- Disease (dcnt=0)
    # > -- PsiMod (dcnt=0)
    # > -- SequenceOntology (dcnt=0)
    ('Disease', ExternalOntology),
    ('PsiMod', ExternalOntology),
    ('SequenceOntology', ExternalOntology),

    #   - DatabaseObject (dcnt=80)
    # > -- CatalystActivity (dcnt=0)
    ('CatalystActivity', CatalystActivity),

    #   - DatabaseObject (dcnt=80)
    # > -- EntityFunctionalStatus (dcnt=0)
    ('EntityFunctionalStatus', EntityFunctionalStatus),

    #   - DatabaseObject (dcnt=80)
    # > -- ReferenceDatabase (dcnt=0)
    ('ReferenceDatabase', ReferenceDatabase),

    # > - Taxon (dcnt=1)
    # > -- Species (dcnt=0)
    ('Taxon', Taxon),
    ('Species', Species),

    #   - DatabaseObject (dcnt=80)
    # > -- DatabaseIdentifier (dcnt=0)
    ('DatabaseIdentifier', DatabaseIdentifier),

    #   - DatabaseObject (dcnt=80)
    # > -- Person (dcnt=0)
    ('Person', Person),

    #   - DatabaseObject (dcnt=80)
    # > -- Summation (dcnt=0)
    ('Summation', Summation),

    #   - DatabaseObject (dcnt=80)
    # > -- FunctionalStatus (dcnt=0)
    ('FunctionalStatus', FunctionalStatus),

    #   - DatabaseObject (dcnt=80)
    # > -- Affiliation (dcnt=0)
    ('Affiliation', Affiliation),

    #   - DatabaseObject (dcnt=80)
    # > -- Figure (dcnt=0)
    ('Figure', Figure),

    #   - DatabaseObject (dcnt=80)
    # > -- FunctionalStatusType (dcnt=0)
    #         2018/12: "loss_of_function"
    #         2018/12: "gain_of_function"
    #         2018/12: "decreased_transcript_level"
    #         2018/12: "partial_loss_of_function"
    ('FunctionalStatusType', FunctionalStatusType),

    #   - DatabaseObject (dcnt=80)
    # > -- EvidenceType (dcnt=0)
    #       2018/12: "inferred by electronic annotation"
    ('EvidenceType', DatabaseObject),
])

ARGSCH = {
    #'PhysicalEntity',
    #'EntitySet',
    #'GenomeEncodedEntity',
    #'Drug',
    'ProteinDrug',
    #'AbstractModifiedResidue',
    #'PositiveRegulation',
    #'NegativeRegulation',
    #'Event',
    #'ReferenceEntity',
    #'ReferenceGeneProduct',
    'ReferenceRNASequence',
    'Disease',
    'PsiMod',
    'SequenceOntology',
    'EvidenceType',
    #'GO_CellularComponent',
    #'Taxon',
}

def new_inst(schemaclass):
    """Create and return the requested object."""
    assert schemaclass in SCHEMACLASS2CLS, '**FATAL: BAD schemaClass({S})'.format(S=schemaclass)
    cls = SCHEMACLASS2CLS[schemaclass]
    if schemaclass not in ARGSCH:
        return cls()
    return cls(schemaclass)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
