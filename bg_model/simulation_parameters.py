# -*- coding: utf-8 -*-

__author__ = "Zafeirios Fountas"
__credits__ = ["Murray Shanahan", "Mark Humphries",  "Rob Leech", "Jeanette Hellgren Kotaleski"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Zafeirios Fountas"
__email__ = "fountas@outlook.com"
__status__ = "Published"

from brian import *
from neuron_parameters import data as pars
from synaptic_parameters import data as pars_syn

class SimulationParameters(object) :

    def __init__(self) :
        # Load neuron parameters
        self.neur = dict()
        self.neur["MSN"] = pars["MSN"]
        self.neur["FSI"] = pars["FSI"]
        self.neur["STN-typeA"] = pars["STN-typeA"]
        self.neur["STN-typeB"] = pars["STN-typeB"]
        self.neur["STN-typeC"] = pars["STN-typeC"]
        self.neur["GPe-typeA"] = pars["GPe-typeA"]
        self.neur["GPe-typeB"] = pars["GPe-typeB"]
        self.neur["GPe-typeC"] = pars["GPe-typeC"]
        self.neur["SNr"] = pars["SNr"]

        # Load synaptic parameters
        self.syn = dict()
        self.syn["MSN"] = pars_syn["MSN"]
        self.syn["FSI"] = pars_syn["FSI"]
        self.syn["STN"] = pars_syn["STN"]
        self.syn["GPe"] = pars_syn["GPe"]
        self.syn["SNr"] = pars_syn["SNr"]
        #print "All parameters loaded."
        

    def get_vpeak(self, neuron) :
        return pars[neuron]['vpeak']['value']


    # -- EXPERIMENT PARAMETERS -------------------------------------------------
    T1_amp = 2.5 * Hz       # Rate (amplitude) of first stimulus 
    T2_amp = 5.0 * Hz       # Rate (amplitude) of second stimulus
    base_input_T1 = 3.0*Hz     
    base_input_T2 = 3.0*Hz     
    base_input_T3 = 3.0*Hz  # Consistent with Belforte et al 2010 and Reed et al 2010.
                            # Also it is also consistent with Bauswein 1989 (Humphries 2006)
    DOPAMINE = 0.8
    iFreq_LOW_T1 = 0.0
    iFreq_HIGH_T1 = 0.0
    iFreq_LOW_T2 = 0.0
    iFreq_HIGH_T2 = 0.0
    iPhase_LOW = 0.0 # * np.pi
    

    # -- NUMBERS ---------------------------------------------------------------
    N = 3                   # Humphries - Number of channels
    Ninput = 1000           # Number of input sources (neurons)
    C = 300                 # Times that the BG is scaled down
    N_str   = 2790000/C     # Oorschot 1996
    Nstn    = 13600/C       # Oorschot 1996
    Ngpe    = 46000/C       # Oorschot 1996
    Ngpi    = 3200/C        # Oorschot 1996
    Nsnr    = 26300/C       # Oorschot 1996
    Nsnc    = 7200/C        # Oorschot 1996

    # Adding FSIs
    FSIratio = 0.01         # Humphries 2010 - FSIs: 1% of striatal neurons
    Nfsi = int( FSIratio * float(N_str) )
    Nmsn = N_str - Nfsi

    Ngpisnr = (3200+26300)/C# 
    Nmsn_d1 = Nmsn/2        # 
    Nmsn_d2 = Nmsn/2        # 

    Nmsn_ch = Nmsn/(2*N)    # Number of neurons within a channel in striatum
    Nstn_ch = Nstn/N        # Number of neurons within a channel in stn
    Ngpe_ch = Ngpe/N        # Number of neurons within a channel in gpe
    Ngpisnr_ch = Ngpisnr/N  # Number of neurons within a channel in GPi/SNr

    
    # -- SYNAPSES --------------------------------------------------------------    
    # Humphries 2014
    # In the random model we ignored distance, and simply made connections to 
    # each neuron at random until the correct number of incoming connections of 
    # each type was made. The target number of connections were derived from the
    # mean values obtained from the central neurons of the three-dimensional 
    # connectivity model in Humphries et al. (2010), and taken from column 1 of 
    # Table 5 in that paper: 
    # SPNs → 1 SPN: 728; 
    # FSIs → 1 SPN: 30.6; 
    # FSIs → 1 FSI: 12.8; 
    # FSI gap junctions per FSI: 0.65.

    # CORTICAL INPUT:
    P_T_MSN = 0.084
    P_T_FSI = P_T_MSN # From Humphries 2010
    P_T_STN = 0.03    # Produces 20 Hz (40 in high mode) without inhibition, and 
    #                   NOTE: Lindahl 2013 also estimated this - no data evailable

    # STRIATUM
    # From Humphries:2010 and Tomkins:2013 and after properly simulating the 
    # channel spatially (explanation in Fountas et al, 2017)
    P_MSN_MSN_in = 0.0718
    P_MSN_MSN_ex = 0.0082

    P_FSI_MSN_in = 0.2925
    P_FSI_MSN_ex = 0.0314

    P_FSI_FSI_in = 0.5864
    P_FSI_FSI_ex = 0.0092

    P_FSI_GAP_in = 0.1082
    P_FSI_GAP_ex = 0.0003

    # --------------------------------------------------------------------------    

    P_CONNECTIONS = "Lindahl"

    if P_CONNECTIONS == "Humphries" :
        _Pc = 0.25           # Humphries - Probability of connectivity
        _P_STN = _Pc / N     # Humphries - Probability of connectivity of STN

        P_STN_GPe = _P_STN
        P_GPe_STN = _Pc
        P_STN_SNr = _P_STN
        P_SD1_SNr = _Pc
        P_SD2_GPe = _Pc
        P_GPe_SNr = _Pc
        P_GPe_GPe = 0.1 # Fountas 2017
        P_SNr_SNr = 0.1 # Fountas 2017

    elif P_CONNECTIONS == "Lindahl" :
        P_STN_GPe = 0.3 # Lindahl says 30% (30 out of 100 STNs are connected to each GPe)
        P_GPe_STN = 0.1 # Lindahl says 10% (30 out of 300 GPes are connected to each STN)
        P_STN_SNr = 0.3 # Lindahl says 30% (30 out of 100 STNs are connected to each SNr)
        P_MSN_SNr = 0.033 # Lindahl says 3.3% (500 out of 15000 MSNs are connected to each SNr)
        P_MSN_GPe = 0.033 # Lindahl says 3.3% (500 out of 15000 MSNs are connected to each GPe)
        P_GPe_SNr = 0.1066 # Lindahl says 10.66% (32 out of 300 GPes are connected to each SNr)
        P_GPe_GPe = 0.1 # Lindahl says 10% (30 out of 300 GPes are connected to each GPe)
        P_SNr_SNr = 0.1 # Lindahl does not mention SNr collaterals
    
    # -- SIMULATION PARAMETERS -------------------------------------------------
    DT = 0.25*ms    # Simulation timestep
    duration = 2000 * ms
    fr_depth = 50 * ms  # Fountas 2017
    # because: fr_depth = int(FREQUENCY/2) * ms

    # --------------------------------------------------------------------------





    # Technique:    ampa = 1.0/(1.0+R)
    #               nmda = R/(1.0+R)
    def resetSynapticParametersWithRatios(self, R_msn, R_stn, R_gpe, R_snr) :
        self.syn["MSN"]["R"] = float(R_msn)
        self.syn["STN"]["R"] = float(R_stn)
        self.syn["GPe"]["R"] = float(R_gpe)
        self.syn["SNr"]["R"] = float(R_snr)

        self.syn["MSN"]["G"]["AMPA"]["value"] = 1.0/(1.0 + self.syn["MSN"]["R"])
        self.syn["MSN"]["G"]["NMDA"]["value"]  = \
                               self.syn["MSN"]["R"]/(1.0 + self.syn["MSN"]["R"])
        self.syn["MSN"]["G"]["GABA"]["value"]  = 1.0

        self.syn["STN"]["G"]["AMPA"]["value"] = 1.0/(1.0 + self.syn["STN"]["R"])
        self.syn["STN"]["G"]["NMDA"]["value"]  = \
                               self.syn["STN"]["R"]/(1.0 + self.syn["STN"]["R"])
        self.syn["STN"]["G"]["GABA"]["value"]  = 1.0

        self.syn["GPe"]["G"]["AMPA"]["value"] = 1.0/(1.0 + self.syn["GPe"]["R"])
        self.syn["GPe"]["G"]["NMDA"]["value"]  = \
                               self.syn["GPe"]["R"]/(1.0 + self.syn["GPe"]["R"])
        self.syn["GPe"]["G"]["GABA"]["value"]  = 1.0

        self.syn["SNr"]["G"]["AMPA"]["value"] = 1.0/(1.0 + self.syn["SNr"]["R"])
        self.syn["SNr"]["G"]["NMDA"]["value"]  = \
                               self.syn["SNr"]["R"]/(1.0 + self.syn["SNr"]["R"])
        self.syn["SNr"]["G"]["GABA"]["value"]  = 1.0

    delta_abs = 2 * ms  # Humphries
    ita = 0.5           # Humphries
    V_lim = - 20 * mV   # Humphries
    
    # Used and mentioned as very significant in: Wolf,Moyer,Lazarewicz etal 2005
    ratio_NMDAoverAMPA = 0.5    # Myme etal 2003, Sugino, Turrigiano, Nelson
    # --------------------------------------------------------------------------























