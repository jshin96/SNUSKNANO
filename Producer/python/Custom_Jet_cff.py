import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.simpleCandidateFlatTableProducer_cfi import simpleCandidateFlatTableProducer
from PhysicsTools.PatAlgos.tools.jetCollectionTools import GenJetAdder, RecoJetAdder

from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.jetsAK4_Puppi_cff import jetPuppiTable, finalJetsPuppi, jetPuppiCorrFactorsNano, updatedJetsPuppi, updatedJetsPuppiWithUserData, jetPuppiTask, jetPuppiTablesTask
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
    AK4PuppiJetSpecialVariablesLabel = "AK4PuppiJetVariables"
    setattr(process,AK4PuppiJetSpecialVariablesLabel,cms.EDProducer("AK4PuppiJetSpecialVariables",
                                jetSrc=cms.InputTag("finalJetsPuppi")
				)
    )
    getattr(process,"jetPuppiTask").add(getattr(process,AK4PuppiJetSpecialVariablesLabel))
#
    process.updatedJetsPuppiWithUserData.src = cms.InputTag('AK4PuppiJetVariables')
    process.updatedJetsPuppiWithUserData.userFloats.chg_frac = cms.InputTag('AK4PuppiJetSpecialVariables:chgfrac')
#    print(process.jetPuppiTask.moduleNames())


#    process.jetPuppiTable.variables.chg_frac = Var("userFloat('chgfrac')",float,doc="fraction of momentum carried by charged PFCands")
    process.jetPuppiTable.variables.CorrectedPt = Var(" correctedJet('L2Relative','UDS').pt() ", float, doc = "pt of the L2Relative level corrected UDS jet", precision=14)
    

    return process



def IncreaseGenPrecesion(process):
    
    process.genParticleTable.variables.pt = Var("pt",  float, precision=16)
    process.genParticleTable.variables.eta = Var("eta",  float,precision=16)
    process.genParticleTable.variables.phi = Var("phi", float,precision=16)
    
    return process

def PrepAK4JetPuppiCustomNanoAOD(process):
    process = AddVariablesForAK4PuppiJet(process)



    return process
