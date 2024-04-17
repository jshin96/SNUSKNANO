# SNUSKNANO

## Setup CMSSW First
  CMSSW_13_0_10 is recommended CMSSW for RUN3 NANOAODv12

  ```
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  cmsrel CMSSW_13_0_10
  cd CMSSW_13_0_10/src
  cmsrel
  ```
## NANOAOD Production
  Recommendation available: https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv12

  make sure you use the correct ${GT} and ${ERA} defined in corresponding NanoAOD version

  Private MC NANOAOD Production
  
  ```cmsDriver.py NANO -s NANO --mc --conditions ${GT} --era ${ERA} --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000" -n -1 --no_exec```
  
  Private DATA NANOAOD Production
  
  ```cmsDriver.py NANO -s NANO --data --conditions ${GT} --era ${ERA} --eventcontent NANOAOD --datatier NANOAOD --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000" -n -1 --no_exec```

## Adding Variables

  Inside Producer/python directory, there are python files for different objects that can be used to add variables that you need. 
  You can define pretty much any variables using any objects defined in DataFormats. This should cover more than enough.
  I am still figuring out on how to implement purely calculated variables that user wants to use. 

  Once you have modified the python file to add variables that you want, you need to add that to --customise_commands so it is implemented in cmsRun code

  ```cmsDriver.py NANO -s NANO --mc --conditions ${GT} --era ${ERA} --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000\n from SNUSKNANO.Producer.##your_python_file##.py import *; process = Prep##Object##CustomNanoAOD(process)" -n -1 --no_exec``` 


## Crab Run

  For Crab Submission, there is a template crab file in crab directory. 
  IMPORTANT: If you run on CRAB, it is important to add ```fakeNameForCrab = cms.untracked.bool(True)``` to the configuration of the NanoAODOutputModule in the CMSSW cfg file (and to run a single instance of it - this should normally be the case).
