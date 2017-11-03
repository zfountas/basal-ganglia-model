from brian import *

__author__ = "Zafeirios Fountas"
__credits__ = ["Murray Shanahan", "Mark Humphries",  "Rob Leech", "Jeanette Hellgren Kotaleski"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Zafeirios Fountas"
__email__ = "fountas@outlook.com"
__status__ = "Published"

class NeuronEquations(object) :
    def __init__(self) :

        # MSN: 12.5*mV produces 1-3Hz with 3Hz input and ~30Hz when T1=10Hz  
        #      20*mV produces MSNs that fire at ~1-3Hz without any cortical input
        # FSI: All this time was sigma = 0.0*mV
        # STN: 1.5 - My tuning and GAs
        # GPe: 7.0*Mv, 4.0*Mv, 1.5*mV
        # SNr: 0.3*mV

        """ BASIC TEMPLATE MODEL (Izhikevich 2007)
        neuron_model = '''
        dv/dt = (k*1*pF/ms/mV*(v-vr)*(v-vt)-u*pF+I)/C + sigma*xi/ms**.5 : volt
        du/dt = a*(b*(v-vr)-u) : volt/second
        a       : 1/second
        b       : 1/second
        c       : volt
        d       : volt/second
        k       : 1
        vr      : volt
        vt      : volt
        C       : pF
        vpeak   : volt
        I = Isyn + Ispon + Istim : amp
        Istim   : amp
        Ispon   : amp
        Isyn = Igaba + Iampa + Inmda : amp
        '''
        """

        # Neuron type       value         BG value     single-sim value/source
        # ----------------------------------------------------------------------
        sigma_msn      =   14.0*mV    #    14.0     #  Fountas 2017 tuning (~1.2-~30Hz)
        sigma_fsi      =    4.6*mV    #     3.6     #  Fountas 2017 tuning (12.5-70Hz)
        sigma_stn      =    0.5*mV    #     0.5     #  1.5 / my tun.(20-40-10Hz)
        sigma_gpe      =    3.0*mV    #     3.0     #  0.0 in GPeAnalysis
        sigma_snr      =    5.0*mV    #     5.0     #  Optimized in Fountas 2017


        # -- GENERAL NEURON EQUATIONS ------------------------------------------
        # nmda = R/(1.0+R)
        # ampa = 1.0/(1.0+R)
        # Isyn = Igaba + Iampa + Inmda : amp

        self.izhi_reset = '''
        v = c
        u += d
        '''

        # -- MSN Neurons -------------------------------------------------------

        KAPA = 0.0289   # Humphries etal 2009a
        #LAMDA = 0.331  # Humphries etal 2009a (Commented because this value is used directly)
        ALPHA = 0.032   # Humphries etal 2009a
        HTA = 0.1       # Humphries 2014
        EPSILON = 0.625 # Humphries 2014
        BITA1 = 0.5     # Humphries 2014
        BITA2 = 0.3     # Humphries 2014
        
        neuron_model_MSN = '''
        dv/dt = (K*1*pF/ms/mV*(v-VR)*(v-vt)-u*pF+I)/C + sigma_msn*xi/ms**.5 : volt
        du/dt = a*(b*(v-VR)-u) : volt/second
        VR = vr*(1+KAPA*Dop1) : volt
        K = k*(1-ALPHA*Dop2) : 1
        a       : 1/second
        b       : 1/second
        c       : volt
        d       : volt/second
        k       : 1
        vr      : volt
        vt      : volt
        C       : pF
        vpeak   : volt
        I = Ispon + Istim + Isyn : amp
        Istim   : amp
        Ispon   : amp
        Isyn = Igaba_MSN + Igaba_FSI + Iampa*(1.0 - BITA2*Dop2) + Inmda*(1.0 + BITA1*Dop1): amp
        Dop1      : 1
        Dop2      : 1
        '''

        synaptic_model_MSN='''
        B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

        Iampa     = G_ampa*g_ampa*(E_ampa-v): amp
        Inmda     = B*G_nmda*g_nmda*(E_nmda-v) : amp
        Igaba_MSN = G_gaba_MSN*g_gaba_MSN*(E_gaba-v) : amp
        Igaba_FSI = G_gaba_FSI*g_gaba_FSI*(E_gaba-v) : amp

        dg_ampa/dt = -g_ampa/tau_ampa : siemens
        dg_nmda/dt = -g_nmda/tau_nmda : siemens
        dg_gaba_MSN/dt = -g_gaba_MSN/tau_gaba : siemens
        dg_gaba_FSI/dt = -g_gaba_FSI/tau_gaba : siemens

        tau_ampa   : ms
        tau_nmda   : ms
        tau_gaba   : ms
        E_ampa     : volt
        E_nmda     : volt
        E_gaba     : volt
        G_ampa     : 1
        G_nmda     : 1
        G_gaba_MSN : 1
        G_gaba_FSI : 1
        '''

        self.izhi_eqs_MSN = Equations(neuron_model_MSN)
        self.izhi_eqs_MSN += Equations(synaptic_model_MSN)
        self.izhi_reset_MSN = '''
        v = c
        u += d*(1-0.331*Dop1)
        '''

        # -- FSI Neurons -------------------------------------------------------
        neuron_model_FSI = '''
        dv/dt = (k*1*pF/ms/mV*(v-VR)*(v-vt)-u*pF+I)/C + sigma_fsi*xi/ms**.5 : volt
        du/dt = a*(b*(v-VR)-u) : volt/second
        VR = vr*(1+HTA*Dop1) : volt
        a        : 1/second
        b        : 1/second
        c        : volt
        d        : volt/second
        k        : 1
        vr       : volt
        vt       : volt
        C        : pF
        vpeak    : volt
        I = Ispon + Istim + Isyn + Igap : amp
        Igap     : amp # gap junction current
        Istim    : amp
        Ispon    : amp
        Isyn = Igaba * (1.0 - EPSILON*Dop2) + Iampa : amp
        Dop1       : 1
        Dop2       : 1
        '''

        # SOS: No nmda from the cortex (Humphries 2014)
        synaptic_model_FSI='''
        B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

        Iampa =   G_ampa*g_ampa*(E_ampa-v) : amp
        Igaba =   G_gaba*g_gaba*(E_gaba-v) : amp

        dg_ampa/dt = -g_ampa/tau_ampa : siemens
        dg_gaba/dt = -g_gaba/tau_gaba : siemens

        tau_ampa : ms
        tau_gaba : ms
        E_ampa   : volt
        E_gaba   : volt
        G_ampa   : 1
        G_gaba   : 1
        '''
        
        self.izhi_eqs_FSI = Equations(neuron_model_FSI)
        self.izhi_eqs_FSI += Equations(synaptic_model_FSI)
        self.izhi_reset_FSI = '''
        v = c
        u += d
        '''

        # -- Gap junctions ----------------------------------------------------
        #dv/dt=(Vgap1 + Vgap2 - 2*v)/tau_gap : 1
        self.eqs_gap = '''
        dv/dt=(Vgap1 + Vgap2)/tau_gap : 1
        tau_gap : ms
        Vgap1 : 1
        Vgap2 : 1
        '''

        # -- STN Neurons -------------------------------------------------------
        from helper_functions import heaviside01, IMP

        # heaviside01 has the same effect with b_special
        # for typeC we just need to set b_thres to be very big (> than vpeak)
        neuron_model_STN = Equations("""
        dv/dt = (k*(v-vr)*(v-vt)*nS/mV - u1*pF - w2*u2*pF + I)/C + sigma_stn*xi/ms**.5 : volt
        du1/dt = a1*( b1*(v-vr) - u1 ) : volt/second
        du2/dt = a2*( heaviside01(b_thres-v)*b2*(v-vr2) - u2 ) : volt/second
        w1      : 1
        w2      : 1
        a1      : 1/ms   
        a2      : 1/ms   
        b1      : 1/ms   
        b2      : 1/ms   
        c       : mV
        d1      : mV/ms
        d2      : mV/ms
        k       : 1
        vr      : mV
        vr2     : mV
        b_thres : mV
        vt      : mV
        C       : pF
        vpeak   : volt
        I = Ispon + Istim + Isyn : amp
        Istim   : pA
        Ispon   : pA
        Isyn = Igaba*(1.0 - 0.5*Dop2) + (Iampa + Inmda)*(1.0 - 0.5*Dop2) : amp 
        Dop1    : 1
        Dop2    : 1
        """)

        synaptic_model_STN='''
        B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

        Iampa =   G_ampa_CTX*g_ampa_CTX*(E_ampa-v) : amp
        Inmda = B*G_nmda_CTX*g_nmda_CTX*(E_nmda-v) : amp
        Igaba =   G_gaba_GPe*g_gaba_GPe*(E_gaba-v) : amp

        dg_ampa_CTX/dt = -g_ampa_CTX/tau_ampa_CTX : siemens
        dg_nmda_CTX/dt = -g_nmda_CTX/tau_nmda_CTX : siemens
        dg_gaba_GPe/dt = -g_gaba_GPe/tau_gaba_GPe : siemens

        tau_ampa_CTX : ms
        tau_nmda_CTX : ms
        tau_gaba_GPe : ms

        E_ampa   : volt
        E_nmda   : volt
        E_gaba   : volt

        G_ampa_CTX   : 1
        G_nmda_CTX   : 1
        G_gaba_GPe   : 1
        '''

        self.threshold_stn = '''v >= (vpeak + IMP(u2, w1) * u2 * ms)'''

        self.izhi_eqs_stn = neuron_model_STN
        self.izhi_eqs_stn += Equations(synaptic_model_STN)


        # -- GPe Neurons -------------------------------------------------------
        neuron_model_GPe = '''
        dv/dt = (k*1*pF/ms/mV*(v-vr)*(v-vt)-u*pF+I)/C + sigma_gpe*xi/ms**.5 : volt
        du/dt = a*(b*(v-vr)-u) : volt/second
        a       : 1/second
        b       : 1/second
        c       : volt
        d       : volt/second
        k       : 1
        vr      : volt
        vt      : volt
        C       : pF
        vpeak   : volt
        I = Ispon + Istim + Isyn : amp
        Istim   : amp
        Ispon   : amp
        Isyn = Igaba*(1.0 - 0.5*Dop2) + (Iampa + Inmda)*(1.0 - 0.5*Dop2) : amp
        Dop1    : 1
        Dop2    : 1
        '''

        synaptic_model_GPe='''
        B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

        Iampa =   G_ampa_STN*g_ampa_STN*(E_ampa-v) : amp
        Inmda = B*G_nmda_STN*g_nmda_STN*(E_nmda-v) : amp
        Igaba =  (G_gaba_MSN*g_gaba_MSN + G_gaba_GPe*g_gaba_GPe)*(E_gaba-v) : amp

        dg_ampa_STN/dt = -g_ampa_STN/tau_ampa_STN : siemens
        dg_nmda_STN/dt = -g_nmda_STN/tau_nmda_STN : siemens

        dg_gaba_MSN/dt = -g_gaba_MSN/tau_gaba_MSN : siemens
        dg_gaba_GPe/dt = -g_gaba_GPe/tau_gaba_GPe : siemens

        tau_ampa_STN : ms
        tau_nmda_STN : ms
        tau_gaba_MSN : ms
        tau_gaba_GPe : ms

        E_ampa       : volt
        E_nmda       : volt
        E_gaba       : volt

        G_ampa_STN   : 1
        G_nmda_STN   : 1
        G_gaba_MSN   : 1
        G_gaba_GPe   : 1
        '''        
        self.izhi_eqs_gpe = Equations(neuron_model_GPe)
        self.izhi_eqs_gpe += Equations(synaptic_model_GPe)


        # -- SNr Neurons -------------------------------------------------------
        neuron_model_SNr = '''
        dv/dt = (k*1*pF/ms/mV*(v-vr)*(v-vt)-u*pF+I)/C + sigma_snr*xi/ms**.5 : volt
        du/dt = a*(b*(v-vr)-u) : volt/second
        a       : 1/second
        b       : 1/second
        c       : volt
        d       : volt/second
        k       : 1
        vr      : volt
        vt      : volt
        C       : pF
        vpeak   : volt
        I = Ispon + Istim + Isyn : amp
        Istim   : amp
        Ispon   : amp
        Isyn = Igaba + Iampa + Inmda : amp
        '''
        synaptic_model_SNr='''
        B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

        Iampa =   G_ampa_STN*g_ampa_STN*(E_ampa-v) : amp
        Inmda = B*G_nmda_STN*g_nmda_STN*(E_nmda-v) : amp
        Igaba =   (G_gaba_MSN*g_gaba_MSN + G_gaba_GPe*g_gaba_GPe + \
                                        G_gaba_SNr*g_gaba_SNr)*(E_gaba-v) : amp

        dg_ampa_STN/dt = -g_ampa_STN/tau_ampa_STN : siemens
        dg_nmda_STN/dt = -g_nmda_STN/tau_nmda_STN : siemens
        dg_gaba_MSN/dt = -g_gaba_MSN/tau_gaba_MSN : siemens
        dg_gaba_GPe/dt = -g_gaba_GPe/tau_gaba_GPe : siemens
        dg_gaba_SNr/dt = -g_gaba_SNr/tau_gaba_SNr : siemens
        tau_ampa_STN : ms
        tau_nmda_STN : ms
        tau_gaba_MSN : ms
        tau_gaba_GPe : ms
        tau_gaba_SNr : ms
        E_ampa       : volt
        E_nmda       : volt
        E_gaba       : volt
        G_ampa_STN   : 1
        G_nmda_STN   : 1
        G_gaba_MSN   : 1
        G_gaba_GPe   : 1
        G_gaba_SNr   : 1
        '''        
        self.izhi_eqs_snr = Equations(neuron_model_SNr)
        self.izhi_eqs_snr+= Equations(synaptic_model_SNr)


    taud=0.0*ms
    tauf=0.0*ms
    U=0.0 


    # -- PLASTICITY -----------------------------------------------------------
    taud_SD1=623*ms
    tauf_SD1=559*ms
    U_SD1=0.0192 

    taud_STN=800.0*ms
    #tauf_STN=0.0*ms # NOTE: It's not working with zero because of the devision!
    U_STN=0.35 # The equilibrioum value

    taud_GPe=969.0*ms
    tauf_GPe=0.0*ms
    U_GPe=0.196

    taud_SD2=11.0*ms
    tauf_SD2=73.0*ms
    U_SD2=0.24

    def stp_model(self, nucleus) :

        if nucleus == "SD1" :
            # print "Starting with complete (simple) model of short-term plasticity."
            model = '''dx/dt=(1-x)/self.eqs.taud_SD1 : 1 #(event-driven)
                       du_syn/dt=(self.eqs.U_SD1-u_syn)/self.eqs.tauf_SD1 : 1 #(event-driven)
                       '''
        elif nucleus == "SD2" :
            # print "Starting with complete (simple) model of short-term plasticity."
            model = '''dx/dt=(1-x)/self.eqs.taud_SD2 : 1 #(event-driven)
                       du_syn/dt=(self.eqs.U_SD2-u_syn)/self.eqs.tauf_SD2 : 1 #(event-driven)
                       '''
        elif nucleus == "GPe":
            # print "Starting without facilitation"
            model = '''dx/dt=(1-x)/self.eqs.taud_GPe : 1 #(event-driven)
                       '''
        elif nucleus == "STN" :
            # print "Starting without facilitation"
            model = '''dx/dt=(1-x)/self.eqs.taud_STN : 1 #(event-driven)
                       '''
        return model


    def stp_pre(self, nucleus) :

        # print "Starting without facilitation"
        EXC_PRE_STN = '''g_ampa_STN+=x*nS
                         g_nmda_STN+=x*nS
                         x*=(1-self.eqs.U_STN)
                         '''
        INH_PRE_GPe = '''g_gaba_GPe+=x*nS
                         x*=(1-self.eqs.U_GPe)
                         '''

        # print "Starting with complete (simple) model of short-term plasticity."
        INH_PRE_SD1 = '''g_gaba_MSN+=u_syn*x*nS
                         x*=(1-u_syn)
                         u_syn+=self.eqs.U_SD1*(1-u_syn)
                         '''
        INH_PRE_SD2 = '''g_gaba_MSN+=u_syn*x*nS
                         x*=(1-u_syn)
                         u_syn+=self.eqs.U_SD2*(1-u_syn)
                         '''

        # Inhibitory synapses
        if nucleus == "SD1" :
            return INH_PRE_SD1
        elif nucleus == "SD2" :
            return INH_PRE_SD2
        elif nucleus == "GPe" :
            return INH_PRE_GPe
        # Excitatory synapse
        elif nucleus == "STN" :
            return EXC_PRE_STN







