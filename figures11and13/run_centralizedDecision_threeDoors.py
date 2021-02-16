import random
import os
import time
import xml.etree.ElementTree as et
import numpy as np
import threading
import itertools
import sys
sys.path.insert(1, '../')
from varEnv import *

# Constants
PATTERNNAME = 'centralizedDecision_threeDoors'
TEST_NAME = 'varChangePolicy'
MODEL_NAME = 'slidingDoor'
#JMTPATH = '~/JMT/JMT-1.0.5.jar'
#MAXTIME = 600
#MAXTHREADS = 10
if PATTERNNAME != '':
	PATTERNNAME = '_' + PATTERNNAME
SOURCEFILE = MODEL_NAME + PATTERNNAME + '.placeholder.jsimg'
if TEST_NAME != '':
	RESULTS_DIR = 'results/three_doors/' + MODEL_NAME + PATTERNNAME + '_' + TEST_NAME + '/'
else:
	RESULTS_DIR = 'results/three_doors/' + MODEL_NAME + PATTERNNAME + '_' + str(int(time.time())) + '/'
PARAM_NAME = [
'A_reqA',
'A_reqB',
'N_robot',
'reqAonRobot',
'reqBonRobot',
'S_door_opening',
'S_door_closing',
'S_reqA_driveToDoor',
'S_reqA_driveFwd',
'S_reqA_driveBack1',
'S_reqA_driveAround',
'S_reqB_driveToDoor',
'S_reqB_driveFwd',
'S_reqB_driveBack',
'S_reqB_driveAround',
'S_robot_driveToDoor',
'S_robot_driveFwd',
'S_robot_driveBack3',
'S_robot_driveAround',
'S_changePolicyToOpen',
'probA',
'probB',
'Z_robot',
'comm_same_room',
'S_reqA_driveBack2',
'S_reqA_driveBack3',
'S_robot_driveBack2',
'S_robot_driveBack1',
]
INDEX_NAME_TMP = [
'R_robot_choosing1_A',
'R_robot_reachDoor1_A',
'R_robot_driveThru1_A',
'R_robot_driveFwd1_A',
'R_robot_driveBack1_A',
'R_robot_driveAround1_A',
'R_robot_choosing1_B',
'R_robot_reachDoor1_B',
'R_robot_driveThru1_B',
'R_robot_driveFwd1_B',
'R_robot_driveBack1_B',
'R_robot_driveAround1_B',
'X_robot_goFast1_A',
'X_robot_goSlow1_A',
'X_robot_success1_A',
'X_robot_fail1_A',
'X_robot_goFast1_B',
'X_robot_goSlow1_B',
'X_robot_success1_B',
'X_robot_fail1_B',
'R_robot_choosing2_A',
'R_robot_reachDoor2_A',
'R_robot_driveThru2_A',
'R_robot_driveFwd2_A',
'R_robot_driveBack2_A',
'R_robot_driveAround2_A',
'R_robot_choosing2_B',
'R_robot_reachDoor2_B',
'R_robot_driveThru2_B',
'R_robot_driveFwd2_B',
'R_robot_driveBack2_B',
'R_robot_driveAround2_B',
'X_robot_goFast2_A',
'X_robot_goSlow2_A',
'X_robot_success2_A',
'X_robot_fail2_A',
'X_robot_goFast2_B',
'X_robot_goSlow2_B',
'X_robot_success2_B',
'X_robot_fail2_B',
'R_robot_choosing3_A',
'R_robot_reachDoor3_A',
'R_robot_driveThru3_A',
'R_robot_driveFwd3_A',
'R_robot_driveBack3_A',
'R_robot_driveAround3_A',
'R_robot_choosing3_B',
'R_robot_reachDoor3_B',
'R_robot_driveThru3_B',
'R_robot_driveFwd3_B',
'R_robot_driveBack3_B',
'R_robot_driveAround3_B',
'X_robot_goFast3_A',
'X_robot_goSlow3_A',
'X_robot_success3_A',
'X_robot_fail3_A',
'X_robot_goFast3_B',
'X_robot_goSlow3_B',
'X_robot_success3_B',
'X_robot_fail3_B'
]
INDEX_NAME = []
for n in INDEX_NAME_TMP:
	INDEX_NAME.append(n + '_mean')
	INDEX_NAME.append(n + '_low')
	INDEX_NAME.append(n + '_up')
ATTRIBUTE_NAME = PARAM_NAME + INDEX_NAME
NUM_PARAM_VALS = len(PARAM_NAME)
NUM_INDEX_VALS = len(INDEX_NAME)
NUM_TOTAL_VALS = len(ATTRIBUTE_NAME)
#Prepare the header of the CSV file (i.e., attribute names)
ATTRIBUTE_STR = ''
for attr in ATTRIBUTE_NAME:
	ATTRIBUTE_STR += attr + ','
