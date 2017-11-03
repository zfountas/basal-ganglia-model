# A large-scale spiking neural network model of the basal ganglia circuitry. 

This model integrates fine-tuned models of phenomenological (Izhikevich) spiking neurons that correspond to different sub-types of cells within the BG nuclei, electrical and conductance-based chemical synapses that include short-term plasticity and neuromodulation, as well as anatomically-derived striatal connectivity. 

In particular, this model comprises 10 neural populations that correspond to the four major nuclei of the biological basal ganglia and form their canonical circuit. These include the striatum (modelled with higher detail than the other groups) and the subthalamic nucleus (STN), the two inputs of the basal gnaglia, the external part of the globus pallidus (GPe), as well as the substantia nigra pars reticulata (SNr), one of the two output structures. Furthermore, the effect of the pars compacta part of the substantia nigra (SNc) is realized through the concentration of the neurotransmitter dopamine in the different parts of the network. The network is divided into three microscopic channels, which are mutually inhibited and used to represent different action requests. A full description of this model can be found in the first two published manuscripts that follow.

A list of citable manuscripts that used this model:

* Fountas, Zafeirios. "*Action selection in the rhythmic brain: The role of the basal ganglia and tremor.*" (2016).

* Fountas, Zafeirios, and Murray Shanahan. "*The role of cortical oscillations in a spiking neural model of the basal ganglia.*" *Under review*, PLOS ONE

* Fountas, Zafeirios, and Murray Shanahan. "*Assessing Selectivity in the Basal Ganglia: The 'Gearbox' Hypothesis.*" bioRxiv (2017): 197129.

The latest version of this project can be also found on github: https://github.com/zfountas/basal-ganglia-model



## Prerequisites

The project's prerequisites include the python2.7 libraries brian, numpy and matplotlib. To install these libraries on a linux machine please open a terminal and type:

```
(sudo) pip install -r requirements.txt
```


## Run simulations

To run a simulation please type:

```
./bgrun -argument1 -argument2 ...
```

where the available arguments are given as:

### BASIC ARGUMENTS
* --help: *shows the basic arguments*
* -fr {value}: *is the frequency of cortical oscillations *
* -ph {value}: *is the phase offset between two different cortical inputs*
* -dop {value}: *is the overall level of dopamine in the system*
* -file {data_file_name}: *is optional, and represents the name of the file where data will be stored*
* -print: *Ff defined, it activates a verbose mode*
* -plots: *If defined, it will generate plots of the simulation*
* -seed {value/random}: *specifies the random seed of the simulation*
* -duration {value}: *specifies the duration of the simulation*
* -fr1 {value}: *is the frequency of the first cortical input*
* -end {value}:

### INPUT TYPES 
* -initial_period: *If defined, the model runs for a initial period of 500ms with only tonic (cortical) stimulation*
* -random_walk: *If defined, the intensity of cortical input follows a random walk*

### RECORDING OPTIONS 
* -rec_rasters: *If defined, records spike trains for all populations*
* -rec_GPe_types: *If defined, records different types of GPe neurons individually*
* -rec_bins: *If defined, records binned spikes for each neuron group*

### INPUT MODES 
* -tonic: *If active, the model will run with only tonic cortical stimulation*
* -one_channel: *If active, only one channel receives stimulation*
* -ramp: *If active, the model receives ramped stimulation*
* -GG_stn_gpe:
* -GG_gpe_stn:

### AMPLITUTE OF INPUTS 
* -T1base {value}: *Lowest value of the firing rate of the cortical input in channel 1*
* -T2base {value}: *Lowest value of the firing rate of the cortical input in channel 2*
* -T3base {value}: *Lowest value of the firing rate of the cortical input in channel 3*
* -T1max {value}: *Highest value of the firing rate of the cortical input in channel 1*
* -T2max {value}: *Highest value of the firing rate of the cortical input in channel 2*

### REST 
* -pd_off_state:
* -weight_Bahuguna:
* -P_striatum_weight {value}:
* -GPe_density {value1,2} {value3}: *Density of the 3 GPe neuron types*
* -gpe_type {A/B/C}: *Allows only one GPe neuron type in the simulation*
* -plasticity {True/False}: *If True, short-term synaptic plasticity activates*


## Authors

* **[Zafeirios Fountas](https://www.doc.ic.ac.uk/~zf509/)** - *Initial work and author of the PhD thesis*


## License

This project is licensed under the GLUv3 License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments

* **Murray Shanahan** who was Zafeirios' PhD supervisior and co-author of published work
* **Mark Humphries** who provided valuable feedback and inspiration
* **Jeanette Hellgren Kotaleski** who was the first PhD examiner
* **Rob Leech** who was the second PhD examiner
* **EPSRC** and **Imperial College London** for providing funding






















