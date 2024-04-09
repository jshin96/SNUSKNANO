#
# Reference: RecoJets/JetProducers/python/PileupJetID_cfi.py
#
import FWCore.ParameterSet.Config as cms


# Calculate+store variables and run MVAs
CustomJet = cms.EDProducer('ProduceCustomJet',
     SNUjet = cms.InputTag(""),
     jets = cms.InputTag("ak4PFJetsPUPPI"),
     vertexes = cms.InputTag("offlinePrimaryVertices"),
     rho     = cms.InputTag("fixedGridRhoFastjetAll"),
     jec     = cms.string("AK4PFpuppi"),
     applyJec = cms.bool(True),
     inputIsCorrected = cms.bool(False),
     residualsFromTxt = cms.bool(False),
     srcConstituentWeights = cms.InputTag(""),
#     residualsTxt     = cms.FileInPath("RecoJets/JetProducers/data/download.url") # must be an existing file
)



CustomJetTask = cms.Task(CustomJet)
