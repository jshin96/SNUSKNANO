
#include <memory>
#include <iostream>

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/UserData.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "PhysicsTools/PatAlgos/interface/PATUserDataMerger.h"

class AK4PuppiJetSpecialVariables : public edm::stream::EDProducer<> {
public:
  explicit AK4PuppiJetSpecialVariables(const edm::ParameterSet&);
  ~AK4PuppiJetSpecialVariables() override {}

  float jetPFCalculator(pat::Jet &jet) const;

private:
  void produce(edm::Event &iEvent, const edm::EventSetup &iSetup) override;
  template <typename T>
  void putInEvent(const std::string&, const edm::Handle<std::vector<pat::Jet>>&, std::vector<T>, edm::Event&) const;   
  edm::EDGetToken jetSrc_;
};
AK4PuppiJetSpecialVariables::AK4PuppiJetSpecialVariables(const edm::ParameterSet& iConfig)
    : jetSrc_(consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetSrc"))) {
        produces<std::vector<pat::Jet>>();
//        produces<edm::ValueMap<float>>("chgfrac");
  }
float AK4PuppiJetSpecialVariables::jetPFCalculator(pat::Jet &jet) const {

  std::vector<reco::CandidatePtr> const &daughters = jet.daughterPtrVector();
  float temp_chg_frac(0.0);
  for (const auto &cand : daughters) {
    if (cand->charge() != 0) {
      temp_chg_frac+=cand->pt();
    }

  }
  temp_chg_frac = temp_chg_frac/jet.pt();
  return temp_chg_frac;
}

void AK4PuppiJetSpecialVariables::produce(edm::Event& iEvent, const edm::EventSetup &iSetup) {
  edm::Handle<std::vector<pat::Jet>> jetSrc;
  iEvent.getByToken(jetSrc_, jetSrc);

  std::vector<float> v_chg_frac;
  std::unique_ptr<std::vector<pat::Jet>> jetCollection(new std::vector<pat::Jet>(*jetSrc));
  v_chg_frac.reserve(jetCollection->size());
  auto out_chg_frac = std::make_unique<edm::ValueMap<float>>();
    
  std::unique_ptr<std::vector<pat::Jet>> outjet(new std::vector<pat::Jet>());
  outjet->reserve(jetCollection->size());
  for (unsigned int i=0; i < jetCollection->size(); i++) {
    pat::Jet &jet = (*jetCollection).at(i);
    jet.addUserFloat("chgfrac",jetPFCalculator(jet));
//    v_chg_frac.push_back(jetPFCalculator(jet));
    outjet->push_back(jet);
  }
//  putInEvent("chgfrac", jetSrc, v_chg_frac, iEvent);
  iEvent.put(std::move(outjet));
}
template <typename T>
void AK4PuppiJetSpecialVariables::putInEvent(const std::string& name,
                                  const edm::Handle<std::vector<pat::Jet>>& jets,
                                  std::vector<T> product,
                                  edm::Event& iEvent) const {
  auto out = std::make_unique<edm::ValueMap<T>>();
  typename edm::ValueMap<T>::Filler filler(*out);
  filler.insert(jets, product.begin(), product.end());
  filler.fill();
  iEvent.put(std::move(out), name);
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(AK4PuppiJetSpecialVariables);


