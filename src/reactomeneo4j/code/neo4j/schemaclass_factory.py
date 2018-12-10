"""Given a schemaClass string, return the associated class instance."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject
from reactomeneo4j.code.neo4j.instanceedit import InstanceEdit
from reactomeneo4j.code.neo4j.physicalentity import PhysicalEntity
from reactomeneo4j.code.neo4j.candidateset import CandidateSet
from reactomeneo4j.code.neo4j.definedset import DefinedSet
from reactomeneo4j.code.neo4j.openset import OpenSet
from reactomeneo4j.code.neo4j.drug import Drug
from reactomeneo4j.code.neo4j.genomeencodedentity import GenomeEncodedEntity
from reactomeneo4j.code.neo4j.entitywithaccessionedsequence import EntityWithAccessionedSequence
from reactomeneo4j.code.neo4j.complex import Complex
from reactomeneo4j.code.neo4j.otherentity import OtherEntity
from reactomeneo4j.code.neo4j.polymer import Polymer
from reactomeneo4j.code.neo4j.simpleentity import SimpleEntity
from reactomeneo4j.code.neo4j.reactionlikeevent import ReactionLikeEvent
from reactomeneo4j.code.neo4j.reaction import Reaction
from reactomeneo4j.code.neo4j.pathway import Pathway
from reactomeneo4j.code.neo4j.toplevelpathway import TopLevelPathway
from reactomeneo4j.code.neo4j.regulation import Regulation
from reactomeneo4j.code.neo4j.referencesequence import ReferenceSequence
from reactomeneo4j.code.neo4j.referencegeneproduct import ReferenceGeneProduct
from reactomeneo4j.code.neo4j.referenceisoform import ReferenceIsoform
from reactomeneo4j.code.neo4j.referencednasequence import ReferenceDNASequence
# from reactomeneo4j.code.neo4j.referencernasequence import ReferenceRNASequence
from reactomeneo4j.code.neo4j.referencegroup import ReferenceGroup
from reactomeneo4j.code.neo4j.referencemolecule import ReferenceMolecule
from reactomeneo4j.code.neo4j.referencetherapeutic import ReferenceTherapeutic
from reactomeneo4j.code.neo4j.referencedatabase import ReferenceDatabase
from reactomeneo4j.code.neo4j.catalystactivity import CatalystActivity
from reactomeneo4j.code.neo4j.entityfunctionalstatus import EntityFunctionalStatus
from reactomeneo4j.code.neo4j.literaturereference import LiteratureReference
from reactomeneo4j.code.neo4j.book import Book
from reactomeneo4j.code.neo4j.url import URL
from reactomeneo4j.code.neo4j.go_term import GOTerm
from reactomeneo4j.code.neo4j.go_molecularfunction import GO_MolecularFunction
from reactomeneo4j.code.neo4j.externalontology import ExternalOntology
from reactomeneo4j.code.neo4j.fragmentmodification import FragmentModification
from reactomeneo4j.code.neo4j.fragmentreplacedmodification import FragmentReplacedModification
from reactomeneo4j.code.neo4j.abstractmodifiedresidue import AbstractModifiedResidue
from reactomeneo4j.code.neo4j.crosslinkedresidue import CrosslinkedResidue
from reactomeneo4j.code.neo4j.undirectedinteraction import UndirectedInteraction
from reactomeneo4j.code.neo4j.taxon import Taxon
from reactomeneo4j.code.neo4j.species import Species
from reactomeneo4j.code.neo4j.databaseidentifier import DatabaseIdentifier
from reactomeneo4j.code.neo4j.person import Person
from reactomeneo4j.code.neo4j.summation import Summation
from reactomeneo4j.code.neo4j.functionalstatus import FunctionalStatus
from reactomeneo4j.code.neo4j.affiliation import Affiliation
from reactomeneo4j.code.neo4j.figure import Figure
from reactomeneo4j.code.neo4j.functionalstatustype import FunctionalStatusType

SCHEMACLASS2CONSTRUCTOR = {
    'InstanceEdit': InstanceEdit(),

    #   - PhysicalEntity(dcnt=13)
    #   -- EntitySet(dcnt=3)
    # > --- CandidateSet(dcnt=0)
    # > --- DefinedSet(dcnt=0)
    # > --- OpenSet(dcnt=0)
    #   -- Drug(dcnt=2)
    # > --- ChemicalDrug(dcnt=0)
    # > --- ProteinDrug(dcnt=0)
    # > -- GenomeEncodedEntity(dcnt=1)
    # > --- EntityWithAccessionedSequence(dcnt=0)
    # > -- Complex(dcnt=0)
    # > -- OtherEntity(dcnt=0)
    # > -- Polymer(dcnt=0)
    # > -- SimpleEntity(dcnt=0)
    'CandidateSet': CandidateSet(),
    'DefinedSet': DefinedSet(),
    'OpenSet': OpenSet(),
    'ChemicalDrug': Drug('ChemicalDrug'),  # ChemicalDrug()
    'ProteinDrug': Drug('ProteinDrug'),   # ProteinDrug()
    'GenomeEncodedEntity': GenomeEncodedEntity(),
    'EntityWithAccessionedSequence': EntityWithAccessionedSequence(),
    'Complex': Complex(),
    'OtherEntity': OtherEntity(),
    'Polymer': Polymer(),
    'SimpleEntity': SimpleEntity(),

    #   - Event (dcnt=8)
    #   -- ReactionLikeEvent (dcnt=5)
    # > --- BlackBoxEvent (dcnt=0)
    # > --- Depolymerisation (dcnt=0)
    # > --- FailedReaction (dcnt=0)
    # > --- Polymerisation (dcnt=0)
    # > --- Reaction (dcnt=0)
    # > -- Pathway (dcnt=1)
    # > --- TopLevelPathway (dcnt=0)
    'BlackBoxEvent': ReactionLikeEvent('BlackBoxEvent'),        # BlackBoxEvent
    'Depolymerisation': ReactionLikeEvent('Depolymerisation'),  # Depolymerisation
    'FailedReaction': ReactionLikeEvent('FailedReaction'),      # FailedReaction
    'Polymerisation': ReactionLikeEvent('Polymerisation'),      # Polymerisation
    'Reaction': Reaction(),                   # Reaction
    'Pathway': Pathway(),                     # Pathway
    'TopLevelPathway': TopLevelPathway(),     # TopLevelPathway

    #   - Regulation (dcnt=5)
    # > -- PositiveRegulation (dcnt=2)
    # > --- PositiveGeneExpressionRegulation (dcnt=0)
    # > --- Requirement (dcnt=0)
    # > -- NegativeRegulation (dcnt=1)
    # > --- NegativeGeneExpressionRegulation (dcnt=0)
    'PositiveRegulation'              : Regulation('PositiveRegulation'),
    'PositiveGeneExpressionRegulation': Regulation('PositiveGeneExpressionRegulation'),
    'Requirement'                     : Regulation('Requirement'),
    'NegativeRegulation'              : Regulation('NegativeRegulation'),
    'NegativeGeneExpressionRegulation': Regulation('NegativeGeneExpressionRegulation'),

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
    'FragmentDeletionModification' : FragmentModification('FragmentDeletionModification'),
    'FragmentInsertionModification' : FragmentModification('FragmentInsertionModification'),
    'FragmentReplacedModification' : FragmentReplacedModification(),
    'ReplacedResidue' : AbstractModifiedResidue('ReplacedResidue'),
    'InterChainCrosslinkedResidue' : CrosslinkedResidue('InterChainCrosslinkedResidue'),
    'IntraChainCrosslinkedResidue' : CrosslinkedResidue('IntraChainCrosslinkedResidue'),
    'GroupModifiedResidue' : AbstractModifiedResidue('GroupModifiedResidue'),
    'ModifiedResidue' : AbstractModifiedResidue('ModifiedResidue'),

    #   - Interaction (dcnt=1)
    # > -- UndirectedInteraction (dcnt=0)
    'UndirectedInteraction': UndirectedInteraction(),

    #   - ReferenceEntity (dcnt=8)
    #   -- ReferenceSequence (dcnt=4)
    # > --- ReferenceGeneProduct (dcnt=1)
    # > ---- ReferenceIsoform (dcnt=0)
    # > --- ReferenceDNASequence (dcnt=0)
    # > --- ReferenceRNASequence (dcnt=0)
    # > -- ReferenceGroup (dcnt=0)
    # > -- ReferenceMolecule (dcnt=0)
    # > -- ReferenceTherapeutic (dcnt=0)
    'ReferenceGeneProduct' : ReferenceGeneProduct(),
    'ReferenceIsoform' : ReferenceIsoform(),
    'ReferenceDNASequence' : ReferenceDNASequence(),
    'ReferenceRNASequence' : ReferenceSequence('ReferenceRNASequence'),
    'ReferenceGroup' : ReferenceGroup(),
    'ReferenceMolecule' : ReferenceMolecule(),
    'ReferenceTherapeutic' : ReferenceTherapeutic(),

    #   - Publication (dcnt=3)
    # > -- LiteratureReference (dcnt=0)
    # > -- Book (dcnt=0)
    # > -- URL  (dcnt=0)
    'LiteratureReference': LiteratureReference(),
    'Book': Book(),
    'URL': URL(),

    #   - GO_Term (dcnt=4)
    # > -- GO_CellularComponent (dcnt=1)
    # > --- Compartment (dcnt=0)
    # > -- GO_BiologicalProcess (dcnt=0)
    # > -- GO_MolecularFunction (dcnt=0)
    'GO_CellularComponent' : GOTerm('GO_CellularComponent'),
    'Compartment' : GOTerm('Compartment'),
    'GO_BiologicalProcess' : GOTerm('GO_BiologicalProcess'),
    'GO_MolecularFunction' : GO_MolecularFunction(),

    #   - ExternalOntology (dcnt=3)
    # > -- Disease (dcnt=0)
    # > -- PsiMod (dcnt=0)
    # > -- SequenceOntology (dcnt=0)
    'Disease' : ExternalOntology('Disease'),
    'PsiMod' : ExternalOntology('PsiMod'),
    'SequenceOntology' : ExternalOntology('SequenceOntology'),

    #   - DatabaseObject (dcnt=80)
    # > -- CatalystActivity (dcnt=0)
    'CatalystActivity': CatalystActivity(),

    #   - DatabaseObject (dcnt=80)
    # > -- EntityFunctionalStatus (dcnt=0)
    'EntityFunctionalStatus': EntityFunctionalStatus(),

    #   - DatabaseObject (dcnt=80)
    # > -- ReferenceDatabase (dcnt=0)
    'ReferenceDatabase': ReferenceDatabase(),

    # > - Taxon (dcnt=1)
    # > -- Species (dcnt=0)
    'Taxon': Taxon(),
    'Species': Species(),

    #   - DatabaseObject (dcnt=80)
    # > -- DatabaseIdentifier (dcnt=0)
    'DatabaseIdentifier': DatabaseIdentifier(),

    #   - DatabaseObject (dcnt=80)
    # > -- Person (dcnt=0)
    'Person': Person(),

    #   - DatabaseObject (dcnt=80)
    # > -- Summation (dcnt=0)
    'Summation': Summation(),

    #   - DatabaseObject (dcnt=80)
    # > -- FunctionalStatus (dcnt=0)
    'FunctionalStatus': FunctionalStatus(),

    #   - DatabaseObject (dcnt=80)
    # > -- Affiliation (dcnt=0)
    'Affiliation': Affiliation(),

    #   - DatabaseObject (dcnt=80)
    # > -- Figure (dcnt=0)
    'Figure': Figure(),

    #   - DatabaseObject (dcnt=80)
    # > -- FunctionalStatusType (dcnt=0)
    'FunctionalStatusType': FunctionalStatusType(),

    #   - DatabaseObject (dcnt=80)
    # > -- EvidenceType (dcnt=0)
    'EvidenceType': DatabaseObject('EvidenceType'),
}


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
