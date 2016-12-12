Getting started for this project
================================

* In addition to the vdmlab dependencies, 
  this project also requires matplotlib, 
  seaborn, jupyter and pandas libraries.

  ```
  conda install matplotlib seaborn jupyter pandas
  ```


Workflow
========

* Pull emi_biconditional.
* Get MedPC data from the server. Put training data files in `emi_biconditional\\cache\\data` folder.

## Specific analyses

This code contains analyses for:
* Behavior (medpc): `analyze_behavior.py`
Which analyzes and plots durations, number of entries, latency to first entry, 
and percent with responses.
* Behavior (vdmlab operant box): `analyze_vdmlab_behavior.py`


Biconditional task description
==============================

Below is a brief overview of biconditional experiment task and 
analysis work flow.


### Objectives

The main objective of this task was to determine whether subjects are able to 
learn a biconditional discrimination in a reasonable amount of time. 

Each session contained 32 trials (8 of each type; with a total of 16 rewarded and 16 unrewarded trials). 
There was an average 4 min intertrial interval (range from 2.5 min to 5.5 min).
Each cue (light or sound) was presented for 10 s, with a 5 s delay between cues. 
Two sessions were run daily during the light cycle; one beginning at 7am, the other ending at 7pm.

Cues in this experiment were:
* light1: steady cue light
* light2: flashing house light (2 flashes per s)
* sound1: pure tone (frequency: 1500, amplitude: 100. ~85dB) [note: outside LED on during sound1]
* sound2: white noise (amplitude: 85. ~85dB) 

#### Counter balanced

Each light-sound pairings were counterbalanced across rats (4 in each group) such 
that each pairing that is rewarded in one group is not in the other and vice versa.

#### Group 1
* Trial 1: light1 -> sound2 -
* Trial 2: light1 -> sound1 +
* Trial 3: light2 -> sound1 -
* Trial 4: light2 -> sound2 +

#### Group 2
* Trial 1: light2 -> sound2 -
* Trial 2: light2 -> sound1 +
* Trial 3: light1 -> sound1 -
* Trial 4: light1 -> sound2 +

### Analysis

RH01-RH06 & R103, R105 were trained in medpc boxes. RH05 & R105 underwent further training in vdmlab operant box.
