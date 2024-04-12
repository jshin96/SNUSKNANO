#define SNUSKNANO_Producer_plugins_ProduceCustomJet_h

// ------------------------------------------------------------------------------------------
//
// Reference: RecoJets/JetProducers/plugins/PileupJetIdProducer.h
//
// ------------------------------------------------------------------------------------------

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"

#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "SNUSKNANO/Producer/plugins/ComputeCustomJet.h"
// ------------------------------------------------------------------------------------------

class GBRForestsAndConstants {
public:
    GBRForestsAndConstants(edm::ParameterSet const&);
    bool inputIsCorrected() const { return inputIsCorrected_; }
    bool applyJec() const { return applyJec_; }
    std::string const& jec() const { return jec_; }
    bool residualsFromTxt() const { return residualsFromTxt_; }
    edm::FileInPath const& residualsTxt() const { return residualsTxt_; }
    bool applyConstituentWeight() const { return applyConstituentWeight_; }

private:

    bool inputIsCorrected_;
    bool applyJec_;
    std::string jec_;
    bool residualsFromTxt_;
    edm::FileInPath residualsTxt_;
    bool applyConstituentWeight_;
};

class ProduceCustomJet : public edm::stream::EDProducer<edm::GlobalCache<GBRForestsAndConstants>> {
public:
  explicit ProduceCustomJet(const edm::ParameterSet&, GBRForestsAndConstants const*);
  ~ProduceCustomJet() override;

  static std::unique_ptr<GBRForestsAndConstants> initializeGlobalCache(edm::ParameterSet const& pset) {
    return std::make_unique<GBRForestsAndConstants>(pset);
  }

  static void globalEndJob(GBRForestsAndConstants*) {}

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  void initJetEnergyCorrector(const edm::EventSetup& iSetup, bool isData);

  std::unique_ptr<ComputeCustomJet> Computed;

  std::unique_ptr<FactorizedJetCorrector> jecCor_;
  std::vector<JetCorrectorParameters> jetCorPars_;

  edm::ValueMap<float> constituentWeights_;
  edm::EDGetTokenT<edm::ValueMap<float>> input_constituent_weights_token_;
  edm::EDGetTokenT<edm::View<reco::Jet>> input_jet_token_;
  edm::EDGetTokenT<reco::VertexCollection> input_vertex_token_;
  edm::EDGetTokenT<edm::ValueMap<DefineCustomJet>> input_SNU_token_;
  edm::EDGetTokenT<double> input_rho_token_;
  edm::ESGetToken<JetCorrectorParametersCollection, JetCorrectionsRecord> parameters_token_;
};

