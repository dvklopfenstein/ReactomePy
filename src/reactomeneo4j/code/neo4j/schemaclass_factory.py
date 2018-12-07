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

    # > -- CatalystActivity (dcnt=0)
    'CatalystActivity': DatabaseObject('CatalystActivity'),

    # > -- DatabaseObject (dcnt=0)
    'EntityFunctionalStatus': DatabaseObject('EntityFunctionalStatus'),
}


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