ATTRIBUTE_STR = ATTRIBUTE_STR[:-1]



#####################################################################################
#####################################################################################
############################ START: Simulation parameters ###########################
#####################################################################################
#####################################################################################
###### Robot parameters ######
AVAIL_ROBOT = [10,50] + list(range(100,1000+1,100)) #N
# PERC_ROBOT_WHEELS is obtained as 1 - PERC_ROBOT_LEGS
REQA_ROBOT = [1] #NOT REQUIRED
REQB_ROBOT = [1] #NOT REQUIRED
###### Door and Stairs parameters ######
DOOR_PERIOD = 60 #mu_switch-A-U + mu_switch-U-A
S_DOOR_OPEN = [30] #mu_switch-A-U
# S_DOOR_CLOSE is obtained as 60 - S_DOOR_OPEN
S_CHANGE_POLICY = [10] #mu_refresh
###### Communication Cost ######
COMM_SAME_ROOM = [1] #mu_fail = mu_ask
###### Arrival rates for classes reqA and reqB ######
A_REQA = [30] #NOT REQUIRED
A_REQB = [30] #NOT REQUIRED
PROB_REQA = [0.1] #NOT REQUIRED
###### reqA and reqB service times at different stations ######
Z_ROBOT = [10] #mu_wait
S_REQA_DOOR = [5] #mu_reach_F
S_REQA_FWD = [5] #mu_goStraight_F
S_REQA_BACK1 = [5] #mu_turn_D1_F
S_REQA_BACK2 = [15] #mu_turn_D2_F
S_REQA_BACK3 = [25] #mu_turn_D3_F
S_REQA_AROUND = [40] #mu_goAround_F
S_REQB_DOOR = [5] #NOT REQUIRED
S_REQB_FWD = [5] #NOT REQUIRED
S_REQB_BACK = [5] #NOT REQUIRED
S_REQB_AROUND = [40] #NOT REQUIRED
S_ROBOT_DOOR = [5] #mu_reach_B
S_ROBOT_FWD = [5] #mu_goStright_B
S_ROBOT_BACK1 = [25] #mu_turn_D1_B
S_ROBOT_BACK2 = [15] #mu_turn_D2_B
S_ROBOT_BACK3 = [5] #mu_turn_D3_B
S_ROBOT_AROUND = [40] #mu_goAround_B
#####################################################################################
#####################################################################################
############################ STOP: Simulation parameters ############################
#####################################################################################
#####################################################################################



###### List for collecting measures. This must be specified following the order of INDEX_NAME_TMP. ['type', 'referenceUserClass', 'station'] ######
collectList = [
['Response Time', 'robot', 'choosing1_A'],
['Response Time', 'robot', 'reachDoor1_A'],
['Response Time', 'robot', 'driveThru1_A'],
['Response Time', 'robot', 'goFwd1_A'],
['Response Time', 'robot', 'goBack1_A'],
['Response Time', 'robot', 'goAround1_A'],
['Response Time', 'robot', 'choosing1_B'],
['Response Time', 'robot', 'reachDoor1_B'],
['Response Time', 'robot', 'driveThru1_B'],
['Response Time', 'robot', 'goFwd1_B'],
['Response Time', 'robot', 'goBack1_B'],
['Response Time', 'robot', 'goAround1_B'],
['Throughput', 'robot', 'ifOpen1_A'],
['Throughput', 'robot', 'ifClosed1_A'],
['Throughput', 'robot', 'success1_A'],
['Throughput', 'robot', 'fail1_A'],
['Throughput', 'robot', 'ifOpen1_B'],
['Throughput', 'robot', 'ifClosed1_B'],
['Throughput', 'robot', 'success1_B'],
['Throughput', 'robot', 'fail1_B'],
['Response Time', 'robot', 'choosing2_A'],
['Response Time', 'robot', 'reachDoor2_A'],
['Response Time', 'robot', 'driveThru2_A'],
['Response Time', 'robot', 'goFwd2_A'],
['Response Time', 'robot', 'goBack2_A'],
['Response Time', 'robot', 'goAround2_A'],
['Response Time', 'robot', 'choosing2_B'],
['Response Time', 'robot', 'reachDoor2_B'],
['Response Time', 'robot', 'driveThru2_B'],
['Response Time', 'robot', 'goFwd2_B'],
['Response Time', 'robot', 'goBack2_B'],
['Response Time', 'robot', 'goAround2_B'],
['Throughput', 'robot', 'ifOpen2_A'],
['Throughput', 'robot', 'ifClosed2_A'],
['Throughput', 'robot', 'success2_A'],
['Throughput', 'robot', 'fail2_A'],
['Throughput', 'robot', 'ifOpen2_B'],
['Throughput', 'robot', 'ifClosed2_B'],
['Throughput', 'robot', 'success2_B'],
['Throughput', 'robot', 'fail2_B'],
['Response Time', 'robot', 'choosing3_A'],
['Response Time', 'robot', 'reachDoor3_A'],
['Response Time', 'robot', 'driveThru3_A'],
['Response Time', 'robot', 'goFwd3_A'],
['Response Time', 'robot', 'goBack3_A'],
['Response Time', 'robot', 'goAround3_A'],
['Response Time', 'robot', 'choosing3_B'],
['Response Time', 'robot', 'reachDoor3_B'],
['Response Time', 'robot', 'driveThru3_B'],
['Response Time', 'robot', 'goFwd3_B'],
['Response Time', 'robot', 'goBack3_B'],
['Response Time', 'robot', 'goAround3_B'],
['Throughput', 'robot', 'ifOpen3_A'],
['Throughput', 'robot', 'ifClosed3_A'],
['Throughput', 'robot', 'success3_A'],
['Throughput', 'robot', 'fail3_A'],
['Throughput', 'robot', 'ifOpen3_B'],
['Throughput', 'robot', 'ifClosed3_B'],
['Throughput', 'robot', 'success3_B'],
['Throughput', 'robot', 'fail3_B'],
]




