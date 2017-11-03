# basal-ganglia-model
A large-scale spiking neural network model of the basal ganglia circuitry

This repo provides the default version of the model that was designed and developed in the frame of the PhD thesis of Zafeirios Fountas, as well as a series of publications regarding the same work. 

The latest version of this project can be also found on github: https://github.com/zfountas/basal-ganglia-model

A full list of citable manuscripts that are used this model:

* Fountas, Zafeirios. "Action selection in the rhythmic brain: The role of the basal ganglia and tremor." (2016).

* Fountas, Zafeirios, and Murray Shanahan. "The role of cortical oscillations in a spiking neural model of the basal ganglia." Under review, PLOS ONE

* Fountas, Zafeirios, and Murray Shanahan. "Assessing Selectivity in the Basal Ganglia: The" Gearbox" Hypothesis." bioRxiv (2017): 197129.


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
*--help*: shows the basic arguments
*-fr <value>*: is the frequency of cortical oscillations 
*-ph <value>*: is the phase offset between two different cortical inputs
*-dop <value>*: is the overall level of dopamine in the system
*-file <data_file_name>*: is optional, and represents the name of the file where data will be stored
*-print*: Ff defined, it activates a verbose mode
*-plots*: If defined, it will generate plots of the simulation
*-seed <value/random>*: specifies the random seed of the simulation
*-duration <value>*: specifies the duration of the simulation
*-fr1 <value>*: is the frequency of the first cortical input
*-end <value>*:

### INPUT TYPES 
*-initial_period*: If defined, the model runs for a initial period of 500ms with only tonic (cortical) stimulation
*-random_walk*: If defined, the intensity of cortical input follows a random walk

### RECORDING OPTIONS 
*-rec_rasters*: If defined, records spike trains for all populations
*-rec_GPe_types*: If defined, records different types of GPe neurons individually
*-rec_bins*: If defined, records binned spikes for each neuron group

### INPUT MODES 
*-tonic*: If active, the model will run with only tonic cortical stimulation
*-one_channel*: If active, only one channel receives stimulation
*-ramp*: If active, the model receives ramped stimulation
*-GG_stn_gpe*: 
*-GG_gpe_stn*:

### AMPLITUTE OF INPUTS 
*-T1base <value>*: Lowest value of the firing rate of the cortical input in channel 1
*-T2base <value>*: Lowest value of the firing rate of the cortical input in channel 2
*-T3base <value>*: Lowest value of the firing rate of the cortical input in channel 3
*-T1max <value>*: Highest value of the firing rate of the cortical input in channel 1
*-T2max <value>*: Highest value of the firing rate of the cortical input in channel 2

### REST 
*-pd_off_state*:
*-weight_Bahuguna*:
*-P_striatum_weight <value>*:
*-GPe_density <value1,2> <value3>*: Density of the 3 GPe neuron types
*-gpe_type <A/B/C>*: Allows only one GPe neuron type in the simulation
*-plasticity <True/False>*: If True, short-term synaptic plasticity activates


## Authors

* **Zafeirios Fountas** - *Initial work* - [PurpleBooth](https://www.doc.ic.ac.uk/~zf509/)


## License

This project is licensed under the GLUv3 License - see the [LICENSE.md](LICENSE.md) file for details.


## Acknowledgments

* **Murray Shanahan** who was Zafeirios' PhD supervisior and co-author of published work.
* **Mark Humphries** who provided valuable feedback and inspiration.
* **Jeanette Hellgren Kotaleski** who was the first PhD examiner
* **Rob Leech** who was the second PhD examiner























