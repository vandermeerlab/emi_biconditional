Getting started for this project
================================

* In addition to the nept dependencies,
  this project also requires pandas, matplotlib,
  seaborn, jupyter and svgutils libraries.

  ```
  conda install pandas, matplotlib seaborn jupyter svgutils
  ```


Workflow
========

* Pull emi_biconditional.
* Get MedPC data from the server. Put data files in `emi_biconditional\\cache\\data\\myproject` folder.

Specific analyses
-----------------

This code contains analyses for:

* Behavior (medpc and cutom vdmlab operant box)

Which analyzes and plots the nosepoke durations, number of entries, latency to first entry,
and percent of trials with responses.


Task descriptions
=================

The main objective of this series of tasks is to establish
a procedure compatible with recording 
that involves the presentation of a discrete cue 
whose meaning is modulated by a seperate discrete cue.

201601
------
Negative occasion setting

hM4Di DREADD in vHC

* 5 rats total; 2 DREADD experimental, 2 mCherry-alone controls, 1 WT CNO control
* 5 second feature cue (steady light)
* 5 second delay gap between feature and target
* 5 second target cue (pure tone ~85dB)
* Phase 1: 16 trials per session. 1:1 ratio; 8 rewarded trials, 8 unrewarded trials. Average 4 minute intertrial interval (range from 2.5 minuts to 5.5 minutes)
* Phase 2: 16 trials per session. 3:1 ratio; 4 rewarded trials, 12 unrewarded trials. Average 4 minute intertrial interval (range from 2.5 minuts to 5.5 minutes)
* Phase 3: 64 trials per session. 3:1 ratio; 16 rewarded trials, 48 unrewarded trials. Average 2 minute intertrial interval

201604
------
Negative occasion setting

Ibotenic acid lesion of vHC

* 8 rats total; 2 lesion experimental, 2 sham controls, 2 WT controls
* 5 second feature cue (steady light)
* 5 second delay gap between feature and target
* 5 second target cue (pure tone ~85dB)
* 32 trials per session
* 3:1 ratio; 8 rewarded trials, 24 unrewarded trials
* Average 4 minute intertrial interval (range from 2.5 minuts to 5.5 minutes)

* Missing data from session 2 (data not saved properly from MedPC system)

201610
------
Biconditional discrimination

Two daily sessions

* 8 rats total
* 10 second feature cue (steady or flashing light)
* 5 second delay gap between feature and target
* 10 second target cue (pure tone or white noise ~85dB)
* 32 trials per session
* 8 of each trial type, with a total of 16 rewarded and 16 unrewarded trials
* Average 4 minute intertrial interval (range from 2.5 minuts to 5.5 minutes)
* Counterbalanced
* Rats 5 and 8 were additionally run in the prototype vdmlab opperant box

201701
------
Biconditional discrimination

Trial blocks

* 8 rats total
* 10 second feature cue (steady or flashing light)
* 1 second delay gap between feature and target
* 10 second target cue (pure tone or click ~85dB)
* 32 trials per session
* 8 of each trial type, with a total of 16 rewarded and 16 unrewarded trials
* Average 4 minute intertrial interval (range from 2.5 minuts to 5.5 minutes)
* Counterbalanced
* Trial sequence in blocks of 4 trials

201704
------
Biconditional discrimination

Feature blocks

* 8 rats total
* 10 second feature cue (steady or flashing light)
* 1 second delay gap between feature and target
* 10 second target cue (pure tone or click ~85dB)
* 32 trials per session
* 8 of each trial type, with a total of 16 rewarded and 16 unrewarded trials
* Average 4 minute intertrial interval (range from 2.5 minuts to 5.5 minutes)
* Counterbalanced
* Both female and male rats
* Trial sequence in blocks of features

201709
------
Occasion setting & biconditional discrimination

Long features

* 8 rats total
* Average 3.5 minute feature cue (steady or flashing light; range from 2.5 minuts to 4.5 minutes)
* No delay gap between feature and target
* 10 second target cue(s) (pure tone and white noise ~85dB introduced for the biconditional discrimination)
* 28 or 30 trials per session
* Equal ratios (1:1 for occasion setting; 1:1:1:1 for biconditional)
* 1 minute intertrial interval
* Counterbalanced
* Both female and male rats
* Phase 1: Conditioning tone only occasion setting (16 sessions)
* Phase 2: Counterconditioning (13 sessions)
* Phase 3: Re-training tone only occasion setting (16 sessions)
* Phase 4: Biconditional discrimination (16 sessions)
* Phase 5: Re-training tone only occasion setting (10 sessions)
* Phase 6: Alternating tone only and white noise only occasion setting sessions (15 noise sessions; 10 tone sessions)
* Phase 7: Joint tone and noise sessions (blocks of noise or tone for 16 sessions)