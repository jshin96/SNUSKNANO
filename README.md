# SNUSKNANO

## Setup CMSSW First
  ```
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  cmsrel CMSSW_13_0_10
  cd CMSSW_13_0_10/src
  cmsrel
  ```
## NANOAOD Production
  Recommendation available: https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Instructions/Private-production\n
  Private MC NANOAOD Production \n
  ```cmsDriver.py NANO -s NANO --mc --conditions ${GT} --era ${ERA} --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000" -n -1 --no_exec```
  Private DATA NANOAOD Production
  ```cmsDriver.py NANO -s NANO --data --conditions ${GT} --era ${ERA} --eventcontent NANOAOD --datatier NANOAOD --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000" -n -1 --no_exec```
