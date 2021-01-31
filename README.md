# Replication Package: Model-based Performance Analysis for Architecting Cyber-Physical Dynamic Spaces



This is a replication package for the paper titled "Model-based Performance Analysis for Architecting Cyber-Physical Dynamic Spaces" and accepted for the IEEE International Conference on Software Architecture (ICSA 2021). The pre-print version of this paper in included in this package and is publicly available [here](https://github.com/rickypinci/CPS-architecture/blob/main/2021_ICSA21_CPS_Architectures_preprint.pdf).

## Authors
Riccardo Pinciroli - Gran Sasso Science Institute (Italy)<br/>
Catia Trubiani - Gran Sasso Science Institute (Italy)

## Abstract
Architecting Cyber-Physical Systems is not trivial since their intrinsic nature of mixing software and hardware components poses several challenges, especially when the physical space is subject to dynamic changes, e.g., paths of robots suddenly not feasible due to objects occupying transit areas or doors being closed with a high probability. This paper provides a quantitative evaluation of different architectural patterns that can be used for cyber-physical systems to understand which patterns are more suitable under some peculiar characteristics of dynamic spaces, e.g., frequency of obstacles in paths. We use stochastic performance models to evaluate architectural patterns, and we specify the dynamic aspects of the physical space as probability values. This way, we aim to support software architects with quantitative results indicating how different design patterns affect some metrics of interest, e.g., the system response time. Experiments show that there is no unique architectural pattern suitable to cope with all the dynamic characteristics of physical spaces. Each architecture differently contributes when varying the physical space, and it is indeed beneficial to switch among multiple patterns for an optimal solution. 

## Available Files
This package contains *i)* three folders (i.e., *figure2/*, *figures10and12/*, and *figures11and13/* ) with the files required to simulate all the scenarios considered in the paper, *ii)* a Jupyter notebook (i.e., *analysis.ipynb*) that plots results generated through simulations, and *iii)* the pre-print of the paper accepted for ICSA 2021.
A list of scripts and other files required to reproduce results is given in the following.
- Jsimg files in *figure2/*, *figures10and12/*, and *figures11and13/* are the models that are simulated using Java Modelling Tools (please, refer to the [Prerequisites](#prerequisites) section below); they should not be modified to avoid that other scripts stop working.
- *figure2/run_centralizedDecision.py* allows generating data for Figure 2 (CE curve).
- *figure2/run_independentDecision.py* allows generating data for Figure 2 (FD curve).
- *figure2/run_semiDistrDecision.py* allows generating data for Figure 2 (SD curve).
- *figure2/results/* contains the simulation outputs used to plot Figure 2 in the paper.
- *figures10and12/run_centralizedDecision_threeDoors.py* allows generating data for Figure 10 (CE curve)
- *figures10and12/run_independentDecision_threeDoors.py* allows generating data for Figure 10 (FD curve)
- *figures10and12/run_semiDistrDecision_threeDoors.py* allows generating data for Figure 10 (SD curve)
- *figures10and12/run_centralizedDecision_elevator.py* allows generating data for Figure 12 (CE curve)
- *figures10and12/run_independentDecision_elevator.py* allows generating data for Figure 12 (FD curve)
- *figures10and12/run_semiDistrDecision_elevator.py* allows generating data for Figure 12 (SD curve)
- *figures10and12/results/* contains the simulation outputs used to plot Figures 10 and 12 in the paper.
- *figures11and13/run_centralizedDecision_threeDoors.py* allows generating data for Figure 11 (CE curve)
- *figures11and13/run_independentDecision_threeDoors.py* allows generating data for Figure 11 (FD curve)
- *figures11and13/run_semiDistrDecision_threeDoors.py* allows generating data for Figure 11 (SD curve)
- *figures11and13/run_centralizedDecision_elevator.py* allows generating data for Figure 13 (CE curve)
- *figures11and13/run_independentDecision_elevator.py* allows generating data for Figure 13 (FD curve)
- *figures11and13/run_semiDistrDecision_elevator.py* allows generating data for Figure 13 (SD curve)
- *figures11and13/results/* contains the simulation outputs used to plot Figures 11 and 13 in the paper.

## Prerequisites
This is a list of other tools, libraries, and modules required to reproduce the results of our paper.
- [Java Modelling Tools](http://jmt.sourceforge.net/Download.html) that provides the simulator (JSIMG) used to obtain these results. Scripts in this repository have been tested with the JAR version of JMT 1.0.5
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
1. Go to *figure2/*, *figures10and12/*, or *figures11and13/* folders depending on which results must be replicated.
2. Open the python scripts in the directory and set the <tt>JMTPATH</tt> variable (line 11) to the PATH of the JMT.jar file that you have downloaded.
3. Run all the python scripts in the desired folder. Use the command: python3 <script_name>.py. For example, to reproduce the centralized (i.e., CE) curve in Figure 10, go to *figures10and12/* and run *python3 run_centralizedDecision_threeDoors.py*
4. All the available scripts are set to run simulations that are not longer than 10 minutes (line 15 is set to 600 seconds). 10 simulations are run concurrently (line 16 is set to 10). Please, change these values as you prefer. The parameters used in these scripts allow obtaining the same results shown in the paper. Feel free to change the "Simulation parameters" section of each script to test different system configurations.
5. If during the script execution an error (i.e., "*java.io.FileNotFoundException*") is raised, please i) stop the script, ii) remove all output files that are in the current directory (i.e., *figure2/*, *figures10and12/*, or *figures11and13/*), and iii) restart the script with a decreased number of parallel executions (i.e., line 16).
6. Note that all folders already contain simulation results used to plot the figures in the paper. If you do not want to run new simulations, you can still try to plot those figures.
7. Once all simulations are completed, open the *analysis.ipynb* file (tested with Jupyter). Execute all cells related to the considered scenario to plot the desired figures.
