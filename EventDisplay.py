from pyLCIO import IOIMPL
from pyLCIO import EVENT, UTIL
from ROOT import *
from math import *
import os
import glob
#########################
#tdrstyle.setTDRStyle()
gROOT.SetBatch()

#Create a reader
#Find all files matching the directory pattern. Currently only reading in one file

reader = IOIMPL.LCFactory.getInstance().createLCReader()
#directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/DataMuC_MuColl_v1/electronGun/reco/*.slcio'
directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/DataMuC_MuColl_v1/electronGun/reco/electronGun_reco_0.slcio' 
file_paths = glob.glob(directory_pattern)
reader.open(file_paths)

# looping over all events in the file
for ievt, event in enumerate(reader):
    
  pfoCollection = event.getCollection('PandoraPFOs')
  trkCollection = event.getCollection('SiTracks_Refitted')    
  mcpCollection = event.getCollection('MCParticle')

  mg=TMultiGraph("mg%i"%ievt,"mg%i"%ievt) 
  '''
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
  '''
  #gets relevant pfos
  for pfo in pfoCollection:

    if fabs(pfo.getType()) == 11:
      dp3 = pfo.getMomentum()
      tlv_pfo = TLorentzVector()
      tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
      phipos= tlv_pfo.Phi()
      etapos=tlv_pfo.Eta()
      ele=TGraph()
      ele.SetPoint(0, phipos, etapos)
      ele.SetMarkerStyle(24)
      ele.SetMarkerColor(kBlue)  
      ele.SetMarkerSize(log(pfo.getEnergy()))
      mg.Add(ele)
    
    if fabs(pfo.getType())==2112:    
      dp3 = pfo.getMomentum()
      tlv_pfo = TLorentzVector()
      tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
      phipos=tlv_pfo.Phi()
      etapos=tlv_pfo.Eta()
      neut = TGraph()
      neut.SetPoint(0, phipos, etapos)
      neut.SetMarkerColor(kRed)
      neut.SetMarkerStyle(24)
      neut.SetMarkerSize(log(pfo.getEnergy()))
      mg.Add(neut)

    if fabs(pfo.getType())==22:    
      dp3 = pfo.getMomentum()
      tlv_pfo = TLorentzVector()
      tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
      phipos=tlv_pfo.Phi()
      etapos=tlv_pfo.Eta()
      pho=TGraph()
      pho.SetPoint(0, phipos, etapos)
      pho.SetMarkerColor(kGreen)
      pho.SetMarkerStyle(24)
      pho.SetMarkerSize(log(pfo.getEnergy()))                        
      mg.Add(pho)

  #draws multigraph
  c2=TCanvas("c%i"%ievt,"c%i"%ievt,700,500)
  mg.Draw("APL")
  mg.SetTitle("Event Display;#phi;#eta")
  mg.GetXaxis().SetLimits(-3.14,3.14)
  mg.GetYaxis().SetRangeUser(-3.14,3.14)

  #Manually making legend
  TL1=TLatex(1,2.5,"Electron") 
  TL2=TLatex(1,2.0,"Neutron")
  TL3=TLatex(1,1.5,"Photon")

  TL1.SetTextFont(42)
  TL2.SetTextFont(42)
  TL3.SetTextFont(42)

  Ecircle=TEllipse(2.2,2.6,0.11,0.15)
  Ncircle=TEllipse(2.2,2.1,0.11,0.15)
  Pcircle=TEllipse(2.2,1.6,0.11,0.15)

  Ecircle.SetLineColor(kBlue)
  Ncircle.SetLineColor(kRed)
  Pcircle.SetLineColor(kGreen)

  Ecircle.SetLineWidth(1)
  Ncircle.SetLineWidth(1)
  Pcircle.SetLineWidth(1)

  Ecircle.Draw()
  Ncircle.Draw()
  Pcircle.Draw()
  TL1.Draw()
  TL2.Draw()
  TL3.Draw()

  reader.close()
  c2.SaveAs("event%i.png"%ievt)

