import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.simpleCandidateFlatTableProducer_cfi import simpleCandidateFlatTableProducer

from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.photons_cff import *
from PhysicsTools.NanoAOD.triggerObjects_cff import triggerObjectTable, mksel

def Custom_Photon_Task(process):
    process.nanoTableTaskCommon.remove(process.metTablesTask)
    process.nanoTableTaskCommon.remove(process.tauTablesTask)
    process.nanoTableTaskCommon.remove(process.boostedTauTablesTask)
    process.nanoTableTaskCommon.remove(process.jetPuppiTablesTask)
    process.nanoTableTaskCommon.remove(process.jetAK8TablesTask)

    process.nanoTableTaskFS.remove(process.photonMCTask)
    process.nanoTableTaskFS.remove(process.jetMCTask)
    process.nanoTableTaskFS.remove(process.tauMCTask)
    process.nanoTableTaskFS.remove(process.boostedTauMCTask)
    process.nanoTableTaskFS.remove(process.metMCTable)
    process.nanoTableTaskFS.remove(process.ttbarCatMCProducersTask)
    process.nanoTableTaskFS.remove(process.ttbarCategoryTableTask)
    
    return process

def AddPFTracks(proc):
    pfTracks = "pfTracks"
    setattr(proc, pfTracks, cms.EDProducer("pfTracksProducer",
                    PFCands=cms.InputTag("packedPFCandidates"),
                    lostTracks=cms.InputTag("lostTracks"),
                    TrkHPurity = cms.bool(False),
                    trkSelection = cms.string("bestTrack.pt()>5 && abs(bestTrack.eta())<2.4 "),
                   )
    )
    
    pfTracksTable = "pfTracksTable"
    setattr(proc, pfTracksTable, cms.EDProducer("SimpleTrackFlatTableProducer",
                        src = cms.InputTag("pfTracks"),
                        cut = cms.string("pt > 15"), # filtered already above
                        name = cms.string("Track"),
                        doc  = cms.string("General tracks with pt > 15 GeV"),
                        singleton = cms.bool(False), # the number of entries is variable
                        extension = cms.bool(False), # this is the main table for the muons
                        variables = cms.PSet(P3Vars,
                            dz = Var("dz",float,doc="dz (with sign) wrt first PV, in cm",precision=10),
                            dxy = Var("dxy",float,doc="dxy (with sign) wrt first PV, in cm",precision=10),
                            charge = Var("charge", int, doc="electric charge"),
                            normChiSq = Var("normalizedChi2", float, precision=14, doc="Chi^2/ndof"),
                            numberOfValidHits = Var('numberOfValidHits()', 'int', precision=-1, doc='Number of valid hits in track'),
                            numberOfLostHits = Var('numberOfLostHits()', 'int', precision=-1, doc='Number of lost hits in track'),
                            trackAlgo = Var('algo()', 'int', precision=-1, doc='Track algo enum, check DataFormats/TrackReco/interface/TrackBase.h for details.'),
                            trackOriginalAlgo = Var('originalAlgo()', 'int', precision=-1, doc='Track original algo enum'),
                            qualityMask = Var('qualityMask()', 'int', precision=-1, doc='Quality mask of the track.'),
                            extraIdx = Var('extra().key()', 'int', precision=-1, doc='Index of the TrackExtra in the original collection'),
                            vx = Var('vx', 'float', precision=-1, doc='Track X position'),
                            vy = Var('vy', 'float', precision=-1, doc='Track Y position'),
                            vz = Var('vz', 'float', precision=-1, doc='Track Z position'),
                           ),
                 )
    )
    
    pfTracksTask = "pfTracksTask"
    setattr(proc,pfTracksTask, cms.Task(
        getattr(proc,pfTracks)
       )
    )
  
    pfTracksTableTask = "pfTracksTableTask"
    setattr(proc,pfTracksTableTask, cms.Task(
        getattr(proc,pfTracksTable)
      ) 
    )
    proc.nanoTableTaskCommon.add(getattr(proc,pfTracksTask))
    proc.nanoTableTaskCommon.add(getattr(proc,pfTracksTableTask))
  
    return proc

    

def AddVariablesForPhoton(proc):
    
#    photonWithVariables = "photonWithVariables"
#    setattr(proc, photonWithVariables, cms.EDProducer("MuonSpecialVariables",
#                    photonSrc=cms.InputTag("finalPhotons"),
#                    vertexSrc=cms.InputTag("offlineSlimmedPrimaryVertices"),
#                    trkSrc=cms.InputTag("pfTracks"),
#                    )
#    )
#    getattr(proc,"photonTask").add(getattr(proc,photonWithVariables))
    
#    proc.slimmedMuonsUpdated.src = cms.InputTag("photonWithVariables")
  
 
    proc.photonTable.variables.trackMomentum = Var("trackMomentumAtVtx().R()",float,doc="trackMomentum at vertex",precision=10)
    
    return proc

def AddTriggerObjectBits(process): 

    return process

def IncreaseGenPrecesion(process):
    
    process.genParticleTable.variables.pt = Var("pt",  float, precision=16)
    process.genParticleTable.variables.eta = Var("eta",  float,precision=16)
    process.genParticleTable.variables.phi = Var("phi", float,precision=16)
    
    return process

def PrepMuonCustomNanoAOD(process):
    
#    process = Custom_Photon_Task(process)
#    process = AddPFTracks(process)
    process = AddVariablesForPhoton(process)
#    process = AddTriggerObjectBits(process)
#    process = IncreaseGenPrecesion(process)


    return process
