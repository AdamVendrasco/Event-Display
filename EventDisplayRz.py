from pyLCIO import IOIMPL
from pyLCIO import EVENT, UTIL
from ROOT import *
import math as math
import os
import glob
#########################
#tdrstyle.setTDRStyle()
gROOT.SetBatch()

#Create a reader
#Find all files matching the directory pattern. Currently only reading in one file

reader = IOIMPL.LCFactory.getInstance().createLCReader()
#directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/DataMuC_MuColl_v1/electronGun/reco/*.slcio'
directory_pattern = '/collab/project/snowmass21/data/muonc/fmeloni/LegacyProductions/before29Jul23/DataMuC_MuColl_v1/electronGun/reco/electronGun_reco_0.slcio' 
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
      >cd(1);
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
      dp3=pfo.getMomentum()
      tlv_pfo = TLorentzVector()
      tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy()) 
      Rpos=tlv_pfo.Rho()
      Zpos=tlv_pfo.Z()    
       
      ele=TGraph()
      ele.SetPoint(0, Zpos, Rpos)
      ele.SetMarkerStyle(24)
      ele.SetMarkerColor(kBlue)  
      ele.SetMarkerSize(fabs(log(pfo.getEnergy())))     
      arrow=TArrow(0,0,Zpos,Rpos)
      arrow.SetArrowSize(log(tlv_pfo.Pt())/300)
      arrow.SetLineWidth(2)
      mg.Add(ele)
      print(tlv_pfo.Pt()) 
   
   # if fabs(pfo.getType())==2112:    
   #   dp3 = pfo.getMomentum()
   #   tlv_pfo = TLorentzVector()
   #   tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
   #   phipos=tlv_pfo.Phi()
   #   etapos=tlv_pfo.Eta()
   #   neut = TGraph()
   #   neut.SetPoint(0, phipos, etapos)
   #   neut.SetMarkerColor(kRed)
   #   neut.SetMarkerStyle(24)
   #   neut.SetMarkerSize(log(pfo.getEnergy()))
   #   #mg.Add(neut)
   #     
   # if fabs(pfo.getType())==22:    
   #   dp3 = pfo.getMomentum()
   #   tlv_pfo = TLorentzVector()
   #   tlv_pfo.SetPxPyPzE(dp3[0], dp3[1], dp3[2], pfo.getEnergy())
   #   
   #   pho=TGraph()
   #   pho.SetPoint(0, Zpos, Rpos)
   #   pho.SetMarkerStyle(24)
   #   pho.SetMarkerColor(kGreen)  
   #   pho.SetMarkerSize(fabs(log(pfo.getEnergy())))     
   #   arrow=TArrow(0,0,Zpos,Rpos)
   #   arrow.SetArrowSize(log(tlv_pfo.Pt())/300)
   #   arrow.SetLineWidth(2)     
   #   mg.Add(pho)
  
  for mcp in mcpCollection:
    if fabs(mcp.getPDG()) == 11:
      
      dp3 = mcp.getVertex()
      tlv_mcp = TLorentzVector()
      tlv_mcp.SetXYZT(dp3[0], dp3[1], dp3[2], dp3[3])
      Rpos=tlv_mcp.Rho()
      Zpos=tlv_mcp.Z()
      mcp_ele=TGraph()
      mcp_ele.SetPoint(0,Zpos,Rpos)
      mcp_ele.SetMarkerStyle(2)
      mcp_ele.SetMarkerColor(kMagenta)  
      #mcp_ele.SetMarkerSize(log(mcp.getEnergy()))
      mg.Add(mcp_ele)
     
     # print("getVertex index 0: "+str(dp3[0])) 
     # print("getVertex index 1: "+str(dp3[1]))
     # print("getVertex index 2: "+str(dp3[2]))
     # print("getVertex index 3: "+str(dp3[3]))
     # print("getVertex index 4: "+str(dp3[4]))
     # print("getVertex index 5: "+str(dp3[5]))
     # print("getVertex index 6: "+str(dp3[6]))
     # print("getVertex index 7: "+str(dp3[7]))
     # print("---------")
  
  #draws multigraph
  c2=TCanvas("c%i"%ievt,"c%i"%ievt,700,500)
  
  mg.Draw("AP")
  arrow.Draw() 
  mg.SetTitle("PFO Event Display;Z [mm];R [mm]")
  mg.GetXaxis().SetLimits(-2500,2500)
  mg.GetYaxis().SetRangeUser(-500,3500)

  #Manually making legend
  TL1=TLatex(1000,3200,"Electron") 
  #TL2=TLatex(2,3.0,"Neutron")
  #TL3=TLatex(2,2.5,"Photon")
  TL4=TLatex(1000,3000,"mcp Electron")

  TL1.SetTextFont(42)
  #TL2.SetTextFont(42)
  #TL3.SetTextFont(42)
  TL4.SetTextFont(42)

  Ecircle=TEllipse(2000,3300,100,100)
  #Ncircle=TEllipse(3.4,3.1,0.15,0.18)
  #Pcircle=TEllipse(3.4,2.6,0.15,0.18)
  MCPele=TMarker(2300,3075,2)

  Ecircle.SetLineColor(kBlue)
  #Ncircle.SetLineColor(kRed)
  #Pcircle.SetLineColor(kGreen)
  MCPele.SetMarkerColor(kMagenta)
  MCPele.SetMarkerSize(2)
  Ecircle.SetLineWidth(1)
  #Ncircle.SetLineWidth(1)
  #Pcircle.SetLineWidth(1)
  #MCPele.SetMarkerWidth(1)

  Ecircle.Draw()
  #Ncircle.Draw()
  #Pcircle.Draw()
  MCPele.Draw()

  TL1.Draw()
  #TL2.Draw()
  #TL3.Draw()
  TL4.Draw()

  reader.close()
  c2.SaveAs("RZevent%i.png"%ievt)
