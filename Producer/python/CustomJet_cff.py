#
#Reference: PhysicsTools/NanoAOD/python/custom_jme_cff.py
#
import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.simpleCandidateFlatTableProducer_cfi import simpleCandidateFlatTableProducer

from RecoJets.JetProducers.hfJetShowerShape_cfi import hfJetShowerShape
from SNUSKNANO.Producer.CustomJet_cfi import CustomJet

from PhysicsTools.NanoAOD.common_cff import Var, P4Vars
from PhysicsTools.NanoAOD.jetsAK4_CHS_cff import jetTable, jetCorrFactorsNano, updatedJets, finalJets, qgtagger
from PhysicsTools.NanoAOD.jetsAK4_Puppi_cff import jetPuppiTable, jetPuppiCorrFactorsNano, updatedJetsPuppi, updatedJetsPuppiWithUserData
from PhysicsTools.NanoAOD.jetMC_cff import genJetTable, genJetFlavourAssociation, genJetFlavourTable

from PhysicsTools.PatAlgos.tools.jetCollectionTools import GenJetAdder, RecoJetAdder
from PhysicsTools.PatAlgos.tools.jetTools import supportedJetAlgos
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

bTagCSVV2       = ['pfCombinedInclusiveSecondaryVertexV2BJetTags']
bTagDeepCSV    = ['pfDeepCSVJetTags:probb','pfDeepCSVJetTags:probbb','pfDeepCSVJetTags:probc','pfDeepCSVJetTags:probudsg']
bTagDeepJet    = [
    'pfDeepFlavourJetTags:probb','pfDeepFlavourJetTags:probbb','pfDeepFlavourJetTags:problepb',
    'pfDeepFlavourJetTags:probc','pfDeepFlavourJetTags:probuds','pfDeepFlavourJetTags:probg'
]
from RecoBTag.ONNXRuntime.pfParticleNetAK4_cff import _pfParticleNetAK4JetTagsAll
from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK4_cff import _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsAll
from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK4_cff import _pfParticleNetFromMiniAODAK4PuppiForwardJetTagsAll
from RecoBTag.ONNXRuntime.pfParticleTransformerAK4_cff import _pfParticleTransformerAK4JetTagsAll
bTagDiscriminatorsForAK4 = cms.PSet(foo = cms.vstring(
    bTagDeepJet+
    _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsAll+_pfParticleNetFromMiniAODAK4PuppiForwardJetTagsAll+
    _pfParticleTransformerAK4JetTagsAll
))
run2_nanoAOD_ANY.toModify(
    bTagDiscriminatorsForAK4,
    foo = bTagCSVV2+bTagDeepCSV+bTagDeepJet+_pfParticleNetAK4JetTagsAll
)
bTagDiscriminatorsForAK4 = bTagDiscriminatorsForAK4.foo.value()

from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsAll
from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfParticleNetJetTagsAll

btagHbb = ['pfBoostedDoubleSecondaryVertexAK8BJetTags']
btagDDX = [
    'pfDeepDoubleBvLJetTags:probHbb',
    'pfDeepDoubleCvLJetTags:probHcc',
    'pfDeepDoubleCvBJetTags:probHcc',
    'pfMassIndependentDeepDoubleBvLJetTags:probHbb',
    'pfMassIndependentDeepDoubleCvLJetTags:probHcc',
    'pfMassIndependentDeepDoubleCvBJetTags:probHcc'
]
btagDDXV2 = [
    'pfMassIndependentDeepDoubleBvLV2JetTags:probHbb',
    'pfMassIndependentDeepDoubleCvLV2JetTags:probHcc',
    'pfMassIndependentDeepDoubleCvBV2JetTags:probHcc'
]

