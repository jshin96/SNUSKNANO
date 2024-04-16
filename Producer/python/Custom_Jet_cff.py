import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.simpleCandidateFlatTableProducer_cfi import simpleCandidateFlatTableProducer
from PhysicsTools.PatAlgos.tools.jetCollectionTools import GenJetAdder, RecoJetAdder
from SNUSKNANO.Producer.AK4PuppiJetSpecialVariables_cfi import AK4PuppiJetSpecialVariables

from PhysicsTools.NanoAOD.common_cff import Var, P3Vars, P4Vars, CandVars
from PhysicsTools.NanoAOD.jetsAK4_Puppi_cff import jetPuppiTable, finalJetsPuppi, jetPuppiCorrFactorsNano, updatedJetsPuppi, updatedJetsPuppiWithUserData
from PhysicsTools.NanoAOD.triggerObjects_cff import triggerObjectTable, mksel

def Reset_Task(process):
    #list unnecessary tasks listed in https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nano_cff.py
    process.nanoTableTaskCommon.remove(process.electronTablesTask)
    process.nanoTableTaskCommon.remove(process.lowPtElectronTablesTask)
    process.nanoTableTaskCommon.remove(process.photonTablesTask)
    process.nanoTableTaskCommon.remove(process.metTablesTask)
    process.nanoTableTaskCommon.remove(process.tauTablesTask)
    process.nanoTableTaskCommon.remove(process.boostedTauTablesTask)

    process.nanoTableTaskFS.remove(process.electronMCTask)
    process.nanoTableTaskFS.remove(process.lowPtElectronMCTask)
    process.nanoTableTaskFS.remove(process.photonMCTask)
    process.nanoTableTaskFS.remove(process.tauMCTask)
    process.nanoTableTaskFS.remove(process.boostedTauMCTask)
    process.nanoTableTaskFS.remove(process.metMCTable)
    
    return process



def AddVariablesForAK4PuppiJet(process):
    CustomPuppiVar = "CustomPuppiVar"
    setattr(process, CustomPuppiVar, cms.EDProducer("AK4PuppiJetSpecialVariables",
        jetSrc = cms.InputTag("updatedJetsPuppi")
        )
    )

    updatedJetsPuppiWithUserData.userFloats.chg_frac = cms.InputTag("CustomPuppiVar:chg_frac")



#    getattr(process,"jetPuppiTable").variables.chg_frac = Var(" userFloat('chg_frac') ", float, doc = "fraction of pt carried by charged PFCandidates")



    process.jetPuppiTable.variables.CorrectedPt = Var(" correctedJet('L2Relative','UDS').pt() ", float, doc = "pt of the L2Relative level corrected UDS jet", precision=14)

    getattr(process, "jetPuppiTask").add(getattr(process,CustomPuppiVar))
    return process



def IncreaseGenPrecesion(process):
    
    process.genParticleTable.variables.pt = Var("pt",  float, precision=16)
    process.genParticleTable.variables.eta = Var("eta",  float,precision=16)
    process.genParticleTable.variables.phi = Var("phi", float,precision=16)
    
    return process

def PrepAK4JetPuppiCustomNanoAOD(process):
    process = Reset_Task(process)
    process = AddVariablesForAK4PuppiJet(process)


    return process