######################################
###### START: Utility functions ######
######################################
class MyThread(threading.Thread):
	def __init__(self, threadID, params, paramsToWrite):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.params = params #list
		self.paramsToWrite = paramsToWrite #list
	def run(self):
		threadLimiter.acquire()
		print('[START] Thread ' + str(self.threadID))
		startTime = time.time()
		runSim(self.threadID, self.params, self.paramsToWrite)
		endTime = time.time()
		print('[END] Thread ' + str(self.threadID) + ' ' + str(endTime - startTime) + ' seconds')
		threadLimiter.release()


# Print iterations progress
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
	iteration   - Required  : current iteration (Int)
	total       - Required  : total iterations (Int)
	prefix      - Optional  : prefix string (Str)
	suffix      - Optional  : suffix string (Str)
	decimals    - Optional  : positive number of decimals in percent complete (Int)
	length      - Optional  : character length of bar (Int)
	fill        - Optional  : bar fill character (Str)
	printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
	# Print New Line on Complete
	if iteration == total: 
		print()
        
        
def getRate(service_time_list):
	return [1/x if x > 0 else 'Infinity' for x in service_time_list]


def generateFileNames(sourcefile, thID):
	tmp = sourcefile.split('.')
	newfile = tmp[0] + '_' + str(thID) + '.' + tmp[2] #Remove "placeholder" from the name
	resultname = tmp[0] + '_' + str(thID) + '.' + tmp[2] + '-result.jsim'
	targetname = tmp[0] + '_collectResults.csv'
	return newfile, resultname, targetname


def replace_placeholder(sourcefile, targetfile, plcList, subList):
	with open(sourcefile, 'r') as f:
		newText = f.read()
		for plc, sub in zip(plcList, subList):
			newText = newText.replace(str(plc), str(sub))

	with open(targetfile, "w") as f:
	    f.write(newText)


def collectResults(filename, targetname, params):
	tree = et.parse(filename)
	root = tree.getroot()
	nextLine = ''
	for p in params:
		nextLine += str(p)
		nextLine += ','
	for l in collectList:
		dictAttrib = root.findall('.//measure[@measureType="'+str(l[0])+'"][@class="'+str(l[1])+'"][@station="'+str(l[2])+'"]')[0].attrib
		nextLine = nextLine + dictAttrib['meanValue'] + ',' + dictAttrib['lowerLimit'] + ',' + dictAttrib['upperLimit'] + ','
	nextLine = nextLine[:-1] #Remove the last comma
	with open(targetname, 'a') as f:
		if os.stat(targetname).st_size == 0:
			f.write(ATTRIBUTE_STR + '\n')
		f.write(nextLine + '\n')
		

#def getParamsToWrite(params):
#	for i in [0, 1] + list(range(5,19,1)):
#		if params[i] != 'Infinity':
#			params[i] = 1/params[i]
#		else:
#			params[i] = 0
#	return params
	
		
def runSim(thID, params, paramsToWrite):
	newfile, resultname, targetname = generateFileNames(SOURCEFILE, thID)
	replace_placeholder(SOURCEFILE, newfile, ['VAL'+str(i).zfill(2) for i in range(len(params))], params)
	rndSeed = str(random.randint(0, sys.maxsize)) #Random seed for the simulation
	cmd = 'java -cp ' + JMTPATH + ' jmt.commandline.Jmt sim ' + newfile + ' -seed ' + rndSeed + ' -maxtime ' + str(MAXTIME)
	os.popen(cmd).read()