#
# By default, these collections are saved in NanoAODs:
# - ak4gen (GenJet in NanoAOD), slimmedGenJets in MiniAOD
# - ak8gen (GenJetAK8 in NanoAOD), slimmedGenJetsAK8 in MiniAOD
# Below is a list of genjets that we can save in NanoAOD. Set
# "enabled" to true if you want to store the jet collection
config_genjets = [
    {
        "jet"     : "ak6gen",
        "enabled" : False,
    },
]
config_genjets = list(filter(lambda k: k['enabled'], config_genjets))
#
# GenJets info in NanoAOD
#
nanoInfo_genjets = {
    "ak6gen"    : {
        "name"  : "GenJetAK6",
        "doc"   : "AK6 Gen jets (made with visible genparticles) with pt > 3 GeV", # default genjets pt cut after clustering is 3 GeV
    },
}
#
# By default, these collections are saved in the main NanoAODs:
# - ak4pfpuppi    (Jet     in NanoAOD), slimmedJetsPuppi in MiniAOD
# - ak8pfpuppi (FatJet in NanoAOD), slimmedJetsAK8 in MiniAOD
# Below is a list of recojets that we can save in NanoAOD. Set
# "enabled" to true if you want to store the recojet collection.
#
config_recojets = [
    {
        "jet"                : "ak4calo",
        "enabled"            : True,
        "inputCollection"    : "slimmedCaloJets", #Exist in MiniAOD
        "genJetsCollection"  : "AK4GenJetsNoNu",
    },
    {
        "jet"                : "ak4pf",
        "enabled"            : False,
        "inputCollection"    : "",
        "genJetsCollection"  : "AK4GenJetsNoNu",
        "minPtFastjet"       : 0.,
    },
    {
        "jet"                : "ak8pf",
        "enabled"            : False,
        "inputCollection"    : "",
        "genJetsCollection"  : "AK8GenJetsNoNu",
        "minPtFastjet"       : 0.,
    },
]
config_recojets = list(filter(lambda k: k['enabled'], config_recojets))
#
# RecoJets info in NanoAOD
#
nanoInfo_recojets = {
    "ak4calo" : {
        "name"    : "JetCalo",
        "doc"     : "AK4 Calo jets (slimmedCaloJets)",
    },
    "ak4pf"   : {
        "name"    : "JetPF",
        "doc"     : "AK4 PF jets",
        "ptcut"   : "",
    },
    "ak8pf"   : {
        "name"    : "FatJetPF",
        "doc"     : "AK8 PF jets",
        "ptcut"   : "",
    },
}

GENJETVARS = cms.PSet(P4Vars,
    nConstituents     = jetPuppiTable.variables.nConstituents,
)
PFJETVARS = cms.PSet(P4Vars,
    rawFactor             = jetPuppiTable.variables.rawFactor,
    area                  = jetPuppiTable.variables.area,
    chHEF                 = jetPuppiTable.variables.chHEF,
    neHEF                 = jetPuppiTable.variables.neHEF,
    chEmEF                = jetPuppiTable.variables.chEmEF,
    neEmEF                = jetPuppiTable.variables.neEmEF,
    muEF                  = jetPuppiTable.variables.muEF,
    hfHEF                 = Var("HFHadronEnergyFraction()",float,doc="hadronic Energy Fraction in HF",precision= 6),
    hfEmEF                = Var("HFEMEnergyFraction()",float,doc="electromagnetic Energy Fraction in HF",precision= 6),
    nMuons                = jetPuppiTable.variables.nMuons,
    nElectrons            = jetPuppiTable.variables.nElectrons,
    nConstituents         = jetPuppiTable.variables.nConstituents,
    chHadMultiplicity     = Var("chargedHadronMultiplicity()","int16",doc="(Puppi-weighted) number of charged hadrons in the jet"),
    neHadMultiplicity     = Var("neutralHadronMultiplicity()","int16",doc="(Puppi-weighted) number of neutral hadrons in the jet"),
    hfHadMultiplicity     = Var("HFHadronMultiplicity()", "int16",doc="(Puppi-weighted) number of HF hadrons in the jet"),
    hfEMMultiplicity      = Var("HFEMMultiplicity()","int16",doc="(Puppi-weighted) number of HF EMs in the jet"),
    muMultiplicity        = Var("muonMultiplicity()","int16",doc="(Puppi-weighted) number of muons in the jet"),
    elMultiplicity        = Var("electronMultiplicity()","int16",doc="(Puppi-weighted) number of electrons in the jet"),
    phoMultiplicity       = Var("photonMultiplicity()","int16",doc="(Puppi-weighted) number of photons in the jet"),
    #MC-only variables
    partonFlavour         = Var("partonFlavour()", "int16", doc="flavour from parton matching"),
    hadronFlavour         = Var("hadronFlavour()", "uint8", doc="flavour from hadron ghost clustering"),
    genJetIdx             = Var("?genJetFwdRef().backRef().isNonnull()?genJetFwdRef().backRef().key():-1", "int16", doc="index of matched gen jet"),
)
SNUVARS = cms.PSet(
    SNU_frac01           = Var("?(pt>=10)?userFloat('SNU_frac01'):-1",float,doc="fraction of constituents' pT contained within dR <0.1 (PileUp ID BDT input variable)", precision=14),
    SNU_frac02           = Var("?(pt>=10)?userFloat('SNU_frac02'):-1",float,doc="fraction of constituents' pT contained within 0.1< dR <0.2 (PileUp ID BDT input variable)", precision=14),
    SNU_frac03           = Var("?(pt>=10)?userFloat('SNU_frac03'):-1",float,doc="fraction of constituents' pT contained within 0.2< dR <0.3 (PileUp ID BDT input variable)", precision=14),
    SNU_frac04           = Var("?(pt>=10)?userFloat('SNU_frac04'):-1",float,doc="fraction of constituents' pT contained within 0.3< dR <0.4 (PileUp ID BDT input variable)", precision=14),
    SNU_nCharged         = Var("?(pt>=10)?userInt('SNU_nCharged'):-1","int16",doc="number of charged constituents (PileUp ID BDT input variable)"),
)


