"""Given a schemaClass string, return the associated class instance."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# pylint: disable=line-too-long
from collections import OrderedDict
from reactomepy.code.node.dbinfo import DBInfo
from reactomepy.code.node.databaseobject import DatabaseObject
from reactomepy.code.node.instanceedit import InstanceEdit
from reactomepy.code.node.physicalentity import PhysicalEntity
from reactomepy.code.node.entityset import EntitySet
from reactomepy.code.node.candidateset import CandidateSet
from reactomepy.code.node.definedset import DefinedSet
from reactomepy.code.node.drug import Drug
from reactomepy.code.node.proteindrug import ProteinDrug
from reactomepy.code.node.chemicaldrug import ChemicalDrug
from reactomepy.code.node.genomeencodedentity import GenomeEncodedEntity
from reactomepy.code.node.entitywithaccessionedsequence import EntityWithAccessionedSequence
from reactomepy.code.node.complex import Complex
from reactomepy.code.node.otherentity import OtherEntity
from reactomepy.code.node.polymer import Polymer
from reactomepy.code.node.simpleentity import SimpleEntity
from reactomepy.code.node.event import Event
from reactomepy.code.node.depolymerisation import Depolymerisation
from reactomepy.code.node.polymerisation import Polymerisation
from reactomepy.code.node.blackboxevent import BlackBoxEvent
from reactomepy.code.node.reaction import Reaction
from reactomepy.code.node.failedreaction import FailedReaction
from reactomepy.code.node.pathway import Pathway
from reactomepy.code.node.toplevelpathway import TopLevelPathway
from reactomepy.code.node.positiveregulation import PositiveRegulation
from reactomepy.code.node.positivegeneexpressionregulation import PositiveGeneExpressionRegulation
from reactomepy.code.node.requirement import Requirement
from reactomepy.code.node.negativeregulation import NegativeRegulation
from reactomepy.code.node.negativegeneexpressionregulation import NegativeGeneExpressionRegulation
from reactomepy.code.node.referenceentity import ReferenceEntity
from reactomepy.code.node.referencesequence import ReferenceSequence
from reactomepy.code.node.referencegeneproduct import ReferenceGeneProduct
from reactomepy.code.node.referenceisoform import ReferenceIsoform
from reactomepy.code.node.referencednasequence import ReferenceDNASequence
# from reactomepy.code.node.referencernasequence import ReferenceRNASequence
from reactomepy.code.node.referencegroup import ReferenceGroup
from reactomepy.code.node.referencemolecule import ReferenceMolecule
from reactomepy.code.node.referencetherapeutic import ReferenceTherapeutic
from reactomepy.code.node.referencedatabase import ReferenceDatabase
from reactomepy.code.node.catalystactivity import CatalystActivity
from reactomepy.code.node.catalystactivityreference import CatalystActivityReference
from reactomepy.code.node.regulationreference import RegulationReference
from reactomepy.code.node.entityfunctionalstatus import EntityFunctionalStatus
from reactomepy.code.node.literaturereference import LiteratureReference
from reactomepy.code.node.book import Book
from reactomepy.code.node.url import URL
from reactomepy.code.node.compartment import Compartment
from reactomepy.code.node.go_cellularcomponent import GOCellularComponent
from reactomepy.code.node.go_biologicalprocess import GOBiologicalProcess
from reactomepy.code.node.go_molecularfunction import GOMolecularFunction
from reactomepy.code.node.externalontology import ExternalOntology
from reactomepy.code.node.psimod import PsiMod
from reactomepy.code.node.abstractmodifiedresidue import AbstractModifiedResidue
from reactomepy.code.node.fragmentdeletionmodification import FragmentDeletionModification
from reactomepy.code.node.fragmentinsertionmodification import FragmentInsertionModification
from reactomepy.code.node.fragmentreplacedmodification import FragmentReplacedModification
from reactomepy.code.node.replacedresidue import ReplacedResidue
from reactomepy.code.node.interchaincrosslinkedresidue import InterChainCrosslinkedResidue
from reactomepy.code.node.intrachaincrosslinkedresidue import IntraChainCrosslinkedResidue
from reactomepy.code.node.groupmodifiedresidue import GroupModifiedResidue
from reactomepy.code.node.modifiedresidue import ModifiedResidue
from reactomepy.code.node.undirectedinteraction import UndirectedInteraction
from reactomepy.code.node.taxon import Taxon
from reactomepy.code.node.species import Species
from reactomepy.code.node.databaseidentifier import DatabaseIdentifier
from reactomepy.code.node.person import Person
from reactomepy.code.node.summation import Summation
from reactomepy.code.node.functionalstatus import FunctionalStatus
from reactomepy.code.node.affiliation import Affiliation
from reactomepy.code.node.figure import Figure
from reactomepy.code.node.functionalstatustype import FunctionalStatusType


SCHEMACLASS2CLS = OrderedDict([
    ('InstanceEdit', InstanceEdit),

    #   - PhysicalEntity (dcnt=13)
    #   -- EntitySet (dcnt=3)
    # > --- CandidateSet (dcnt=0)
    # > --- DefinedSet (dcnt=0)
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
    ('Drug', Drug),
    ('ChemicalDrug', ChemicalDrug),
    ('ProteinDrug', ProteinDrug),
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

    ('CatalystActivityReference', CatalystActivityReference),
    ('RegulationReference', RegulationReference),

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
    ('GO_CellularComponent', GOCellularComponent),
    ('Compartment', Compartment),
    ('GO_BiologicalProcess', GOBiologicalProcess),
    ('GO_MolecularFunction', GOMolecularFunction),

    #   - ExternalOntology (dcnt=3)
    # > -- Disease (dcnt=0)
    # > -- PsiMod (dcnt=0)
    # > -- SequenceOntology (dcnt=0)
    ('Disease', ExternalOntology),
    ('PsiMod', PsiMod),
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
    (None, DBInfo),
])

def _new_inst(schemaclass):
    """Create and return the requested object."""
    argsch = {
        'ReferenceRNASequence',
        'Disease',
        'SequenceOntology',
        'EvidenceType',
    }
    cls = SCHEMACLASS2CLS[schemaclass]
    if schemaclass not in argsch:
        return cls()
    return cls(schemaclass)

SCHEMACLASS2OBJ = OrderedDict([(s, _new_inst(s)) for s in SCHEMACLASS2CLS])


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
