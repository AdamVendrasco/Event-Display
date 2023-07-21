from pyLCIO import IOIMPL
from pyLCIO import EVENT, UTIL
from ROOT import *
from math import *
from optparse import OptionParser
from array import array
import os
import glob
import fnmatch
#########################
#tdrstyle.setTDRStyle()
gROOT.SetBatch()
#Create a reader and open an LCIO file
#Find all files matching the directory pattern

reader = IOIMPL.LCFactory.getInstance().createLCReader()
#directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/DataMuC_MuColl_v1/electronGun/reco/*.slcio'
directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/DataMuC_MuColl_v1/electronGun/reco/electronGun_reco_0.slcio' 
file_paths = glob.glob(directory_pattern)
reader.open(file_paths)

#Initalizing entries

# looping over all events in the file
for ievt, event in enumerate(reader):
    print(event)
    print(ievt)
    pfoCollection = event.getCollection('PandoraPFOs')
    trkCollection = event.getCollection('SiTracks_Refitted')    
    mcpCollection = event.getCollection('MCParticle')
    
    c2=TCanvas("c%i"%ievt,"c%i"%ievt,700,500)
    mg=TMultiGraph("mg","mg")
    mg.SetTitle("Event Display;Phi;Eta")
    mg.GetXaxis().SetLimits(-3.14,3.14)
    mg.GetYaxis().SetRangeUser(-3.14,3.14)
    
    leg = TLegend(0.65,0.65,0.9,0.9)
    
#within file for only MC particles   
    for mcp in mcpCollection:
        charge = mcp.getCharge()
        status = mcp.getGeneratorStatus()
        if fabs(charge) > 0:
            if fabs(mcp.getPDG()) == 11:
                vx = mcp.getVertex()
                rprod = sqrt(vx[0]*vx[0]+vx[1]*vx[1])
                dp3 = mcp.getMomentum()
                tlv = TLorentzVector()
                tlv.SetPxPyPzE(dp3[0], dp3[1], dp3[2], mcp.getEnergy())
                goodtheta = False


                if tlv.Theta() > 30.*TMath.Pi()/180. and tlv.Theta() < 150.*TMath.Pi()/180.:
                    goodtheta = True
                if tlv.Perp() > 1 and not mcp.isDecayedInTracker() and goodtheta:
                    
                    print(str(mcp))
                    for pfo in pfoCollection:
                        if fabs(pfo.getType()) == 11:
                            dp3 = pfo.getMomentum()
                            tlv_pfo = TLorentzVector()
                            tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
                            
                            ele=TGraph()
                            phipos= tlv_pfo.Phi()
                            etapos=tlv_pfo.Eta()
                            ele.SetPoint(ievt, phipos,etapos)
                            ele.SetMarkerColorAlpha(i, i-(0.1*i))
                            ele.SetMarkerStyle(kFullCircle)  
                            ele.SetMarkerSize(log(pfo.getEnergy()))
                            mg.Add(ele)
                            
                           # print("event",str(ievt),"electron energy:",str(pfo.getEnergy()))   
                            leg.AddEntry(ele,"Electron","p")

                        if fabs(pfo.getType())==2112:    
                            dp3 = pfo.getMomentum()
                            tlv_pfo = TLorentzVector()
                            tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
                            
                            neut=TGraph()
                            phipos=tlv_pfo.Phi()
                            etapos=tlv_pfo.Eta()
                            neut.SetPoint(ievt,phipos,etapos)
                            neut.SetMarkerColor(kRed)
                            neut.SetMarkerStyle(24)
                            neut.SetMarkerSize(log(pfo.getEnergy()))
                            mg.Add(neut)

                           # print("event",str(ievt),"neut energy:",str(pfo.getEnergy()))
                            leg.AddEntry(neut,"neut","p")


                        if fabs(pfo.getType())==22:    
                            dp3 = pfo.getMomentum()
                            tlv_pfo = TLorentzVector()
                            tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
                            
                            pho=TGraph()
                            phipos=tlv_pfo.Phi()
                            etapos=tlv_pfo.Eta()
                            pho.SetPoint(ievt,phipos,etapos)
                            pho.SetMarkerColor(kGreen)
                            pho.SetMarkerStyle(24)
                            pho.SetMarkerSize(log(pfo.getEnergy()))                        
                            mg.Add(pho)


                            leg.AddEntry(pho,"pho","p")
                            #print("event",str(ievt),"pho energy:",str(pfo.getEnergy()))

    
    mg.Draw("AP same")
    leg.Draw()
    reader.close()
    c2.SaveAs("Event%i.png"%ievt)

    print(ievt)
