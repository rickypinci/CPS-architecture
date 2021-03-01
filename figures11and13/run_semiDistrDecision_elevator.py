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
PATTERNNAME = 'semiDistrDecision_stairsElevator'
TEST_NAME = 'varArrivals'
MODEL_NAME = 'slidingDoor'
#JMTPATH = '~/JMT/JMT-1.0.5.jar'
#MAXTIME = 600
#MAXTHREADS = 10
if PATTERNNAME != '':
	PATTERNNAME = '_' + PATTERNNAME
SOURCEFILE = MODEL_NAME + PATTERNNAME + '.placeholder.jsimg'
if TEST_NAME != '':
	RESULTS_DIR = 'results/stairs_elevator/' + MODEL_NAME + PATTERNNAME + '_' + TEST_NAME + '/'
else:
	RESULTS_DIR = 'results/stairs_elevator/' + MODEL_NAME + PATTERNNAME + '_' + str(int(time.time())) + '/'
PARAM_NAME = [
'A_reqA',
'A_reqB',
'N_robot_legs',
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
'N_robot_wheels',
'S_elevator_changeFloor',
'S_reqA_climb1',
'S_reqA_climb2',
'S_reqA_unclimb',
'elevator_capacity',
'S_robot_climb1',
'S_robot_climb2',
'S_robot_unclimb',
]
INDEX_NAME_TMP = [
'R_legs_choosing1_A',
'R_legs_reachDoor1_A',
'R_legs_driveThru1_A',
'R_legs_driveFwd1_A',
'R_legs_driveBack1_A',
'R_legs_driveAround1_A',
'R_legs_communicate1_A',
'R_legs_choosing1_B',
'R_legs_reachDoor1_B',
'R_legs_driveThru1_B',
'R_legs_driveFwd1_B',
'R_legs_driveBack1_B',
'R_legs_driveAround1_B',
'R_legs_communicate1_B',
'X_legs_goFast1_A',
'X_legs_success1_A',
'X_legs_fail1_A',
'X_legs_goFast1_B',
'X_legs_success1_B',
'X_legs_fail1_B',
'R_legs_choosing2_A',
'R_legs_startClimbing2_A',
'R_legs_obstacles?2_A',
'R_legs_keepClimbing2_A',
'R_legs_goBack2_A',
'R_legs_communicate2_A',
'R_legs_boarding2_A',
'R_legs_onBoard2_A',
'R_legs_choosing2_B',
'R_legs_startClimbing2_B',
'R_legs_obstacles?2_B',
'R_legs_keepClimbing2_B',
'R_legs_goBack2_B',
'R_legs_communicate2_B',
'R_legs_boarding2_B',
'R_legs_onBoard2_B',
'X_legs_stairs2_A',
'X_legs_elevator2_A',
'X_legs_success2_A',
'X_legs_fail2_A',
'X_legs_stairs2_B',
'X_legs_elevator2_B',
'X_legs_success2_B',
'X_legs_fail2_B',
'X_legs_follow1_A',
'X_legs_follow1_B',
'X_legs_follow2_A',
'X_legs_follow2_B',
'R_wheels_choosing1_A',
'R_wheels_reachDoor1_A',
'R_wheels_driveThru1_A',
'R_wheels_driveFwd1_A',
'R_wheels_driveBack1_A',
'R_wheels_driveAround1_A',
'R_wheels_communicate1_A',
'R_wheels_choosing1_B',
'R_wheels_reachDoor1_B',
'R_wheels_driveThru1_B',
'R_wheels_driveFwd1_B',
'R_wheels_driveBack1_B',
'R_wheels_driveAround1_B',
'R_wheels_communicate1_B',
'X_wheels_goFast1_A',
'X_wheels_success1_A',
'X_wheels_fail1_A',
'X_wheels_goFast1_B',
'X_wheels_success1_B',
'X_wheels_fail1_B',
'R_wheels_choosing2_A',
'R_wheels_startClimbing2_A',
'R_wheels_obstacles?2_A',
'R_wheels_keepClimbing2_A',
'R_wheels_goBack2_A',
'R_wheels_communicate2_A',
'R_wheels_boarding2_A',
'R_wheels_onBoard2_A',
'R_wheels_choosing2_B',
'R_wheels_startClimbing2_B',
'R_wheels_obstacles?2_B',
'R_wheels_keepClimbing2_B',
'R_wheels_goBack2_B',
'R_wheels_communicate2_B',
'R_wheels_boarding2_B',
'R_wheels_onBoard2_B',
'X_wheels_stairs2_A',
'X_wheels_elevator2_A',
'X_wheels_success2_A',
'X_wheels_fail2_A',
'X_wheels_stairs2_B',
'X_wheels_elevator2_B',
'X_wheels_success2_B',
'X_wheels_fail2_B',
'X_wheels_follow1_A',
'X_wheels_follow1_B',
'X_wheels_follow2_A',
'X_wheels_follow2_B',
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
AVAIL_ROBOT = 100 #N
ROBOT_WITH_LEGS = list(range(0,100+1,10)) #N_two_legged
# PERC_ROBOT_WHEELS is obtained as 1 - PERC_ROBOT_LEGS
REQA_ROBOT = [1] #NOT REQUIRED
REQB_ROBOT = [1] #NOT REQUIRED
###### Door and Stairs parameters ######
DOOR_PERIOD = 60 #mu_switch-A-U + mu_switch-U-A
S_DOOR_OPEN = [55] #mu_switch-A-U
# S_DOOR_CLOSE is obtained as 60 - S_DOOR_OPEN
S_CHANGE_POLICY = [300] #NOT REQURIED
###### Elevator parameters ######
ELEV_CAPACITY = [20] #K
S_ELEV_MOVE = [15] #mu_moving = mu_empty
###### Communication Cost ######
COMM_SAME_ROOM = [1] #mu_follow
###### Arrival rates for classes reqA and reqB ######
A_REQA = [30] #NOT REQUIRED
A_REQB = [30] #NOT REQUIRED
PROB_REQA = [0.1] #NOT REQUIRED
###### reqA and reqB service times at different stations ######
Z_ROBOT = [10] #mu_wait
S_REQA_DOOR = [5] #mu_reach_door_F
S_REQA_FWD = [5] #mu_goStraight_door_F
S_REQA_BACK1 = [5] #mu_turn_door_F
S_REQA_BACK2 = [5] #NOT REQUIRED
S_REQA_BACK3 = [5] #NOT REQUIRED
S_REQA_AROUND = [15] #mu_goAround_door_F
S_REQA_CLIMB1 = [15] #mu_reach_stairs_F
S_REQA_CLIMB2 = [15] #mu_goStraight_stairs_F
S_REQA_UNCLIMB = [15] #mu_turn_stairs_F
S_REQB_DOOR = [5] #NOT REQUIRED
S_REQB_FWD = [5] #NOT REQUIRED
S_REQB_BACK = [5] #NOT REQUIRED
S_REQB_AROUND = [40] #NOT REQUIRED
S_ROBOT_DOOR = [5] #mu_reach_door_B
S_ROBOT_FWD = [5] #mu_goStright_door_B
S_ROBOT_BACK1 = [25] #mu_turn_door_B
S_ROBOT_BACK2 = [15] #NOT REQUIRED
S_ROBOT_BACK3 = [5] #NOT REQUIRED
S_ROBOT_AROUND = [40] #mu_goAround_door_B
S_ROBOT_CLIMB1 = [15] #mu_reach_stairs_B
S_ROBOT_CLIMB2 = [15] #mu_goStraight_stairs_B
S_ROBOT_UNCLIMB = [15] #mu_turn_stairs_B
#####################################################################################
#####################################################################################
############################ STOP: Simulation parameters ############################
#####################################################################################
#####################################################################################


###### List for collecting measures. This must be specified following the order of INDEX_NAME_TMP. ['type', 'referenceUserClass', 'station'] ######
collectList = [
['Response Time', 'robotLegs', 'choosing1_A'],
['Response Time', 'robotLegs', 'reachDoor1_A'],
['Response Time', 'robotLegs', 'driveThru1_A'],
['Response Time', 'robotLegs', 'goFwd1_A'],
['Response Time', 'robotLegs', 'goBack1_A'],
['Response Time', 'robotLegs', 'goAround1_A'],
['Response Time', 'robotLegs', 'sayClose1_A'],
['Response Time', 'robotLegs', 'choosing1_B'],
['Response Time', 'robotLegs', 'reachDoor1_B'],
['Response Time', 'robotLegs', 'driveThru1_B'],
['Response Time', 'robotLegs', 'goFwd1_B'],
['Response Time', 'robotLegs', 'goBack1_B'],
['Response Time', 'robotLegs', 'goAround1_B'],
['Response Time', 'robotLegs', 'sayClose1_B'],
['Throughput', 'robotLegs', 'ifOpen1_A'],
['Throughput', 'robotLegs', 'success1_A'],
['Throughput', 'robotLegs', 'fail1_A'],
['Throughput', 'robotLegs', 'ifOpen1_B'],
['Throughput', 'robotLegs', 'success1_B'],
['Throughput', 'robotLegs', 'fail1_B'],
['Response Time', 'robotLegs', 'choosing2_A'],
['Response Time', 'robotLegs', 'startClimbing2_A'],
['Response Time', 'robotLegs', 'obstacles?2_A'],
['Response Time', 'robotLegs', 'keepClimbing2_A'],
['Response Time', 'robotLegs', 'goBack2_A'],
['Response Time', 'robotLegs', 'sayClose2_A'],
['Response Time', 'robotLegs', 'boarding2_A'],
['Response Time', 'robotLegs', 'onBoard2_A'],
['Response Time', 'robotLegs', 'choosing2_B'],
['Response Time', 'robotLegs', 'startClimbing2_B'],
['Response Time', 'robotLegs', 'obstacles?2_B'],
['Response Time', 'robotLegs', 'keepClimbing2_B'],
['Response Time', 'robotLegs', 'goBack2_B'],
['Response Time', 'robotLegs', 'sayClose2_B'],
['Response Time', 'robotLegs', 'boarding2_B'],
['Response Time', 'robotLegs', 'onBoard2_B'],
['Throughput', 'robotLegs', 'stairs2_A'],
['Throughput', 'robotLegs', 'elevator2_A'],
['Throughput', 'robotLegs', 'no2_A'],
['Throughput', 'robotLegs', 'yes2_A'],
['Throughput', 'robotLegs', 'stairs2_B'],
['Throughput', 'robotLegs', 'elevator2_B'],
['Throughput', 'robotLegs', 'no2_B'],
['Throughput', 'robotLegs', 'yes2_B'],
['Throughput', 'robotTkL', 'followTheLeader1_A'],
['Throughput', 'robotTkL', 'followTheLeader1_B'],
['Throughput', 'robotTkL', 'followTheLeader2_A'],
['Throughput', 'robotTkL', 'followTheLeader2_B'],
['Response Time', 'robotWheels', 'choosing1_A'],
['Response Time', 'robotWheels', 'reachDoor1_A'],
['Response Time', 'robotWheels', 'driveThru1_A'],
['Response Time', 'robotWheels', 'goFwd1_A'],
['Response Time', 'robotWheels', 'goBack1_A'],
['Response Time', 'robotWheels', 'goAround1_A'],
['Response Time', 'robotWheels', 'sayClose1_A'],
['Response Time', 'robotWheels', 'choosing1_B'],
['Response Time', 'robotWheels', 'reachDoor1_B'],
['Response Time', 'robotWheels', 'driveThru1_B'],
['Response Time', 'robotWheels', 'goFwd1_B'],
['Response Time', 'robotWheels', 'goBack1_B'],
['Response Time', 'robotWheels', 'goAround1_B'],
['Response Time', 'robotWheels', 'sayClose1_B'],
['Throughput', 'robotWheels', 'ifOpen1_A'],
['Throughput', 'robotWheels', 'success1_A'],
['Throughput', 'robotWheels', 'fail1_A'],
['Throughput', 'robotWheels', 'ifOpen1_B'],
['Throughput', 'robotWheels', 'success1_B'],
['Throughput', 'robotWheels', 'fail1_B'],
['Response Time', 'robotWheels', 'choosing2_A'],
['Response Time', 'robotWheels', 'startClimbing2_A'],
['Response Time', 'robotWheels', 'obstacles?2_A'],
['Response Time', 'robotWheels', 'keepClimbing2_A'],
['Response Time', 'robotWheels', 'goBack2_A'],
['Response Time', 'robotWheels', 'sayClose2_A'],
['Response Time', 'robotWheels', 'boarding2_A'],
['Response Time', 'robotWheels', 'onBoard2_A'],
['Response Time', 'robotWheels', 'choosing2_B'],
['Response Time', 'robotWheels', 'startClimbing2_B'],
['Response Time', 'robotWheels', 'obstacles?2_B'],
['Response Time', 'robotWheels', 'keepClimbing2_B'],
['Response Time', 'robotWheels', 'goBack2_B'],
['Response Time', 'robotWheels', 'sayClose2_B'],
['Response Time', 'robotWheels', 'boarding2_B'],
['Response Time', 'robotWheels', 'onBoard2_B'],
['Throughput', 'robotWheels', 'stairs2_A'],
['Throughput', 'robotWheels', 'elevator2_A'],
['Throughput', 'robotWheels', 'no2_A'],
['Throughput', 'robotWheels', 'yes2_A'],
['Throughput', 'robotWheels', 'stairs2_B'],
['Throughput', 'robotWheels', 'elevator2_B'],
['Throughput', 'robotWheels', 'no2_B'],
['Throughput', 'robotWheels', 'yes2_B'],
['Throughput', 'robotTkW', 'followTheLeader1_A'],
['Throughput', 'robotTkW', 'followTheLeader1_B'],
['Throughput', 'robotTkW', 'followTheLeader2_A'],
['Throughput', 'robotTkW', 'followTheLeader2_B'],
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
rate_elevator_move = getRate(S_ELEV_MOVE)
rate_reqA = getRate(A_REQA)
rate_reqA_door = getRate(S_REQA_DOOR)
rate_reqA_fwd = getRate(S_REQA_FWD)
rate_reqA_back1 = getRate(S_REQA_BACK1)
rate_reqA_back2 = getRate(S_REQA_BACK2)
rate_reqA_back3 = getRate(S_REQA_BACK3)
rate_reqA_around = getRate(S_REQA_AROUND)
rate_reqA_climb1 = getRate(S_REQA_CLIMB1)
rate_reqA_climb2 = getRate(S_REQA_CLIMB2)
rate_reqA_unclimb = getRate(S_REQA_UNCLIMB)
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
rate_robot_climb1 = getRate(S_ROBOT_CLIMB1)
rate_robot_climb2 = getRate(S_ROBOT_CLIMB2)
rate_robot_unclimb = getRate(S_ROBOT_UNCLIMB)
rate_changePolicy = getRate(S_CHANGE_POLICY)
rate_think_time = getRate(Z_ROBOT)
rate_comm_same = getRate(COMM_SAME_ROOM)


threadLock = threading.Lock() #Define thredLock variable
threadLimiter = threading.BoundedSemaphore(MAXTHREADS) #Limit the number of threads running concurrently
thID = 0
threads = []
#Configurations are specified with rates
allConfigList = list(itertools.product(rate_reqA, rate_reqB, ROBOT_WITH_LEGS, REQA_ROBOT, REQB_ROBOT, rate_door_open, rate_reqA_door, rate_reqA_fwd, rate_reqA_back1, rate_reqA_around, rate_reqB_door, rate_reqB_fwd, rate_reqB_back, rate_reqB_around, rate_robot_door, rate_robot_fwd, rate_robot_back3, rate_robot_around, rate_changePolicy, PROB_REQA, rate_think_time, rate_comm_same, rate_reqA_back2, rate_reqA_back3, rate_robot_back2, rate_robot_back1, rate_elevator_move, rate_reqA_climb1, rate_reqA_climb2, rate_reqA_unclimb, ELEV_CAPACITY, rate_robot_climb1, rate_robot_climb2, rate_robot_unclimb))
#Parameters to write are specified with average time
configsToWrite = list(itertools.product(A_REQA, A_REQB, ROBOT_WITH_LEGS, REQA_ROBOT, REQB_ROBOT, S_DOOR_OPEN, S_REQA_DOOR, S_REQA_FWD, S_REQA_BACK1, S_REQA_AROUND, S_REQB_DOOR, S_REQB_FWD, S_REQB_BACK, S_REQB_AROUND, S_ROBOT_DOOR, S_ROBOT_FWD, S_ROBOT_BACK3, S_ROBOT_AROUND, S_CHANGE_POLICY, PROB_REQA, Z_ROBOT, COMM_SAME_ROOM, S_REQA_BACK2, S_REQA_BACK3, S_ROBOT_BACK2, S_ROBOT_BACK1, S_ELEV_MOVE, S_REQA_CLIMB1, S_REQA_CLIMB2, S_REQA_UNCLIMB, ELEV_CAPACITY, S_ROBOT_CLIMB1, S_ROBOT_CLIMB2, S_ROBOT_UNCLIMB))
total = len(allConfigList)
for params, paramsToWrite in zip(allConfigList, configsToWrite):
	paramsToWrite = paramsToWrite[:6] + (DOOR_PERIOD-paramsToWrite[5],) + paramsToWrite[6:]
	params = params[:6] + (1/paramsToWrite[6],) + params[6:]
	paramsToWrite = paramsToWrite[:21] + (1-paramsToWrite[20],) + paramsToWrite[21:]
	params = params[:21] + (paramsToWrite[21],) + params[21:]
	paramsToWrite = paramsToWrite[:28] + (AVAIL_ROBOT-paramsToWrite[2],) + paramsToWrite[28:]
	params = params[:28] + (paramsToWrite[28],) + params[28:]
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
