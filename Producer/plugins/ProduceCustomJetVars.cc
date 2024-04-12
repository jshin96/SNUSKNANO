#include <memory>
#include <vector>

#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "SNUSKNANO/Producer/plugins/ProduceCustomJet.h"

class ProduceCustomJetVars : public edm::global::EDProducer<> {
public:
  explicit ProduceCustomJetVars(const edm::ParameterSet& iConfig)
      : srcJet_(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("srcJet"))),
        srcJetVars_(
            consumes<edm::ValueMap<DefineCustomJet>>(iConfig.getParameter<edm::InputTag>("srcJetVars"))) {
    produces<edm::ValueMap<float>>("frac01");
    produces<edm::ValueMap<float>>("frac02");
    produces<edm::ValueMap<float>>("frac03");
    produces<edm::ValueMap<float>>("frac04");
    produces<edm::ValueMap<int>>("nCharged");
  }
  ~ProduceCustomJetVars() override{};


private:
  void produce(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

  // ----------member data ---------------------------
  edm::EDGetTokenT<edm::View<pat::Jet>> srcJet_;
  edm::EDGetTokenT<edm::ValueMap<DefineCustomJet>> srcJetVars_;
};

// ------------ method called to produce the data  ------------
void ProduceCustomJetVars::produce(edm::StreamID streamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  auto srcJet = iEvent.getHandle(srcJet_);
  const auto& JetVarProd = iEvent.get(srcJetVars_);

  unsigned int nJet = srcJet->size();

  std::vector<float> frac01(nJet, -1);
  std::vector<float> frac02(nJet, -1);
  std::vector<float> frac03(nJet, -1);
  std::vector<float> frac04(nJet, -1);
  std::vector<int> nCharged(nJet, -1);

  for (unsigned int ij = 0; ij < nJet; ij++) {
    auto jet = srcJet->ptrAt(ij);

    edm::RefToBase<pat::Jet> jetRef = srcJet->refAt(ij);

    frac01[ij] = JetVarProd[jetRef].frac01();
    frac02[ij] = JetVarProd[jetRef].frac02();
    frac03[ij] = JetVarProd[jetRef].frac03();
    frac04[ij] = JetVarProd[jetRef].frac04();
    nCharged[ij] = JetVarProd[jetRef].nCharged();
  }

  std::unique_ptr<edm::ValueMap<float>> frac01V(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler_frac01(*frac01V);
  filler_frac01.insert(srcJet, frac01.begin(), frac01.end());
  filler_frac01.fill();
  iEvent.put(std::move(frac01V), "frac01");

  std::unique_ptr<edm::ValueMap<float>> frac02V(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler_frac02(*frac02V);
  filler_frac02.insert(srcJet, frac02.begin(), frac02.end());
  filler_frac02.fill();
  iEvent.put(std::move(frac02V), "frac02");

  std::unique_ptr<edm::ValueMap<float>> frac03V(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler_frac03(*frac03V);
  filler_frac03.insert(srcJet, frac03.begin(), frac03.end());
  filler_frac03.fill();
  iEvent.put(std::move(frac03V), "frac03");

  std::unique_ptr<edm::ValueMap<float>> frac04V(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler_frac04(*frac04V);
  filler_frac04.insert(srcJet, frac04.begin(), frac04.end());
  filler_frac04.fill();
  iEvent.put(std::move(frac04V), "frac04");

  std::unique_ptr<edm::ValueMap<int>> nChargedV(new edm::ValueMap<int>());
  edm::ValueMap<int>::Filler filler_nCharged(*nChargedV);
  filler_nCharged.insert(srcJet, nCharged.begin(), nCharged.end());
  filler_nCharged.fill();
  iEvent.put(std::move(nChargedV), "nCharged");
}


//define this as a plug-in
DEFINE_FWK_MODULE(ProduceCustomJetVars);
