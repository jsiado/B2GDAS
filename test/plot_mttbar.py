#! /usr/bin/env python


## _________                _____.__                            __  .__
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/
import sys
import array as array
from optparse import OptionParser


def plot_mttbar(argv) :
    parser = OptionParser()

    parser.add_option('--file_in', type='string', action='store',
                      dest='file_in',
                      help='Input file')

    parser.add_option('--file_out', type='string', action='store',
                      dest='file_out',
                      help='Output file')

    parser.add_option('--is_electron', action='store_true',
                      dest='is_electron',default = False,
                      help='flag sets code to use electron rather than muon')

    parser.add_option('--is_bkg', action='store_true',
                      dest='is_bkg', default = False,
                      help='is this a background data rather than signal')


    parser.add_option('--origin', type='string', action='store',
                      dest='origin',
                      help='Output file')


    parser.add_option('--enable_top_tagging', action='store_true',
                     dest='enable_top_tagging', default=False,
                     help='Whether a cut is made based on top tagging')

    parser.add_option('--isData', action='store_true',
                      dest='isData',
                      default = False,
                      help='Is this Data?')

    parser.add_option('--hist_name', type='string', action='store',
                      dest='signal',
                      help='Output file')


    (options, args) = parser.parse_args(argv)
    argv = []

    print '===== Command line options ====='
    print options
    print '================================'

    import ROOT

    if options.is_electron:
        leptonname = "E"

    if not options.is_electron:
        leptonname = "M"

    if options.is_bkg:
        sortofdata = "bkg"

    if not options.is_bkg:
        sortofdata = "signal"


    from leptonic_nu_z_component import solve_nu_tmass, solve_nu

    fout= ROOT.TFile(options.file_out, "RECREATE")

    #mass histograms

    h_mttbar = ROOT.TH1F("mttbar"+options.origin+"_"+leptonname+"_"+sortofdata, ";m_{t#bar{t}} (GeV);Number", 100, 0, 5000)
    h_mtopHad = ROOT.TH1F("mtopHad"+options.origin+"_"+leptonname+"_"+sortofdata, ";m_{jet} (GeV);Number", 100, 0, 400)
    h_mtopHadGroomed = ROOT.TH1F("mtopHadGroomed"+options.origin+"_"+leptonname+"_"+sortofdata, ";Groomed m_{jet} (GeV);Number", 100, 0, 400)
    h_mfatjet = ROOT.TH1F("fatjetmass"+options.origin+"_"+leptonname+"_"+sortofdata, ";m (GeV);Number", 100, 0, 5000)
    h_mlep = ROOT.TH1F("lepmass"+options.origin+"_"+leptonname+"_"+sortofdata, ";m (GeV);Number", 100, 0, 5000)
    h_mAK4Jet = ROOT.TH1F("AK4Jetmass"+options.origin+"_"+leptonname+"_"+sortofdata, ";m (GeV);Number", 100, 0, 5000)
    h_mlepTop = ROOT.TH1F("lepTopmass"+options.origin+"_"+leptonname+"_"+sortofdata, ";m (GeV);Number", 100, 0, 5000)

    #pt histograms
    h_fatjetpt = ROOT.TH1F("fatjetpt"+options.origin+"_"+leptonname+"_"+sortofdata, ";pt (GeV);Number", 500, 0, 5000)
    h_leppt = ROOT.TH1F("leppt"+options.origin+"_"+leptonname+"_"+sortofdata, ";pt (GeV);Number", 100, 0, 5000)
    h_AK4Jetpt = ROOT.TH1F("AK4Jetpt"+options.origin+"_"+leptonname+"_"+sortofdata, ";pt (GeV);Number", 100, 0, 5000)
    h_lepTop = ROOT.TH1F("lepTop"+options.origin+"_"+leptonname+"_"+sortofdata, ";pt (GeV);Number", 100, 0, 5000)


    #eta histograms
    h_fatjeteta = ROOT.TH1F("fatjeteta"+options.origin+"_"+leptonname+"_"+sortofdata, ";#eta;Number", 500, -3, 3)
    h_lepeta = ROOT.TH1F("lepeta"+options.origin+"_"+leptonname+"_"+sortofdata, ";#eta;Number", 500, -3, 3)
    h_AK4Jeteta = ROOT.TH1F("AK4Jeteta"+options.origin+"_"+leptonname+"_"+sortofdata, ";#eta;Number", 500, -3, 3)
    h_lepTopeta = ROOT.TH1F("lepTopeta"+options.origin+"_"+leptonname+"_"+sortofdata, ";#eta;Number", 500, -3, 3)

    #phi histograms
    h_fatjetphi = ROOT.TH1F("fatjetphi"+options.origin+"_"+leptonname+"_"+sortofdata, ";#phi (rad);Number", 500, -4, 4)
    h_lepphi = ROOT.TH1F("lepphi"+options.origin+"_"+leptonname+"_"+sortofdata, ";#phi (rad);Number", 500, -4, 4)
    h_AK4Jetphi = ROOT.TH1F("AK4Jetphi"+options.origin+"_"+leptonname+"_"+sortofdata, ";#phi (rad);Number", 500, -4, 4)
    h_lepTopphi = ROOT.TH1F("lepTopphi"+options.origin+"_"+leptonname+"_"+sortofdata, ";#phi (rad);Number", 500, -4, 4)


    #MET histograms
    h_MET = ROOT.TH1F("MET"+options.origin+"_"+leptonname+"_"+sortofdata, ";MET (GeV);Number", 100, 0, 5000)
    h_METphi = ROOT.TH1F("METphi"+options.origin+"_"+leptonname+"_"+sortofdata, ";#phi (rad);Number", 500, -4, 4)


    #other histograms
    h_fatjettau32 = ROOT.TH1F("fatjettau32"+options.origin+"_"+leptonname+"_"+sortofdata, ": );Number", 500, 0,10 )
    h_fatjettau21 = ROOT.TH1F("fatjettau21"+options.origin+"_"+leptonname+"_"+sortofdata, "; ;Number", 500, 0, 10)
    h_etattbar = ROOT.TH1F("etattbar"+options.origin+"_"+leptonname+"_"+sortofdata, ";#eta (rad);Number", 500, -3, 3)
    h_deltaRfatjetvslepTop = ROOT.TH1F("deltaRfatjetvslepTop"+options.origin+"_"+leptonname+"_"+sortofdata, ";#Delta R;Number", 500, 0,5 )
    h_btag = ROOT.TH1F("btag"+options.origin+"_"+leptonname+"_"+sortofdata, ";disc;Number", 500, 0, 1)

    fin = ROOT.TFile.Open(options.file_in)


    trees = [ fin.Get("TreeSemiLept") ]



    for itree,t in enumerate(trees) :

        #if options.isData :
        SemiLeptTrig        =  ROOT.vector('int')()
        SemiLeptWeight      = array.array('f', [0.] )
        PUWeight            = array.array('f', [0.] )
        GenWeight           = array.array('f', [0.] )
        FatJetPt            = array.array('f', [-1.])
        FatJetEta           = array.array('f', [-1.])
        FatJetPhi           = array.array('f', [-1.])
        FatJetRap           = array.array('f', [-1.])
        FatJetEnergy        = array.array('f', [-1.])
        FatJetBDisc         = array.array('f', [-1.])
        FatJetMass          = array.array('f', [-1.])
        FatJetMassSoftDrop  = array.array('f', [-1.])
        FatJetTau32         = array.array('f', [-1.])
        FatJetTau21         = array.array('f', [-1.])
        FatJetSDBDiscW      = array.array('f', [-1.])
        FatJetSDBDiscB      = array.array('f', [-1.])
        FatJetSDsubjetWpt   = array.array('f', [-1.])
        FatJetSDsubjetWmass = array.array('f', [-1.])
        FatJetSDsubjetBpt   = array.array('f', [-1.])
        FatJetSDsubjetBmass = array.array('f', [-1.])
        FatJetJECUpSys      = array.array('f', [-1.])
        FatJetJECDnSys      = array.array('f', [-1.])
        FatJetJERUpSys      = array.array('f', [-1.])
        FatJetJERDnSys      = array.array('f', [-1.])
        LeptonType          = array.array('i', [-1])
        LeptonPt            = array.array('f', [-1.])
        LeptonEta           = array.array('f', [-1.])
        LeptonPhi           = array.array('f', [-1.])
        LeptonEnergy        = array.array('f', [-1.])
        LeptonIso           = array.array('f', [-1.])
        LeptonPtRel         = array.array('f', [-1.])
        LeptonDRMin         = array.array('f', [-1.])
        SemiLepMETpt        = array.array('f', [-1.])
        SemiLepMETphi       = array.array('f', [-1.])
        SemiLepNvtx         = array.array('f', [-1.])
        FatJetDeltaPhiLep      = array.array('f', [-1.])
        NearestAK4JetBDisc            = array.array('f', [-1.])
        NearestAK4JetPt     = array.array('f', [-1.])
        NearestAK4JetEta    = array.array('f', [-1.])
        NearestAK4JetPhi    = array.array('f', [-1.])
        NearestAK4JetMass   = array.array('f', [-1.])
        NearestAK4JetJECUpSys = array.array('f', [-1.])
        NearestAK4JetJECDnSys = array.array('f', [-1.])
        NearestAK4JetJERUpSys = array.array('f', [-1.])
        NearestAK4JetJERDnSys = array.array('f', [-1.])
        SemiLeptRunNum        = array.array('f', [-1.])
        SemiLeptLumiNum     = array.array('f', [-1.])
        SemiLeptEventNum      = array.array('f', [-1.])


        #if options.isData :
        t.SetBranchAddress('SemiLeptTrig'        , SemiLeptTrig )
        t.SetBranchAddress('SemiLeptWeight'      , SemiLeptWeight      ) #Combined weight of all scale factors (lepton, PU, generator) relevant for the smeileptonic event selection
        t.SetBranchAddress('PUWeight'            , PUWeight            )
        t.SetBranchAddress('GenWeight'           , GenWeight               )
        t.SetBranchAddress('FatJetPt'            , FatJetPt            )
        t.SetBranchAddress('FatJetEta'           , FatJetEta           )
        t.SetBranchAddress('FatJetPhi'           , FatJetPhi           )
        t.SetBranchAddress('FatJetRap'           , FatJetRap           )
        t.SetBranchAddress('FatJetEnergy'        , FatJetEnergy        )
        t.SetBranchAddress('FatJetBDisc'         , FatJetBDisc         )
        t.SetBranchAddress('FatJetMass'          , FatJetMass           )
        t.SetBranchAddress('FatJetMassSoftDrop'  , FatJetMassSoftDrop  )
        t.SetBranchAddress('FatJetTau32'         , FatJetTau32         )
        t.SetBranchAddress('FatJetTau21'         , FatJetTau21         )
        t.SetBranchAddress('FatJetSDBDiscW'      , FatJetSDBDiscW      )
        t.SetBranchAddress('FatJetSDBDiscB'      , FatJetSDBDiscB              )
        t.SetBranchAddress('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   )
        t.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
        t.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
        t.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )
        t.SetBranchAddress('FatJetJECUpSys'      , FatJetJECUpSys      )
        t.SetBranchAddress('FatJetJECDnSys'      , FatJetJECDnSys      )
        t.SetBranchAddress('FatJetJERUpSys'      , FatJetJERUpSys      )
        t.SetBranchAddress('FatJetJERDnSys'      , FatJetJERDnSys      )
        t.SetBranchAddress('LeptonType'          , LeptonType          )
        t.SetBranchAddress('LeptonPt'            , LeptonPt            )
        t.SetBranchAddress('LeptonEta'           , LeptonEta           )
        t.SetBranchAddress('LeptonPhi'           , LeptonPhi           )
        t.SetBranchAddress('LeptonEnergy'        , LeptonEnergy        )
        t.SetBranchAddress('LeptonIso'           , LeptonIso           )
        t.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
        t.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )
        t.SetBranchAddress('SemiLepMETpt'        , SemiLepMETpt        )
        t.SetBranchAddress('SemiLepMETphi'       , SemiLepMETphi       )
        t.SetBranchAddress('SemiLepNvtx'         , SemiLepNvtx         )
        t.SetBranchAddress('FatJetDeltaPhiLep'      , FatJetDeltaPhiLep      )
        t.SetBranchAddress('NearestAK4JetBDisc'            ,NearestAK4JetBDisc             )
        t.SetBranchAddress('NearestAK4JetPt'     ,NearestAK4JetPt      )
        t.SetBranchAddress('NearestAK4JetEta'    ,NearestAK4JetEta     )
        t.SetBranchAddress('NearestAK4JetPhi'    ,NearestAK4JetPhi     )
        t.SetBranchAddress('NearestAK4JetMass'   ,NearestAK4JetMass    )
        t.SetBranchAddress('NearestAK4JetJECUpSys'      , NearestAK4JetJECUpSys)
        t.SetBranchAddress('NearestAK4JetJECDnSys'      , NearestAK4JetJECDnSys)
        t.SetBranchAddress('NearestAK4JetJERUpSys'      , NearestAK4JetJERUpSys)
        t.SetBranchAddress('NearestAK4JetJERDnSys'      , NearestAK4JetJERDnSys)
        t.SetBranchAddress('SemiLeptRunNum'         ,  SemiLeptRunNum       )
        t.SetBranchAddress('SemiLeptLumiNum'      ,  SemiLeptLumiNum    )
        t.SetBranchAddress('SemiLeptEventNum'       ,  SemiLeptEventNum     )


        t.SetBranchStatus ('*', 0)
        t.SetBranchStatus ('SemiLeptWeight', 1)
        t.SetBranchStatus ('PUWeight', 1)
        t.SetBranchStatus ('GenWeight', 1)
        t.SetBranchStatus ('FatJetPt', 1)
        t.SetBranchStatus ('FatJetEta', 1)
        t.SetBranchStatus ('FatJetPhi', 1)
        t.SetBranchStatus ('FatJetMass', 1)
        t.SetBranchStatus ('FatJetMassSoftDrop', 1)
        t.SetBranchStatus ('FatJetTau32', 1)
        t.SetBranchStatus ('SemiLeptTrig', 1)
        t.SetBranchStatus ('NearestAK4JetBDisc', 1)
        t.SetBranchStatus ('NearestAK4JetPt'   ,1 )
        t.SetBranchStatus ('NearestAK4JetEta'  ,1 )
        t.SetBranchStatus ('NearestAK4JetPhi'  ,1 )
        t.SetBranchStatus ('NearestAK4JetMass' ,1 )
        t.SetBranchStatus ('SemiLepMETpt' , 1 )
        t.SetBranchStatus ('SemiLepMETphi' , 1 )
        t.SetBranchStatus ('LeptonType'          , 1 )
        t.SetBranchStatus ('LeptonPt'            , 1)
        t.SetBranchStatus ('LeptonEta'           , 1)
        t.SetBranchStatus ('LeptonPhi'           , 1)
        t.SetBranchStatus ('LeptonEnergy'        , 1)
        t.SetBranchStatus ('LeptonIso'           , 1)
        t.SetBranchStatus ('LeptonPtRel'         , 1)
        t.SetBranchStatus ('LeptonDRMin'         , 1)


        entries = t.GetEntriesFast()
        print 'Processing tree ' + str(itree)

        eventsToRun = entries

        for jentry in xrange( eventsToRun ):
            if jentry % 100000 == 0 :
                print 'processing ' + str(jentry)
            # get the next tree in the chain and verify
            ientry = t.GetEntry( jentry )
            if ientry < 0:
                break


            if options.is_electron and LeptonType[0] != 11:
                continue
            elif not options.is_electron and LeptonType[0] !=13:
                continue

            if not options.is_bkg and options.is_electron:
                if SemiLeptTrig[1] != 1 and SemiLeptTrig[2] != 1 :
                    continue
            elif not options.is_bkg and not options.is_electron:
                if SemiLeptTrig[0] != 1  :
                    continue

            hadTopCandP4 = ROOT.TLorentzVector()
            hadTopCandP4.SetPtEtaPhiM( FatJetPt[0], FatJetEta[0], FatJetPhi[0], FatJetMass[0])
            bJetCandP4 = ROOT.TLorentzVector()
            bJetCandP4.SetPtEtaPhiM( NearestAK4JetPt[0], NearestAK4JetEta[0], NearestAK4JetPhi[0], NearestAK4JetMass[0])
            nuCandP4 = ROOT.TLorentzVector( )
            nuCandP4.SetPtEtaPhiM( SemiLepMETpt[0], 0, SemiLepMETphi[0], SemiLepMETpt[0] )
            theLepton = ROOT.TLorentzVector()
            theLepton.SetPtEtaPhiE( LeptonPt[0], LeptonEta[0], LeptonPhi[0], LeptonEnergy[0] ) # Assume massless


            tau32 = FatJetTau32[0]
            mass_sd = FatJetMassSoftDrop[0]
            bdisc = NearestAK4JetBDisc[0]

            passKin = hadTopCandP4.Perp() > 400.
            passTopTag = tau32 < 0.6 and mass_sd > 110. and mass_sd < 250.
            pass2DCut = LeptonPtRel[0] > 55. or LeptonDRMin[0] > 0.4
            passBtag = bdisc > 0.7

            if options.enable_top_tagging:
                if not passKin or not pass2DCut or not passBtag or not passTopTag :
                    continue
            else:
                if not passKin or not pass2DCut or not passBtag:
                    continue


            ##  ____  __.__                              __  .__         __________
            ## |    |/ _|__| ____   ____   _____ _____ _/  |_|__| ____   \______   \ ____   ____  ____
            ## |      < |  |/    \_/ __ \ /     \\__  \\   __\  |/ ___\   |       _// __ \_/ ___\/  _ \
            ## |    |  \|  |   |  \  ___/|  Y Y  \/ __ \|  | |  \  \___   |    |   \  ___/\  \__(  <_> )
            ## |____|__ \__|___|  /\___  >__|_|  (____  /__| |__|\___  >  |____|_  /\___  >\___  >____/
            ##         \/       \/     \/      \/     \/             \/          \/     \/     \/

            # Now we do our kinematic calculation based on the categories of the
            # number of top and bottom tags
            mttbar = -1.0


            lepTopCandP4 = None
            # Get the z-component of the lepton from the W mass constraint
            solution, nuz1, nuz2 = solve_nu( vlep=theLepton, vnu=nuCandP4 )
            # If there is at least one real solution, pick it up
            if solution :
                nuCandP4.SetPz( nuz1 )
            else :
                nuCandP4.SetPz( nuz1.real )

            lepTopCandP4 = nuCandP4 + theLepton + bJetCandP4

            ttbarCand = hadTopCandP4 + lepTopCandP4
            mttbar = ttbarCand.M()
            # Fill Histograms

            #Mass histograms
            h_mttbar.Fill( mttbar, SemiLeptWeight[0] )
            h_mtopHadGroomed.Fill( mass_sd, SemiLeptWeight[0] )
            h_mtopHad.Fill( hadTopCandP4.M(), SemiLeptWeight[0] )
            h_mfatjet.Fill(FatJetMass[0], SemiLeptWeight[0])

            h_mAK4Jet.Fill(NearestAK4JetMass[0],SemiLeptWeight[0])
            h_mlepTop.Fill(ttbarCand)

            #pt histograms
            h_fatjetpt.Fill(FatJetPt[0], SemiLeptWeight[0])
            h_leppt.Fill(LeptonPt[0], SemiLeptWeight[0])
            h_AK4Jetpt.Fill(NearestAK4JetPt[0],SemiLeptWeight[0])

            h_lepTop.Fill(lepTopCandP4[0],SemiLeptWeight[0])
            h_ttbarpt.Fill(ttbarCand[0],SemiLeptWeight[0])
            
            #eta histograms
            h_fatjeteta.Fill(FatJetEta[0],SemiLeptWeight[0])
            h_lepeta.Fill(LeptonEta[0],SemiLeptWeight[0])
            h_AK4JETeta.Fill(NearestAK4JetEta[0],SemiLeptWeight[0])
            h_lepTopeta.Fill(lepTopCandP4[1],SemiLeptWeight[0])
            h_ttbareta.Fill(ttbarCand[1],SemiLeptWeight[0])

            #phi histograms
            h_fatjetphi.Fill(FatJetPhi[0], SemiLeptWeight[0])
            h_lepphi.Fill(LeptonPhi[0],SemiLeptWeight[0])
            h_AK4Jetphi.Fill(NearestAK4JetEta[0],SemiLeptWeight[0])

            h_lepTopphi.Fill(lepTopCandp4[1],SemiLeptWeight[0])
            h_ttbarphi.Fill(ttbarCand[2],SemiLeptWeight[0])

            #MET histograms
            h_MET.Fill(SemiLepMETpt[0],SemiLeptWeight[0])
            # h_METphi.Fill(semiLepMETphi[0],SemiLeptWeight[0])

            #other histograms
            h_fatjettau32.Fill(FatJetTau32[0],SemiLeptWeight[0])
            h_fatjettau21.Fill(FatJetTau21[0],SemiLeptWeight[0])

            h_deltaRfatjetvslepTop.Fill(LeptonDRMin[0],SemiLeptWeight[0])
            h_btag.Fill(bdisc,SemiLeptWeight[0])

    fout.cd()
    fout.Write()
    fout.Close()

if __name__ == "__main__" :
    plot_mttbar(sys.argv)
