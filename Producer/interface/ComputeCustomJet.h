#ifndef SNUSKNANO_Producer_interface_ComputeCustomJet_h
#define SNUSKNANO_Producer_interface_ComputeCustomJet_h

#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"
#include "CondFormats/GBRForest/interface/GBRForest.h"


class ComputeCustomJet {
public:
    PileupJetIdAlgo();
    ~PileupJetIdAlgo();
    const variables_list_t& getVariables() const { return variables_; };
    void set(const DefineCustomJet&);
    DefineCustomJet computeVariables(const reco::Jet* jet,
                                     float jec,
                                     const reco::Vertex*,
                                     const reco::VertexCollection&,
                                     double rho,
                                     edm::ValueMap<float>& constituentWeights,
                                     bool applyConstituentWeight);

protected:
    void resetVariables();
    void initVariables();
    DefineCustomJet JET_;
    variables_list_t variables_;

}
