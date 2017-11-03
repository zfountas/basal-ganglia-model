##  -*- coding: utf-8 -*-

__author__ = "Zafeirios Fountas"
__credits__ = ["Murray Shanahan", "Mark Humphries",  "Rob Leech", "Jeanette Hellgren Kotaleski"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Zafeirios Fountas"
__email__ = "fountas@outlook.com"
__status__ = "Published"

# NOTES: 
# vr is the resting potential & vt the instantaneous threshold potential!
# The MSN model was taken from Humphries 2014 and the parameters were adjusted 
# using various sources

from brian import mV, pF, ms, pA

data = dict()
data["MSN"] = {
    "a" :          { "value" : 0.01/ms,   "source" : "Mahon etal 2000b, Izhikevich 2007", "unit" : ""},
    "b" :          { "value" : -20/ms,    "source" : "Izhikevich 2007", "unit" : ""},
    "c" :          { "value" : -55*mV,    "source" : "Izhikevich 2007", "unit" : ""},
    "d" :          { "value" : 91*mV/ms,  "source" : "Humphries 2009B", "unit" : ""},
    "vpeak" :      { "value" : 40 * mV,   "source" : "Izhikevich 2007", "unit" : "mV"},
    "vr" :         { "value" : -80 * mV,  "source" : "Izhikevich 2007", "unit" : "mV"},
    "vt" :         { "value" : -29.7 * mV,"source" : "Humphries 2009B", "unit" : "mV"},
    "k" :          { "value" : 1.0,       "source" : "Izhikevich 2007", "unit" : ""},
    "C" :          { "value" : 15.2*pF,   "source" : "Humphries 2009B", "unit" : "pF"},
        
    "v" :          { "value" : -80.0 * mV,"source" : "resting (Vr)", "unit" : "mV"},
    "u" :          { "value" : 0.0 * mV,  "source" : "??", "unit" : "mV"},

    "Ispon" :      { "value" : 0.0 * mV,  "source" : "??", "unit" : "mV"},

    "K" :          { "value" : 0.0289,    "source" : "Humphries 2009B", "unit" : ""},
    "L" :          { "value" : 0.331,     "source" : "Humphries 2009B", "unit" : ""},
    "alpha" :      { "value" : 0.032,     "source" : "Humphries 2009B", "unit" : ""},

    #"bita1" :      { "value" : 6.3,       "source" : "Humphries 2009B", "unit" : ""},
    #"bita2" :      { "value" : 0.215,     "source" : "Humphries 2009B", "unit" : ""}
    "bita1" :      { "value" : 0.5,       "source" : "Humphries 2014", "unit" : ""},
    "bita2" :      { "value" : 0.3,       "source" : "Humphries 2014", "unit" : ""}
}

data["FSI"] = {
    "a" :          { "value" : 0.2/ms,    "source" : "Izhikevich 2007", "unit" : ""},
    "b" :          { "value" : 0.025/ms,  "source" : "Izhikevich 2007", "unit" : ""},
    "c" :          { "value" : -60.0*mV,  "source" : "Tetano 2004 - Humphries 2014", "unit" : ""},
    "d" :          { "value" : 0.0*mV/ms, "source" : "Izhikevich 2007", "unit" : ""},
    "vpeak" :      { "value" : 25.0*mV,   "source" : "Izhikevich 2007", "unit" : "mV"},
    "vr" :         { "value" : -70.0*mV,  "source" : "Tetano 2004 - Humphries 2014", "unit" : "mV"},
    "vt" :         { "value" : -50.0*mV,  "source" : "Tetano 2004 - Humphries 2014", "unit" : "mV"},
    "k" :          { "value" : 1.0,       "source" : "Izhikevich 2007", "unit" : "none"},
    "C" :          { "value" : 80.0*pF,   "source" : "Tetano 2004 - Humphries 2014", "unit" : "pF"},

    "v" :          { "value" : -70.0*mV,  "source" : "resting (Vr)", "unit" : "mV"},
    "u" :          { "value" : 0.0*mV,    "source" : "??", "unit" : "mV"},

    "Ispon" :      { "value" : 0.0*mV,    "source" : "??", "unit" : "mV"},

    "vb" :         { "value" : -55.0*mV,  "source" : "Izhikevich 2007", "unit" : "mV"},

    "hta" :        { "value" : 0.1,       "source" : "Humphries 2014", "unit" : ""},
    "epsilon" :    { "value" : 0.625*mV,  "source" : "Humphries 2014", "unit" : ""},
}

# -- Fountas 2014 --------------------------------------------------------------

 
data["GPe-typeA"] = {
    "a" :          { "value" : 0.29 / ms,       "source" : "GA", "unit" : ""},
    "b" :          { "value" : 4.26 / ms,        "source" : "GA", "unit" : ""},
    "c" :          { "value" : -57.4 * mV,      "source" : "GA", "unit" : ""},
    "d" :          { "value" : 110.0 * mV/ms,   "source" : "GA", "unit" : ""},
    "vpeak" :      { "value" : 38.0 * mV,       "source" : "", "unit" : "mV"},
    "vr" :         { "value" : -50.7 * mV,      "source" : "", "unit" : "mV"},
    "vt" :         { "value" : -42.0 * mV,      "source" : "", "unit" : "mV"},
    "k" :          { "value" : 0.06 ,          "source" : "GA", "unit" : ""},
    "C" :          { "value" : 70.0,       "source" : "GA", "unit" : "pF"},
    "Cfig" :       { "value" : 55.0,       "source" : "GA", "unit" : "pF"},
    "C_var" :      { "value" : 20.0,       "source" : "manual", "unit" : "pF"},
    "C_var_real" : { "value" : 20.0,       "source" : "manual", "unit" : "pF"},
 
    "v" :          { "value" : -50.7 * mV,      "source" : "", "unit" : "mV"},
    "u" :          { "value" : 0.0 * mV,        "source" : "", "unit" : "mV"},
 
    # NOTE: Although Ivivo was 117 in the final tuning experiment, we need 15pA 
    # more to make the spontaneous activation (10Hz) to be consistent among GPes.
    "Ivivo" :      { "value" : (107.0+60.0)*pA, "source" : "Manual tuning", "unit" : "pA"},
    "Ivitro" :     { "value" : 107.0 * pA,      "source" : "GA", "unit" : "pA"},
    "sigma_vivo" : { "value" : 0.7,             "source" : "manual", "unit" : ""},
    "sigma_vitro" :{ "value" : 0.0,             "source" : "manual", "unit" : ""},
    "density" :    { "value" : 0.0405,          "source" : "From Bugaysen and Delong (15% LFB)", "unit" : ""}
}
 
data["GPe-typeB"] = {
    "a" :          { "value" : 0.0045 / ms,       "source" : "GA", "unit" : ""},
    "b" :          { "value" : 3.895 / ms,        "source" : "GA", "unit" : ""},
    "c" :          { "value" : -58.36 * mV,      "source" : "GA", "unit" : ""},
    "d" :          { "value" : 0.353 * mV/ms,   "source" : "GA", "unit" : ""},
    "vpeak" :      { "value" : 25.0 * mV,       "source" : "", "unit" : "mV"},
    "vr" :         { "value" : -53.0 * mV,      "source" : "", "unit" : "mV"},
    "vt" :         { "value" : -44.0 * mV,      "source" : "", "unit" : "mV"},
    "k" :          { "value" : 0.943 ,          "source" : "GA", "unit" : ""},
    "C" :          { "value" : 68.0,       "source" : "GA", "unit" : "pF"},
    "Cfig" :       { "value" : 68.0,       "source" : "GA", "unit" : "pF"},
    "C_var" :      { "value" : 20.0,       "source" : "manual", "unit" : "pF"},
    "C_var_real" : { "value" : 20.0,       "source" : "manual", "unit" : "pF"},
 
    "v" :          { "value" : -53.0 * mV,      "source" : "", "unit" : "mV"},
    "u" :          { "value" : 0.0 * mV,        "source" : "", "unit" : "mV"},
 
    "Ivivo" :      { "value" : 64.0 * pA,      "source" : "Manual tuning", "unit" : "pA"}, # Because I deleted Istim
    "Ivitro" :     { "value" : 52.0 * pA,      "source" : "GA", "unit" : "pA"},
    "sigma_vivo" : { "value" : 1.6,             "source" : "manual", "unit" : ""},
    "sigma_vitro" :{ "value" : 0.0,             "source" : "manual", "unit" : ""},
    "density" :    { "value" : 0.85,            "source" : "From Delong (85% HFP)", "unit" : ""}
}
 
data["GPe-typeC"] = {
    "a" :          { "value" : 0.42 / ms,       "source" : "GA", "unit" : ""},
    "b" :          { "value" : 7.0 / ms,        "source" : "GA", "unit" : ""},
    "c" :          { "value" : -52.0 * mV,      "source" : "GA", "unit" : ""},
    "d" :          { "value" : 166.0 * mV/ms,   "source" : "GA", "unit" : ""},
    "vpeak" :      { "value" : 34.5 * mV,       "source" : "", "unit" : "mV"},
    "vr" :         { "value" : -54.0 * mV,      "source" : "", "unit" : "mV"},
    "vt" :         { "value" : -43.0 * mV,      "source" : "", "unit" : "mV"},
    "k" :          { "value" : 0.099 ,          "source" : "GA", "unit" : ""},
    "C" :          { "value" : 65.0,            "source" : "GA", "unit" : "pF"},
    "Cfig" :       { "value" : 57.0,            "source" : "GA", "unit" : "pF"},
    "C_var" :      { "value" : 20.0,            "source" : "manual", "unit" : "pF"},
    "C_var_real" : { "value" : 20.0,            "source" : "manual", "unit" : "pF"},
 
    "v" :          { "value" : -54.0 * mV,      "source" : "", "unit" : "mV"},
    "u" :          { "value" : 0.0 * mV,        "source" : "", "unit" : "mV"},
 
    #"Ivivo" :      { "value" : 328.5 * pA,      "source" : "cGA2-2", "unit" : "pA"},
    #"Ivivo" :      { "value" : 197.5 * pA,      "source" : "Manual tuning", "unit" : "pA"},
    "Ivivo" :      { "value" : (187.5+50.0)* pA,"source" : "Manual tuning", "unit" : "pA"},
    "Ivitro" :     { "value" :  187.5 * pA,     "source" : "GA", "unit" : "pA"},
    "sigma_vivo" : { "value" : 1.3,             "source" : "manual", "unit" : ""},
    "sigma_vitro" :{ "value" : 0.0,             "source" : "manual", "unit" : ""},
    "density" :    { "value" : 0.1095,          "source" : "Bugaysen and Delong (15% LFB)", "unit" : ""}
}
 
data["SNr"] = {
    "a" :          { "value" : 0.113 / ms,        "source" : "GA", "unit" : ""},
    "b" :          { "value" : 11.057 / ms,        "source" : "GA", "unit" : ""},
    "c" :          { "value" : -62.7 * mV,      "source" : "GA", "unit" : ""},
    "d" :          { "value" : 138.4 * mV/ms,    "source" : "GA", "unit" : ""},
    "vpeak" :      { "value" : 9.8 * mV,       "source" : "", "unit" : "mV"},
    "vr" :         { "value" : -64.58 * mV,      "source" : "", "unit" : "mV"},
    "vt" :         { "value" : -51.8 * mV,      "source" : "", "unit" : "mV"},
    "k" :          { "value" : 0.7836 ,           "source" : "GA", "unit" : ""},
    "C" :          { "value" : 200.0,       "source" : "GA", "unit" : "pF"},
    "Cfig" :       { "value" : 172.1,       "source" : "GA", "unit" : "pF"},
    "C_var" :      { "value" : 50.0,   "source" : "manual", "unit" : "pF"},
    "C_var_real" : { "value" : 50.0,   "source" : "manual", "unit" : "pF"},

    "v" :          { "value" : -64.58 * mV,      "source" : "", "unit" : "mV"},
    "u" :          { "value" : 0.0 * mV,    "source" : "", "unit" : "mV"},
    "IvivoC" :     { "value" : 150.0 * pA,     "source" : "GA", "unit" : "pA"},
    "Ivivo" :      { "value" : 235.0 * pA,     "source" : "Manual tuning - This gives us 14.36Hz without STN connections which is consistent with Lindahl2013, Féger&Robledo 1991", "unit" : "pA"},
    "Ivitro" :     { "value" : 206.0 * pA,     "source" : "GA", "unit" : "pA"},
    "sigma_vivo" : { "value" : 0.3,     "source" : "GA", "unit" : ""},
    "sigma_vitro" :{ "value" : 0.3,     "source" : "GA", "unit" : ""}
}
 
data["STN-typeA"] = {
    "a1" :        { "value" : 0.021 / ms,        "source" : "GA", "unit" : ""},
    "b1" :        { "value" : 4.0 / ms,        "source" : "GA", "unit" : ""},
    "c" :         { "value" : -47.7 * mV,      "source" : "GA", "unit" : ""},
    "d1" :        { "value" : 17.1 * mV/ms,    "source" : "GA", "unit" : ""},
    "vpeak" :     { "value" : 15.4 * mV,       "source" : "", "unit" : "mV"},
    "vr" :        { "value" : -56.2 * mV,      "source" : "", "unit" : "mV"},
    "vt" :        { "value" : -41.4 * mV,      "source" : "", "unit" : "mV"},
    "k" :         { "value" : 0.439 ,           "source" : "GA", "unit" : ""},
    "C" :         { "value" : 23.0,       "source" : "GA", "unit" : "pF"},
    "Cfig" :      { "value" : 23.0,       "source" : "GA", "unit" : "pF"},
    "C_var" :     { "value" : 10.0,   "source" : "manual", "unit" : "pF"},
    "C_var_real" :{ "value" : 10.0,   "source" : "manual", "unit" : "pF"},
 
    "vr2" :       { "value" : -60.0 * mV,      "source" : "", "unit" : "mV"},
    "b_thres" :   { "value" : -60.0 * mV,      "source" : "", "unit" : "mV"},
    "a2" :        { "value" : 0.123 / ms,        "source" : "GA", "unit" : ""},
    "b2" :        { "value" : 0.015 / ms,        "source" : "GA", "unit" : ""},
    "d2" :        { "value" : -68.4 * mV/ms,    "source" : "GA", "unit" : ""},
 
    "w1" :        { "value" : 0.1,      "source" : "", "unit" : ""},
    "w2" :        { "value" : 0.0,      "source" : "", "unit" : ""},
 
    "v" :         { "value" : -56.2 * mV,      "source" : "", "unit" : "mV"},
    "u1" :        { "value" : 0.0,    "source" : "", "unit" : ""},
    "u2" :        { "value" : 0.0,    "source" : "", "unit" : ""},
 
    "Ivivo" :     { "value" : 56.1 * pA,     "source" : "GA", "unit" : "pA"},
    "Ivitro" :    { "value" : 56.1 * pA,     "source" : "GA", "unit" : "pA"},
    "sigma_vivo" :{ "value" : 1.5,     "source" : "GA", "unit" : ""},
    "sigma_vitro":{ "value" : 1.5,     "source" : "GA", "unit" : ""},
    "density" :    { "value" : 0.6,             "source" : "Bevan 2000", "unit" : ""}
}
 
data["STN-typeB"] = {
    "a1" :        { "value" : 0.05 / ms,        "source" : "GA", "unit" : ""},
    "b1" :        { "value" : 0.2 / ms,        "source" : "GA", "unit" : ""},
    "c" :         { "value" : -60.0 * mV,      "source" : "GA", "unit" : ""},
    "d1" :        { "value" : 1.0 * mV/ms,    "source" : "GA", "unit" : ""},
    "vpeak" :     { "value" : 15.4 * mV,       "source" : "", "unit" : "mV"},
    "vr" :        { "value" : -56.2 * mV,      "source" : "", "unit" : "mV"},
    "vt" :        { "value" : -50.0 * mV,      "source" : "", "unit" : "mV"},
    "k" :         { "value" : 0.3 ,           "source" : "GA", "unit" : ""},
    "C" :         { "value" : 40.0,       "source" : "GA", "unit" : "pF"},
    "Cfig" :      { "value" : 40.0,       "source" : "GA", "unit" : "pF"},
    "C_var" :     { "value" : 10.0,   "source" : "manual", "unit" : "pF"},
    "C_var_real" :{ "value" : 10.0,   "source" : "manual", "unit" : "pF"},
 
    "vr2" :       { "value" : -60.0 * mV,      "source" : "", "unit" : "mV"},
    "b_thres" :   { "value" : -60.0 * mV,      "source" : "", "unit" : "mV"},
    "a2" :        { "value" : 0.001 / ms,        "source" : "GA", "unit" : ""},
    "b2" :        { "value" : 0.3 / ms,        "source" : "GA", "unit" : ""},
    "d2" :        { "value" : 10.0 * mV/ms,    "source" : "GA", "unit" : ""},
 
    "w1" :        { "value" : 0.01,      "source" : "", "unit" : ""},
    "w2" :        { "value" : 0.0,      "source" : "", "unit" : ""},
 
    "v" :         { "value" : -56.2 * mV,      "source" : "", "unit" : "mV"},
    "u1" :        { "value" : 0.0,    "source" : "", "unit" : ""},
    "u2" :        { "value" : 0.0,    "source" : "", "unit" : ""},
 
    "Ivivo" :     { "value" : 8.0 * pA,     "source" : "GA", "unit" : "pA"},
    "Ivitro" :    { "value" : 25.0 * pA,     "source" : "GA", "unit" : "pA"},
    "sigma_vivo" :{ "value" : 1.5,     "source" : "GA", "unit" : ""},
    "sigma_vitro":{ "value" : 1.5,     "source" : "GA", "unit" : ""},
    "density" :    { "value" : 0.25,            "source" : "Bevan 2000", "unit" : ""}
}
 
data["STN-typeC"] = {
    "a1" :        { "value" : 0.44 / ms,        "source" : "GA", "unit" : ""},
    "b1" :        { "value" : -1.35 / ms,        "source" : "GA", "unit" : ""},
    "c" :         { "value" : -52.34 * mV,      "source" : "GA", "unit" : ""},
    "d1" :        { "value" : 17.65 * mV/ms,    "source" : "GA", "unit" : ""},
    "vpeak" :     { "value" : 15.4 * mV,       "source" : "", "unit" : "mV"},
    "vr" :        { "value" : -58.5 * mV,      "source" : "", "unit" : "mV"},
    "vt" :        { "value" : -43.75 * mV,      "source" : "", "unit" : "mV"},
    "k" :         { "value" : 0.105 ,           "source" : "GA", "unit" : ""},
    "C" :         { "value" : 30.0,       "source" : "GA", "unit" : "pF"},
    "Cfig" :      { "value" : 23.0,       "source" : "GA", "unit" : "pF"},
    "C_var" :     { "value" : 20.0,   "source" : "manual", "unit" : "pF"},
    "C_var_real" :{ "value" : 20.0,   "source" : "manual", "unit" : "pF"},
 
    "vr2" :       { "value" : -43.2 * mV,      "source" : "", "unit" : "mV"},
    "b_thres" :   { "value" : 1000.0 * mV,     "source" : "", "unit" : "mV"},
    "a2" :        { "value" : 0.32 / ms,        "source" : "GA", "unit" : ""},
    "b2" :        { "value" : 3.13 / ms,        "source" : "GA", "unit" : ""},
    "d2" :        { "value" : 92.0 * mV/ms,    "source" : "GA", "unit" : ""},
 
    "w1" :        { "value" : 0.001,      "source" : "", "unit" : ""},
    "w2" :        { "value" : 1.0,      "source" : "", "unit" : ""},
 
    "v" :         { "value" : -58.5 * mV,      "source" : "", "unit" : "mV"},
    "u1" :        { "value" : 0.0,    "source" : "", "unit" : ""},
    "u2" :        { "value" : 0.0,    "source" : "", "unit" : ""},
 
    "Ivivo" :     { "value" : -18.0 * pA,     "source" : "GA", "unit" : "pA"},
    "Ivitro" :    { "value" : -1.0 * pA,     "source" : "GA", "unit" : "pA"},
    "sigma_vivo" :{ "value" : 1.5,     "source" : "GA", "unit" : ""},
    "sigma_vitro":{ "value" : 0.5,     "source" : "GA", "unit" : ""},
    "density" :    { "value" : 0.15,            "source" : "Bevan 2000", "unit" : ""}
}


