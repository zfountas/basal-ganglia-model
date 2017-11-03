
__author__ = "Zafeirios Fountas"
__credits__ = ["Murray Shanahan", "Mark Humphries",  "Rob Leech", "Jeanette Hellgren Kotaleski"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Zafeirios Fountas"
__email__ = "fountas@outlook.com"
__status__ = "Published"

from brian import *
from os import path, mkdir
import numpy as np
import time
from gc import collect # Garbage collector
import random as pyrandom 
from helper_functions import *
from simulation_parameters import SimulationParameters
from equations import NeuronEquations


# ---------------------------------------------------------------------------- #
#                             BASAL GANGLIA CLASS                              #
# ---------------------------------------------------------------------------- #
class BasalGanglia(object) :

    def __init__(self, PLOTS=False, PRINT = True, SEED = 1000) :
        self.PRINT = PRINT

        if self.PRINT == True :
            print "---------------------------------------------- "
            print "     *    BASAL GANGLIA SIMULATION     *       "
            print "     *                                 *       "
            print "     *    author: Zafeirios Fountas    *       "
        print "---------------------------------------------- "
        
        self.global_time = time.time()

        self.net = Network()

        self.final_score = 0
        self.FOLDER = ''
        self.data = dict()
        self.choices_gpe = []
        self.choices_stn = []
        self.PLOTS = PLOTS

       
        # -- INITIALIZE SIMULATION PARAMETERS AND EQUATIONS --------------------
        self.pars = SimulationParameters()
        self.eqs = NeuronEquations()

        self.SD1toSD2_CONNECTIONS = True
        self.weight_Bahuguna = 1.5
        
        self.ALL_TO_ALL_MSNs = False
        # Show graphs with all STNs individually!
        self.SHOW_STNs = False 
        #self.BASIC_TUNING = True # Used to just show firing rates of the nuclei
        self.DETERMINISTIC_TYPES = True

        # Record binned spike data!
        self.RECORD_BINS = False
        self.RECORD_RASTERS = False
        self.RECORD_GPe_types = False
        
        # In PD off state we set PD_OFF_WEIGHT = 1.1, DOP = 0.0
        self.PD_OFF_WEIGHT = 1.0
        # If 0,1 or 2 it will allow only this neuron type!
        self.GPe_type = -1 

        # Activation of synapses
        self.GAP_JUNCTIONS = True
        self.SYNAPSES_STRIATUM = True
        self.SYNAPSES_CTX_STN = True
        self.SYNAPSES_CTX_SD1 = True
        self.SYNAPSES_CTX_SD2 = True
        self.SYNAPSES_CTX_FSI = True
        self.SYNAPSES_SD1_SNr = True
        self.SYNAPSES_SD2_GPe = True
        self.SYNAPSES_STN_SNr = True
        self.SYNAPSES_STN_GPe = True ####### STN-GPe loop #######
        self.SYNAPSES_GPe_STN = True ####### STN-GPe loop #######
        self.SYNAPSES_GPe_SNr = True
        self.SYNAPSES_GPe_GPe = True
        self.SYNAPSES_SNr_SNr = True

        # Activation of nuclei
        self.ACTIVATE_MSN = True
        self.ACTIVATE_FSI = True
        self.ACTIVATE_STN = True
        self.ACTIVATE_GPe = True
        self.ACTIVATE_SNr = True
        
        # Plasticity parameters
        self.Plasticity = False
        self.STDep_GPe = 0.0
        self.STDep_STN = 0.0
        self.STPot_SD1 = 0.0
        self.STPot_SD2 = 0.0

        self.END = 1000000*ms
        self.RAMP = -1


        # RANDOM SEED!   
        self.mySeed = SEED

        # To make it random ;)
        if self.mySeed == 0 :
            self.mySeed = int(pyrandom.random() * 1000.0)
            
        seed(seed=self.mySeed)
        np.random.seed(seed=self.mySeed)
        pyrandom.seed(self.mySeed)
        defaultclock.dt = self.pars.DT # Simulation timestep
    

    def print_features(self) :
        print "Features:"
        print " - Total number of neurons:", self.pars.Nmsn + self.pars.Nfsi +\
              self.pars.Nstn + self.pars.Ngpe + self.pars.Nsnr, "(", \
              "Nmsn:", self.pars.Nmsn, "Nfsi:", self.pars.Nfsi,\
              "Nstn:", self.pars.Nstn, "Ngpe:", self.pars.Ngpe,\
              "Nsnr:", self.pars.Nsnr, ")"
        #print " - NMDA:AMPA ratio in MSNs:", self.pars.syn["MSN"]["R"]
        #print " - NMDA:AMPA ratio in STN:", self.pars.syn["STN"]["R"]
        #print " - NMDA:AMPA ratio in GPe:", self.pars.syn["GPe"]["R"]
        #print " - NMDA:AMPA ratio in SNr:", self.pars.syn["SNr"]["R"]
        print " - P_CTX-MSN:", self.pars.P_T_MSN
        print " - P_CTX-FSI:", self.pars.P_T_FSI
        print " - P_CTX-STN:", self.pars.P_T_STN
        print " - P_MSN-MSN-in:", self.pars.P_MSN_MSN_in
        print " - P_MSN-MSN-ex:", self.pars.P_MSN_MSN_ex
        print " - P_FSI-MSN-in:", self.pars.P_FSI_MSN_in
        print " - P_FSI-MSN-ex:", self.pars.P_FSI_MSN_ex
        print " - P_FSI-FSI-in:", self.pars.P_FSI_FSI_in
        print " - P_FSI-FSI-ex:", self.pars.P_FSI_FSI_ex
        print " - P_STN-GPe:", self.pars.P_STN_GPe
        print " - P_GPe-STN:", self.pars.P_GPe_STN
        print " - P_STN-SNr:", self.pars.P_STN_SNr
        print " - P_SD1-SNr:", self.pars.P_MSN_SNr
        print " - P_SD2-GPe:", self.pars.P_MSN_GPe
        print " - P_GPe-SNr:", self.pars.P_GPe_SNr
        print " - P_GPe-GPe:", self.pars.P_GPe_GPe
        print " - P_SNr-SNr:", self.pars.P_SNr_SNr
        print ""
        print " - T1_amp:", self.pars.T1_amp
        print " - T2_amp:", self.pars.T2_amp
        print " - base freq_T1:", self.pars.base_input_T1
        print " - base freq_T2:", self.pars.base_input_T2
        print " - base freq_T3:", self.pars.base_input_T3
        print ""
        print " - freq_T1:", self.pars.iFreq_LOW_T1
        print " - freq_T2:", self.pars.iFreq_LOW_T2
        print " - phase offset:", self.pars.iPhase_LOW
        print " - Dopamine:", self.pars.DOPAMINE
        print ""
        if self.Plasticity == True :
            print " - Plasticity is on!"
        else :
            print " - No plasticity."
        print ""
        print " - Random seed:", self.mySeed
        print " - fr_depth:", self.pars.fr_depth

    def init_neurons(self, experiment="none") :
        if self.PRINT == True :
            start_time = time.time()
        # ARCHITECTURE:
        if experiment == "initial_period" :
            INPUT_START = 500*ms
        else :
            INPUT_START = 0*ms

        if experiment == "random_walk" :
            walk_list1 = RandWalkList(LOW = 0.0, HIGH = 10.0)#NOTE: default duration!!
            walk_list2 = RandWalkList(LOW = 0.0, HIGH = 10.0)#NOTE: default duration!!
            walk_list3 = RandWalkList(LOW = 0.0, HIGH = 10.0)#NOTE: default duration!!

        if experiment == "random_walk" :
            self.T1 = PoissonGroup(self.pars.Ninput, 
                                   rates=lambda t: ListRates(t, walk_list1))
        elif float(self.RAMP) > 0 :
            self.T1 = PoissonGroup(self.pars.Ninput, 
                              rates=lambda t: RampRates(t, start = INPUT_START, 
                                                        end = 500*ms + self.END,
                                                        ramp_dur = self.RAMP*ms,
                                                        base=self.pars.base_input_T1, 
                                                        freqLOW=self.pars.iFreq_LOW_T1, 
                                                        freqHIGH=self.pars.iFreq_HIGH_T1, 
                                                        phaseLOW=0.0,
                                                        Tamp = self.pars.T1_amp))
        else :
            self.T1 = PoissonGroup(self.pars.Ninput, 
                              rates=lambda t: T1rates_tr(t, start = INPUT_START, 
                                                         end = 500*ms + self.END,
                                                         base=self.pars.base_input_T1, 
                                                         freqLOW=self.pars.iFreq_LOW_T1, 
                                                         freqHIGH=self.pars.iFreq_HIGH_T1, 
                                                         T1_amp = self.pars.T1_amp))
    
        if experiment == "random_walk" :
            self.T2 = PoissonGroup(self.pars.Ninput, 
                                   rates=lambda t: ListRates(t, walk_list2))
        elif float(self.RAMP) > 0 :
            self.T2 = PoissonGroup(self.pars.Ninput, 
                              rates=lambda t: RampRates(t, start = INPUT_START, 
                                                        end = 500*ms + self.END,
                                                        ramp_dur = self.RAMP*ms,
                                                        base=self.pars.base_input_T2, 
                                                         freqLOW=self.pars.iFreq_LOW_T2, 
                                                         freqHIGH=self.pars.iFreq_HIGH_T2, 
                                                         phaseLOW=self.pars.iPhase_LOW,
                                                         Tamp = self.pars.T2_amp))
        else :
            self.T2 = PoissonGroup(self.pars.Ninput, 
                              rates=lambda t: T2rates_tr(t, start = INPUT_START, 
                                                         end = 500*ms + self.END,
                                                         base=self.pars.base_input_T2, 
                                                         freqLOW=self.pars.iFreq_LOW_T2, 
                                                         freqHIGH=self.pars.iFreq_HIGH_T2, 
                                                         phaseLOW=self.pars.iPhase_LOW,
                                                         T2_amp = self.pars.T2_amp))
        if experiment == "random_walk" :
            self.T3 = PoissonGroup(self.pars.Ninput, 
                                   rates=lambda t: ListRates(t, walk_list3))
        else :
            self.T3 = PoissonGroup(self.pars.Ninput, rates = self.pars.base_input_T3)
        self.net.add(self.T1)
        self.net.add(self.T2)
        self.net.add(self.T3)

        if self.ACTIVATE_FSI == True :
            self.FSI = NeuronGroup(self.pars.Nfsi, model=self.eqs.izhi_eqs_FSI, 
                                   threshold = "v>=vpeak",
                                   reset=self.eqs.izhi_reset_FSI)
            self.net.add(self.FSI)
    
        if self.GAP_JUNCTIONS == True :
            self.GAPS = NeuronGroup(int(self.pars.Nfsi*0.65), 
                                    model=self.eqs.eqs_gap,
                                    threshold=100, reset=0)
            self.net.add(self.GAPS)
    
        if self.ACTIVATE_MSN == True :
            if experiment == "GPe tuning" or experiment == "SNr tuning" :
                self.SD1 = PoissonGroup(self.pars.Nmsn_d1, rates = 1.0 * Hz)
                self.SD2 = PoissonGroup(self.pars.Nmsn_d2, rates = 1.0 * Hz)
            else :
                self.SD1 = NeuronGroup(self.pars.Nmsn_d1, model=self.eqs.izhi_eqs_MSN,
                                       threshold="v>=vpeak",
                                       reset=self.eqs.izhi_reset_MSN)
                self.SD2 = NeuronGroup(self.pars.Nmsn_d2, model=self.eqs.izhi_eqs_MSN,
                                       threshold="v>=vpeak",
                                       reset=self.eqs.izhi_reset_MSN)
            self.net.add(self.SD1)
            self.net.add(self.SD2)

        if self.ACTIVATE_SNr == True :
            self.SNr = NeuronGroup(self.pars.Nsnr, model=self.eqs.izhi_eqs_snr, 
                                   threshold = "v>=vpeak", 
                                   reset=self.eqs.izhi_reset)
            self.net.add(self.SNr)
    
        if self.ACTIVATE_STN == True :
            if experiment == "GPe tuning" or experiment == "SNr tuning" or experiment == "zaf":
                self.STN = PoissonGroup(self.pars.Nstn, rates = 10.0 * Hz)
            else :
                self.STN = NeuronGroup(self.pars.Nstn, model=self.eqs.izhi_eqs_stn, 
                                  threshold = self.eqs.threshold_stn, 
                                  reset=izhi_reset_stn)
            self.net.add(self.STN)

        if self.ACTIVATE_GPe == True :
            if experiment == "STN tuning with GPe" or experiment == "SNr tuning":
                self.GPe = PoissonGroup(self.pars.Ngpe, rates = 30*Hz)
            else :
                self.GPe = NeuronGroup(self.pars.Ngpe, model=self.eqs.izhi_eqs_gpe, 
                                       threshold = "v>=vpeak",
                                       reset=self.eqs.izhi_reset)
            self.net.add(self.GPe)

        if self.PRINT == True :
            print "Neurons ok! (", time.time() - start_time, "sec )"


        self.init_neuron_parameters()
 

    # -- NEURON PARAMETERS -----------
    def init_neuron_parameters(self) :
        if self.PRINT == True :
            start_time = time.time()


        # -- Short-term plasticity parameters ----- (Perfect!) -----------------
        self.STDep_GPe = 0.154#self.eqs.U_GPe # In 30Hz according to the graph
        self.STDep_STN = 0.283#self.eqs.U_STN # In 10Hz        - '' -
        self.STPot_SD1 = 1.5  *self.eqs.U_SD1 # In 1.1Hz       - '' -           
        self.STPot_SD2 = 1.05 *self.eqs.U_SD2 # In 1.1Hz       - '' -           

 
        # -- STN PARAMETERS --------------------------------------------------------
        if self.ACTIVATE_STN == True :
            if self.DETERMINISTIC_TYPES == True :
                self.choices_stn = three_det_choices(self.pars.Nstn, self.pars.N,
                                            self.pars.neur["STN-typeA"]["density"]["value"],
                                            self.pars.neur["STN-typeB"]["density"]["value"],
                                            "typeA", "typeB", "typeC")
            else :
                self.choices_stn = three_choices(self.pars.Nstn,
                                        self.pars.neur["STN-typeA"]["density"]["value"],
                                        self.pars.neur["STN-typeB"]["density"]["value"],
                                        "typeA", "typeB", "typeC")

            if self.SHOW_STNs == True :
                self.MY_NEURON = -1

            self.STN.tau_ampa_CTX = self.pars.syn["STN"]["tau"]["AMPA"]["value"]
            self.STN.tau_nmda_CTX = self.pars.syn["STN"]["tau"]["NMDA"]["value"]
            self.STN.tau_gaba_GPe = self.pars.syn["STN"]["tau"]["GABA"]["value"]
            self.STN.E_ampa =       self.pars.syn["STN"]["E"]["AMPA"]["value"]
            self.STN.E_nmda =       self.pars.syn["STN"]["E"]["NMDA"]["value"]
            self.STN.E_gaba =       self.pars.syn["STN"]["E"]["GABA"]["value"]
            self.STN.G_ampa_CTX =   self.pars.syn["STN"]["G"]["AMPA"]["value"]*self.PD_OFF_WEIGHT
            self.STN.G_nmda_CTX =   self.pars.syn["STN"]["G"]["NMDA"]["value"]*self.PD_OFF_WEIGHT
            self.STN.G_gaba_GPe =   self.pars.syn["STN"]["G"]["GABA"]["value"]
            self.STN.Dop1 =         self.pars.DOPAMINE
            self.STN.Dop2 =         self.pars.DOPAMINE
            self.STN.Istim =        0.0*pA

            for i,neuron in zip(range(len(self.STN)), self.choices_stn) :
                if self.SHOW_STNs == True :
                    print neuron
                    if neuron == "typeC" and self.MY_NEURON == -1:
                        self.MY_NEURON = i
                self.STN[i].u1 =           self.pars.neur["STN-"+neuron]["u1"]["value"]
                self.STN[i].u2 =           self.pars.neur["STN-"+neuron]["u2"]["value"]
                self.STN[i].v =            self.pars.neur["STN-"+neuron]["v"]["value"]

                self.STN[i].Ispon =     self.pars.neur["STN-"+neuron]["Ivivo"]["value"] #- 16*pA
                self.STN[i].a1 =        self.pars.neur["STN-"+neuron]["a1"]["value"]
                self.STN[i].b1 =        self.pars.neur["STN-"+neuron]["b1"]["value"]
                self.STN[i].c =         self.pars.neur["STN-"+neuron]["c"]["value"]
                self.STN[i].d1 =        self.pars.neur["STN-"+neuron]["d1"]["value"]
                self.STN[i].a2 =        self.pars.neur["STN-"+neuron]["a2"]["value"]
                self.STN[i].b2 =        self.pars.neur["STN-"+neuron]["b2"]["value"]
                self.STN[i].d2 =        self.pars.neur["STN-"+neuron]["d2"]["value"]
                self.STN[i].vr2 =       self.pars.neur["STN-"+neuron]["vr2"]["value"]
                self.STN[i].b_thres =   self.pars.neur["STN-"+neuron]["b_thres"]["value"]
                self.STN[i].k =         self.pars.neur["STN-"+neuron]["k"]["value"]
                self.STN[i].vr =        self.pars.neur["STN-"+neuron]["vr"]["value"]
                self.STN[i].vt =        self.pars.neur["STN-"+neuron]["vt"]["value"]
                self.STN[i].C =         self.pars.neur["STN-"+neuron]["C"]["value"]
                self.STN[i].C =         get_random_C(self.pars.neur["STN-"+neuron]["C"]["value"], 
                                       self.pars.neur["STN-"+neuron]["C_var"]["value"],1,
                                       self.mySeed)*pF
                self.STN[i].vpeak = self.pars.neur["STN-"+neuron]["vpeak"]["value"]
                self.STN[i].w1 =        self.pars.neur["STN-"+neuron]["w1"]["value"]
                self.STN[i].w2 =        self.pars.neur["STN-"+neuron]["w2"]["value"]
    
        # -- GPe PARAMETERS --------------------------------------------------------
        if self.ACTIVATE_GPe == True :
            if self.GPe_type == -1 :
                if self.DETERMINISTIC_TYPES == True :
                    self.choices_gpe = three_det_choices(self.pars.Ngpe, self.pars.N,
                                                self.pars.neur["GPe-typeA"]["density"]["value"],
                                                self.pars.neur["GPe-typeB"]["density"]["value"],
                                                "typeA", "typeB", "typeC")
                else :
                    self.choices_gpe = three_choices(self.pars.Ngpe,
                                            self.pars.neur["GPe-typeA"]["density"]["value"],
                                            self.pars.neur["GPe-typeB"]["density"]["value"],
                                            "typeA", "typeB", "typeC")
            elif self.GPe_type == 1 :
                if self.DETERMINISTIC_TYPES == True :
                    self.choices_gpe = three_det_choices(self.pars.Ngpe, self.pars.N,
                                                0.0, 1.0, "typeA", "typeB", "typeC")
                else :
                    self.choices_gpe = three_choices(self.pars.Ngpe,
                                                0.0, 1.0, "typeA", "typeB", "typeC")
            elif self.GPe_type == 0 :
                if self.DETERMINISTIC_TYPES == True :
                    self.choices_gpe = three_det_choices(self.pars.Ngpe, self.pars.N,
                                                1.0, 0.0, "typeA", "typeB", "typeC")
                else :
                    self.choices_gpe = three_choices(self.pars.Ngpe,
                                                1.0, 0.0, "typeA", "typeB", "typeC")
            elif self.GPe_type == 2 :
                if self.DETERMINISTIC_TYPES == True :
                    self.choices_gpe = three_det_choices(self.pars.Ngpe, self.pars.N,
                                                0.0, 0.0, "typeA", "typeB", "typeC")
                else :
                    self.choices_gpe = three_choices(self.pars.Ngpe,
                                                0.0, 0.0, "typeA", "typeB", "typeC")
            else :
                print "GPe type not recognized. Exiting.."
                exit()
            
            self.GPe.tau_ampa_STN = self.pars.syn["GPe"]["tau"]["STN-GPe"]["AMPA"]["value"]
            self.GPe.tau_nmda_STN = self.pars.syn["GPe"]["tau"]["STN-GPe"]["NMDA"]["value"]
            self.GPe.tau_gaba_GPe = self.pars.syn["GPe"]["tau"]["GPe-GPe"]["GABA"]["value"]
            self.GPe.tau_gaba_MSN = self.pars.syn["GPe"]["tau"]["MSN-GPe"]["GABA"]["value"]
            self.GPe.E_ampa =       self.pars.syn["GPe"]["E"]["AMPA"]["value"]
            self.GPe.E_nmda =       self.pars.syn["GPe"]["E"]["NMDA"]["value"]
            self.GPe.E_gaba =       self.pars.syn["GPe"]["E"]["GABA"]["value"]
            self.GPe.G_ampa_STN =   self.pars.syn["GPe"]["G"]["STN-GPe"]["AMPA"]["value"]
            self.GPe.G_nmda_STN =   self.pars.syn["GPe"]["G"]["STN-GPe"]["NMDA"]["value"]
            self.GPe.G_gaba_GPe =   self.pars.syn["GPe"]["G"]["GPe-GPe"]["GABA"]["value"]
            self.GPe.G_gaba_MSN =   self.pars.syn["GPe"]["G"]["MSN-GPe"]["GABA"]["value"]
            self.GPe.Dop1 =         self.pars.DOPAMINE
            self.GPe.Dop2 =         self.pars.DOPAMINE
            self.GPe.Istim =        0.0*pA #1.91*pA
    

            if self.Plasticity == True :
                self.GPe.G_gaba_MSN = self.pars.syn["GPe"]["G"]["MSN-GPe"]["GABA"]["value"]/self.STPot_SD2 # Because SD2 is connected to GPe
            if self.GPe_type != -1 : print self.choices_gpe
            for i,neuron in zip(range(len(self.GPe)), self.choices_gpe) :
                self.GPe[i].u =            self.pars.neur["GPe-"+neuron]["u"]["value"]
                self.GPe[i].v =            self.pars.neur["GPe-"+neuron]["v"]["value"]
                self.GPe[i].Ispon =     self.pars.neur["GPe-"+neuron]["Ivivo"]["value"]#+ 40*pA # 20*pA
                self.GPe[i].a =         self.pars.neur["GPe-"+neuron]["a"]["value"]
                self.GPe[i].b =         self.pars.neur["GPe-"+neuron]["b"]["value"]
                self.GPe[i].c =         self.pars.neur["GPe-"+neuron]["c"]["value"]
                self.GPe[i].d =         self.pars.neur["GPe-"+neuron]["d"]["value"]
                self.GPe[i].k =         self.pars.neur["GPe-"+neuron]["k"]["value"]
                self.GPe[i].vr =        self.pars.neur["GPe-"+neuron]["vr"]["value"]
                self.GPe[i].vt =        self.pars.neur["GPe-"+neuron]["vt"]["value"]
                self.GPe[i].C =         self.pars.neur["GPe-"+neuron]["C"]["value"]
                self.GPe[i].C =         get_random_C(self.pars.neur["GPe-"+neuron]["C"]["value"], 
                                        self.pars.neur["GPe-"+neuron]["C_var"]["value"],1,
                                        self.mySeed)*pF
                #self.GPe[i].C =         self.pars.neur["GPe-"+neuron]["C"]["value"]*pF
                self.GPe[i].vpeak = self.pars.neur["GPe-"+neuron]["vpeak"]["value"]
    
    
        # -- SNr PARAMETERS -------------------------------------------------------
        if self.ACTIVATE_SNr == True :
            self.SNr.u =            self.pars.neur["SNr"]["u"]["value"]
            self.SNr.v =            self.pars.neur["SNr"]["v"]["value"]
            self.SNr.tau_ampa_STN = self.pars.syn["SNr"]["tau"]["STN-SNr"]["AMPA"]["value"]
            self.SNr.tau_nmda_STN = self.pars.syn["SNr"]["tau"]["STN-SNr"]["NMDA"]["value"]
            self.SNr.tau_gaba_SNr = self.pars.syn["SNr"]["tau"]["SNr-SNr"]["GABA"]["value"]
            self.SNr.tau_gaba_MSN = self.pars.syn["SNr"]["tau"]["MSN-SNr"]["GABA"]["value"]
            self.SNr.tau_gaba_GPe = self.pars.syn["SNr"]["tau"]["GPe-SNr"]["GABA"]["value"]
            self.SNr.E_ampa =       self.pars.syn["SNr"]["E"]["AMPA"]["value"]
            self.SNr.E_nmda =       self.pars.syn["SNr"]["E"]["NMDA"]["value"]
            self.SNr.E_gaba =       self.pars.syn["SNr"]["E"]["GABA"]["value"]
            self.SNr.G_ampa_STN =   self.pars.syn["SNr"]["G"]["STN-SNr"]["AMPA"]["value"]
            self.SNr.G_nmda_STN =   self.pars.syn["SNr"]["G"]["STN-SNr"]["NMDA"]["value"]
            self.SNr.G_gaba_SNr=    self.pars.syn["SNr"]["G"]["SNr-SNr"]["GABA"]["value"]
            self.SNr.G_gaba_MSN=    self.pars.syn["SNr"]["G"]["MSN-SNr"]["GABA"]["value"]
            self.SNr.G_gaba_GPe=    self.pars.syn["SNr"]["G"]["GPe-SNr"]["GABA"]["value"]
            self.SNr.Dop1 =         0.0
            self.SNr.Dop2 =         0.0
            self.SNr.Istim =        80.0*pA # Second best pars set: 48.0*pA
            self.SNr.Ispon =        self.pars.neur["SNr"]["Ivivo"]["value"]
            self.SNr.a =            self.pars.neur["SNr"]["a"]["value"]
            self.SNr.b =            self.pars.neur["SNr"]["b"]["value"]
            self.SNr.c =            self.pars.neur["SNr"]["c"]["value"]
            self.SNr.d =            self.pars.neur["SNr"]["d"]["value"]
            self.SNr.k =            self.pars.neur["SNr"]["k"]["value"]
            self.SNr.vr =           self.pars.neur["SNr"]["vr"]["value"]
            self.SNr.vt =           self.pars.neur["SNr"]["vt"]["value"]
            self.SNr.C = get_random_C(self.pars.neur["SNr"]["C"]["value"], 
                                    self.pars.neur["SNr"]["C_var"]["value"], 
                                    self.pars.Nsnr,self.mySeed)*pF
            self.SNr.vpeak =        self.pars.neur["SNr"]["vpeak"]["value"]

            if self.Plasticity == True :
                self.SNr.G_gaba_MSN = self.pars.syn["SNr"]["G"]["MSN-SNr"]["GABA"]["value"]/self.STPot_SD1 # Because SD1 is connected to SNr

                self.SNr.G_gaba_GPe = self.pars.syn["SNr"]["G"]["GPe-SNr"]["GABA"]["value"]/self.STDep_GPe

                self.SNr.G_ampa_STN = self.pars.syn["SNr"]["G"]["STN-SNr"]["AMPA"]["value"]/self.STDep_STN
                self.SNr.G_nmda_STN = self.pars.syn["SNr"]["G"]["STN-SNr"]["NMDA"]["value"]/self.STDep_STN

    
        # -- FSI PARAMETERS -------------------------------------------------------
        if self.ACTIVATE_FSI == True :
            self.FSI.u =         self.pars.neur["FSI"]["u"]["value"]
            self.FSI.v =         self.pars.neur["FSI"]["v"]["value"]
            self.FSI.tau_ampa =  self.pars.syn["FSI"]["tau"]["AMPA"]["value"]
            self.FSI.tau_gaba =  self.pars.syn["FSI"]["tau"]["GABA"]["value"]
            self.FSI.E_ampa =    self.pars.syn["FSI"]["E"]["AMPA"]["value"]
            self.FSI.E_gaba =    self.pars.syn["FSI"]["E"]["GABA"]["value"]
            self.FSI.G_ampa =    self.pars.syn["FSI"]["G"]["Ctx-FSI"]["AMPA"]["value"]*self.PD_OFF_WEIGHT
            self.FSI.G_gaba =    self.pars.syn["FSI"]["G"]["FSI-FSI"]["GABA"]["value"]
            self.FSI.Dop1 =      self.pars.DOPAMINE
            self.FSI.Dop2 =      self.pars.DOPAMINE
            self.FSI.Istim =     0.0*pA
            self.FSI.Ispon =     self.pars.neur["FSI"]["Ispon"]["value"]
            self.FSI.a =         self.pars.neur["FSI"]["a"]["value"]
            self.FSI.b =         self.pars.neur["FSI"]["b"]["value"]
            self.FSI.c =         self.pars.neur["FSI"]["c"]["value"]
            self.FSI.d =         self.pars.neur["FSI"]["d"]["value"]
            self.FSI.k =         self.pars.neur["FSI"]["k"]["value"]
            self.FSI.vr =        self.pars.neur["FSI"]["vr"]["value"]
            self.FSI.vt =        self.pars.neur["FSI"]["vt"]["value"]
            self.FSI.C = np.random.normal(self.pars.neur["FSI"]["C"]["value"], 
                                 self.pars.neur["FSI"]["C"]["value"]*0.1, self.pars.Nfsi)
            self.FSI.vb =        self.pars.neur["FSI"]["vb"]["value"]
            self.FSI.vpeak =     self.pars.neur["FSI"]["vpeak"]["value"]
    
    
        # -- GAP JUNCTIONS PARAMETERS -----------------------------------------
        if self.GAP_JUNCTIONS == True :
            self.GAPS.tau_gap = self.pars.syn["FSI"]["gap"]["tau"]["value"]

        # -- MSN PARAMETERS --------------------------------------------------------
        if self.ACTIVATE_MSN == True :
            self.SD1.u =         self.pars.neur["MSN"]["u"]["value"]
            self.SD1.v =         self.pars.neur["MSN"]["v"]["value"]
            self.SD1.tau_ampa =  self.pars.syn["MSN"]["tau"]["AMPA"]["value"]
            self.SD1.tau_nmda =  self.pars.syn["MSN"]["tau"]["NMDA"]["value"]
            self.SD1.tau_gaba =  self.pars.syn["MSN"]["tau"]["GABA"]["value"]
            self.SD1.E_ampa =    self.pars.syn["MSN"]["E"]["AMPA"]["value"]
            self.SD1.E_nmda =    self.pars.syn["MSN"]["E"]["NMDA"]["value"]
            self.SD1.E_gaba =    self.pars.syn["MSN"]["E"]["GABA"]["value"]
            self.SD1.G_ampa =    self.pars.syn["MSN"]["G"]["Ctx-MSN"]["AMPA"]["value"]*self.PD_OFF_WEIGHT
            self.SD1.G_nmda =    self.pars.syn["MSN"]["G"]["Ctx-MSN"]["NMDA"]["value"]*self.PD_OFF_WEIGHT
            self.SD1.G_gaba_MSN =self.pars.syn["MSN"]["G"]["MSN-MSN"]["GABA"]["value"]#*self.weight_Bahuguna
            self.SD1.G_gaba_FSI =self.pars.syn["MSN"]["G"]["FSI-MSN"]["GABA"]["value"]#*self.weight_Bahuguna
            self.SD1.Dop1 =      self.pars.DOPAMINE
            self.SD1.Dop2 =      0.0
            self.SD1.Istim =     0.0*pA
            self.SD1.Ispon =     self.pars.neur["MSN"]["Ispon"]["value"]
            self.SD1.a =         self.pars.neur["MSN"]["a"]["value"]
            self.SD1.b =         self.pars.neur["MSN"]["b"]["value"]
            self.SD1.c =         self.pars.neur["MSN"]["c"]["value"]
            self.SD1.d =         self.pars.neur["MSN"]["d"]["value"]
            self.SD1.k =         self.pars.neur["MSN"]["k"]["value"]
            self.SD1.vr =        self.pars.neur["MSN"]["vr"]["value"]
            self.SD1.vt =        self.pars.neur["MSN"]["vt"]["value"]
            self.SD1.C = np.random.normal(self.pars.neur["MSN"]["C"]["value"], 
                                 self.pars.neur["MSN"]["C"]["value"]*0.1, self.pars.Nmsn_d1)
            self.SD1.vpeak =     self.pars.neur["MSN"]["vpeak"]["value"]
        
            self.SD2.u =         self.pars.neur["MSN"]["u"]["value"]
            self.SD2.v =         self.pars.neur["MSN"]["v"]["value"]
            #self.SD2.ratio = self.pars.ratio_str
            self.SD2.tau_ampa =  self.pars.syn["MSN"]["tau"]["AMPA"]["value"]
            self.SD2.tau_nmda =  self.pars.syn["MSN"]["tau"]["NMDA"]["value"]
            self.SD2.tau_gaba =  self.pars.syn["MSN"]["tau"]["GABA"]["value"]
            self.SD2.E_ampa =    self.pars.syn["MSN"]["E"]["AMPA"]["value"]
            self.SD2.E_nmda =    self.pars.syn["MSN"]["E"]["NMDA"]["value"]
            self.SD2.E_gaba =    self.pars.syn["MSN"]["E"]["GABA"]["value"]
            self.SD2.G_ampa =    self.pars.syn["MSN"]["G"]["Ctx-MSN"]["AMPA"]["value"]*self.PD_OFF_WEIGHT
            self.SD2.G_nmda =    self.pars.syn["MSN"]["G"]["Ctx-MSN"]["NMDA"]["value"]*self.PD_OFF_WEIGHT
            self.SD2.G_gaba_MSN =self.pars.syn["MSN"]["G"]["MSN-MSN"]["GABA"]["value"]
            self.SD2.G_gaba_FSI =self.pars.syn["MSN"]["G"]["FSI-MSN"]["GABA"]["value"]
            self.SD2.Dop1 =      0.0
            self.SD2.Dop2 =      self.pars.DOPAMINE
            self.SD2.Istim =     0.0*pA
            self.SD2.Ispon =     self.pars.neur["MSN"]["Ispon"]["value"]
            self.SD2.a =         self.pars.neur["MSN"]["a"]["value"]
            self.SD2.b =         self.pars.neur["MSN"]["b"]["value"]
            self.SD2.c =         self.pars.neur["MSN"]["c"]["value"]
            self.SD2.d =         self.pars.neur["MSN"]["d"]["value"]
            self.SD2.k =         self.pars.neur["MSN"]["k"]["value"]
            self.SD2.vr =        self.pars.neur["MSN"]["vr"]["value"]
            self.SD2.vt =        self.pars.neur["MSN"]["vt"]["value"]
            self.SD2.C = np.random.normal(self.pars.neur["MSN"]["C"]["value"], 
                                 self.pars.neur["MSN"]["C"]["value"]*0.1, self.pars.Nmsn_d2)
            self.SD2.vpeak =     self.pars.neur["MSN"]["vpeak"]["value"]

        if self.PRINT == True :
            print "Neuron parameters ok! (", time.time() - start_time, "sec )"

    # == SYNAPSES ==============================================================
    def init_synapses(self) :
        if self.PRINT == True :
            start_time = time.time()
        if self.ACTIVATE_FSI == True :
            self.ch_fsi = len(self.FSI)/self.pars.N
        if self.ACTIVATE_MSN == True :
            self.ch_sd1 = len(self.SD1)/self.pars.N
            self.ch_sd2 = len(self.SD2)/self.pars.N
        if self.ACTIVATE_STN == True :
            self.ch_stn = len(self.STN)/self.pars.N
        if self.ACTIVATE_SNr == True :
            self.ch_snr = len(self.SNr)/self.pars.N
        if self.ACTIVATE_GPe == True :
            self.ch_gpe = len(self.GPe)/self.pars.N
        
        EXC_PRE = '''g_ampa+=1.0*nS
                     g_nmda+=1.0*nS'''

        # -- Cortical (poisson) inputs -----------------------------------------
        if self.SYNAPSES_CTX_SD1 == True :
            self.ConT11 = Synapses(self.T1, self.SD1, model='', pre = EXC_PRE)
            self.ConT11.connect_random(self.T1, self.SD1[0:self.ch_sd1], sparseness=self.pars.P_T_MSN)
            self.ConT11.delay = 10*ms
            self.ConT21 = Synapses(self.T2, self.SD1, model='', pre = EXC_PRE)
            self.ConT21.connect_random(self.T2, self.SD1[self.ch_sd1:2*self.ch_sd1], sparseness=self.pars.P_T_MSN)
            self.ConT21.delay = 10*ms
            self.ConT31 = Synapses(self.T3, self.SD1, model='', pre = EXC_PRE)
            self.ConT31.connect_random(self.T3, self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_T_MSN)
            self.ConT31.delay = 10*ms
            self.net.add(self.ConT11)
            self.net.add(self.ConT21)
            self.net.add(self.ConT31)
        
        if self.SYNAPSES_CTX_STN == True :
            self.ConT12 = Synapses(self.T1, self.STN, model='', pre = '''g_ampa_CTX+=1.0*nS
                                                                   g_nmda_CTX+=1.0*nS''')
            self.ConT12.connect_random(self.T1, self.STN[0:self.ch_stn], sparseness=self.pars.P_T_STN)
            self.ConT12.delay = 2.5*ms # Lindahl agrees from Fujimoto and Kita 1993
            self.ConT22 = Synapses(self.T2, self.STN, model='', pre = '''g_ampa_CTX+=1.0*nS
                                                                   g_nmda_CTX+=1.0*nS''')
            self.ConT22.connect_random(self.T2, self.STN[self.ch_stn:2*self.ch_stn], sparseness=self.pars.P_T_STN)
            self.ConT22.delay = 2.5*ms # Lindahl agrees from Fujimoto and Kita 1993
            self.ConT32 = Synapses(self.T3, self.STN, model='', pre = '''g_ampa_CTX+=1.0*nS
                                                                   g_nmda_CTX+=1.0*nS''')
            self.ConT32.connect_random(self.T3, self.STN[2*self.ch_stn:3*self.ch_stn], sparseness=self.pars.P_T_STN)
            self.ConT32.delay = 2.5*ms # Lindahl agrees from Fujimoto and Kita 1993
            self.net.add(self.ConT12)
            self.net.add(self.ConT22)
            self.net.add(self.ConT32)
    
        if self.SYNAPSES_CTX_SD2 == True :    
            self.ConT13 = Synapses(self.T1, self.SD2, model='', pre = EXC_PRE)
            self.ConT13.connect_random(self.T1, self.SD2[0:self.ch_sd2], sparseness=self.pars.P_T_MSN)
            self.ConT13.delay = 10*ms
            self.ConT23 = Synapses(self.T2, self.SD2, model='', pre = EXC_PRE)
            self.ConT23.connect_random(self.T2, self.SD2[self.ch_sd2:2*self.ch_sd2], sparseness=self.pars.P_T_MSN)
            self.ConT23.delay = 10*ms
            self.ConT33 = Synapses(self.T3, self.SD2, model='', pre = EXC_PRE)
            self.ConT33.connect_random(self.T3, self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_T_MSN)
            self.ConT33.delay = 10*ms
            self.net.add(self.ConT13)
            self.net.add(self.ConT23)
            self.net.add(self.ConT33)
        
        if self.SYNAPSES_CTX_FSI == True :
            self.ConT14 = Synapses(self.T1, self.FSI, model='', pre = '''g_ampa+=1.0*nS''')
            self.ConT14.connect_random(self.T1, self.FSI[0:self.ch_fsi], sparseness=self.pars.P_T_FSI)
            self.ConT14.delay = 10*ms
            self.ConT24 = Synapses(self.T2, self.FSI, model='', pre = '''g_ampa+=1.0*nS''')
            self.ConT24.connect_random(self.T2, self.FSI[self.ch_fsi:2*self.ch_fsi], sparseness=self.pars.P_T_FSI)
            self.ConT24.delay = 10*ms
            self.ConT34 = Synapses(self.T3, self.FSI, model='', pre = '''g_ampa+=1.0*nS''')
            self.ConT34.connect_random(self.T3, self.FSI[2*self.ch_fsi:3*self.ch_fsi], sparseness=self.pars.P_T_FSI)
            self.ConT34.delay = 10*ms
            self.net.add(self.ConT14)
            self.net.add(self.ConT24)
            self.net.add(self.ConT34)
        # --------------------------------------------------------------------------
    
        if self.SYNAPSES_STRIATUM == True:

            # Gap Junctions!!
            if self.GAP_JUNCTIONS == True :
                # Define synapses                
                self.ConGap1=Synapses(self.FSI, self.GAPS, 
                                 model='''g:siemens # gap junction conductance
                                          Vgap=(v_pre-v_post) : mV''')
                self.ConGapn =Synapses(self.GAPS, self.FSI, 
                                  model='''g:siemens# gap junction conductance
                                           Igap=g*(v_pre-v_post) : amp''')
                self.ConGap2=Synapses(self.FSI, self.GAPS, 
                                 model='''g:siemens # gap junction conductance
                                          Vgap=(v_pre-v_post) : mV''')
                self.net.add(self.ConGap1, self.ConGapn, self.ConGap2)

                # Find connections
                sources = np.random.randint(0, len(self.FSI), len(self.GAPS))
                exists = []
                # For every gap junction
                for g in range(len(self.GAPS)) :
                    source = sources[g]
                    target = pyrandom.choice(range(0,source)+range(source+1,len(self.FSI)))
                    while (source, target) in exists :
                        target = pyrandom.choice(range(0,source)+range(source+1,len(self.FSI)))
                
                    #print source, target
                    self.ConGap1[source,g] = True
                    self.ConGap2[target,g] = True
                    self.ConGapn[g,source] = True
                    self.ConGapn[g,target] = True
                    exists.append((source, target))
                
                # Connect the variables
                self.GAPS.Vgap1 = self.ConGap1.Vgap
                self.GAPS.Vgap2 = self.ConGap2.Vgap
                self.FSI.Igap = self.ConGapn.Igap

                self.ConGap1.g = 0.0 # Not used anyway!
                self.ConGap2.g = 0.0 # Not used anyway!
                self.ConGapn.g = self.pars.syn["FSI"]["gap"]["g"]["value"]

            # -- Latteral Connectivity in Striatum ---------------------------------------------------------------------------------------
            if self.ACTIVATE_FSI == True :
                self.Con_fsi_fsi = Synapses(self.FSI, self.FSI, model='', pre='''g_gaba+=1.0*nS''')

                # Connect Channels Internally
                self.Con_fsi_fsi.connect_random(self.FSI[0:self.ch_fsi],               self.FSI[0:self.ch_fsi],               sparseness=self.pars.P_FSI_FSI_in)
                self.Con_fsi_fsi.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.FSI[self.ch_fsi:2*self.ch_fsi],   sparseness=self.pars.P_FSI_FSI_in)
                self.Con_fsi_fsi.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.FSI[2*self.ch_fsi:3*self.ch_fsi], sparseness=self.pars.P_FSI_FSI_in)

                # Connect Channels Externally
                self.Con_fsi_fsi.connect_random(self.FSI[0:self.ch_fsi],               self.FSI[self.ch_fsi:2*self.ch_fsi],   sparseness=self.pars.P_FSI_FSI_ex)
                self.Con_fsi_fsi.connect_random(self.FSI[0:self.ch_fsi],               self.FSI[2*self.ch_fsi:3*self.ch_fsi], sparseness=self.pars.P_FSI_FSI_ex)
             
                self.Con_fsi_fsi.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.FSI[0:self.ch_fsi],               sparseness=self.pars.P_FSI_FSI_ex)
                self.Con_fsi_fsi.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.FSI[2*self.ch_fsi:3*self.ch_fsi], sparseness=self.pars.P_FSI_FSI_ex)
            
                self.Con_fsi_fsi.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.FSI[0:self.ch_fsi],               sparseness=self.pars.P_FSI_FSI_ex)
                self.Con_fsi_fsi.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.FSI[self.ch_fsi:2*self.ch_fsi],   sparseness=self.pars.P_FSI_FSI_ex)

                self.Con_fsi_fsi.delay = 1*ms
                self.net.add(self.Con_fsi_fsi)
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


                self.Con_fsi_sd1 = Synapses(self.FSI, self.SD1, model='', pre ='''g_gaba_FSI+=1.0*nS''')

                # Connect Channels Internally
                self.Con_fsi_sd1.connect_random(self.FSI[0:self.ch_fsi],               self.SD1[0:self.ch_sd1],               sparseness=self.pars.P_FSI_MSN_in*self.weight_Bahuguna)
                self.Con_fsi_sd1.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.SD1[  self.ch_sd1:2*self.ch_sd1], sparseness=self.pars.P_FSI_MSN_in*self.weight_Bahuguna)
                self.Con_fsi_sd1.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_FSI_MSN_in*self.weight_Bahuguna)

                # Connect Channels Externally
                self.Con_fsi_sd1.connect_random(self.FSI[0:self.ch_fsi],               self.FSI[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_FSI_MSN_ex*self.weight_Bahuguna)
                self.Con_fsi_sd1.connect_random(self.FSI[0:self.ch_fsi],               self.FSI[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_FSI_MSN_ex*self.weight_Bahuguna)
             
                self.Con_fsi_sd1.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.FSI[0:self.ch_sd1],               sparseness=self.pars.P_FSI_MSN_ex*self.weight_Bahuguna)
                self.Con_fsi_sd1.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.FSI[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_FSI_MSN_ex*self.weight_Bahuguna)
            
                self.Con_fsi_sd1.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.FSI[0:self.ch_sd1],               sparseness=self.pars.P_FSI_MSN_ex*self.weight_Bahuguna)
                self.Con_fsi_sd1.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.FSI[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_FSI_MSN_ex*self.weight_Bahuguna)

                self.Con_fsi_sd1.delay = 1*ms
                self.net.add(self.Con_fsi_sd1)
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


                self.Con_fsi_sd2 = Synapses(self.FSI, self.SD2, model='', pre ='''g_gaba_FSI+=1.0*nS''')

                # Connect Channels Internally
                self.Con_fsi_sd2.connect_random(self.FSI[0:self.ch_fsi],               self.SD2[0:self.ch_sd2],               sparseness=self.pars.P_FSI_MSN_in*(2.0-self.weight_Bahuguna))
                self.Con_fsi_sd2.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.SD2[  self.ch_sd2:2*self.ch_sd2], sparseness=self.pars.P_FSI_MSN_in*(2.0-self.weight_Bahuguna))
                self.Con_fsi_sd2.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_FSI_MSN_in*(2.0-self.weight_Bahuguna))

                # Connect Channels Externally
                self.Con_fsi_sd2.connect_random(self.FSI[0:self.ch_fsi],               self.FSI[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_FSI_MSN_ex*(2.0-self.weight_Bahuguna))
                self.Con_fsi_sd2.connect_random(self.FSI[0:self.ch_fsi],               self.FSI[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_FSI_MSN_ex*(2.0-self.weight_Bahuguna))
             
                self.Con_fsi_sd2.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.FSI[0:self.ch_sd2],               sparseness=self.pars.P_FSI_MSN_ex*(2.0-self.weight_Bahuguna))
                self.Con_fsi_sd2.connect_random(self.FSI[self.ch_fsi:2*self.ch_fsi],   self.FSI[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_FSI_MSN_ex*(2.0-self.weight_Bahuguna))
            
                self.Con_fsi_sd2.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.FSI[0:self.ch_sd2],               sparseness=self.pars.P_FSI_MSN_ex*(2.0-self.weight_Bahuguna))
                self.Con_fsi_sd2.connect_random(self.FSI[2*self.ch_fsi:3*self.ch_fsi], self.FSI[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_FSI_MSN_ex*(2.0-self.weight_Bahuguna))

                self.Con_fsi_sd2.delay = 1*ms
                self.net.add(self.Con_fsi_sd2)
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





            self.ConSD1SD1 = Synapses(self.SD1,self.SD1, model='', pre='''g_gaba_MSN+=0.4*nS''') # Taverna:2008

            self.ConSD1SD1.connect_random(self.SD1[0:self.ch_sd1],               self.SD1[0:self.ch_sd1],               sparseness=self.pars.P_MSN_MSN_in)
            self.ConSD1SD1.connect_random(self.SD1[0:self.ch_sd1],               self.SD1[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_MSN_MSN_ex)
            self.ConSD1SD1.connect_random(self.SD1[0:self.ch_sd1],               self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_MSN_MSN_ex)
        
            self.ConSD1SD1.connect_random(self.SD1[self.ch_sd1:2*self.ch_sd1],   self.SD1[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_MSN_MSN_in)
            self.ConSD1SD1.connect_random(self.SD1[self.ch_sd1:2*self.ch_sd1],   self.SD1[0:self.ch_sd1],               sparseness=self.pars.P_MSN_MSN_ex)
            self.ConSD1SD1.connect_random(self.SD1[self.ch_sd1:2*self.ch_sd1],   self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_MSN_MSN_ex)
        
            self.ConSD1SD1.connect_random(self.SD1[2*self.ch_sd1:3*self.ch_sd1], self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_MSN_MSN_in)
            self.ConSD1SD1.connect_random(self.SD1[2*self.ch_sd1:3*self.ch_sd1], self.SD1[0:self.ch_sd1],               sparseness=self.pars.P_MSN_MSN_ex)
            self.ConSD1SD1.connect_random(self.SD1[2*self.ch_sd1:3*self.ch_sd1], self.SD1[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_MSN_MSN_ex)

            self.ConSD1SD1.delay = 1*ms
            self.net.add(self.ConSD1SD1)


            self.ConSD2SD2 = Synapses(self.SD2,self.SD2, model='', pre='''g_gaba_MSN+=1.0*nS''')

            self.ConSD2SD2.connect_random(self.SD2[0:self.ch_sd2],               self.SD2[0:self.ch_sd2],               sparseness=self.pars.P_MSN_MSN_in)
            self.ConSD2SD2.connect_random(self.SD2[0:self.ch_sd2],               self.SD2[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_MSN_MSN_ex)
            self.ConSD2SD2.connect_random(self.SD2[0:self.ch_sd2],               self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_MSN_MSN_ex)
        
            self.ConSD2SD2.connect_random(self.SD2[self.ch_sd2:2*self.ch_sd2],   self.SD2[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_MSN_MSN_in)
            self.ConSD2SD2.connect_random(self.SD2[self.ch_sd2:2*self.ch_sd2],   self.SD2[0:self.ch_sd2],               sparseness=self.pars.P_MSN_MSN_ex)
            self.ConSD2SD2.connect_random(self.SD2[self.ch_sd2:2*self.ch_sd2],   self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_MSN_MSN_ex)
        
            self.ConSD2SD2.connect_random(self.SD2[2*self.ch_sd2:3*self.ch_sd2], self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_MSN_MSN_in)
            self.ConSD2SD2.connect_random(self.SD2[2*self.ch_sd2:3*self.ch_sd2], self.SD2[0:self.ch_sd2],               sparseness=self.pars.P_MSN_MSN_ex)
            self.ConSD2SD2.connect_random(self.SD2[2*self.ch_sd2:3*self.ch_sd2], self.SD2[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_MSN_MSN_ex)

            self.ConSD2SD2.delay = 1*ms
            self.net.add(self.ConSD2SD2)


            self.ConSD1SD2 = Synapses(self.SD1,self.SD2, model='', pre='''g_gaba_MSN+=1.0*nS''')

            self.ConSD1SD2.connect_random(self.SD1[0:self.ch_sd1],               self.SD2[0:self.ch_sd2],               sparseness=self.pars.P_MSN_MSN_in*(2.0-self.weight_Bahuguna))
            self.ConSD1SD2.connect_random(self.SD1[0:self.ch_sd1],               self.SD2[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_MSN_MSN_ex*(2.0-self.weight_Bahuguna))
            self.ConSD1SD2.connect_random(self.SD1[0:self.ch_sd1],               self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_MSN_MSN_ex*(2.0-self.weight_Bahuguna))
        
            self.ConSD1SD2.connect_random(self.SD1[self.ch_sd1:2*self.ch_sd1],   self.SD2[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_MSN_MSN_in*(2.0-self.weight_Bahuguna))
            self.ConSD1SD2.connect_random(self.SD1[self.ch_sd1:2*self.ch_sd1],   self.SD2[0:self.ch_sd2],               sparseness=self.pars.P_MSN_MSN_ex*(2.0-self.weight_Bahuguna))
            self.ConSD1SD2.connect_random(self.SD1[self.ch_sd1:2*self.ch_sd1],   self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_MSN_MSN_ex*(2.0-self.weight_Bahuguna))
        
            self.ConSD1SD2.connect_random(self.SD1[2*self.ch_sd1:3*self.ch_sd1], self.SD2[2*self.ch_sd2:3*self.ch_sd2], sparseness=self.pars.P_MSN_MSN_in*(2.0-self.weight_Bahuguna))
            self.ConSD1SD2.connect_random(self.SD1[2*self.ch_sd1:3*self.ch_sd1], self.SD2[0:self.ch_sd2],               sparseness=self.pars.P_MSN_MSN_ex*(2.0-self.weight_Bahuguna))
            self.ConSD1SD2.connect_random(self.SD1[2*self.ch_sd1:3*self.ch_sd1], self.SD2[self.ch_sd2:2*self.ch_sd2],   sparseness=self.pars.P_MSN_MSN_ex*(2.0-self.weight_Bahuguna))

            self.ConSD1SD2.delay = 1*ms
            self.net.add(self.ConSD1SD2)



            self.ConSD2SD1 = Synapses(self.SD2,self.SD1, model='', pre='''g_gaba_MSN+=1.2*nS''') # Taverna:2008

            self.ConSD2SD1.connect_random(self.SD2[0:self.ch_sd2],               self.SD1[0:self.ch_sd1],               sparseness=self.pars.P_MSN_MSN_in*self.weight_Bahuguna)
            self.ConSD2SD1.connect_random(self.SD2[0:self.ch_sd2],               self.SD1[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_MSN_MSN_ex*self.weight_Bahuguna)
            self.ConSD2SD1.connect_random(self.SD2[0:self.ch_sd2],               self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_MSN_MSN_ex*self.weight_Bahuguna)
        
            self.ConSD2SD1.connect_random(self.SD2[self.ch_sd2:2*self.ch_sd2],   self.SD1[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_MSN_MSN_in*self.weight_Bahuguna)
            self.ConSD2SD1.connect_random(self.SD2[self.ch_sd2:2*self.ch_sd2],   self.SD1[0:self.ch_sd1],               sparseness=self.pars.P_MSN_MSN_ex*self.weight_Bahuguna)
            self.ConSD2SD1.connect_random(self.SD2[self.ch_sd2:2*self.ch_sd2],   self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_MSN_MSN_ex*self.weight_Bahuguna)
        
            self.ConSD2SD1.connect_random(self.SD2[2*self.ch_sd2:3*self.ch_sd2], self.SD1[2*self.ch_sd1:3*self.ch_sd1], sparseness=self.pars.P_MSN_MSN_in*self.weight_Bahuguna)
            self.ConSD2SD1.connect_random(self.SD2[2*self.ch_sd2:3*self.ch_sd2], self.SD1[0:self.ch_sd1],               sparseness=self.pars.P_MSN_MSN_ex*self.weight_Bahuguna)
            self.ConSD2SD1.connect_random(self.SD2[2*self.ch_sd2:3*self.ch_sd2], self.SD1[self.ch_sd1:2*self.ch_sd1],   sparseness=self.pars.P_MSN_MSN_ex*self.weight_Bahuguna)

            self.ConSD2SD1.delay = 1*ms
            self.net.add(self.ConSD2SD1)

            # ----------------------------------------------------------------------------------------------------------------------------

        if self.SYNAPSES_STN_GPe == True :
            self.Con11 = Synapses(self.STN, self.GPe, model='w:volt',pre = '''g_ampa_STN+=1.0*nS
                                                                         g_nmda_STN+=1.0*nS''')
            self.Con11.connect_random(self.STN, self.GPe, sparseness=self.pars.P_STN_GPe)
            # Lindahl says 30% (30 out of 100 STNs are connected to each GPe)
            self.Con11.delay = 2*ms # Lindahl says 5ms from Ammari etal 2010
            self.net.add(self.Con11)
    
        if self.SYNAPSES_GPe_STN == True :
            self.Con18 = Synapses(self.GPe, self.STN, model='w:volt', pre = '''g_gaba_GPe+=1.0*nS''')
            self.Con18.connect_random(self.GPe[0:self.ch_gpe],          self.STN[0:self.ch_stn],          sparseness=self.pars.P_GPe_STN)
            self.Con18.connect_random(self.GPe[  self.ch_gpe:2*self.ch_gpe], self.STN[self.ch_stn:2*self.ch_stn],   sparseness=self.pars.P_GPe_STN)
            self.Con18.connect_random(self.GPe[2*self.ch_gpe:3*self.ch_gpe], self.STN[2*self.ch_stn:3*self.ch_stn], sparseness=self.pars.P_GPe_STN)
            # Lindahl says 10% (30 out of 300 GPes are connected to each STN)
            self.Con18.delay = 4*ms # Lindahl says 5ms from Baufreton et al 2005
            self.net.add(self.Con18)

        if self.SYNAPSES_STN_SNr == True :
            if self.Plasticity == False :
                self.Con10 = Synapses(self.STN, self.SNr, model='w:volt',
                                      pre='''g_ampa_STN+=1.0*nS
                                             g_nmda_STN+=1.0*nS''')
            else :
                self.Con10 = Synapses(self.STN, self.SNr,
                                      model = self.eqs.stp_model("STN"), 
                                      pre = self.eqs.stp_pre("STN") )

            self.Con10.connect_random(self.STN, self.SNr, sparseness=self.pars.P_STN_SNr)
            # Lindahl says 30% (30 out of 100 STNs are connected to each SNr)
            self.Con10.delay = 1.5*ms # Lindahl says 4.5 from Shen and Johnson 2006 and Ammari etal 2010
            if self.Plasticity == True :
                self.Con10.x = 1
                self.Con10.y = 1
                self.Con10.u_syn = self.eqs.U_STN
            self.net.add(self.Con10)
        
        if self.SYNAPSES_SD1_SNr == True :
            if self.Plasticity == False :
                self.Con12 = Synapses(self.SD1, self.SNr, model='w:volt', 
                                      pre = '''g_gaba_MSN+=1.0*nS''')
            else :
                self.Con12 = Synapses(self.SD1, self.SNr, 
                                      model = self.eqs.stp_model("SD1"), 
                                      pre = self.eqs.stp_pre("SD1") )

            self.Con12.connect_random(self.SD1[0:self.ch_sd1],          self.SNr[0:self.ch_snr],          sparseness=self.pars.P_MSN_SNr)
            self.Con12.connect_random(self.SD1[self.ch_sd1:2*self.ch_sd1],   self.SNr[  self.ch_snr:2*self.ch_snr], sparseness=self.pars.P_MSN_SNr)
            self.Con12.connect_random(self.SD1[2*self.ch_sd1:3*self.ch_sd1], self.SNr[2*self.ch_snr:3*self.ch_snr], sparseness=self.pars.P_MSN_SNr)
            # Lindahl says 3.3% (500 out of 15000 MSNs are connected to each SNr)
            self.Con12.delay = 4*ms # Lindahl says 7ms from conelly etal 2010
            if self.Plasticity == True :
                self.Con12.x = 1
                self.Con12.y = 1
                self.Con12.u_syn = self.eqs.U_SD1
            self.net.add(self.Con12)


            
        if self.SYNAPSES_SD2_GPe == True :
            if self.Plasticity == False :
                self.Con15 = Synapses(self.SD2, self.GPe, model='w:volt', 
                                      pre = '''g_gaba_MSN+=1.0*nS''')
            else :
                self.Con15 = Synapses(self.SD2, self.GPe, 
                                      model = self.eqs.stp_model("SD2"), 
                                      pre = self.eqs.stp_pre("SD2") )
                                      
            self.Con15.connect_random(self.SD2[0:self.ch_sd2],          self.GPe[0:self.ch_gpe],          sparseness=self.pars.P_MSN_GPe)
            self.Con15.connect_random(self.SD2[  self.ch_sd2:2*self.ch_sd2], self.GPe[  self.ch_gpe:2*self.ch_gpe], sparseness=self.pars.P_MSN_GPe)
            self.Con15.connect_random(self.SD2[2*self.ch_sd2:3*self.ch_sd2], self.GPe[2*self.ch_gpe:3*self.ch_gpe], sparseness=self.pars.P_MSN_GPe)
            # Lindahl says 3.3% (500 out of 15000 MSNs are connected to each GPe)
            self.Con15.delay = 5*ms # Lindahl says 7ms from Park etal 1982
            if self.Plasticity == True :
                self.Con15.x = 1
                self.Con15.y = 1
                self.Con15.u_syn = self.eqs.U_SD2
            self.net.add(self.Con15)
        
        if self.SYNAPSES_GPe_SNr == True :
            if self.Plasticity == False :
                self.Con21 = Synapses(self.GPe, self.SNr, model='w:volt', 
                                      pre = '''g_gaba_GPe+=1.0*nS''')
            else :
                self.Con21 = Synapses(self.GPe, self.SNr,
                                      model = self.eqs.stp_model("GPe"), 
                                      pre = self.eqs.stp_pre("GPe") )

            self.Con21.connect_random(self.GPe[0:self.ch_gpe],          self.SNr[0:self.ch_snr],          sparseness=self.pars.P_GPe_SNr)
            self.Con21.connect_random(self.GPe[self.ch_gpe:2*self.ch_gpe],   self.SNr[self.ch_snr:2*self.ch_snr],   sparseness=self.pars.P_GPe_SNr)
            self.Con21.connect_random(self.GPe[2*self.ch_gpe:3*self.ch_gpe], self.SNr[2*self.ch_snr:3*self.ch_snr], sparseness=self.pars.P_GPe_SNr)
            # Lindahl says 10.66% (32 out of 300 GPes are connected to each SNr)
            self.Con21.delay = 3*ms # Lindahl agrees from Nakanishi et al 1991
            if self.Plasticity == True :
                self.Con21.x = 1
                self.Con21.y = 1
                self.Con21.u_syn = self.eqs.U_GPe
            self.net.add(self.Con21)
        
        if self.SYNAPSES_GPe_GPe == True :
            self.Con24 = Synapses(self.GPe, self.GPe, model='w:volt', pre = '''g_gaba_GPe+=1.0*nS''')
            self.Con24.connect_random(self.GPe, self.GPe, sparseness=self.pars.P_GPe_GPe) # Achieves 34.8 Hz FR when only base input
            # Lindahl says 10% (30 out of 300 GPes are connected to each GPe)
            self.Con24.delay = 1*ms # Lindahl agrees without citation
            self.net.add(self.Con24)
        
        if self.SYNAPSES_SNr_SNr == True :
            self.Con25 = Synapses(self.SNr, self.SNr, model='w:volt', pre = '''g_gaba_SNr+=1.0*nS''')
            self.Con25.connect_random(self.SNr, self.SNr, sparseness=self.pars.P_SNr_SNr)
            self.Con25.delay = 1*ms # Lindahl does not mention SNr collaterals
            self.net.add(self.Con25)

        if self.PRINT == True :
            print "Synapses ok! (", time.time() - start_time, "sec )"
            self.print_features()





    def init_monitors(self) :
        if self.PRINT == True :
            start_time = time.time()

        # ----------------------------------------------------------------------
        #         Population rate monitors (used to save binned data)
        # ----------------------------------------------------------------------
        if self.RECORD_BINS :
            self.FR1_T = PopulationRateMonitor(self.T1, bin=1.0 * ms)
            self.FR2_T = PopulationRateMonitor(self.T2, bin=1.0 * ms)
            self.FR3_T = PopulationRateMonitor(self.T3, bin=1.0 * ms)
            self.net.add(self.FR1_T, self.FR2_T, self.FR3_T)

            if self.ACTIVATE_MSN == True :
                self.FR1_SD1 = PopulationRateMonitor(self.SD1[0:self.ch_sd1], bin=1.0 * ms)
                self.FR2_SD1 = PopulationRateMonitor(self.SD1[self.ch_sd1:2*self.ch_sd1], bin=1.0 * ms)
                self.FR3_SD1 = PopulationRateMonitor(self.SD1[2*self.ch_sd1:3*self.ch_sd1], bin=1.0 * ms)
                self.net.add(self.FR1_SD1, self.FR2_SD1, self.FR3_SD1)

                self.FR1_SD2 = PopulationRateMonitor(self.SD2[0:self.ch_sd2], bin=1.0 * ms)
                self.FR2_SD2 = PopulationRateMonitor(self.SD2[self.ch_sd2:2*self.ch_sd2], bin=1.0 * ms)
                self.FR3_SD2 = PopulationRateMonitor(self.SD2[2*self.ch_sd2:3*self.ch_sd2], bin=1.0 * ms)
                self.net.add(self.FR1_SD2, self.FR2_SD2, self.FR3_SD2)

            if self.ACTIVATE_FSI == True :
                self.FR1_FSI = PopulationRateMonitor(self.FSI[0:self.ch_fsi], bin=1.0 * ms)
                self.FR2_FSI = PopulationRateMonitor(self.FSI[self.ch_fsi:2*self.ch_fsi], bin=1.0 * ms)
                self.FR3_FSI = PopulationRateMonitor(self.FSI[2*self.ch_fsi:3*self.ch_fsi], bin=1.0 * ms)
                self.net.add(self.FR1_FSI, self.FR2_FSI, self.FR3_FSI)

            if self.ACTIVATE_STN == True :
                self.FR1_STN = PopulationRateMonitor(self.STN[0:self.ch_stn], bin=1.0 * ms)
                self.FR2_STN = PopulationRateMonitor(self.STN[self.ch_stn:2*self.ch_stn], bin=1.0 * ms)
                self.FR3_STN = PopulationRateMonitor(self.STN[2*self.ch_stn:3*self.ch_stn], bin=1.0 * ms)
                self.net.add(self.FR1_STN, self.FR2_STN, self.FR3_STN)

            if self.ACTIVATE_GPe == True :
                self.FR1_GPe = PopulationRateMonitor(self.GPe[0:self.ch_gpe], bin=1.0 * ms)
                self.FR2_GPe = PopulationRateMonitor(self.GPe[self.ch_gpe:2*self.ch_gpe], bin=1.0 * ms)
                self.FR3_GPe = PopulationRateMonitor(self.GPe[2*self.ch_gpe:3*self.ch_gpe], bin=1.0 * ms)
                self.net.add(self.FR1_GPe, self.FR2_GPe, self.FR3_GPe)

            if self.ACTIVATE_SNr == True :
                self.FR1_SNr = PopulationRateMonitor(self.SNr[0:self.ch_snr], bin=1.0 * ms)
                self.FR2_SNr = PopulationRateMonitor(self.SNr[self.ch_snr:2*self.ch_snr], bin=1.0 * ms)
                self.FR3_SNr = PopulationRateMonitor(self.SNr[2*self.ch_snr:3*self.ch_snr], bin=1.0 * ms)
                self.net.add(self.FR1_SNr, self.FR2_SNr, self.FR3_SNr)

        if self.ACTIVATE_GPe == True and self.RECORD_GPe_types:
            if not self.DETERMINISTIC_TYPES :
                print "Error: Trying to record GPe types without populating GPe deterministicly."
                exit()
            type_start = self.ch_gpe
            type_end = type_start + int(round(self.pars.neur["GPe-typeA"]["density"]["value"]*self.ch_gpe))
            self.FR2_GPe_A = PopulationRateMonitor(self.GPe[type_start:type_end], bin=1.0 * ms)
            type_start = type_end
            type_end = type_start + int(round(self.pars.neur["GPe-typeB"]["density"]["value"]*self.ch_gpe))
            self.FR2_GPe_B = PopulationRateMonitor(self.GPe[type_start:type_end], bin=1.0 * ms)
            type_start = type_end
            type_end = 2*self.ch_gpe
            self.FR2_GPe_C = PopulationRateMonitor(self.GPe[type_start:type_end], bin=1.0 * ms)
            self.net.add(self.FR2_GPe_A, self.FR2_GPe_B, self.FR2_GPe_C)


        # ----------------------------------------------------------------------
        #                           STATE MONITORS
        # ----------------------------------------------------------------------
        if self.ACTIVATE_STN == True :
            if self.SHOW_STNs == True :
                self.trace = StateMonitor(self.STN, 'v', record=True)
                self.traceI = StateMonitor(self.STN, 'I', record=True)
                self.traceIsyn = StateMonitor(self.STN, 'Isyn', record=True)
                self.traceIampa = StateMonitor(self.STN,'Iampa',record=True)
                self.traceInmda = StateMonitor(self.STN,'Inmda',record=True)
                self.traceIgaba = StateMonitor(self.STN,'Igaba',record=True)
                self.MSNtrace = StateMonitor(self.SD1, 'v', record=True)
                self.MSNtraceI = StateMonitor(self.SD1, 'I', record=True)
                self.net.add(self.trace, self.traceI, self.traceIsyn,
                             self.traceIampa, self.traceInmda, 
                             self.traceIgaba, self.MSNtrace, self.MSNtraceI)
        # ----------------------------------------------------------------------




        # ----------------------------------------------------------------------
        #         SPIKE MONITORS (used for raster plots and spike trains)
        # ----------------------------------------------------------------------
        if self.RECORD_RASTERS or True : # Because always we need to calc FR
            self.MT1 = SpikeMonitor(self.T1)
            self.MT2 = SpikeMonitor(self.T2)
            self.MT3 = SpikeMonitor(self.T3)
            self.net.add(self.MT1, self.MT2, self.MT3)

            if self.ACTIVATE_FSI == True :
                self.M01 = SpikeMonitor(self.FSI[0:self.ch_fsi])
                self.M02 = SpikeMonitor(self.FSI[self.ch_fsi:2*self.ch_fsi])
                self.M03 = SpikeMonitor(self.FSI[2*self.ch_fsi:3*self.ch_fsi])
                self.net.add(self.M01, self.M02, self.M03) 
            if self.ACTIVATE_MSN == True :
                self.M11 = SpikeMonitor(self.SD1[0:self.ch_sd1])
                self.M12 = SpikeMonitor(self.SD1[self.ch_sd1:2*self.ch_sd1])
                self.M13 = SpikeMonitor(self.SD1[2*self.ch_sd1:3*self.ch_sd1])
                self.net.add(self.M11, self.M12, self.M13)
            if self.ACTIVATE_STN == True :
                self.M21 = SpikeMonitor(self.STN[0:self.ch_stn])
                self.M22 = SpikeMonitor(self.STN[self.ch_stn:2*self.ch_stn])
                self.M23 = SpikeMonitor(self.STN[2*self.ch_stn:3*self.ch_stn])
                self.net.add(self.M21, self.M22, self.M23)
            if self.ACTIVATE_MSN == True :
                self.M31 = SpikeMonitor(self.SD2[0:self.ch_sd2])
                self.M32 = SpikeMonitor(self.SD2[self.ch_sd2:2*self.ch_sd2])
                self.M33 = SpikeMonitor(self.SD2[2*self.ch_sd2:3*self.ch_sd2])
                self.net.add(self.M31, self.M32, self.M33)
            if self.ACTIVATE_GPe == True :
                self.M41 = SpikeMonitor(self.GPe[0:self.ch_gpe])
                self.M42 = SpikeMonitor(self.GPe[self.ch_gpe:2*self.ch_gpe])
                self.M43 = SpikeMonitor(self.GPe[2*self.ch_gpe:3*self.ch_gpe])
                self.net.add(self.M41, self.M42, self.M43)
            if self.ACTIVATE_SNr == True :
                self.M51 = SpikeMonitor(self.SNr[0:self.ch_snr])
                self.M52 = SpikeMonitor(self.SNr[self.ch_snr:2*self.ch_snr])
                self.M53 = SpikeMonitor(self.SNr[2*self.ch_snr:3*self.ch_snr])
                self.net.add(self.M51, self.M52, self.M53)

        if self.PRINT :
            print "Monitors ok! (", time.time() - start_time, "sec )"


    def initialize(self, EXPERIMENT="none"):

        if EXPERIMENT == "Striatum tuning" :
            self.SYNAPSES_STRIATUM = True
    
            self.SYNAPSES_CTX_STN = False
            self.SYNAPSES_CTX_SD1 = True
            self.SYNAPSES_CTX_SD2 = True
            self.SYNAPSES_CTX_FSI = True
    
            self.SYNAPSES_SD1_SNr = False
            self.SYNAPSES_SD2_GPe = False
            self.SYNAPSES_STN_SNr = False
            self.SYNAPSES_STN_GPe = False
            self.SYNAPSES_GPe_STN = False
            self.SYNAPSES_GPe_SNr = False
            self.SYNAPSES_GPe_GPe = False
            self.SYNAPSES_SNr_SNr = False

            self.ACTIVATE_STN = False
            self.ACTIVATE_GPe = False
            self.ACTIVATE_SNr = False

        elif EXPERIMENT == "STN tuning" :
            self.SYNAPSES_STRIATUM = False

            self.SYNAPSES_CTX_STN = True
            self.SYNAPSES_CTX_SD1 = False
            self.SYNAPSES_CTX_SD2 = False
            self.SYNAPSES_CTX_FSI = False

            self.SYNAPSES_SD1_SNr = False
            self.SYNAPSES_SD2_GPe = False
            self.SYNAPSES_STN_SNr = False
            self.SYNAPSES_STN_GPe = False
            self.SYNAPSES_GPe_STN = False
            self.SYNAPSES_GPe_SNr = False
            self.SYNAPSES_GPe_GPe = False
            self.SYNAPSES_SNr_SNr = False

            self.ACTIVATE_MSN = False
            self.ACTIVATE_FSI = False
            self.ACTIVATE_STN = True
            self.ACTIVATE_GPe = False
            self.ACTIVATE_SNr = False

        elif EXPERIMENT == "STN tuning with GPe" :
            self.SYNAPSES_STRIATUM = False

            self.SYNAPSES_CTX_STN = True 
            self.SYNAPSES_CTX_SD1 = False
            self.SYNAPSES_CTX_SD2 = False
            self.SYNAPSES_CTX_FSI = False

            self.SYNAPSES_SD1_SNr = False
            self.SYNAPSES_SD2_GPe = False
            self.SYNAPSES_STN_SNr = False
            self.SYNAPSES_STN_GPe = False
            self.SYNAPSES_GPe_STN = True
            self.SYNAPSES_GPe_SNr = False
            self.SYNAPSES_GPe_GPe = False
            self.SYNAPSES_SNr_SNr = False

            self.ACTIVATE_MSN = False
            self.ACTIVATE_FSI = False
            self.ACTIVATE_STN = True 
            self.ACTIVATE_GPe = True
            self.ACTIVATE_SNr = False

        elif EXPERIMENT == "GPe tuning" :
            self.SYNAPSES_STRIATUM = False

            self.SYNAPSES_CTX_STN = False
            self.SYNAPSES_CTX_SD1 = False
            self.SYNAPSES_CTX_SD2 = False
            self.SYNAPSES_CTX_FSI = False

            self.SYNAPSES_SD1_SNr = False
            self.SYNAPSES_SD2_GPe = True
            self.SYNAPSES_STN_SNr = False
            self.SYNAPSES_STN_GPe = True
            self.SYNAPSES_GPe_STN = False
            self.SYNAPSES_GPe_SNr = False
            self.SYNAPSES_GPe_GPe = True
            self.SYNAPSES_SNr_SNr = False

            self.ACTIVATE_MSN = True
            self.ACTIVATE_FSI = False
            self.ACTIVATE_STN = True
            self.ACTIVATE_GPe = True
            self.ACTIVATE_SNr = False

        elif EXPERIMENT == "SNr tuning" :
            self.SYNAPSES_STRIATUM = False

            self.SYNAPSES_CTX_STN = False
            self.SYNAPSES_CTX_SD1 = False
            self.SYNAPSES_CTX_SD2 = False
            self.SYNAPSES_CTX_FSI = False

            self.SYNAPSES_SD1_SNr = True
            self.SYNAPSES_SD2_GPe = False
            self.SYNAPSES_STN_SNr = True
            self.SYNAPSES_STN_GPe = False
            self.SYNAPSES_GPe_STN = False
            self.SYNAPSES_GPe_SNr = True
            self.SYNAPSES_GPe_GPe = False
            self.SYNAPSES_SNr_SNr = True

            self.ACTIVATE_MSN = True
            self.ACTIVATE_FSI = False
            self.ACTIVATE_STN = True
            self.ACTIVATE_GPe = True
            self.ACTIVATE_SNr = True

        elif EXPERIMENT == "zaf" :
            self.SYNAPSES_STRIATUM = True

            self.SYNAPSES_CTX_STN = False
            self.SYNAPSES_CTX_SD1 = True
            self.SYNAPSES_CTX_SD2 = True
            self.SYNAPSES_CTX_FSI = True

            self.SYNAPSES_SD1_SNr = False
            self.SYNAPSES_SD2_GPe = True
            self.SYNAPSES_STN_SNr = False
            self.SYNAPSES_STN_GPe = False
            self.SYNAPSES_GPe_STN = False
            self.SYNAPSES_GPe_SNr = False
            self.SYNAPSES_GPe_GPe = True
            self.SYNAPSES_SNr_SNr = False

            self.ACTIVATE_MSN = True
            self.ACTIVATE_FSI = True
            self.ACTIVATE_STN = False
            self.ACTIVATE_GPe = True
            self.ACTIVATE_SNr = False

        # Probably to-delete!
        elif EXPERIMENT == "STN-GPe" :
            self.SYNAPSES_STRIATUM = True
    
            self.SYNAPSES_CTX_STN = True
            self.SYNAPSES_CTX_SD1 = True
            self.SYNAPSES_CTX_SD2 = True
            self.SYNAPSES_CTX_FSI = True
    
            self.SYNAPSES_SD1_SNr = False
            self.SYNAPSES_SD2_GPe = False
            self.SYNAPSES_STN_SNr = False
            self.SYNAPSES_STN_GPe = True
            self.SYNAPSES_GPe_STN = False
            self.SYNAPSES_GPe_SNr = False
            self.SYNAPSES_GPe_GPe = False
            self.SYNAPSES_SNr_SNr = False

            self.ACTIVATE_MSN = True
            self.ACTIVATE_FSI = True
            self.ACTIVATE_SNr = False


        self.init_neurons(experiment=EXPERIMENT)
        self.init_synapses()
        self.init_monitors()



    # Goodman: The reinit command only does things like emptying all spikes from 
    #     SpikeMonitor, and things like that - it won't change the values of any 
    #     variables. Changing the values of the variables you have to do 
    #     explicitly by e.g. G.V=... Similarly, the values for the connections 
    #     won't be changed. 
    def clear_memory(self) : # NOTE: Neuron groups should not be defined again!!
        self.net.reinit(False) # With true cleans neuron group state!
        reinit_default_clock() # Resets the clock to 0
        #return current_file
        #self.net.clear(True)
        collected = collect() # Force garbage collector to clean the memory..
        #print "BG:Garbage collector: collected %d objects." % (collected)
        clear(True) # Clears remaining data 

    def re_initialize(self) :
        self.clear_memory()
        # Re-define any randomly defined variable..
        # ... eg. neuron.C
        # ...
    
        #self.net.run(200*ms)
        #if self.PRINT == True :
        #    print "Running initial period ok!"


    def run_basic_tuning(self) :
        # If this is not the first time we run the simulation, re-init variables
        if defaultclock.t > 700*ms :
            self.re_initialize()
            
        start_time = time.time()

        # One of the following two lines resets the counters two :D
        reinit_default_clock()
        self.net.reinit(False)

        for i in range(4) :
            if self.PRINT == True :
                string = str(i) + ") "
                if self.ACTIVATE_MSN == True :
                    string += " SD1: " + str(round((self.M11.nspikes+self.M12.nspikes+self.M13.nspikes)/float(len(self.SD1)),3))
                    string += " SD2: " + str(round((self.M31.nspikes+self.M32.nspikes+self.M33.nspikes)/float(len(self.SD2)),3))
                if self.ACTIVATE_FSI == True :
                    string += " FSI: " + str(round((self.M01.nspikes+self.M02.nspikes+self.M03.nspikes)/float(len(self.FSI)),3))
                print string
            self.net.run(250 * ms)

        self.how_long = time.time() - start_time
        if self.PRINT == True :
            print "Basic tuning Done: Time passed:", self.how_long, "secs"
            print "                   Time in simulation:", defaultclock.t

        return self.record_results()


    def save_data(self, filename) :
        import cPickle as pickle
        import os.path
        
        if os.path.isfile(filename) :
            pkl_file = open(filename, 'rb')
            ALL = pickle.load(pkl_file)
            pkl_file.close()
        else :
            ALL = []

        ALL.append(self.data)

        pkl_file = open(filename, 'wb')
        pickle.dump(ALL, pkl_file)
        pkl_file.close()

    def save_rasters(self) :
        temp= dict()
        temp["T"] = [self.MT1.spikes, self.MT2.spikes, self.MT3.spikes]
        if self.ACTIVATE_FSI == True :
            temp["FSI"] = [self.M01.spikes, self.M02.spikes, self.M03.spikes]
        if self.ACTIVATE_MSN == True :
            temp["SD1"] = [self.M11.spikes, self.M12.spikes, self.M13.spikes]
        if self.ACTIVATE_STN == True :
            temp["STN"] = [self.M21.spikes, self.M22.spikes, self.M23.spikes]
        if self.ACTIVATE_MSN == True :
            temp["SD2"] = [self.M31.spikes, self.M32.spikes, self.M33.spikes]
        if self.ACTIVATE_GPe == True :
            temp["GPe"] = [self.M41.spikes, self.M42.spikes, self.M43.spikes]
        if self.ACTIVATE_SNr == True :
            temp["SNr"] = [self.M51.spikes, self.M52.spikes, self.M53.spikes]
        return temp

    def save_bins(self) :
        temp= dict()
        temp["T"] = [] # NOTE: filter should be either 'gaussian' or 'flat'
        temp["T"].append(self.FR1_T.smooth_rate(width=1*ms, filter='flat'))
        temp["T"].append(self.FR2_T.smooth_rate(width=1*ms, filter='flat'))
        temp["T"].append(self.FR3_T.smooth_rate(width=1*ms, filter='flat'))
        if self.ACTIVATE_FSI == True :
            temp["FSI"] = []
            temp["FSI"].append(self.FR1_FSI.smooth_rate(width=1*ms, filter='flat'))
            temp["FSI"].append(self.FR2_FSI.smooth_rate(width=1*ms, filter='flat'))
            temp["FSI"].append(self.FR3_FSI.smooth_rate(width=1*ms, filter='flat'))
        if self.ACTIVATE_MSN == True :
            temp["SD1"] = []
            temp["SD1"].append(self.FR1_SD1.smooth_rate(width=1*ms, filter='flat'))
            temp["SD1"].append(self.FR2_SD1.smooth_rate(width=1*ms, filter='flat'))
            temp["SD1"].append(self.FR3_SD1.smooth_rate(width=1*ms, filter='flat'))
            temp["SD2"] = []
            temp["SD2"].append(self.FR1_SD2.smooth_rate(width=1*ms, filter='flat'))
            temp["SD2"].append(self.FR2_SD2.smooth_rate(width=1*ms, filter='flat'))
            temp["SD2"].append(self.FR3_SD2.smooth_rate(width=1*ms, filter='flat'))
        if self.ACTIVATE_STN == True :
            temp["STN"] = []
            temp["STN"].append(self.FR1_STN.smooth_rate(width=1*ms, filter='flat'))
            temp["STN"].append(self.FR2_STN.smooth_rate(width=1*ms, filter='flat'))
            temp["STN"].append(self.FR3_STN.smooth_rate(width=1*ms, filter='flat'))
        if self.ACTIVATE_GPe == True :
            temp["GPe"] = []
            temp["GPe"].append(self.FR1_GPe.smooth_rate(width=1*ms, filter='flat'))
            temp["GPe"].append(self.FR2_GPe.smooth_rate(width=1*ms, filter='flat'))
            temp["GPe"].append(self.FR3_GPe.smooth_rate(width=1*ms, filter='flat'))
        if self.ACTIVATE_SNr == True :
            temp["SNr"] = []
            temp["SNr"].append(self.FR1_SNr.smooth_rate(width=1*ms, filter='flat'))
            temp["SNr"].append(self.FR2_SNr.smooth_rate(width=1*ms, filter='flat'))
            temp["SNr"].append(self.FR3_SNr.smooth_rate(width=1*ms, filter='flat'))
        return temp


    def record_results(self) :
	print "Recording results", self.RECORD_BINS

        self.data["STATS"] = dict()
        self.data["STATS"]["DOPAMINE"] = self.pars.DOPAMINE
        self.data["STATS"]["PHASE"] = self.pars.iPhase_LOW
        self.data["STATS"]["Freq1"] = self.pars.iFreq_LOW_T1
        self.data["STATS"]["Freq2"] = self.pars.iFreq_LOW_T2
        self.data["STATS"]["T1_amp"] = self.pars.T1_amp
        self.data["STATS"]["T2_amp"] = self.pars.T2_amp
        self.data["STATS"]["base"] = [self.pars.base_input_T1, self.pars.base_input_T2, self.pars.base_input_T3]
        self.data["STATS"]["weight_Bahuguna"] = self.weight_Bahuguna


        self.data["FR"] = dict()

        self.data["FR"]["CTX"] = [round(self.MT1.nspikes/(float(self.pars.Ninput)*defaultclock.t),2), \
                       round(self.MT2.nspikes/(float(self.pars.Ninput)*defaultclock.t),2), \
                       round(self.MT3.nspikes/(float(self.pars.Ninput)*defaultclock.t),2)]

        if self.ACTIVATE_FSI == True :
            self.data["FR"]["FSI"] = calc_firing_rates([self.M01.nspikes,
                                                        self.M02.nspikes,
                                                        self.M03.nspikes], 
                               neurons_per_ch=len(self.FSI)/self.pars.N, 
                               duration = defaultclock.t)

        if self.ACTIVATE_MSN == True :
            self.data["FR"]["SD1"] = calc_firing_rates([self.M11.nspikes,
                                                        self.M12.nspikes,
                                                        self.M13.nspikes], 
                               neurons_per_ch=len(self.SD1)/self.pars.N, 
                               duration = defaultclock.t)

            self.data["FR"]["SD2"] = calc_firing_rates([self.M31.nspikes,
                                                        self.M32.nspikes,
                                                        self.M33.nspikes], 
                               neurons_per_ch=len(self.SD2)/self.pars.N, 
                               duration = defaultclock.t)

        if self.ACTIVATE_STN == True :
            self.data["FR"]["STN"] = calc_firing_rates([self.M21.nspikes,
                                                        self.M22.nspikes,
                                                        self.M23.nspikes], 
                               neurons_per_ch=len(self.STN)/self.pars.N, 
                               duration = defaultclock.t)

        if self.ACTIVATE_GPe == True :
            self.data["FR"]["GPe"] = calc_firing_rates([self.M41.nspikes,
                                                        self.M42.nspikes,
                                                        self.M43.nspikes], 
                               neurons_per_ch=len(self.GPe)/self.pars.N, 
                               duration = defaultclock.t)

        if self.ACTIVATE_SNr == True :
            self.data["FR"]["SNr"] = calc_firing_rates([self.M51.nspikes,
                                                        self.M52.nspikes,
                                                        self.M53.nspikes], 
                               neurons_per_ch=len(self.SNr)/self.pars.N, 
                               duration = defaultclock.t)

        self.data["STATS"]["t"] = self.how_long

        if self.RECORD_BINS :
            print "Recoding bins.."
            self.data["BINS"] = self.save_bins()

        if self.RECORD_RASTERS :
            self.data["RASTERS"] = self.save_rasters()

        if self.RECORD_GPe_types :  # filter should be either 'gaussian' or 'flat'
            self.data["GPe_fr_types"] = []
            self.data["GPe_fr_types"].append(self.FR2_GPe_A.smooth_rate(width=1*ms, filter='flat'))
            self.data["GPe_fr_types"].append(self.FR2_GPe_B.smooth_rate(width=1*ms, filter='flat'))
            self.data["GPe_fr_types"].append(self.FR2_GPe_C.smooth_rate(width=1*ms, filter='flat'))
        return self.data



    # ------------- EXPERIMENTS -----------------------------------------------
    def run_experiment(self, DURATION = 3500) :

        start_time = time.time()
        reinit_default_clock()
        self.net.reinit(False)

        print "Starting: - duration:", DURATION
        self.net.run(DURATION * ms)
        
        self.how_long = time.time() - start_time
        if self.PRINT == True :
            print "Experiment Done: Time passed:", self.how_long, "secs"
            print "                 Time in simulation:", defaultclock.t
            print "                 Global time:",time.time()-self.global_time

        return self.record_results()
    # -------------------------------------------------------------------------



    def plot_results(self, SHOW=False) :

        import matplotlib.gridspec as gridspec
        f = figure()
        #gs = gridspec.GridSpec(5, 1,height_ratios=[6,2,1,1,1])
        gs = gridspec.GridSpec(10, 1,height_ratios=[1,1,1,1,1,1,2,1,1,1])
    
        # Subplot 1, Raster plots
        #ax1 = plt.subplot(gs[0])
        #xlim(0, defaultclock.t/ms)
        if self.ACTIVATE_FSI == True :
            ax1 = plt.subplot(gs[0])
            raster_plot(self.M01, self.M02, self.M03, ylabel='FSI')
            xlim(0, defaultclock.t/ms)
            ylim(0, 3)
        if self.ACTIVATE_MSN == True :
            ax1 = plt.subplot(gs[1])
            raster_plot(self.M11,self.M12,self.M13, ylabel='SD1', showgrouplines=1)
            xlim(0, defaultclock.t/ms)
            ylim(0, 3)
        if self.ACTIVATE_STN == True :
            ax1 = plt.subplot(gs[2])
            raster_plot(self.M21, self.M22, self.M23, ylabel='STN')
            xlim(0, defaultclock.t/ms)
            ylim(0, 3)
        if self.ACTIVATE_MSN == True :
            ax1 = plt.subplot(gs[3])
            raster_plot(self.M31,self.M32,self.M33, ylabel='SD2', showgrouplines=1)
            xlim(0, defaultclock.t/ms)
            ylim(0, 3)
        if self.ACTIVATE_GPe == True :
            ax1 = plt.subplot(gs[4])
            raster_plot(self.M41, self.M42, self.M43, ylabel='GPe')
            xlim(0, defaultclock.t/ms)
            ylim(0, 3)
        if self.ACTIVATE_SNr == True :
            ax1 = plt.subplot(gs[5])
            raster_plot(self.M51, self.M52, self.M53, ylabel='SNr')
            xlim(0, defaultclock.t/ms)
            ylim(0, 3)
    
        # Subplot 2, Firing rates
        if self.ACTIVATE_SNr == True :
            ax2 = plt.subplot(gs[6])
            #plot(self.FR1_SNr.smooth_rate(width=self.pars.fr_depth,filter='gaussian')) # gaussian or flat
            #plot(self.FR2_SNr.smooth_rate(width=self.pars.fr_depth,filter='gaussian'))
            #plot(self.FR3_SNr.smooth_rate(width=self.pars.fr_depth,filter='gaussian'))
            xlim(0, defaultclock.t/ms)
            ylabel('SNr FR')
    
    
        # Subplot 3, Input raster plots
        ax1 = plt.subplot(gs[7])
        raster_plot(self.MT1, self.MT2, self.MT3, ylabel='T1/2/3',showgrouplines=1)
        xlim(0, defaultclock.t/ms)
    
        # Subplot 4, Input rates
        plt.subplot(gs[8])
        if 1 :
            #plot(self.FR1_T.smooth_rate(width=self.pars.fr_depth,filter='gaussian'))
            #plot(self.FR2_T.smooth_rate(width=self.pars.fr_depth,filter='gaussian'))
            #plot(self.FR3_T.smooth_rate(width=self.pars.fr_depth,filter='gaussian'))
            xlim(0, defaultclock.t/ms)
            ylabel('T1/2/3 FR')
        else :
            print ''
    
        # Subplot 5, Cortical oscillation pattern
        plt.subplot(gs[9])
        xx = np.arange(0.0,2000.0, 0.25)
        yytemp = []
        for t in xx :
            yytemp.append(float(T1rates(t*ms, self.pars.base_input_T1,
                                self.pars.iFreq_LOW_T1, self.pars.iFreq_HIGH_T1, 
                                T1_amp = self.pars.T1_amp) / Hz))
        yy1 = np.array(yytemp)
        yytemp = []
        for t in xx :
            yytemp.append(float(T2rates(t*ms, self.pars.base_input_T2,
                         self.pars.iFreq_LOW_T2, self.pars.iFreq_HIGH_T2, 
                         self.pars.iPhase_LOW, T2_amp = self.pars.T2_amp) / Hz))
        yy2 = np.array(yytemp)
        yytemp = []
        for t in xx :
            yytemp.append(float(self.pars.base_input_T3 / Hz))
        yy3 = np.array(yytemp)
        plot(xx, yy1)
        plot(xx, yy2)
        plot(xx, yy3)
        ylim(0, float((self.pars.base_input_T2 + self.pars.T2_amp)/Hz) + 2)
        xlim(0, defaultclock.t/ms)
    
        #if self.ACTIVATE_SNr == True :
        #plot(FR1_SNr.times_/ms, FR1_SNr.rate)
        #plot(FR2_SNr.times_/ms, FR2_SNr.rate)
        #plot(FR3_SNr.times_/ms, FR3_SNr.rate)
    
        f.suptitle(str('Dopamine: ' + str(self.pars.DOPAMINE) + \
                   ' Score: ' + str("%.2g" % self.final_score)))
    
        if self.FOLDER != '' and self.SAVEPLOTS > 0 :
            if not path.exists(self.FOLDER):
                mkdir(self.FOLDER)
            foldername = self.FOLDER + "/images/"
            if not path.exists(foldername):
                mkdir(foldername)
            filename = 'd' + str(self.pars.DOPAMINE) + 'fLOW' + \
                      str(self.pars.iFreq_LOW_T1)+ 'fHIGH' + \
                      str(self.pars.iFreq_HIGH_T1)+'p'+str(self.pars.iPhase_LOW)
            savefig(foldername+filename+'.png', bbox_inches=0)
            #savefig(foldername+filename+'.pdf', bbox_inches=0)
            print 'Plots saved.'
    
        # ---------------------------------------
        
        if self.SHOW_STNs == True :
            self.show_stns()

        if SHOW : show()
    




    def plot_MSN(self) :
        if self.ACTIVATE_MSN == True :
            sd1_fr = []
            for i in range(len(self.SD1)/3) :
                sd1_fr.append(len(self.M11[i])/defaultclock.t/second)
            for i in range(len(self.SD1)/3) :
                sd1_fr.append(len(self.M12[i])/defaultclock.t/second)
            for i in range(len(self.SD1)/3) :
                sd1_fr.append(len(self.M13[i])/defaultclock.t/second)
            sd2_fr = []
            for i in range(len(self.SD2)/3) :
                sd2_fr.append(len(self.M31[i])/defaultclock.t/second)
            for i in range(len(self.SD2)/3) :
                sd2_fr.append(len(self.M32[i])/defaultclock.t/second)
            for i in range(len(self.SD2)/3) :
                sd2_fr.append(len(self.M33[i])/defaultclock.t/second)
            figure()
            subplot(211)
            plot(range(len(sd1_fr)), sd1_fr, 'bo')
            plot(range(len(sd2_fr)), sd2_fr, 'ro')
            subplot(211)
            # ...

    def plot_GPe(self) :
        if self.ACTIVATE_GPe == True :
            fr = []
            for i in range(len(self.GPe)/3) :
                fr.append(len(self.M41[i])/defaultclock.t/second)
            for i in range(len(self.GPe)/3) :
                fr.append(len(self.M42[i])/defaultclock.t/second)
            for i in range(len(self.GPe)/3) :
                fr.append(len(self.M43[i])/defaultclock.t/second)
            figure()
            subplot(211)
            plot(range(len(fr)), fr, 'bo')
            subplot(211)
            # ...
            savefig("GPe.png")
            

    def plot_SNr(self) :
        if self.ACTIVATE_SNr == True :
            snr_fr = []
            for i in range(len(self.SNr)/3) :
                snr_fr.append(len(self.M51[i])/defaultclock.t/second)
            for i in range(len(self.SNr)/3) :
                snr_fr.append(len(self.M52[i])/defaultclock.t/second)
            for i in range(len(self.SNr)/3) :
                snr_fr.append(len(self.M53[i])/defaultclock.t/second)
            figure()
            subplot(211)
            plot(range(len(snr_fr)), snr_fr, 'bo')
            subplot(211)
            # ...




    def plot_GPe_results(self, SHOW = False) :

        import matplotlib.gridspec as gridspec
        f = figure()
        gs = gridspec.GridSpec(2, 1,height_ratios=[2,1])
    
        plt.subplot(gs[0])
        raster_plot(self.M41, self.M42, self.M43, ylabel='GPe')
        xlim(0, defaultclock.t/ms)

        plt.subplot(gs[1])
        gpe_fr = []
        for i in range(len(self.GPe)/3) :
            gpe_fr.append(len(self.M41[i])/float(defaultclock.t)/second)
        for i in range(len(self.GPe)/3) :
            gpe_fr.append(len(self.M42[i])/float(defaultclock.t)/second)
        for i in range(len(self.GPe)/3) :
            gpe_fr.append(len(self.M43[i])/float(defaultclock.t)/second)

        plot(range(len(gpe_fr)), gpe_fr, 'bo')
        savefig("GPe_neurons.png")
        if SHOW : show()

    def print_GPe_results(self) :
        gpe_fr = []
        for i in range(len(self.GPe)/3) :
            gpe_fr.append(len(self.M41[i])/float(defaultclock.t)/second)
        for i in range(len(self.GPe)/3) :
            gpe_fr.append(len(self.M42[i])/float(defaultclock.t)/second)
        for i in range(len(self.GPe)/3) :
            gpe_fr.append(len(self.M43[i])/float(defaultclock.t)/second)

        #print "GPe types --> firing rates:" #print array(gpe_fr)/Hz
        #for i in range(len(self.choices_gpe)/3) :
        #    print i, ")", self.choices_gpe[i], "-->", gpe_fr[i]
        tA = 0.0
        tB = 0.0
        tC = 0.0
        cA = 0
        cB = 0
        cC = 0
        for i in range(len(self.choices_gpe)) :
            if(self.choices_gpe[i] == "typeA") :
                tA += float(gpe_fr[i]/Hz)
                cA += 1
            elif(self.choices_gpe[i] == "typeB") :
                tB += float(gpe_fr[i]/Hz)
                cB += 1
            elif(self.choices_gpe[i] == "typeC") :
                tC += float(gpe_fr[i]/Hz)
                cC += 1
        print "GPe firing rates: TypeA:", tA/cA
        print "                  TypeB:", tB/cB
        print "                  TypeC:", tC/cC



    def show_stns(self) :
        if self.ACTIVATE_STN == False :
            return
        figure()
        subplot(311)
        plot(self.trace.times/ms, self.trace[0]/mV)
        plot(self.trace.times/ms, self.trace[1]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(312)
        plot(self.traceI.times/ms, self.traceI[0]/pA)
        plot(self.traceI.times/ms, self.traceI[1]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(313)
        raster_plot(self.M21, self.M22, self.M23, ylabel='STN')
        xlim(0, defaultclock.t/ms)
        ylim(-1,self.pars.Nstn)
    
        figure()
        for i in range(len(self.STN)) :    
            subplot(9,5,1+i)
            plot(self.trace.times/ms, self.trace[i]/mV)
            ylabel("neur"+str(i))
            xlim(0, defaultclock.t/ms)

        figure()
        subplot(921)
        plot(self.trace.times/ms, self.trace[0]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(922)
        plot(self.trace.times/ms, self.trace[1]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(923)
        plot(self.trace.times/ms, self.trace[2]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(924)
        plot(self.trace.times/ms, self.trace[3]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(925)
        plot(self.trace.times/ms, self.trace[4]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(926)
        plot(self.trace.times/ms, self.trace[5]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(927)
        plot(self.trace.times/ms, self.trace[6]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(928)
        plot(self.trace.times/ms, self.trace[7]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(929)
        plot(self.trace.times/ms, self.trace[8]/mV)
        xlim(0, defaultclock.t/ms)
    
        subplot(9,2,10)
        plot(self.traceI.times/ms, self.traceI[0]/pA)
        plot(self.traceI.times/ms, self.traceIampa[0]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[0]/pA)
        plot(self.traceI.times/ms, self.traceInmda[0]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,11)
        plot(self.traceI.times/ms, self.traceI[1]/pA)
        plot(self.traceI.times/ms, self.traceIampa[1]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[1]/pA)
        plot(self.traceI.times/ms, self.traceInmda[1]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,12)
        plot(self.traceI.times/ms, self.traceI[2]/pA)
        plot(self.traceI.times/ms, self.traceIampa[2]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[2]/pA)
        plot(self.traceI.times/ms, self.traceInmda[2]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,13)
        plot(self.traceI.times/ms, self.traceI[3]/pA)
        plot(self.traceI.times/ms, self.traceIampa[3]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[3]/pA)
        plot(self.traceI.times/ms, self.traceInmda[3]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,14)
        plot(self.traceI.times/ms, self.traceI[4]/pA)
        plot(self.traceI.times/ms, self.traceIampa[4]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[4]/pA)
        plot(self.traceI.times/ms, self.traceInmda[4]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,15)
        plot(self.traceI.times/ms, self.traceI[5]/pA)
        plot(self.traceI.times/ms, self.traceIampa[5]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[5]/pA)
        plot(self.traceI.times/ms, self.traceInmda[5]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,16)
        plot(self.traceI.times/ms, self.traceI[6]/pA)
        plot(self.traceI.times/ms, self.traceIampa[6]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[6]/pA)
        plot(self.traceI.times/ms, self.traceInmda[6]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,17)
        plot(self.traceI.times/ms, self.traceI[7]/pA)
        plot(self.traceI.times/ms, self.traceIampa[7]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[7]/pA)
        plot(self.traceI.times/ms, self.traceInmda[7]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(9,2,18)
        plot(self.traceI.times/ms, self.traceI[8]/pA)
        plot(self.traceI.times/ms, self.traceIampa[8]/pA)
        plot(self.traceI.times/ms, self.traceIsyn[8]/pA)
        plot(self.traceI.times/ms, self.traceInmda[8]/pA)
        xlim(0, defaultclock.t/ms)
    
        figure()
        subplot(511)
        plot(self.trace.times/ms, self.trace[self.MY_NEURON]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(512)
        plot(self.traceI.times/ms, self.traceIgaba[self.MY_NEURON]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(513)
        plot(self.traceI.times/ms, self.traceInmda[self.MY_NEURON]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(514)
        plot(self.traceI.times/ms, self.traceIampa[self.MY_NEURON]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(515)
        plot(self.traceI.times/ms, self.traceIsyn[self.MY_NEURON]/mV)
        xlim(0, defaultclock.t/ms)
    
        for i in range(len(self.STN)/3) :
            print i, ")", len(self.M21[i])/defaultclock.t/second
        for i in range(len(self.STN)/3) :
            print i, ")", len(self.M22[i])/defaultclock.t/second
        for i in range(len(self.STN)/3) :
            print i, ")", len(self.M23[i])/defaultclock.t/second
    
        figure()
        subplot(311)
        plot(self.MSNtrace.times/ms, self.MSNtrace[0]/mV)
        plot(self.MSNtrace.times/ms, self.MSNtrace[1]/mV)
        xlim(0, defaultclock.t/ms)
        subplot(312)
        plot(self.MSNtraceI.times/ms, self.traceI[0]/pA)
        plot(self.MSNtraceI.times/ms, self.traceI[1]/pA)
        xlim(0, defaultclock.t/ms)
        subplot(313)
        raster_plot(self.M21, self.M22, self.M23, ylabel='STN')
        xlim(0, defaultclock.t/ms)
        ylim(-1,self.pars.Nstn)



    def print_results(self) :
        print ""
        print "Basic tuning Done: Average FRs:  T1: ", self.data["FR"]["CTX"][0], \
              "  T2: ", self.data["FR"]["CTX"][1], "  T3: ", self.data["FR"]["CTX"][2]
        if self.ACTIVATE_FSI == True :
            print "                                FSI: ", self.data["FR"]["FSI"][0], \
                  "\t- channels:", self.data["FR"]["FSI"][1], self.data["FR"]["FSI"][2], \
                  self.data["FR"]["FSI"][3]
        if self.ACTIVATE_MSN == True :
            print "                                SD1: ", self.data["FR"]["SD1"][0], \
                  "\t- channels:", self.data["FR"]["SD1"][1], self.data["FR"]["SD1"][2], \
                  self.data["FR"]["SD1"][3]
            print "                                SD2: ", self.data["FR"]["SD2"][0], \
                  "\t- channels:", self.data["FR"]["SD2"][1], self.data["FR"]["SD2"][2], \
                  self.data["FR"]["SD2"][3]
        if self.ACTIVATE_STN == True :
            print "                                STN: ", self.data["FR"]["STN"][0], \
                  "\t- channels:", self.data["FR"]["STN"][1], self.data["FR"]["STN"][2], \
                  self.data["FR"]["STN"][3]
        if self.ACTIVATE_GPe == True :
            print "                                GPe: ", self.data["FR"]["GPe"][0], \
                  "\t- channels:", self.data["FR"]["GPe"][1], self.data["FR"]["GPe"][2], \
                  self.data["FR"]["GPe"][3]
        if self.ACTIVATE_SNr == True :
            print "                                SNr: ", self.data["FR"]["SNr"][0], \
                  "\t- channels:", self.data["FR"]["SNr"][1], self.data["FR"]["SNr"][2], \
                  self.data["FR"]["SNr"][3]




















