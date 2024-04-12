#define SNUSKNANO_Producer_interface_ComputeCustomJet_h

#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CondFormats/GBRForest/interface/GBRForest.h"
#include "SNUSKNANO/Producer/plugins/DefineCustomJet.h"


class ComputeCustomJet {
public:
    ComputeCustomJet();
    ~ComputeCustomJet();
    typedef std::map<std::string, std::pair<float*, float>> variables_list_t;
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

};