#******************************************
#
#
# Reco Jets related functions
#
#
#******************************************

def AddCustomJetVars(proc, jetName="", jetSrc="", jetTableName="", jetTaskName=""):
    """
    Setup modules to calculate pileup jet ID input variables for PF jet
    """

    #
    # Calculate pileup jet ID variables
    #
    SNUJetVarsCalculator = "SNUJetCalculator{}".format(jetName)
    setattr(proc, SNUJetVarsCalculator, CustomJet.clone(
            jets = jetSrc,
            vertexes    = "offlineSlimmedPrimaryVertices",
            inputIsCorrected = True,
            applyJec    = False,
            srcConstituentWeights = "packedpuppi" if "PUPPI" in jetName.upper() else ""
        )
    )
    getattr(proc,jetTaskName).add(getattr(proc, SNUJetVarsCalculator))

    #
    # Get the variables
    #
    SNUJetVar = "SNUJetVar{}".format(jetName)
    setattr(proc, SNUJetVar, cms.EDProducer("ProduceCustomJetVars",
            srcJet = cms.InputTag(jetSrc),
            srcPileupJetId = cms.InputTag(SNUJetVarsCalculator)
        )
    )
    getattr(proc,jetTaskName).add(getattr(proc, SNUJetVar))

    #
    # Save variables as userFloats and userInts for each jet
    #
    patJetWithUserData = "{}WithUserData".format(jetSrc)
    getattr(proc,patJetWithUserData).userFloats.SNU_frac01     = cms.InputTag("{}:frac01".format(SNUJetVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_frac02     = cms.InputTag("{}:frac02".format(SNUJetVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_frac03     = cms.InputTag("{}:frac03".format(SNUJetVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_frac04     = cms.InputTag("{}:frac04".format(SNUJetVar))
    getattr(proc,patJetWithUserData).userInts.SNU_nCharged     = cms.InputTag("{}:nCharged".format(SNUJetVar))

    #
    # Specfiy variables in the jet table to save in NanoAOD
    #
    getattr(proc,jetTableName).variables.SNU_frac01     = SNUVARS.SNU_frac01
    getattr(proc,jetTableName).variables.SNU_frac02     = SNUVARS.SNU_frac02
    getattr(proc,jetTableName).variables.SNU_frac03     = SNUVARS.SNU_frac03
    getattr(proc,jetTableName).variables.SNU_frac04     = SNUVARS.SNU_frac04
    getattr(proc,jetTableName).variables.SNU_nCharged = SNUVARS.SNU_nCharged

    return proc

def SaveAK4PUPPICustomJetVars(proc, recoJA, runOnMC):
    cfg = {
        "jet" : "ak4pfpuppi",
        "inputCollection" : "",
        "genJetsCollection": "AK4GenJetsNoNu",
        "minPtFastjet" : 0.,
    }
    recoJetInfo = recoJA.addRecoJetCollection(proc,**cfg)
    jetName = recoJetInfo.jetUpper
    patJetFinalColl = recoJetInfo.patJetFinalCollection
    proc.jetPuppiCorrFactorsNano.src=patJetFinalColl
    proc.updatedJetsPuppi.jetSource=patJetFinalColl

    finalJetsPuppiCut = ""
    if runOnMC:
        finalJetsPuppiCut = "(pt >= 8) || ((pt < 8) && (genJetFwdRef().backRef().isNonnull()))"
    else:
        finalJetsPuppiCut = "(pt >= 8)"
    run2_nanoAOD_ANY.toModify(
        proc.jetTable, name = "Jet"
    )

    #
    # Jet table documentation
    #
    jetPuppiTableDoc = "AK4 PF Puppi jets with JECs applied. Jets with pt >= 8 GeV are stored."
    if runOnMC:
      jetPuppiTableDoc += "For jets with pt < 8 GeV, only those matched to AK4 Gen jets are stored."
    proc.jetPuppiTable.doc = jetPuppiTableDoc

    proc.jetPuppiTable.variables.rawFactor.precision = 10

    #
    # Add variables
    #
    proc = AddCustomJetVars(proc,
    jetName = jetName,
    jetSrc = "updatedJetsPuppi",
    jetTableName = "jetPuppiTable",
    jetTaskName = "jetPuppiTask"
    )
#    proc.jetPuppiTable.variables.btagRobustParTAK4B   = ROBUSTPARTAK4VARS.btagRobustParTAK4B
#    proc.jetPuppiTable.variables.btagRobustParTAK4CvL = ROBUSTPARTAK4VARS.btagRobustParTAK4CvL
#    proc.jetPuppiTable.variables.btagRobustParTAK4CvB = ROBUSTPARTAK4VARS.btagRobustParTAK4CvB

    if runOnMC:
        jetMCTableName = "jet{}MCTable".format(jetName)
        setattr(proc, jetMCTableName, proc.jetMCTable.clone(
            src = proc.jetPuppiTable.src,
            name = proc.jetPuppiTable.name
        )
        )
        getattr(proc,jetMCTableName).variables.genJetIdx = PFJETVARS.genJetIdx

        jetMCTableTaskName = "jet{}MCTablesTask".format(jetName)
        setattr(proc, jetMCTableTaskName, cms.Task(getattr(proc,jetMCTableName)))

    return proc
#===========================================================================
#
# Misc. functions
#
#===========================================================================
def RemoveAllJetPtCuts(proc):
    """
    Remove default pt cuts for all jets set in jets_cff.py
    """

    proc.finalJets.cut                         = "" # 15 -> 10
    proc.finalJetsPuppi.cut                = "" # 15 -> 10
    proc.finalJetsAK8.cut                    = "" # 170 -> 170
    proc.genJetTable.cut                     = "" # 10 -> 8
    proc.genJetFlavourTable.cut        = "" # 10 -> 8
    proc.genJetAK8Table.cut                = "" # 100 -> 80
    proc.genJetAK8FlavourTable.cut = "" # 100 -> 80

    return proc

#===========================================================================
#
# CUSTOMIZATION function
#
#===========================================================================
def PrepCustomJet(process):
    runOnMC=True
    if hasattr(process,"NANOEDMAODoutput") or hasattr(process,"NANOAODoutput"):
        runOnMC = False
    ############################################################################
    # Remove all default jet pt cuts from jets_cff.py
    ############################################################################
    process = RemoveAllJetPtCuts(process)

    ###########################################################################
    #
    # Gen-level jets related functions. Only for MC.
    #
    ###########################################################################
#    if runOnMC:



    ###########################################################################
    #
    # Reco-level jets related functions. For both MC and data.
    #
    ###########################################################################
    # Add Custom Variables
    ###########################################################################
    recoJA = RecoJetAdder(runOnMC=runOnMC)
    # Add Custom Variables
    ###########################################################################
    process = SaveAK4PUPPICustomJetVars(process,recoJA, runOnMC)
    ###########################################################################
    def addAK4JetTasks(proc, addAK4CHSJetTasks, addAK4PuppiJetTasks):
        if addAK4CHSJetTasks:
            proc.nanoTableTaskCommon.add(proc.jetTask)
            proc.nanoTableTaskCommon.add(proc.jetTablesTask)
            proc.nanoTableTaskCommon.add(proc.jetForMETTask)
        if addAK4PuppiJetTasks:
            proc.nanoTableTaskCommon.add(proc.jetPuppiTask)
            proc.nanoTableTaskCommon.add(proc.jetPuppiTablesTask)
            proc.nanoTableTaskCommon.add(proc.jetPuppiForMETTask)
        return proc

    addAK4JetTasks_switch = cms.PSet(
        addAK4CHS_switch = cms.untracked.bool(True),
        addAK4Puppi_switch = cms.untracked.bool(False)
    )
    run2_nanoAOD_ANY.toModify(addAK4JetTasks_switch,
        jmeNano_addAK4CHS_switch = False,
        jmeNano_addAK4Puppi_switch = True
    )
    process = addAK4JetTasks(process,
        addAK4CHSJetTasks = addAK4JetTasks_switch.addAK4CHS_switch,
        addAK4PuppiJetTasks = addAK4JetTasks_switch.addAK4Puppi_switch,
    )

    ###########################################################################
    # Save Maximum of Pt Hat Max
    ###########################################################################
    if runOnMC:
        process.puTable.savePtHatMax = True

    ###########################################################################
    # Save all Parton-Shower weights
    ###########################################################################
    if runOnMC:
        process.genWeightsTable.keepAllPSWeights = True

    return process
