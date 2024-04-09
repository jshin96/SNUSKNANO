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
    SNU_dR2Mean          = Var("?(pt>=10)?userFloat('SNU_dR2Mean'):-1",float,doc="pT^2-weighted average square distance of jet constituents from the jet axis (PileUp ID BDT input variable)", precision=14),
    SNU_majW             = Var("?(pt>=10)?userFloat('SNU_majW'):-1",float,doc="major axis of jet ellipsoid in eta-phi plane (PileUp ID BDT input variable)", precision=14),
    SNU_minW             = Var("?(pt>=10)?userFloat('SNU_minW'):-1",float,doc="minor axis of jet ellipsoid in eta-phi plane (PileUp ID BDT input variable)", precision=14),
    SNU_frac01           = Var("?(pt>=10)?userFloat('SNU_frac01'):-1",float,doc="fraction of constituents' pT contained within dR <0.1 (PileUp ID BDT input variable)", precision=14),
    SNU_frac02           = Var("?(pt>=10)?userFloat('SNU_frac02'):-1",float,doc="fraction of constituents' pT contained within 0.1< dR <0.2 (PileUp ID BDT input variable)", precision=14),
    SNU_frac03           = Var("?(pt>=10)?userFloat('SNU_frac03'):-1",float,doc="fraction of constituents' pT contained within 0.2< dR <0.3 (PileUp ID BDT input variable)", precision=14),
    SNU_frac04           = Var("?(pt>=10)?userFloat('SNU_frac04'):-1",float,doc="fraction of constituents' pT contained within 0.3< dR <0.4 (PileUp ID BDT input variable)", precision=14),
    SNU_ptD              = Var("?(pt>=10)?userFloat('SNU_ptD'):-1",float,doc="pT-weighted average pT of constituents (PileUp ID BDT input variable)", precision=14),
    SNU_beta             = Var("?(pt>=10)?userFloat('SNU_beta'):-1",float,doc="fraction of pT of charged constituents associated to PV (PileUp ID BDT input variable)", precision=14),
    SNU_pull             = Var("?(pt>=10)?userFloat('SNU_pull'):-1",float,doc="magnitude of pull vector (PileUp ID BDT input variable)", precision=14),
    SNU_jetR             = Var("?(pt>=10)?userFloat('SNU_jetR'):-1",float,doc="fraction of jet pT carried by the leading constituent (PileUp ID BDT input variable)", precision=14),
    SNU_jetRchg          = Var("?(pt>=10)?userFloat('SNU_jetRchg'):-1",float,doc="fraction of jet pT carried by the leading charged constituent (PileUp ID BDT input variable)", precision=14),
    SNU_nCharged         = Var("?(pt>=10)?userInt('SNU_nCharged'):-1","int16",doc="number of charged constituents (PileUp ID BDT input variable)"),
)
QGLVARS = cms.PSet(
    qgl_axis2             =    Var("?(pt>=10)?userFloat('qgl_axis2'):-1",float,doc="ellipse minor jet axis (Quark vs Gluon likelihood input variable)", precision=14),
    qgl_ptD                 =    Var("?(pt>=10)?userFloat('qgl_ptD'):-1",float,doc="pT-weighted average pT of constituents (Quark vs Gluon likelihood input variable)", precision=14),
    qgl_mult                =    Var("?(pt>=10)?userInt('qgl_mult'):-1", "int16",doc="PF candidates multiplicity (Quark vs Gluon likelihood input variable)"),
)
BTAGVARS = cms.PSet(
    btagDeepB = Var("?(pt>=15)&&((bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'))>=0)?bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'):-1",float,doc="DeepCSV b+bb tag discriminator",precision=10),
    btagDeepCvL = Var("?(pt>=15)&&(bDiscriminator('pfDeepCSVJetTags:probc')>=0)?bDiscriminator('pfDeepCSVJetTags:probc')/(bDiscriminator('pfDeepCSVJetTags:probc')+bDiscriminator('pfDeepCSVJetTags:probudsg')):-1", float,doc="DeepCSV c vs udsg discriminator",precision=10),
    btagDeepCvB = Var("?(pt>=15)&&bDiscriminator('pfDeepCSVJetTags:probc')>=0?bDiscriminator('pfDeepCSVJetTags:probc')/(bDiscriminator('pfDeepCSVJetTags:probc')+bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')):-1",float,doc="DeepCSV c vs b+bb discriminator",precision=10),
)
DEEPJETVARS = cms.PSet(
    btagDeepFlavB     = Var("?(pt>=15)?bDiscriminator('pfDeepFlavourJetTags:probb')+bDiscriminator('pfDeepFlavourJetTags:probbb')+bDiscriminator('pfDeepFlavourJetTags:problepb'):-1",float,doc="DeepJet b+bb+lepb tag discriminator",precision=10),
    btagDeepFlavC     = Var("?(pt>=15)?bDiscriminator('pfDeepFlavourJetTags:probc'):-1",float,doc="DeepFlavour charm tag raw score",precision=10),
    btagDeepFlavG     = Var("?(pt>=15)?bDiscriminator('pfDeepFlavourJetTags:probg'):-1",float,doc="DeepFlavour gluon tag raw score",precision=10),
    btagDeepFlavUDS = Var("?(pt>=15)?bDiscriminator('pfDeepFlavourJetTags:probuds'):-1",float,doc="DeepFlavour uds tag raw score",precision=10),
    btagDeepFlavCvL = Var("?(pt>=15)&&(bDiscriminator('pfDeepFlavourJetTags:probc')+bDiscriminator('pfDeepFlavourJetTags:probuds')+bDiscriminator('pfDeepFlavourJetTags:probg'))>0?bDiscriminator('pfDeepFlavourJetTags:probc')/(bDiscriminator('pfDeepFlavourJetTags:probc')+bDiscriminator('pfDeepFlavourJetTags:probuds')+bDiscriminator('pfDeepFlavourJetTags:probg')):-1",float,doc="DeepJet c vs uds+g discriminator",precision=10),
    btagDeepFlavCvB = Var("?(pt>=15)&&(bDiscriminator('pfDeepFlavourJetTags:probc')+bDiscriminator('pfDeepFlavourJetTags:probb')+bDiscriminator('pfDeepFlavourJetTags:probbb')+bDiscriminator('pfDeepFlavourJetTags:problepb'))>0?bDiscriminator('pfDeepFlavourJetTags:probc')/(bDiscriminator('pfDeepFlavourJetTags:probc')+bDiscriminator('pfDeepFlavourJetTags:probb')+bDiscriminator('pfDeepFlavourJetTags:probbb')+bDiscriminator('pfDeepFlavourJetTags:problepb')):-1",float,doc="DeepJet c vs b+bb+lepb discriminator",precision=10),
    btagDeepFlavQG    = Var("?(pt>=15)&&(bDiscriminator('pfDeepFlavourJetTags:probg')+bDiscriminator('pfDeepFlavourJetTags:probuds'))>0?bDiscriminator('pfDeepFlavourJetTags:probg')/(bDiscriminator('pfDeepFlavourJetTags:probg')+bDiscriminator('pfDeepFlavourJetTags:probuds')):-1",float,doc="DeepJet g vs uds discriminator",precision=10),
)
ROBUSTPARTAK4VARS = cms.PSet(
    btagRobustParTAK4B     = Var("?(pt>=15)?bDiscriminator('pfParticleTransformerAK4JetTags:probb')+bDiscriminator('pfParticleTransformerAK4JetTags:probbb')+bDiscriminator('pfParticleTransformerAK4JetTags:problepb'):-1",float,doc="RobustParTAK4 b+bb+lepb tag discriminator",precision=10),
    btagRobustParTAK4C     = Var("?(pt>=15)?bDiscriminator('pfParticleTransformerAK4JetTags:probc'):-1",float,doc="RobustParTAK4 charm tag raw score",precision=10),
    btagRobustParTAK4G     = Var("?(pt>=15)?bDiscriminator('pfParticleTransformerAK4JetTags:probg'):-1",float,doc="RobustParTAK4 gluon tag raw score",precision=10),
    btagRobustParTAK4UDS = Var("?(pt>=15)?bDiscriminator('pfParticleTransformerAK4JetTags:probuds'):-1",float,doc="RobustParTAK4 uds tag raw score",precision=10),
    btagRobustParTAK4CvL = Var("?(pt>=15)&&(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds')+bDiscriminator('pfParticleTransformerAK4JetTags:probg'))>0?bDiscriminator('pfParticleTransformerAK4JetTags:probc')/(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds')+bDiscriminator('pfParticleTransformerAK4JetTags:probg')):-1",float,doc="RobustParTAK4 c vs uds+g discriminator",precision=10),
    btagRobustParTAK4CvB = Var("?(pt>=15)&&(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probb')+bDiscriminator('pfParticleTransformerAK4JetTags:probbb')+bDiscriminator('pfParticleTransformerAK4JetTags:problepb'))>0?bDiscriminator('pfParticleTransformerAK4JetTags:probc')/(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probb')+bDiscriminator('pfParticleTransformerAK4JetTags:probbb')+bDiscriminator('pfParticleTransformerAK4JetTags:problepb')):-1",float,doc="RobustParTAK4 c vs b+bb+lepb discriminator",precision=10),
    btagRobustParTAK4QG    = Var("?(pt>=15)&&(bDiscriminator('pfParticleTransformerAK4JetTags:probg')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds'))>0?bDiscriminator('pfParticleTransformerAK4JetTags:probg')/(bDiscriminator('pfParticleTransformerAK4JetTags:probg')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds')):-1",float,doc="RobustParTAK4 g vs uds discriminator",precision=10),
)
PARTICLENETAK4VARS = cms.PSet(
    particleNetAK4_B = Var("?(pt>=15)?bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:BvsAll'):-1",float,doc="ParticleNetAK4 tagger b vs all (udsg, c) discriminator",precision=10),
    particleNetAK4_CvsL = Var("?(pt>=15)?bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:CvsL'):-1",float,doc="ParticleNetAK4 tagger c vs udsg discriminator",precision=10),
    particleNetAK4_CvsB = Var("?(pt>=15)?bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:CvsB'):-1",float,doc="ParticleNetAK4 tagger c vs b discriminator",precision=10),
    particleNetAK4_QvsG = Var("?(pt>=15)?bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:QvsG'):-1",float,doc="ParticleNetAK4 tagger uds vs g discriminator",precision=10),
    particleNetAK4_G = Var("?(pt>=15)?bDiscriminator('pfParticleNetAK4JetTags:probg'):-1",float,doc="ParticleNetAK4 tagger g raw score",precision=10),
    particleNetAK4_puIdDisc = Var("?(pt>=15)?1-bDiscriminator('pfParticleNetAK4JetTags:probpu'):-1",float,doc="ParticleNetAK4 tagger pileup jet discriminator",precision=10),
)

