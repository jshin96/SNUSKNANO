#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/MuonReco/interface/MuonSimInfo.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/UserData.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "PhysicsTools/PatAlgos/interface/PATUserDataMerger.h"


class AK4PuppiJetSpecialVariables : public edm::stream::EDProducer<> {
public:
  explicit AK4PuppiJetSpecialVariables(const edm::ParameterSet &iConfig);
  
  ~AK4PuppiJetSpecialVariables() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  void produce(edm::Event &iEvent, const edm::EventSetup &iSetup) override;
  edm::EDGetTokenT<std::vector<pat::Jet>> jetSrc_;
  pat::Jet CalculatePFCands(pat::Jet jet);
};

AK4PuppiJetSpecialVariables::AK4PuppiJetSpecialVariables(const edm::ParameterSet& iConfig) : 
    jetSrc_(consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetSrc"))) {
    produces<std::vector<pat::Jet>>();
}

AK4PuppiJetSpecialVariables::~AK4PuppiJetSpecialVariables() = default;

pat::Jet AK4PuppiJetSpecialVariables::CalculatePFCands(pat::Jet jet) {

  std::vector<reco::CandidatePtr> const &daughters = jet.daughterPtrVector();
  float chg_frac(0.0);
  for (const auto &cand : daughters) {
    
    if (cand->charge() != 0) {
      chg_frac+=cand->pt();
    }

  }
  chg_frac = chg_frac/jet.pt();
  jet.addUserFloat("chg_frac", chg_frac);
  return jet;
}

void AK4PuppiJetSpecialVariables::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {

  std::unique_ptr<std::vector<pat::Jet>> out(new std::vector<pat::Jet>());
  edm::Handle<std::vector<pat::Jet>> jets;
  iEvent.getByToken(jetSrc_, jets);

  out->reserve(jets->size());

  for (const auto& jet : *jets) {
    pat::Jet jetcopy = jet;
    jetcopy = CalculatePFCands(jetcopy);
    out->push_back(jetcopy);
  }
  iEvent.put(std::move(out));
}

void AK4PuppiJetSpecialVariables::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    edm::ParameterSetDescription desc;
    descriptions.add("AK4PuppiJetSpecialVariables", desc);
}


DEFINE_FWK_MODULE(AK4PuppiJetSpecialVariables);


