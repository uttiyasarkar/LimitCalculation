import os
from array import array
from ROOT import *
f=open("realistic-counting-experimentoptimization.txt", "r")
#Signal yields in MET bins for each of the mass points
#Bkg Yields in the same MET bins for the mass points
finputs=TFile("BkgEstimates.root", "READ");
#fsig=TFile("T5ZZSignalModels.root", "READ");

Other=finputs.Get("METBinsOther")
TT=finputs.Get("METBinsTT")
ZJets=finputs.Get("METBinsZJets")
WJets=finputs.Get("METBinsWJets")
QCD=finputs.Get("METBinsQCD")
SnglT=finputs.Get("METBinsSnglT")
TT.SetFillColor(kCyan);
ZJets.SetFillColor(kGreen);
WJets.SetFillColor(kBlue);
Other.SetFillColor(kMagenta);
QCD.SetFillColor(kRed);
SnglT.SetFillColor(kOrange);
hs=THStack();
hs.Add(Other);
hs.Add(SnglT);
hs.Add(TT);
hs.Add(QCD);
hs.Add(WJets);
hs.Add(ZJets);
Total=hs.GetStack().Last()
fout=TFile("HistogramsOptimization.root","RECREATE");
fout.cd();
hs.Write("TotalBkgMET");
Total.Write("InputBkg");




METBin=[300, 450, 600, 800, 1000,2000]
mGo=[750,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100]
SearchBins=TH1D("SearchBins", "", len(METBin)-1, array('d',METBin));
BkgBins=[]
BkgUnc=[]
#HERE YOU Should add the uncertainty on the mass shape from the 1sigma bands in the mass window [75,95]
BkgUncMass=[4,4, 4,4,4]
#HERE YOU should add the uncertainty in the MET bins from the single lepton region fractions
BkgUncMET=[1.08, 1.15, 1.38, 1.56, 1.71]
##Bkg Bins
for i in range(0,len(METBin)-1):
	lowbin=Total.GetXaxis().FindBin(METBin[i])	
	highbin=Total.GetXaxis().FindBin(METBin[i+1])	
	BkgBins.append(Total.Integral(lowbin,highbin))
	SearchBins.Fill(METBin[i],Total.Integral(lowbin,highbin))
	sbin=SearchBins.GetXaxis().FindBin(METBin[i])
	TotalBkgUnc=BkgUncMass[i]*Total.Integral(lowbin,highbin)-Total.Integral(lowbin,highbin)
	METUnc=BkgUncMET[i]*Total.Integral(lowbin,highbin)-Total.Integral(lowbin,highbin)
	TotalBkgUnc=METUnc+TotalBkgUnc
	SearchBins.SetBinError(sbin, BkgUncMass[i]*Total.Integral(lowbin,highbin)-Total.Integral(lowbin,highbin));
	BkgUnc.append(TotalBkgUnc)
SearchBins.Write("BkgSearchBins");	
print BkgBins,BkgUnc
for m in mGo:
	signal=finputs.Get("METT5HH%d" %m)
	SignalYields=[]
	for i in range(0,len(METBin)-1):
		lowbin=signal.GetXaxis().FindBin(METBin[i])
        	highbin=signal.GetXaxis().FindBin(METBin[i+1])	
		SignalYields.append(signal.Integral(lowbin,highbin));
	print SignalYields
	fout=open("T5ZZ%dSingleJet.txt" %m,"w")
	fout.write("# Simple counting experiment, with one signal and a few background processes\n");
	fout.write("# Simplified version of the 35/pb H->WW analysis for mH = 160 GeV\n")
	fout.write("imax %d  number of channels\n" %(len(METBin)-1))
	fout.write("jmax 1  number of backgrounds\n")
	fout.write("kmax *  number of nuisance parameters (sources of systematical uncertainties)\n")
	fout.write("bin ");
	for i in range(0,len(METBin)-1):fout.write("bin%d " %i);
	fout.write("\n");
	fout.write("observation ")
	for i in range(0,len(METBin)-1):fout.write(" %.2f" %BkgBins[i])
	fout.write("\n");
	fout.write("bin ");
	for i in range(0,len(METBin)-1):fout.write(" bin%d bin%d " %(i,i));
	fout.write("\nprocess ");
	for i in range(0,len(METBin)-1):fout.write(" sig bkg ")
	fout.write("\nprocess ");
	for i in range(0,len(METBin)-1):fout.write(" 0 1 ")
	fout.write("\nrate ")
	for i in range(0,len(METBin)-1):fout.write("%.2f %.2f " %(SignalYields[i],BkgBins[i]))
	fout.write("\n------------\n");
	fout.write("BkgMetUnc lnN ")
	for i in range(0,len(METBin)-1):fout.write(" -  %.2f " %BkgUncMET[i])
	fout.write("\nBkgShapeUnc lnN ")
	for i in range(0,len(METBin)-1):fout.write(" -  %.2f " %BkgUncMass[i])
	fout.close()
	os.system("combine -M Asymptotic T5ZZ%dSingleJet.txt -m %d -n T5ZZ%d " %(m,m,m))
	f.seek(0);
	#break;
'''
	for line in f:
		if "rate" in line:
			line=line.replace("sig1", "%g" %signal.GetBinContent(1));
			line=line.replace("sig2", "%g" %signal.GetBinContent(2));
			line=line.replace("sig3", "%g" %signal.GetBinContent(3));
			#print line
		fout.write(line)
	fout.close()
	#os.system("combine -M Asymptotic T5ZZ%d.txt -m %d -n T5ZZ%d.txt " %(m,m,m))
f1=open("realistic-counting-experimentSingleBin.txt", "r")

for m in mGo:
        signal=fsig1.Get("T5HH%d" %m)
	f1.seek(0);
  	for line in f1:
                if "rate" in line:line=line.replace("sig1", "%g" %signal.GetBinContent(3));
		fout.write(line)
	fout.close()
	#os.system("combineCards.py T5ZZ%d.txt T5ZZ%dSingleJet.txt> T5ZZCombine%d.txt" %(m,m,m) ) 
	#os.system("combine -M Asymptotic T5ZZCombine%d.txt -m %d -n T5ZZ%d.txt " %(m,m,m))
f2=open("realistic-counting-experimentBtags.txt","r")
fsigb=TFile("SignalCards2Ak8DoubleB.root", "READ");

for m in mGo:
        signal=fsigb.Get("T5HH%d" %m)
        fout=open("T5ZZ%dBtags.txt" %m,"w")
	f2.seek(0);
	for line in f2:
                if "rate" in line:line=line.replace("sig1", "%g" %signal.GetBinContent(1));
                if "rate" in line:line=line.replace("sig2", "%g" %signal.GetBinContent(2));
                if "rate" in line:line=line.replace("sig3", "%g" %signal.GetBinContent(3));
                fout.write(line)
        fout.close()
	#os.system("combineCards.py T5ZZ%d.txt T5ZZ%dSingleJet.txt T5ZZ%dBtags.txt  > T5ZZCombine%d.txt" %(m,m,m,m) ) 
	os.system("combineCards.py T5ZZ%d.txt T5ZZ%dSingleJet.txt   > T5ZZCombine%d.txt" %(m,m,m) ) 
	os.system("combine -M Asymptotic T5ZZCombine%d.txt -m %d -n T5ZZ%d.txt " %(m,m,m))
'''	
