"""Given a schemaClass string, return the associated class instance."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

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

# pylint: disable=multiple-statements,too-many-return-statements
def get_schemaclass(schemaclass):
    """Given a schemaClass string, return the associated class instance."""
    if schemaclass == 'InstanceEdit': return InstanceEdit()

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
    if schemaclass == 'CandidateSet': return CandidateSet()
    if schemaclass == 'DefinedSet': return DefinedSet()
    if schemaclass == 'OpenSet': return OpenSet()
    if schemaclass == 'ChemicalDrug': return PhysicalEntity()  # ChemicalDrug()
    if schemaclass == 'ProteinDrug': return PhysicalEntity()   # ProteinDrug()
    if schemaclass == 'GenomeEncodedEntity': return GenomeEncodedEntity()
    if schemaclass == 'EntityWithAccessionedSequence': return EntityWithAccessionedSequence()
    if schemaclass == 'Complex': return Complex()
    if schemaclass == 'OtherEntity': return OtherEntity()
    if schemaclass == 'Polymer': return Polymer()
    if schemaclass == 'SimpleEntity': return SimpleEntity()

    #   - Event (dcnt=8)
    #   -- ReactionLikeEvent (dcnt=5)
    # > --- BlackBoxEvent (dcnt=0)
    # > --- Depolymerisation (dcnt=0)
    # > --- FailedReaction (dcnt=0)
    # > --- Polymerisation (dcnt=0)
    # > --- Reaction (dcnt=0)
    # > -- Pathway (dcnt=1)
    # > --- TopLevelPathway (dcnt=0)
    if schemaclass == 'BlackBoxEvent': return ReactionLikeEvent()     # BlackBoxEvent
    if schemaclass == 'Depolymerisation': return ReactionLikeEvent()  # Depolymerisation
    if schemaclass == 'FailedReaction': return ReactionLikeEvent()    # FailedReaction
    if schemaclass == 'Polymerisation': return ReactionLikeEvent()    # Polymerisation
    if schemaclass == 'Reaction': return Reaction()                   # Reaction
    if schemaclass == 'Pathway': return Pathway()                     # Pathway
    if schemaclass == 'TopLevelPathway': return TopLevelPathway()     # TopLevelPathway

    assert False, 'UNRECOGNIZED schemaClass({S})'.format(S=schemaclass)
    return None


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