CALOJETVARS = cms.PSet(P4Vars,
    area            = jetPuppiTable.variables.area,
    rawFactor = jetPuppiTable.variables.rawFactor,
    emf             = Var("emEnergyFraction()", float, doc = "electromagnetic energy fraction", precision = 10),
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
    getattr(proc,jetTaskName).add(getattr(proc, puJetIdVarsCalculator))

    #
    # Get the variables
    #
    SNUJetVar = "SNUJetVar{}".format(jetName)
    setattr(proc, SNUJetVar, cms.EDProducer("ProduceCustomJet",
            srcJet = cms.InputTag(jetSrc),
            srcPileupJetId = cms.InputTag(puJetIdVarsCalculator)
        )
    )
    getattr(proc,jetTaskName).add(getattr(proc, puJetIDVar))

    #
    # Save variables as userFloats and userInts for each jet
    #
    patJetWithUserData = "{}WithUserData".format(jetSrc)
    getattr(proc,patJetWithUserData).userFloats.SNU_dR2Mean    = cms.InputTag("{}:dR2Mean".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_majW         = cms.InputTag("{}:majW".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_minW         = cms.InputTag("{}:minW".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_frac01     = cms.InputTag("{}:frac01".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_frac02     = cms.InputTag("{}:frac02".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_frac03     = cms.InputTag("{}:frac03".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_frac04     = cms.InputTag("{}:frac04".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_ptD            = cms.InputTag("{}:ptD".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_beta         = cms.InputTag("{}:beta".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_pull         = cms.InputTag("{}:pull".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_jetR         = cms.InputTag("{}:jetR".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userFloats.SNU_jetRchg    = cms.InputTag("{}:jetRchg".format(puJetIDVar))
    getattr(proc,patJetWithUserData).userInts.SNU_nCharged     = cms.InputTag("{}:nCharged".format(puJetIDVar))

    #
    # Specfiy variables in the jet table to save in NanoAOD
    #
    getattr(proc,jetTableName).variables.SNU_dR2Mean    = SNUVARS.SNU_dR2Mean
    getattr(proc,jetTableName).variables.SNU_majW         = SNUVARS.SNU_majW
    getattr(proc,jetTableName).variables.SNU_minW         = SNUVARS.SNU_minW
    getattr(proc,jetTableName).variables.SNU_frac01     = SNUVARS.SNU_frac01
    getattr(proc,jetTableName).variables.SNU_frac02     = SNUVARS.SNU_frac02
    getattr(proc,jetTableName).variables.SNU_frac03     = SNUVARS.SNU_frac03
    getattr(proc,jetTableName).variables.SNU_frac04     = SNUVARS.SNU_frac04
    getattr(proc,jetTableName).variables.SNU_ptD            = SNUVARS.SNU_ptD
    getattr(proc,jetTableName).variables.SNU_beta         = SNUVARS.SNU_beta
    getattr(proc,jetTableName).variables.SNU_pull         = SNUVARS.SNU_pull
    getattr(proc,jetTableName).variables.SNU_jetR         = SNUVARS.SNU_jetR
    getattr(proc,jetTableName).variables.SNU_jetRchg    = SNUVARS.SNU_jetRchg
    getattr(proc,jetTableName).variables.SNU_nCharged = SNUVARS.SNU_nCharged

    return proc

def AddBTaggingScores(proc, jetTableName=""):
    """
    Store b-tagging scores from various algortihm
    """

    getattr(proc, jetTableName).variables.btagDeepFlavB     = DEEPJETVARS.btagDeepFlavB
    getattr(proc, jetTableName).variables.btagDeepFlavCvL = DEEPJETVARS.btagDeepFlavCvL
    getattr(proc, jetTableName).variables.btagDeepFlavCvB = DEEPJETVARS.btagDeepFlavCvB

    run2_nanoAOD_ANY.toModify(
        getattr(proc, jetTableName).variables,
        btagCSVV2 = Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",float,doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)",precision=10),
        btagDeepB = Var("?(bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'))>=0?bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'):-1",float,doc="DeepCSV b+bb tag discriminator",precision=10),
        btagDeepCvL = Var("?bDiscriminator('pfDeepCSVJetTags:probc')>=0?bDiscriminator('pfDeepCSVJetTags:probc')/(bDiscriminator('pfDeepCSVJetTags:probc')+bDiscriminator('pfDeepCSVJetTags:probudsg')):-1", float,doc="DeepCSV c vs udsg discriminator",precision=10),
        btagDeepCvB = Var("?bDiscriminator('pfDeepCSVJetTags:probc')>=0?bDiscriminator('pfDeepCSVJetTags:probc')/(bDiscriminator('pfDeepCSVJetTags:probc')+bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')):-1",float,doc="DeepCSV c vs b+bb discriminator",precision=10)
    )

    return proc

def AddDeepJetGluonLQuarkScores(proc, jetTableName=""):
    """
    Store DeepJet raw score in jetTable for gluon and light quark
    """

    getattr(proc, jetTableName).variables.btagDeepFlavG     = DEEPJETVARS.btagDeepFlavG
    getattr(proc, jetTableName).variables.btagDeepFlavUDS = DEEPJETVARS.btagDeepFlavUDS
    getattr(proc, jetTableName).variables.btagDeepFlavQG    = DEEPJETVARS.btagDeepFlavQG

    return proc

def AddRobustParTAK4Scores(proc, jetTableName=""):
    """
    Store RobustParTAK4 scores in jetTable
    """

    getattr(proc, jetTableName).variables.btagRobustParTAK4B = ROBUSTPARTAK4VARS.btagRobustParTAK4B
    getattr(proc, jetTableName).variables.btagRobustParTAK4CvL = ROBUSTPARTAK4VARS.btagRobustParTAK4CvL
    getattr(proc, jetTableName).variables.btagRobustParTAK4CvB = ROBUSTPARTAK4VARS.btagRobustParTAK4CvB

    return proc

def AddParticleNetAK4Scores(proc, jetTableName=""):
    """
    Store ParticleNetAK4 scores in jetTable
    """

    getattr(proc, jetTableName).variables.particleNetAK4_B = PARTICLENETAK4VARS.particleNetAK4_B
    getattr(proc, jetTableName).variables.particleNetAK4_CvsL = PARTICLENETAK4VARS.particleNetAK4_CvsL
    getattr(proc, jetTableName).variables.particleNetAK4_CvsB = PARTICLENETAK4VARS.particleNetAK4_CvsB
    getattr(proc, jetTableName).variables.particleNetAK4_QvsG = PARTICLENETAK4VARS.particleNetAK4_QvsG
    getattr(proc, jetTableName).variables.particleNetAK4_G = PARTICLENETAK4VARS.particleNetAK4_G
    getattr(proc, jetTableName).variables.particleNetAK4_puIDDisc = PARTICLENETAK4VARS.particleNetAK4_puIdDisc

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
    process = AddCustomJetVars(process)
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
