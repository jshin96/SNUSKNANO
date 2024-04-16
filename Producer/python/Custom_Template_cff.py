import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.simpleCandidateFlatTableProducer_cfi import simpleCandidateFlatTableProducer

from PhysicsTools.NanoAOD.common_cff import Var, P3Vars, P4Vars
from PhysicsTools.NanoAOD.muons_cff import muonTable, finalMuons
from PhysicsTools.NanoAOD.triggerObjects_cff import triggerObjectTable, mksel

def Custom_Muon_Task(process):
    process.nanoTableTaskCommon.remove(process.electronTablesTask)
    process.nanoTableTaskCommon.remove(process.lowPtElectronTablesTask)
    process.nanoTableTaskCommon.remove(process.photonTablesTask)
    process.nanoTableTaskCommon.remove(process.metTablesTask)
    process.nanoTableTaskCommon.remove(process.tauTablesTask)
    process.nanoTableTaskCommon.remove(process.boostedTauTablesTask)
    process.nanoTableTaskCommon.remove(process.jetPuppiTablesTask)
    process.nanoTableTaskCommon.remove(process.jetAK8TablesTask)

    process.nanoTableTaskFS.remove(process.electronMCTask)
    process.nanoTableTaskFS.remove(process.lowPtElectronMCTask)
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

    

def AddVariablesForMuon(proc):
    
    muonWithVariables = "muonWithVariables"
    setattr(proc, muonWithVariables, cms.EDProducer("MuonSpecialVariables",
                    muonSrc=cms.InputTag("slimmedMuons"),
                    vertexSrc=cms.InputTag("offlineSlimmedPrimaryVertices"),
                    trkSrc=cms.InputTag("pfTracks"),
                    )
    )
    getattr(proc,"muonTask").add(getattr(proc,muonWithVariables))
    
    proc.slimmedMuonsUpdated.src = cms.InputTag("muonWithVariables")
    #proc.muonMVATTH.src = cms.InputTag("muonWithVariables") 
    #proc.muonMVALowPt.src = cms.InputTag("muonWithVariables") 
    #proc.muonTable.src = cms.InputTag("muonWithVariables") 
    #proc.muonMCTable.src = cms.InputTag("muonWithVariables") 
    #proc.muonsMCMatchForTable.src = cms.InputTag("muonWithVariables") 
  
 
    #SandAlone Variables
    proc.muonTable.variables.standalonePt = Var("? standAloneMuon().isNonnull() ? standAloneMuon().pt() : -1", float, doc = "pt of the standalone muon", precision=14)
    proc.muonTable.variables.standaloneEta = Var("? standAloneMuon().isNonnull() ? standAloneMuon().eta() : -99", float, doc = "eta of the standalone muon", precision=14)
    proc.muonTable.variables.standalonePhi = Var("? standAloneMuon().isNonnull() ? standAloneMuon().phi() : -99", float, doc = "phi of the standalone muon", precision=14)
    proc.muonTable.variables.standaloneCharge = Var("? standAloneMuon().isNonnull() ? standAloneMuon().charge() : -99", float, doc = "phi of the standalone muon", precision=14)
    
    return proc

