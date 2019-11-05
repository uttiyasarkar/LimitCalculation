# LimitCalculation

1) You will need to make a CMSSW area with the Higgs Combine Tool: https://cms-hcomb.gitbooks.io/combine/content/part1/
2) Now you can take the above folder and use the python script MakeDataCardsLimits.py
3) In the script: MakeDataCardsLimits.py You input a script that is finely binned in MET (look at BkgEstimates.root in the folder which has 100 MET bins) The script will add up the histograms based on the search bin definition here:
METBin=[300, 500, 700, 900, 1100,2000]
Also you need to write in what the MET uncertainty and the uncertainty on the mass shape is:
BkgUncMass=[1.2,1.2, 1.2,1.2,1.2]
BkgUncMET=[1.01, 1.01, 1.02, 1.5, 1.88]
Then the loop below will make the search bin histogram and set the bin errors based on the systematics you set above.These are stored in the output file: HistogramsOptimization.root
4)
Run the script in python: python MakeDataCardsLimits.py
The script produces text files for each signal point, you can take a look at one of them: T5ZZ750SingleJet.txt and it will contain the bkg in the MET bins the signal yield and the all the uncertainties assigned in 3). If you run the script it will give the limit for each mass point, and produce a root file.: higgsCombineT5ZZ2000.Asymptotic.mH2000.root which contains the Exp limit, the 1 sigma bands and the observed limit (which will be equal to the expected because Obs=Total Bkg
5) Now you can plot the limits with the script : python brazilFullSimLims.py
