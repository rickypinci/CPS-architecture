# Replication Package: Model-based Performance Analysis for Architecting Cyber-Physical Dynamic Spaces



This is a replication package for the paper titled "Model-based Performance Analysis for Architecting Cyber-Physical Dynamic Spaces" and accepted for the IEEE International Conference on Software Architecture (ICSA 2021). The submitted version of the paper is included in this package and is publicly available [here](https://github.com/rickypinci/CPS-architecture/blob/main/2021-ICSA-PerfAnalysis-CPS-dynamicSpaces-submitted-version.pdf). We are currently working on the camera-ready version of the paper to address reviewers' comments, but there will be no changes in the showed experimental results.

## Authors
Riccardo Pinciroli - Gran Sasso Science Institute (Italy)<br/>
Catia Trubiani - Gran Sasso Science Institute (Italy)

## Abstract
Architecting Cyber-Physical Systems is not trivial since their intrinsic nature of mixing software and hardware components poses several challenges, especially when the physical space is subject to dynamic changes, e.g., paths of robots suddenly not feasible due to objects occupying transit areas or doors being closed with a high probability. This paper provides a quantitative evaluation of different architectural patterns that can be used for cyber-physical systems to understand which patterns are more suitable under some peculiar characteristics of dynamic spaces, e.g., frequency of obstacles in paths. We use stochastic performance models to evaluate architectural patterns, and we specify the dynamic aspects of the physical space as probability values. This way, we aim to support software architects with quantitative results indicating how different design patterns affect some metrics of interest, e.g., the system response time. Experiments show that there is no unique architectural pattern suitable to cope with all the dynamic characteristics of physical spaces. Each architecture differently contributes when varying the physical space, and it is indeed beneficial to switch among multiple patterns for an optimal solution. 

## Available Files
This package contains *i)* three folders (i.e., *figure2/*, *figures10and12/*, and *figures11and13/* ) with the files required to simulate all the scenarios considered in the paper, *ii)* a Jupyter notebook (i.e., *analysis.ipynb*) that plots results generated through simulations, and *iii)* the submitted version of the paper accepted at ICSA 2021.
A list of scripts and other files required to reproduce results is given in the following.
- *varEnv.py* allows specifying three variables that are used by all the scripts in the package. Specifically, they are <tt>JMTPATH</tt> (where the *jar* file of the *Java Modelling Tools* is located), <tt>MAXTIME</tt> (the maximum simulation time), and <tt>MAXTHREADS</tt> (the number of concurrent simulations).
- Jsimg files in *figure2/*, *figures10and12/*, and *figures11and13/* are the models that are simulated using Java Modelling Tools (please, refer to the [Prerequisites](#prerequisites) section below); they should not be modified to avoid that other scripts stop working.
- *figure2/run_centralizedDecision.py* allows generating data for Figure 2 (CE curve).
- *figure2/run_fullyDistrDecision.py* allows generating data for Figure 2 (FD curve).
- *figure2/run_semiDistrDecision.py* allows generating data for Figure 2 (SD curve).
- *figure2/results/* contains the simulation outputs used to plot Figure 2 in the paper.
- *figures10and12/run_centralizedDecision_threeDoors.py* allows generating data for Figure 10 (CE curve)
- *figures10and12/run_fullyDistrDecision_threeDoors.py* allows generating data for Figure 10 (FD curve)
- *figures10and12/run_semiDistrDecision_threeDoors.py* allows generating data for Figure 10 (SD curve)
- *figures10and12/run_centralizedDecision_elevator.py* allows generating data for Figure 12 (CE curve)
- *figures10and12/run_fullyDistrDecision_elevator.py* allows generating data for Figure 12 (FD curve)
- *figures10and12/run_semiDistrDecision_elevator.py* allows generating data for Figure 12 (SD curve)
- *figures10and12/results/* contains the simulation outputs used to plot Figures 10 and 12 in the paper.
- *figures11and13/run_centralizedDecision_threeDoors.py* allows generating data for Figure 11 (CE curve)
- *figures11and13/run_fullyDistrDecision_threeDoors.py* allows generating data for Figure 11 (FD curve)
- *figures11and13/run_semiDistrDecision_threeDoors.py* allows generating data for Figure 11 (SD curve)
- *figures11and13/run_centralizedDecision_elevator.py* allows generating data for Figure 13 (CE curve)
- *figures11and13/run_fullyDistrDecision_elevator.py* allows generating data for Figure 13 (FD curve)
- *figures11and13/run_semiDistrDecision_elevator.py* allows generating data for Figure 13 (SD curve)
- *figures11and13/results/* contains the simulation outputs used to plot Figures 11 and 13 in the paper.

## Prerequisites
This is a list of other tools, libraries, and modules required to reproduce the results of our paper.
- [Java Modelling Tools](http://jmt.sourceforge.net/Download.html) that provides the simulator (JSIMG) used to obtain these results. Scripts in this repository have been tested with the JAR version of JMT 1.1.0
- Python 3
- The following Python modules:
  - Numpy (install with *pip3 install numpy*)
  - Pandas (install with *pip3 install pandas*)
  - Matplotlib (install with *pip3 install matplotlib*)
  - Jupyter (install with *pip3 install notebook*)
- Other Python modules that are in *stdlib* (they do not require to be installed)
  - os
  - sys
  - random
  - xml.etree.ElementTree

## Run a JMT model
1. Download this package and unzip it where you prefer. Then, <tt>cd</tt> the unzipped package. This package does not need to be installed and can be used with any operating systems that supports the [Prerequisites](#prerequisites).
2. Download and install modules and tools in the [Prerequisites](#prerequisites) section.
3. Set the <tt>JMTPATH</tt> variable in *varEnv.py* to the path of the *JMT.jar* file that you have downloaded. All the scripts are set to run 10 concurrent simulations that are not longer than 10 minutes (i.e, <tt>MAXTHREADS = 10</tt> and <tt>MAXTIME = 600</tt>, respectively, in *varEnv.py*). Please, change these values according to your preferences.
4. <tt>cd</tt> *figure2/*, *figures10and12/*, or *figures11and13/*, depending on which results must be replicated.
5. Run all the python scripts in the folder using: <tt>python3 *script\_name*.py</tt>. For example, to reproduce the centralized (i.e., CE) curve in Figure 10, <tt>cd</tt> *figures10and12/* and run <tt>python3 run\_centralizedDecision_threeDoors.py</tt>
6. The parameters used in these scripts allow obtaining the same results shown in the paper. Feel free to change the *Simulation parameters* section of each script to test different system configurations.
7. If during the script execution an error (i.e., <tt>java.io.FileNotFoundException</tt>) is raised, please *i)* stop the script, *ii)* remove all output files that have been created in the directory (i.e., *figure2/*, *figures10and12/*, or *figures11and13/*), and *iii)* restart the script. If the error persist, please consider to reduce the number of concurrent simulations in *varEnv.py*.
8. Note that all the directories already contain simulation results used to plot the figures in the paper. If you do not want to run new simulations, you can still try to plot those figures using the provided data.
9. Once all simulations are completed, open the *analysis.ipynb* file (tested with Jupyter). Execute all cells related to the considered scenario to plot the desired figures.
