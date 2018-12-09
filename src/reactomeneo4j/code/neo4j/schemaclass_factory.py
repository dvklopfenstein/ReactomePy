"""Given a schemaClass string, return the associated class instance."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject
from reactomeneo4j.code.neo4j.instanceedit import InstanceEdit
from reactomeneo4j.code.neo4j.physicalentity import PhysicalEntity
from reactomeneo4j.code.neo4j.candidateset import CandidateSet
from reactomeneo4j.code.neo4j.definedset import DefinedSet
from reactomeneo4j.code.neo4j.openset import OpenSet
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
    'ChemicalDrug': PhysicalEntity('ChemicalDrug'),  # ChemicalDrug()
    'ProteinDrug': PhysicalEntity('ProteinDrug'),   # ProteinDrug()
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

    #   - DatabaseObject (dcnt=80)
    # > -- CatalystActivity (dcnt=0)
    'CatalystActivity': CatalystActivity(),

    #   - DatabaseObject (dcnt=80)
    # > -- EntityFunctionalStatus (dcnt=0)
    'EntityFunctionalStatus': EntityFunctionalStatus(),

    #   - DatabaseObject (dcnt=80)
    # > -- ReferenceDatabase (dcnt=0)
    'ReferenceDatabase': ReferenceDatabase(),
}


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
