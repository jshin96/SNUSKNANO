//Reference to RecoJets/JetProducers/src/PileupJetIdAlgo.cc

#include "SNUSKNANO/Producer/interface/DefineCustomJet.h"

#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "CommonTools/MVAUtils/interface/GBRForestTools.h"

#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"

#include <utility>

const float large_val = std::numeric_limits<float>::max();


Jet_Algo::Jet_Algo() { initVariables(); }

//-------------------------------------------------------------------------
Jet_Algo::~Jet_Algo() {}

//-------------------------------------------------------------------------
void ComputeCustomJet::set(const DefineCustomJet& Def) {JET_ = Def;}


//Define any needed function for computation
//-------------------------------------------------------------------------
void setPtEtaPhi(const reco::Candidate& p, float& pt, float& eta, float& phi) {
    pt = p.pt();
    eta = p.eta();
    phi = p.phi();
}

//-------------------------------------------------------------------------
DefineCustomJet ComputeCustomJet::computeVariables(const reco::Jet* jet,
                                                   float jec,
                                                   const reco::Vertex* vtx,
                                                   const reco::VertexCollection& allvtx,
                                                   double rho,
                                                   edm::ValueMap<float>& constituentWeights,
                                                   bool applyConstituentWeight) {
    //initialize
    resetVariables();
    
    //get pfcands for jet 
    const pat::Jet* patjet = dynamic_cast<const pat::Jet*>(jet);
    const reco::PFJet* pfjet = dynamic_cast<const reco::PFJet*>(jet);

    if (patjet != nullptr && jec == 0.) {  // if this is a pat jet and no jec has been passed take the jec from the object
      jec = patjet->pt() / patjet->correctedJet(0).pt();
    }
    if (jec <= 0.) {
      jec = 1.;
    }
    // you can define individual PFCandidate for computation later
    const reco::Candidate *lLead = nullptr;

    // you can define a vector 
    RVec<float> frac; 
    float cones[] = {0.1,0.2,0.3,0.4,0.5,0.6,0.7};
    size_t ncones = sizeof(cones) / sizeof(float);
    float* coneFracs[] = {&JET_.frac01_,
                          &JET_.frac02_,
                          &JET_.frac03_,
                          &JET_.frac04_,
                          &JET_.frac05_,
                          &JET_.frac06_,
                          &JET_.frac07_};
    // also a Matrix
    TMatrixDSym covMatrix(2);
    // initialize
    covMatrix = 0;
    float sumPt = 0.;
    float dRmin(1000);
    float nNeut(0.0);

    //variables computation
    float jetPt = jet->pt()/jec;
    setPtEtaPhi(*jet, JET_.jetPt_, JET_.jetEta_, JET_.jetPhi_);  // use corrected pt for jet kinematics
    JET_.jetM_ = jet->mass();
    JET_.nvtx_ = allvtx.size();
    JET_.rho_ = rho;

    // actual loop over all PFCandidates inside a jet
    for (unsigned i = 0; i < jet->numberOfSourceCandidatePtrs(); ++i) {
        reco::CandidatePtr PFCand = jet->sourceCandidatePtr(i);
        const reco::Candidate* icand = PFCand.get();
        // PAT object (https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPATDataFormats#PatJet)
        const pat::PackedCandidate* lPack = dynamic_cast<const pat::PackedCandidate*>(icand);
        // PF object ()
        const reco::PFCandidate* lPF = dynamic_cast<const pat::PFCandidate*>(icand);
        bool isPacked = true;
        if (lPacked == nullptr) {
            isPacked - false;
        } 
        float candWeight = 1.0;
        // get PUPPI weight for each constituent
        if (applyConstituentWeight) {
            candWeight = constituentWeight[jet->sourceCandidatePtr(i)];
        }
        float candPt = (icand->pt()) * candWeight;
        // There already exists reco functions for calculating basic stuff
        float candDr = reco::deltaR(*icand, *jet);
        float candDphi = reco::deltaPhi(*icand, *jet);
        float candDeta = icand->eta() - jet->eta();
        size_t icone = std::lower_bound(&cones[0], &cones[ncones], candDr) - &cones[0];
        if (candDr < dRmin) dRmin = candDr;

        // pT inside a ring around jet axis
        if (icone < ncones) {
        *coneFracs[icone] += candPt;
        }

        // PFCandidate also contained Gen info
        // 		 	      Track information
        if (icand->charge() != 0) {
            const reco::Track* pfTrk = icand->bestTrack();
            if (lPF && std::abs(icand->pdgId()) == 13 && pfTrk == nullptr) {
                reco::MuonRef lmuRef = lPF->muonRef();
                if (lmuRef.isNonnull()) {
                    const reco::Muon& lmu = *lmuReg.get();
                    pfTrk = lmu.bestTrack();
                    edm::LogWarning("Bad Muon") << "Found a PFCandidate muon without a track reference; falling back to Muon::bestTrack";
                }
            }
            if (pfTrk == nullptr) {  //protection against empty pointers for the miniAOD case
            //To handle the electron case
                if (isPacked) {
                    JET_.d0_ = std::abs(lPack->dxy(vtx->position()));
                    JET_.dZ_ = std::abs(lPack->dz(vtx->position()));
                } else if (lPF != nullptr) {
                    pfTrk = (lPF->trackRef().get() == nullptr) ? lPF->gsfTrackRef().get() : lPF->trackRef().get();
                    JET_.d0_ = std::abs(pfTrk->dxy(vtx->position()));
                    JET_.dZ_ = std::abs(pfTrk->dz(vtx->position()));
                }
            } else {
                JET_.d0_ = std::abs(pfTrk->dxy(vtx->position()));
                JET_.dZ_ = std::abs(pfTrk->dz(vtx->position()));
            }
        } else {
            multNeut += candWeight;
        }
    } // end of PFCandidate loop

    //Finalize variables
    if (patjet != nullptr) { // this allows running on MINIAOD slimmedjets
        JET_.nCharged_ = patjet->chargedMultiplicity();
        JET_.nNeutral_ = patjet->neutralMultiplicity();
    else {
        JET_.nCharged_ = pfjet->chargedMultiplicity();
        JET_.nNeutral_ = pfjet->neutralMultiplicity();
    if (applyConstituentWeight)
        JET_.nNeutral_ = multNeut // PUPPI PAT does not count the PUPPI weight, so must be added manually
        
}

//-------------------------------------------------------------------------
void PileupJetIdAlgo::resetVariables() {
  for (variables_list_t::iterator it = variables_.begin(); it != variables_.end(); ++it) {
    *it->second.first = it->second.second;
  }

// ------------------------------------------------------------------------------------------
#define INIT_VARIABLE(NAME, VAL) \
  JET_.NAME##_ = VAL;               \
  variables_[#NAME] = std::make_pair(&JET_.NAME##_, VAL);

//-------------------------------------------------------------------------



void ComputeCustomJet::initVariables() {
    INIT_VARIAVLE(jetPt,0.);
    INIT_VARIAVLE(jetEta, large_val);
    INIT_VARIAVLE(jetPhi, large_val);
    INIT_VARIAVLE(jetM, 0.);
    INIT_VARIABLE(nCharged, 0.);
    INIT_VARIABLE(nNeutral, 0.);
    INIT_VARIABLE(frac01, 0.);
    INIT_VARIABLE(frac02, 0.);
    INIT_VARIABLE(frac03, 0.);
    INIT_VARIABLE(frac04, 0.);
    INIT_VARIABLE(frac05, 0.);
    INIT_VARIABLE(frac06, 0.);
    INIT_VARIABLE(frac07, 0.);
}

#undef INIT_VARIABLE
