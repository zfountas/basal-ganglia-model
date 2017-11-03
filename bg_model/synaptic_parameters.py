from brian import mV, nS, ms

__author__ = "Zafeirios Fountas"
__credits__ = ["Murray Shanahan", "Mark Humphries",  "Rob Leech", "Jeanette Hellgren Kotaleski"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Zafeirios Fountas"
__email__ = "fountas@outlook.com"
__status__ = "Published"

data = dict()
data["MSN"] = dict()
data["MSN"]["tau"] = {
    "AMPA" :   { "value" : 6 * ms,    "source" : "Moyer etal 2007, Humphries 2014", "unit" : "ms"},
    "NMDA" :   { "value" : 160 * ms,  "source" : "Moyer etal 2007, Humphries 2014", "unit" : "ms"},
    "GABA" :   { "value" : 4 * ms,    "source" : "Moyer etal 2007, Humphries 2014", "unit" : "ms"}
}
data["MSN"]["E"] = {
    "AMPA" :   { "value" : 0 * mV,    "source" : "Moyer etal 2007, Humphries 2014", "unit" : "mV"},
    "NMDA" :   { "value" : 0 * mV,    "source" : "Moyer etal 2007, Humphries 2014", "unit" : "mV"},
    "GABA" :   { "value" : -60 * mV,  "source" : "Moyer etal 2007, Humphries 2014", "unit" : "mV"},
}
data["MSN"]["G"] = {
    "Ctx-MSN" : {
        "AMPA":   { "value" : 0.6,    "source" : "tuned to mach the FRs when only base cortical input is given","unit" : "nS"},
        "NMDA":   { "value" : 0.3,    "source" : "2:1 AMPA:NMDA ratio-Moyer 2007", "unit" : "nS"},
        "GABA":   { "value" : 0.0,    "source" : "None",  "unit" : "nS"},
    },
    "MSN-MSN" : {
        "AMPA":   { "value" : 0.0,    "source" : "None", "unit" : "nS"},
        "NMDA":   { "value" : 0.0,    "source" : "None", "unit" : "nS"},
        "GABA":   { "value" : 0.75,   "source" : "Koos etal 2004 - Humphries 2014",  "unit" : "nS"},
    },
    "FSI-MSN" : {
        "AMPA":   { "value" : 0.0,    "source" : "None", "unit" : "nS"},
        "NMDA":   { "value" : 0.0,    "source" : "None", "unit" : "nS"},
        "GABA":   { "value" : 3.75,   "source" : "Tuning in Humphries 2014", "unit" : "nS"},
    }
}

data["FSI"] = dict()
data["FSI"]["gap"] = {
    "tau" :   { "value" : 5 * ms,    "source" : "Humphries 2014", "unit" : "ms"},
    "g" :     { "value" : 5 * nS,    "source" : "Humphries 2014", "unit" : "nS"},
}
data["FSI"]["tau"] = {
    "AMPA" :   { "value" : 6 * ms,    "source" : "Moyer etal 2007, Humphries 2014", "unit" : "ms"},
    "GABA" :   { "value" : 4 * ms,    "source" : "Moyer etal 2007, Humphries 2014", "unit" : "ms"}
}
data["FSI"]["E"] = {
    "AMPA" :   { "value" : 0 * mV,    "source" : "Moyer etal 2007, Humphries 2014", "unit" : "mV"},
    "GABA" :   { "value" : -60 * mV,  "source" : "Moyer etal 2007, Humphries 2014", "unit" : "mV"},
}
data["FSI"]["G"] = {
    "Ctx-FSI" : {
        "AMPA":   { "value" : 0.55,    "source" : "My tuning (12.5-70Hz) with gap junctions", "unit" : "nS"},
    },
    "FSI-FSI" : {
        "GABA":   { "value" : 1.1,    "source" : "Gittis etal 2010 - used in Humphries 2014", "unit" : "nS"},
    }
}

data["STN"] = dict()
data["STN"]["tau"] = {
    "AMPA" :   { "value" : 2 * ms,    "source" : "Default value", "unit" : "ms"},
    "NMDA" :   { "value" : 100 * ms,  "source" : "Default value", "unit" : "ms"},
    "GABA" :   { "value" : 8 * ms,    "source" : "Lindahl 2013 from Baufreton 2005", "unit" : "ms"}
}
data["STN"]["E"] = {
    "AMPA" :   { "value" : 0 * mV,    "source" : "", "unit" : "mV"},
    "NMDA" :   { "value" : 0 * mV,    "source" : "", "unit" : "mV"},
    "GABA" :   { "value" : -84 * mV,  "source" : "Lindahl 2013 from Baufreton 2009", "unit" : "mV"},
}
data["STN"]["G"] = {
    "AMPA":      { "value" : 0.388,  "source" : "My tuning - Achieves 20 Hz (40Hz in high mode) FR when no GPe inhibition - works with different scales", "unit" : "nS"},
    "NMDA":      { "value" : 0.233,  "source" : "ampa*0.6 - Gotz:1997", "unit" : "nS"},
    "GABA":      { "value" : 0.518,  "source" : "My tuning - Achieves 10 Hz FR when GPe inhibition when C=300.", "unit" : "nS"}
}


data["GPe"] = dict()
data["GPe"]["tau"] = {
    "MSN-GPe" : {
        "GABA" :   { "value" : 6 * ms,    "source" : "Lindahl", "unit" : "ms"}
    },
    "GPe-GPe" : {
        "GABA" :   { "value" : 5 * ms,    "source" : "Lindahl", "unit" : "ms"}
    },
    "STN-GPe" : {
        "AMPA" :   { "value" : 2 * ms,    "source" : "General value, Abbott", "unit" : "ms"},
        "NMDA" :   { "value" : 100 * ms,  "source" : "General value, Abbott", "unit" : "ms"},
    }
}
data["GPe"]["E"] = {
    "AMPA" :   { "value" : 0 * mV,    "source" : "", "unit" : "mV"},
    "NMDA" :   { "value" : 0 * mV,    "source" : "", "unit" : "mV"},
    "GABA" :   { "value" : -65 * mV,  "source" : "RavAcha2005, Lindahl2013", "unit" : "mV"}
}
data["GPe"]["G"] = {
    "MSN-GPe" : {
        "GABA":      { "value" : 5.435, "source" : "c_GA_2-2", "unit" : "nS"}
    },
    "GPe-GPe" : {
        "GABA":      { "value" : 0.765, "source" : "c_GA_2-2", "unit" : "nS"}
    },
    "STN-GPe" : {
        "AMPA":      { "value" : 1.447, "source" : "Tuned to cause 30Hz in GPe when STN in 10Hz!", "unit" : "nS"},
        "NMDA":      { "value" : 0.518, "source" : "ampa*0.36 - Gotz:1997", "unit" : "nS"}
    } 
}

data["SNr"] = dict()
data["SNr"]["tau"] = {
    "GPe-SNr" : {
        "GABA" :   { "value" : 2.1 * ms,  "source" : "Lindahl 2013 from Conelly 2010", "unit" : "ms"}
    },
    "SNr-SNr" : {
        "GABA" :   { "value" : 3 * ms,    "source" : "General value", "unit" : "ms"}
    },
    "MSN-SNr" : {
        "GABA" :   { "value" : 5.2 * ms,  "source" : "Lindahl 2013 from Conelly 2010", "unit" : "ms"}
    },
    "STN-SNr" : {
        "AMPA" :   { "value" : 2 * ms,    "source" : "Default AMPA value", "unit" : "ms"},
        "NMDA" :   { "value" : 100 * ms,  "source" : "Default NMDA value", "unit" : "ms"},
    }

}
data["SNr"]["E"] = {
    "AMPA" :   { "value" : 0 * mV,    "source" : "Default AMPA value", "unit" : "mV"},
    "NMDA" :   { "value" : 0 * mV,    "source" : "Default NMDA value", "unit" : "mV"},
    "GABA" :   { "value" : -80 * mV,  "source" : "Default GABA value", "unit" : "mV"},
}
data["SNr"]["G"] = {
    "GPe-SNr" : {
        "GABA":      { "value" : 93.0,  "source" : "Manual tuning", "unit" : "nS"}
    },
    "SNr-SNr" : {
        "GABA":      { "value" : 0.2,  "source" : "Manual tuning", "unit" : "nS"}
    },
    "MSN-SNr" : {
        "GABA":      { "value" : 4.5,  "source" : "Manual tuning", "unit" : "nS"}
    },
    "STN-SNr" : {
        "AMPA":      { "value" : 14.0,"source" : "Local optimization", "unit" : "nS"},
        "NMDA":      { "value" : 5.88, "source" : "ampa*0.42 - Gotz:1997", "unit" : "nS"},
    }
}