#	paramsToWrite = getParamsToWrite(params)
	threadLock.acquire() #Only one thread at a time can collect results
	collectResults(resultname, targetname, paramsToWrite)
	threadLock.release() #Free lock to release next thread
	os.popen('rm ' + newfile + ' ' + resultname)		
#####################################
###### STOP: Utility functions ######
#####################################



###### Change all the service (or arrival) times to rates
rate_door_open = getRate(S_DOOR_OPEN)
rate_reqA = getRate(A_REQA)
rate_reqA_door = getRate(S_REQA_DOOR)
rate_reqA_fwd = getRate(S_REQA_FWD)
rate_reqA_back1 = getRate(S_REQA_BACK1)
rate_reqA_back2 = getRate(S_REQA_BACK2)
rate_reqA_back3 = getRate(S_REQA_BACK3)
rate_reqA_around = getRate(S_REQA_AROUND)
rate_reqB = getRate(A_REQB)
rate_reqB_door = getRate(S_REQB_DOOR)
rate_reqB_fwd = getRate(S_REQB_FWD)
rate_reqB_back = getRate(S_REQB_BACK)
rate_reqB_around = getRate(S_REQB_AROUND)
rate_robot_door = getRate(S_ROBOT_DOOR)
rate_robot_fwd = getRate(S_ROBOT_FWD)
rate_robot_back1 = getRate(S_ROBOT_BACK1)
rate_robot_back2 = getRate(S_ROBOT_BACK2)
rate_robot_back3 = getRate(S_ROBOT_BACK3)
rate_robot_around = getRate(S_ROBOT_AROUND)
rate_changePolicy = getRate(S_CHANGE_POLICY)
rate_think_time = getRate(Z_ROBOT)
rate_comm_same = getRate(COMM_SAME_ROOM)


threadLock = threading.Lock() #Define thredLock variable
threadLimiter = threading.BoundedSemaphore(MAXTHREADS) #Limit the number of threads running concurrently
thID = 0
threads = []
#Configurations are specified with rates
allConfigList = list(itertools.product(rate_reqA, rate_reqB, AVAIL_ROBOT, REQA_ROBOT, REQB_ROBOT, rate_door_open, rate_reqA_door, rate_reqA_fwd, rate_reqA_back1, rate_reqA_around, rate_reqB_door, rate_reqB_fwd, rate_reqB_back, rate_reqB_around, rate_robot_door, rate_robot_fwd, rate_robot_back3, rate_robot_around, rate_changePolicy, PROB_REQA, rate_think_time, rate_comm_same, rate_reqA_back2, rate_reqA_back3, rate_robot_back2, rate_robot_back1))
#Parameters to write are specified with average time
configsToWrite = list(itertools.product(A_REQA, A_REQB, AVAIL_ROBOT, REQA_ROBOT, REQB_ROBOT, S_DOOR_OPEN, S_REQA_DOOR, S_REQA_FWD, S_REQA_BACK1, S_REQA_AROUND, S_REQB_DOOR, S_REQB_FWD, S_REQB_BACK, S_REQB_AROUND, S_ROBOT_DOOR, S_ROBOT_FWD, S_ROBOT_BACK3, S_ROBOT_AROUND, S_CHANGE_POLICY, PROB_REQA, Z_ROBOT, COMM_SAME_ROOM, S_REQA_BACK2, S_REQA_BACK3, S_ROBOT_BACK2, S_ROBOT_BACK1))
total = len(allConfigList)
for params, paramsToWrite in zip(allConfigList, configsToWrite):
	paramsToWrite = paramsToWrite[:6] + (DOOR_PERIOD-paramsToWrite[5],) + paramsToWrite[6:]
	params = params[:6] + (1/paramsToWrite[6],) + params[6:]
	paramsToWrite = paramsToWrite[:21] + (1-paramsToWrite[20],) + paramsToWrite[21:]
	params = params[:21] + (paramsToWrite[21],) + params[21:]
	threads.append(MyThread(thID, params, paramsToWrite))
	thID += 1
	#printProgressBar(count, total, prefix = 'Simulating', suffix = 'Completed', length = 50)

#Start all threads
for th in threads:
	th.start()
	
#Sync all threads
for th in threads:
	th.join()
	
if not os.path.isdir(RESULTS_DIR):
	os.popen('mkdir ' + RESULTS_DIR)
	os.popen('sleep 3') #TODO: Fix this, it should wait the previous operation to complete, not sleep like this
_, _, fileToMove = generateFileNames(SOURCEFILE, -1)
os.popen('mv ' + fileToMove + ' ' + RESULTS_DIR)