def AddTriggerObjectBits(process): 
    process.triggerObjectTable.selections.Muon_POG = cms.PSet(
            id = cms.int32(1313),
            sel = cms.string("type(83) && pt > 5 && (coll('hltIterL3MuonCandidates') || (pt > 45 && coll('hltHighPtTkMuonCands')) || (pt > 95 && coll('hltOldL3MuonCandidates')))"),
            l1seed = cms.string("type(-81)"), l1deltaR = cms.double(0.5),
            l2seed = cms.string("type(83) && coll('hltL2MuonCandidates')"),  l2deltaR = cms.double(0.3),
            skipObjectsNotPassingQualityBits = cms.bool(True),
            qualityBits = cms.VPSet(
                mksel("filter('hltTripleMuonL2PreFiltered0')","hltTripleMuonL2PreFiltered0"), #0
                mksel("filter('hltTripleMuL3PreFiltered222')","hltTripleMuL3PreFiltered222"), #1
                mksel("filter('hltJpsiMuonL3Filtered3p5')","hltJpsiMuonL3Filtered3p5"), #2 
                mksel("filter('hltVertexmumuFilterJpsiMuon3p5')","hltVertexmumuFilterJpsiMuon3p5"), #3
                mksel("filter('hltL2fL1sDoubleMu0er15OSIorDoubleMu0er14OSIorDoubleMu4OSIorDoubleMu4p5OSL1Filtered0')","hltL2fL1sDoubleMu0er15OSIorDoubleMu0er14OSIorDoubleMu4OSIorDoubleMu4p5OSL1Filtered0"), #4
                mksel("filter('hltDoubleMu4JpsiDisplacedL3Filtered')","hltDoubleMu4JpsiDisplacedL3Filtered"), #5
                mksel("filter('hltDisplacedmumuFilterDoubleMu4Jpsi')","hltDisplacedmumuFilterDoubleMu4Jpsi"), #6
                mksel("filter('hltJpsiTkVertexFilter')","hltJpsiTkVertexFilter"), #7
                mksel("filter('hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07')","hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07"), #8
                mksel("filter('hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p08')","hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p08"), #9
                mksel("filter('hltL3fL1DoubleMu155fPreFiltered8')","hltL3fL1DoubleMu155fPreFiltered8"), #10
                mksel("filter('hltL3fL1DoubleMu155fFiltered17')","hltL3fL1DoubleMu155fFiltered17"), #11
                mksel("filter('hltDiMuon178RelTrkIsoFiltered0p4')","hltDiMuon178RelTrkIsoFiltered0p4"), #12
                mksel("filter('hltDiMuon178RelTrkIsoFiltered0p4DzFiltered0p2')","hltDiMuon178RelTrkIsoFiltered0p4DzFiltered0p2"), #13
                mksel("filter('hltDiMuon178RelTrkIsoVVLFiltered')","hltDiMuon178RelTrkIsoVVLFiltered"), #14
                mksel("filter('hltDiMuon178RelTrkIsoVVLFilteredDzFiltered0p2')","hltDiMuon178RelTrkIsoVVLFilteredDzFiltered0p2"), #15
                mksel("filter('hltDiMuon178Mass3p8Filtered')","hltDiMuon178Mass3p8Filtered"), #16
                mksel("filter('hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q')","hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q"), #17
                mksel("filter('hltL2fOldL1sMu22or25L1f0L2Filtered10Q')","hltL2fOldL1sMu22or25L1f0L2Filtered10Q"), #18
                mksel("filter('hltL3fL1sMu22Or25L1f0L2f10QL3Filtered100Q')","hltL3fL1sMu22Or25L1f0L2f10QL3Filtered100Q"), #19
                mksel("filter('hltL3fL1sMu25f0TkFiltered100Q')","hltL3fL1sMu25f0TkFiltered100Q"), #20
                mksel("filter('hltL3fL1sMu15DQlqL1f0L2f10L3Filtered17')","hltL3fL1sMu15DQlqL1f0L2f10L3Filtered17"), #21
                mksel("filter('hltL3fL1sMu1lqL1f0L2f10L3Filtered17TkIsoFiltered0p4')","hltL3fL1sMu1lqL1f0L2f10L3Filtered17TkIsoFiltered0p4"), #22
                mksel("filter('hltL3fL1sMu1lqL1f0L2f10L3Filtered17TkIsoVVLFiltered')","hltL3fL1sMu1lqL1f0L2f10L3Filtered17TkIsoVVLFiltered"), #23
                mksel("filter('hltL3fL1sMu5L1f0L2f5L3Filtered8')","hltL3fL1sMu5L1f0L2f5L3Filtered8"), #24
                mksel("filter('hltL3fL1sMu5L1f0L2f5L3Filtered8TkIsoFiltered0p4')","hltL3fL1sMu5L1f0L2f5L3Filtered8TkIsoFiltered0p4"), #25
                mksel("filter('hltL3fL1sMu5L1f0L2f5L3Filtered8TkIsoVVLFiltered')","hltL3fL1sMu5L1f0L2f5L3Filtered8TkIsoVVLFiltered"), #26
                mksel("filter('hltL3fL1sMu15DQlqL1f0L2f10L3Filtered12')","hltL3fL1sMu15DQlqL1f0L2f10L3Filtered12"), #27
                mksel("filter('hltL3fL1sMu15DQlqL1f0L2f10L3Filtered15')","hltL3fL1sMu15DQlqL1f0L2f10L3Filtered15"), #28
                mksel("filter('hltL3fL1sMu15DQlqL1f0L2f10L3Filtered19')","hltL3fL1sMu15DQlqL1f0L2f10L3Filtered19"), #29
                mksel("filter('hltL3fL1sMu15DQlqL1f0L2f10L3Filtered19')","hltL3fL1sMu15DQlqL1f0L2f10L3Filtered19") #30
            )
        )

    process.triggerObjectTable.selections.Muon_POG_v2 = cms.PSet(
            id = cms.int32(131313),
            sel = cms.string("type(83) && pt > 5 && (coll('hltIterL3MuonCandidates') || (pt > 45 && coll('hltHighPtTkMuonCands')) || (pt > 95 && coll('hltOldL3MuonCandidates')))"),
            l1seed = cms.string("type(-81)"), l1deltaR = cms.double(0.5),
            l2seed = cms.string("type(83) && coll('hltL2MuonCandidates')"),  l2deltaR = cms.double(0.3),
            skipObjectsNotPassingQualityBits = cms.bool(True),
            qualityBits = cms.VPSet(
                mksel("filter('hltL3fL1sSingleMuOpenCandidateL1f0L2f3QL3Filtered50Q')","hltL3fL1sSingleMuOpenCandidateL1f0L2f3QL3Filtered50Q"), #0
                mksel("filter('hltTrk200MuonEndcapFilter')","hltTrk200MuonEndcapFilter") #1
            )
        )

    return process

def IncreaseGenPrecesion(process):
    
    process.genParticleTable.variables.pt = Var("pt",  float, precision=16)
    process.genParticleTable.variables.eta = Var("eta",  float,precision=16)
    process.genParticleTable.variables.phi = Var("phi", float,precision=16)
    
    return process

def PrepMuonCustomNanoAOD(process):
    
    process = Custom_Muon_Task(process)
    process = AddPFTracks(process)
    process = AddVariablesForMuon(process)
    process = AddTriggerObjectBits(process)
    process = IncreaseGenPrecesion(process)


    return process
