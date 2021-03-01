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
PATTERNNAME = 'centralizedDecision'
TEST_NAME = 'varChangePolicy'
MODEL_NAME = 'slidingDoor'
#JMTPATH = '~/JMT/JMT-1.0.5.jar'
#MAXTIME = 600
#MAXTHREADS = 10
if PATTERNNAME != '':
	PATTERNNAME = '_' + PATTERNNAME
SOURCEFILE = MODEL_NAME + PATTERNNAME + '.placeholder.jsimg'
if TEST_NAME != '':
	RESULTS_DIR = 'results/' + MODEL_NAME + PATTERNNAME + '_' + TEST_NAME + '/'
else:
	RESULTS_DIR = 'results/' + MODEL_NAME + PATTERNNAME + '_' + str(int(time.time())) + '/'
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
'S_reqA_driveBack',
'S_reqA_driveAround',
'S_reqB_driveToDoor',
'S_reqB_driveFwd',
'S_reqB_driveBack',
'S_reqB_driveAround',
'S_robot_driveToDoor',
'S_robot_driveFwd',
'S_robot_driveBack',
'S_robot_driveAround',
'S_changePolicyToOpen',
'probA',
'probB',
'Z_robot',
'comm_same_room',
]
INDEX_NAME_TMP = [
'R_robot_choosing',
'R_robot_reachDoor_A',
'R_robot_driveThru_A',
'R_robot_driveFwd_A',
'R_robot_driveBack_A',
'R_robot_driveAround_A',
'R_robot_delivered',
'R_robot_reachDoor_R',
'R_robot_driveThru_R',
'R_robot_driveFwd_R',
'R_robot_driveBack_R',
'R_robot_driveAround_R',
'X_robot_goFast_A',
'X_robot_goSlow_A',
'X_robot_success_A',
'X_robot_fail_A',
'X_robot_goFast_R',
'X_robot_goSlow_R',
'X_robot_success_R',
'X_robot_fail_R',
'N_robot_avail'
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
AVAIL_ROBOT = [100] #N
REQA_ROBOT = [1] #NOT REQUIRED
REQB_ROBOT = [1] #NOT REQUIRED
###### Door parameters ######
DOOR_PERIOD = 60 #mu_switch-A-U + mu_switch-U-A
S_DOOR_OPEN = [1] + list(range(5,55+1,5)) + [59] #mu_switch-A-U
# S_DOOR_CLOSE is obtained as 60 - S_DOOR_OPEN
S_CHANGE_POLICY = [300] #mu_refresh
###### Communication Cost ######
COMM_SAME_ROOM = [1] #mu_fail = mu_ask
###### Arrival rates for classes reqA and reqB ######
A_REQA = [30] #NOT REQUIRED
A_REQB = [30] #NOT REQUIRED
PROB_REQA = [0.1] #NOT REQUIRED
###### reqA and reqB service times at different stations ######
Z_ROBOT = [1] #mu_wait
S_REQA_DOOR = [9] #mu_reach_F
S_REQA_FWD = [9] #mu_goStraight_F
S_REQA_BACK = [9] #mu_turn_F
S_REQA_AROUND = [27] #mu_goAround_F
S_REQB_DOOR = [9] #NOT REQUIRED
S_REQB_FWD = [9] #NOT REQUIRED
S_REQB_BACK = [9] #NOT REQUIRED
S_REQB_AROUND = [27] #NOT REQUIRED
S_ROBOT_DOOR = [1] #mu_reach_B
S_ROBOT_FWD = [1] #mu_goStraight_B
S_ROBOT_BACK = [1] #mu_turn_B
S_ROBOT_AROUND = [3] #mu_goAround_B
#####################################################################################
#####################################################################################
############################ STOP: Simulation parameters ############################
#####################################################################################
#####################################################################################



###### List for collecting measures. This must be specified following the order of INDEX_NAME_TMP. ['type', 'referenceUserClass', 'station'] ######
collectList = [
['Response Time', 'robot', 'choosing'],
['Response Time', 'robot', 'reachDoor 1'],
['Response Time', 'robot', 'driveThru 1'],
['Response Time', 'robot', 'goFwd 1'],
['Response Time', 'robot', 'goBack 1'],
['Response Time', 'robot', 'goAround 1'],
['Response Time', 'robot', 'delivered'],
['Response Time', 'robot', 'reachDoor 2'],
['Response Time', 'robot', 'driveThru 2'],
['Response Time', 'robot', 'goFwd 2'],
['Response Time', 'robot', 'goBack 2'],
['Response Time', 'robot', 'goAround 2'],
['Throughput', 'robot', 'ifOpen 1'],
['Throughput', 'robot', 'ifClosed 1'],
['Throughput', 'robot', 'success 1'],
['Throughput', 'robot', 'fail 1'],
['Throughput', 'robot', 'ifOpen 2'],
['Throughput', 'robot', 'ifClosed 2'],
['Throughput', 'robot', 'success 2'],
['Throughput', 'robot', 'fail 2'],
['Number of Customers', 'robot', 'availRobot']
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
		runSim(self.threadID, self.params, self.paramsToWrite)
		print('[END] Thread ' + str(self.threadID))
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
rate_reqA_back = getRate(S_REQA_BACK)
rate_reqA_around = getRate(S_REQA_AROUND)
rate_reqB = getRate(A_REQB)
rate_reqB_door = getRate(S_REQB_DOOR)
rate_reqB_fwd = getRate(S_REQB_FWD)
rate_reqB_back = getRate(S_REQB_BACK)
rate_reqB_around = getRate(S_REQB_AROUND)
rate_robot_door = getRate(S_ROBOT_DOOR)
rate_robot_fwd = getRate(S_ROBOT_FWD)
rate_robot_back = getRate(S_ROBOT_BACK)
rate_robot_around = getRate(S_ROBOT_AROUND)
rate_changePolicy = getRate(S_CHANGE_POLICY)
rate_think_time = getRate(Z_ROBOT)
rate_comm_same = getRate(COMM_SAME_ROOM)


threadLock = threading.Lock() #Define thredLock variable
threadLimiter = threading.BoundedSemaphore(MAXTHREADS) #Limit the number of threads running concurrently
thID = 0
threads = []
#Configurations are specified with rates
allConfigList = list(itertools.product(rate_reqA, rate_reqB, AVAIL_ROBOT, REQA_ROBOT, REQB_ROBOT, rate_door_open, rate_reqA_door, rate_reqA_fwd, rate_reqA_back, rate_reqA_around, rate_reqB_door, rate_reqB_fwd, rate_reqB_back, rate_reqB_around, rate_robot_door, rate_robot_fwd, rate_robot_back, rate_robot_around, rate_changePolicy, PROB_REQA, rate_think_time, rate_comm_same))
#Parameters to write are specified with average time
configsToWrite = list(itertools.product(A_REQA, A_REQB, AVAIL_ROBOT, REQA_ROBOT, REQB_ROBOT, S_DOOR_OPEN, S_REQA_DOOR, S_REQA_FWD, S_REQA_BACK, S_REQA_AROUND, S_REQB_DOOR, S_REQB_FWD, S_REQB_BACK, S_REQB_AROUND, S_ROBOT_DOOR, S_ROBOT_FWD, S_ROBOT_BACK, S_ROBOT_AROUND, S_CHANGE_POLICY, PROB_REQA, Z_ROBOT, COMM_SAME_ROOM))
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
