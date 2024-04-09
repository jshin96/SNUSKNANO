//
// Reference: RecoJets/JetProducers/plugins/PileupJetIdProducer.cc
//

#include "SNUSKNANO/Producer/plugins/ProduceCustomJet.h"

#include <memory>

GBRForestsAndConstants::GBRForestsAndConstants(edm::ParameterSet const& iConfig) 
    : inputIsCorrected_(iConfig.getParameter<bool>("inputIsCorrected")),
      applyJec_(iConfig.getParameter<bool>("applyJec")),
      jec_(iConfig.getParameter<std::string>("jec")),
      residualsFromTxt_(iConfig.getParameter<bool>("residualsFromTxt")),
      applyConstituentWeight_(false) {
  if (residualsFromTxt_) {
    residualsTxt_ = iConfig.getParameter<edm::FileInPath>("residualsTxt");
  }


  edm::InputTag srcConstituentWeights = iConfig.getParameter<edm::InputTag>("srcConstituentWeights");
  if (!srcConstituentWeights.label().empty()) {
    applyConstituentWeight_ = true;
  }
}

// ------------------------------------------------------------------------------------------
ProduceCustomJet::ProduceCustomJet(const edm::ParameterSet& iConfig) {
    produces<edm::ValueMap<DefineCustomJet>>("");
    input_jet_token_                    = consumes<edm::View<reco::Jet>>(iConfig.getParameter<edm::InputTag>("jets"));
    input_vertex_token_                 = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexes"));
    input_SNU_token_               = consumes<edm::ValueMap<StoredPileupJetIdentifier>>(iConfig.getParameter<edm::InputTag>("SNUjet"));
    input_rho_token_                    = consumes<double>(iConfig.getParameter<edm::InputTag>("rho"));
    parameters_token_                   = esConsumes(edm::ESInputTag("", globalCache->jec()));
    edm::InputTag srcConstituentWeights = iConfig.getParameter<edm::InputTag>("srcConstituentWeights");
    if (!srcConstituentWeights.label().empty()) {
        input_constituent_weights_token_ = consumes<edm::ValueMap<float>>(srcConstituentWeights);
    }
}

// ------------------------------------------------------------------------------------------
ProduceCustomJet::~ProduceCustomJet() {}

// ------------------------------------------------------------------------------------------
void ProduceCustomJet::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    using namespace edm;
    using namespace std;
    using namespace reco;

    // Input jets
    Handle<View<Jet>> jetHandle;
    iEvent.getByToken(input_jet_token_, jetHandle);
    const View<Jet>& jets = *jetHandle;

    // Constituent weight (e.g PUPPI) Value Map
    edm::ValueMap<float> constituentWeights;
    if (!input_constituent_weights_token_.isUninitialized()) {
        constituentWeights = iEvent.get(input_constituent_weights_token_);
    }

    // input variables
    Handle<ValueMap<DefineCustomJet>> vmap;
    iEvent.getByToken(input_SNU_token_, vmap);

    // rho
    edm::Handle<double> rhoH;
    double rho = 0.;

    // products
    vector<DefineCustomJet> ids;

    const VertexCollection* vertexes = nullptr;
    VertexCollection::const_iterator vtx;
    Handle<VertexCollection> vertexHandle;
    iEvent.getByToken(input_vertex_token_, vertexHandle);
    vertexes = vertexHandle.product();
    // require basic quality cuts on the vertexes
    vtx = vertexes->begin();
    while (vtx != vertexes->end() && (vtx->isFake() || vtx->ndof() < 4)) {
        ++vtx;
    }
    if (vtx == vertexes->end()) {
        vtx = vertexes->begin();
    }

    // Loop over input jets
    bool ispat = true;
    for (unsigned int i = 0; i < jets.size(); ++i) {

    const Jet& jet = jets.at(i);
    const pat::Jet* patjet = nullptr;
    if (ispat) {
      patjet = dynamic_cast<const pat::Jet*>(&jet);
      ispat = patjet != nullptr;
    }

    // Get jet energy correction
    float jec = 0.;
    if (gc->applyJec()) {
        // If haven't done it get rho from the event
        if (rho == 0.) {
            iEvent.getByToken(input_rho_token_, rhoH);
            rho = *rhoH;
        }
        // jet corrector
        if (not jecCor_) {
            initJetEnergyCorrector(iSetup, iEvent.isRealData());
        }
        if (ispat) {
            jecCor_->setJetPt(patjet->correctedJet(0).pt());
        } else {
            jecCor_->setJetPt(jet.pt());
        }
        jecCor_->setJetEta(jet.eta());
        jecCor_->setJetA(jet.jetArea());
        jecCor_->setRho(rho);
        jec = jecCor_->getCorrection();
    }
    // If it was requested AND the input is an uncorrected jet apply the JEC
    bool applyJec = gc->applyJec() && (ispat || !gc->inputIsCorrected());
    std::unique_ptr<reco::Jet> corrJet;

    if (applyJec) {
        float scale = jec;
        if (ispat) {
            corrJet = std::make_unique<pat::Jet>(patjet->correctedJet(0));
        } else {
            corrJet.reset(dynamic_cast<reco::Jet*>(jet.clone()));
        }
        corrJet->scaleEnergy(scale);
    }
    const reco::Jet* theJet = (applyJec ? corrJet.get() : &jet);

    DefineCustomJet Identifier;
    // Compute the input variables
    ////////////////////////////// added PUPPI weight Value Map
    Identifier = Computed->computeIdVariables(theJet, jec, &(*vtx), *vertexes, rho, constituentWeights, gc->applyConstituentWeight());
    ids.push_back(Identifier);
  }

    // input variables
    assert(jetHandle->size() == ids.size());
    auto idsout = std::make_unique<ValueMap<DefineCustomJet>>();
    ValueMap<DefineCustomJet>::Filler idsfiller(*idsout);
    idsfiller.insert(jetHandle, ids.begin(), ids.end());
    idsfiller.fill();
    iEvent.put(std::move(idsout));
  }
}


// ------------------------------------------------------------------------------------------
void ProduceCustomJet::initJetEnergyCorrector(const edm::EventSetup& iSetup, bool isData) {
  GBRForestsAndConstants const* gc = globalCache();

  //jet energy correction levels to apply on raw jet
  std::vector<std::string> jecLevels;
  jecLevels.push_back("L1FastJet");
  jecLevels.push_back("L2Relative");
  jecLevels.push_back("L3Absolute");
  if (isData && !gc->residualsFromTxt())
    jecLevels.push_back("L2L3Residual");

  //check the corrector parameters needed according to the correction levels
  auto const& parameters = iSetup.getData(parameters_token_);
  for (std::vector<std::string>::const_iterator ll = jecLevels.begin(); ll != jecLevels.end(); ++ll) {
    const JetCorrectorParameters& ip = parameters[*ll];
    jetCorPars_.push_back(ip);
  }
  if (isData && gc->residualsFromTxt()) {
    jetCorPars_.push_back(JetCorrectorParameters(gc->residualsTxt().fullPath()));
  }

  //instantiate the jet corrector
  jecCor_ = std::make_unique<FactorizedJetCorrector>(jetCorPars_);
}
//define this as a plug-in
DEFINE_FWK_MODULE(ProduceCustomJet);
