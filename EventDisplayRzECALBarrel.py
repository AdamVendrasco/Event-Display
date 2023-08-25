from pyLCIO import IOIMPL
from pyLCIO import EVENT, UTIL
from ROOT import *
import math as math
import os
import glob
#########################
gROOT.SetBatch()
gStyle.SetPalette(kSolar)

#Create a reader
#Find all files matching the directory pattern. Currently only reading in one file
reader = IOIMPL.LCFactory.getInstance().createLCReader()
#directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/DataMuC_MuColl_v1/electronGun/reco/*.slcio'
directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/LegacyProductions/before29Jul23/DataMuC_MuColl_v1/electronGun/reco/electronGun_reco_0.slcio' 
file_paths = glob.glob(directory_pattern)
reader.open(file_paths)
array=[]

# looping over all events in the file
for ievt, event in enumerate(reader):
    
  pfoCollection = event.getCollection('PandoraPFOs')
  trkCollection = event.getCollection('SiTracks_Refitted')    
  mcpCollection = event.getCollection('MCParticle')
  ecalCollection = event.getCollection('ECALBarrel')
  mg=TMultiGraph("mg%i"%ievt,"mg%i"%ievt) 
  
  #gets relevant pfos
  for pfo in pfoCollection:
    if fabs(pfo.getType()) == 11:
      
      dp3=pfo.getMomentum()
      tlv_pfo = TLorentzVector()
      tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy()) 
      Rpos=tlv_pfo.Perp()
      Zpos=tlv_pfo.Z()    
      ele=TGraph()
      ele.SetPoint(0, Zpos, Rpos)
      mg.Add(ele)
  
  for mcp in mcpCollection:
    status=mcp.getGeneratorStatus()
    if status ==0:
      dp3=mcp.getMomentum()
      vert = mcp.getVertex()

      tlv_mcpP3 = TLorentzVector()
      tlv_mcpVert=TLorentzVector()

      tlv_mcpVert.SetXYZT(vert[0], vert[1], vert[2], 0)
      tlv_mcpP3.SetPxPyPzE(dp3[0],dp3[1],dp3[2],dp3[3])
      
      Rpos=tlv_mcpVert.Perp()
      Zpos=tlv_mcpVert.Z()
      mcp_ele=TGraph()
      mcp_ele.SetPoint(0,Zpos,Rpos)
      mcp_ele.SetMarkerStyle(2)
      mcp_ele.SetMarkerColor(kMagenta)  
      mg.Add(mcp_ele)
    
    if status==1: 
      arrow=TArrow(0,0,Zpos,Rpos)
      arrow.SetArrowSize(0.02)
      arrow.SetLineWidth(2)
    
     
  for ecal in ecalCollection:
    dp3 = ecal.getPosition()
    tlv_ecal = TLorentzVector()
    tlv_ecal.SetXYZT(dp3[0], dp3[1], dp3[2], 0)
    Rpos=tlv_ecal.Perp()
    Zpos=tlv_ecal.Z()
    ecal_hit=TGraph()
    ecal_hit.SetPoint(0,Zpos,Rpos)
    ecal_hit.SetMarkerStyle(20)
    
    array.append(ecal.getEnergy())
    maxx = max(array)
    minn =min(array)
    normalE =0.1+0.9*((ecal.getEnergy()-minn)/(maxx))
    ecal_hit.SetMarkerColorAlpha(kBlack,normalE)  
    
    mg.Add(ecal_hit)
  #draws multigraph
  c2=TCanvas("c%i"%ievt,"c%i"%ievt,700,500)
  mg.Draw("AP")
  arrow.Draw() 
  mg.SetTitle("PFO Event Display;Z [mm];R [mm]")
  mg.GetXaxis().SetLimits(-2500,2500)
  mg.GetYaxis().SetRangeUser(-300,3500)

  #Manually making legend
  TL1=TLatex(1250,3300,"PFO Electron")
  TL1.SetTextSize(0.03)
  
  TL2=TLatex(1250,3100,"MCP")
  TL2.SetTextSize(0.03)
  
  TL3=TLatex(1250,2900,"ECal Barrel Hit")
  TL3.SetTextSize(0.03)

  TL1.SetTextFont(42)
  TL2.SetTextFont(42)
  TL3.SetTextFont(42)
  
  Earrow=TArrow(2050,3350,2150,3350)
  Earrow.SetArrowSize(0.01)
  Earrow.SetLineWidth(2)
  MCPele=TMarker(2075,3175,2)
  EcalHit=TMarker(2100,2965,20)
  
  MCPele.SetMarkerColor(kMagenta)
  MCPele.SetMarkerSize(1)
  EcalHit.SetMarkerColor(kBlack)
  EcalHit.SetMarkerSize(1)

  Earrow.Draw()
  MCPele.Draw()
  EcalHit.Draw()

  TL1.Draw()
  TL2.Draw()
  TL3.Draw()

  reader.close()
  c2.SaveAs("RzECALBarrel_event%i.png"%ievt)

