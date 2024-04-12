#include <map>
#include <string>

#define SNUSKNANO_Producer_plugins_DefineCustomJet_h

#define DECLARE_VARIABLE(NAME, TYPE)           \
private:                                       \
  TYPE NAME##_ = 0;                            \
                                               \
public:                                        \
  const TYPE &NAME() const { return NAME##_; } \
  void NAME(const TYPE val) { NAME##_ = val; }

// ----------------------------------------------------------------------------------------------------
class DefineCustomJet {
public:
  friend class ComputeCustomJet;

  DefineCustomJet();
  ~DefineCustomJet();

  DECLARE_VARIABLE(jetM, float);
  DECLARE_VARIABLE(jetPhi, float);
  DECLARE_VARIABLE(jetEta, float);
  DECLARE_VARIABLE(jetPt, float);
  DECLARE_VARIABLE(nCharged, float);
  DECLARE_VARIABLE(nNeutral, float);
  DECLARE_VARIABLE(dZ, float);
  DECLARE_VARIABLE(d0, float);
//  DECLARE_VARIABLE(dR2Mean, float);  /// a.k.a RMS
//  void RMS(const float val) { dR2Mean(val); }
//  const float &RMS() const { return dR2Mean(); }
  DECLARE_VARIABLE(frac01, float);
  DECLARE_VARIABLE(frac02, float);
  DECLARE_VARIABLE(frac03, float);
  DECLARE_VARIABLE(frac04, float);
  DECLARE_VARIABLE(frac05, float);
  DECLARE_VARIABLE(frac06, float);
  DECLARE_VARIABLE(frac07, float);
  DECLARE_VARIABLE(nvtx, int);
  DECLARE_VARIABLE(rho, float);
};
//namespace GlobalCache { 
//  bool applyConstituentWeight = true;
//}


#undef DECLARE_VARIABLE

