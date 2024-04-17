from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = config()

config.General.requestName = "SNUCustom"
config.General.workArea = 'SNUCustom_crab'
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'NANO_NANO.py'
#config.JobType.maxMemoryMB = 4000
#config.JobType.numCores = 8

config.Data.outputPrimaryDataset = 'SNUCustomMuon'
config.Data.outLFNDirBase = "/store/user/%s/" % (getUsernameFromCRIC())
config.Data.outputDatasetTag = 'Run3Summer19NanoAOD-2023Scenario_130X_mcRun3_2023_realistic_v3-v2'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 2500 # num. of jobs to submit
NJOBS = 200  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True

config.Site.storageSite = 'T3_KR_KNU'
