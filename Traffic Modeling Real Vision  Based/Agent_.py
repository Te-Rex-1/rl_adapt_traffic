from __future__ import absolute_import
from __future__ import print_function
from select import select
# import termios
import os
import sys
import optparse
import subprocess
import random
import time
import cv2
import curses

import readScreen2
import numpy as np


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def generate_routefile():
    with open("data/cross_auto.rou.xml", "w") as routes:
        print("""<routes>
    <vTypeDistribution id="mixed">
        <vType id="car" vClass="passenger" speedDev="0.2" latAlignment="compact" probability="0.3"/>
        <vType id="moped" vClass="moped" speedDev="0.4" latAlignment="compact" probability="0.7"/>
    </vTypeDistribution>
    <route id="r0" edges="51o 1i 2o 52i"/>
    <route id="r1" edges="51o 1i 4o 54i"/>
    <route id="r2" edges="51o 1i 3o 53i"/>
    <route id="r3" edges="54o 4i 3o 53i"/>
    <route id="r4" edges="54o 4i 1o 51i"/>
    <route id="r5" edges="54o 4i 2o 52i"/>
    <route id="r6" edges="52o 2i 1o 51i"/>
    <route id="r7" edges="52o 2i 4o 54i"/>
    <route id="r8" edges="52o 2i 3o 53i"/>
    <route id="r9" edges="53o 3i 4o 54i"/>
    <route id="r10" edges="53o 3i 1o 51i"/>
    <route id="r11" edges="53o 3i 2o 52i"/>
    <flow id="mixed1" begin="0" end="1500" number="150" route="r0" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed2" begin="0" end="1500" number="20" route="r1" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed3" begin="0" end="1500" number="20" route="r2" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed4" begin="0" end="1500" number="100" route="r3" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed5" begin="0" end="1500" number="20" route="r4" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed6" begin="0" end="1500" number="20" route="r5" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed7" begin="0" end="1500" number="100" route="r6" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed8" begin="0" end="1500" number="20" route="r7" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed9" begin="0" end="1500" number="20" route="r8" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed10" begin="0" end="1500" number="50" route="r9" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed11" begin="0" end="1500" number="20" route="r10" type="mixed" departLane="random" departPosLat="random"/>
    <flow id="mixed12" begin="0" end="1500" number="20" route="r11" type="mixed" departLane="random" departPosLat="random"/>
</routes>""", file=routes)
        lastVeh = 0
        vehNr = 0



try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


options = get_options()

# this script has been called from the command line. It will start sumo as a
# server, then connect and run

if options.nogui:
    sumoBinary = checkBinary('sumo')
else:
    sumoBinary = checkBinary('sumo-gui')

# first, generate the route file for this simulation

# this is the normal way of using traci. sumo is started as a
# subprocess and then the python script connects and runs


print("TraCI Started")




#State = State_Lengths()
#print(State.get_tails())

#states = State.get_tails



#runner = Runner()
#print(Runner().run)


def getState():

    #print(States_.get_tails())

    state = np.zeros((5,1))

    # state[i,0] = readScreen2.getUpperQlength()
    # state[i,1] = readScreen2.getLowerQlength()
    # state[i,2] = readScreen2.getRightQlength()
    # state[i,3] = readScreen2.getLeftQlength()
    # phase = traci.trafficlight.getPhase("0")
    # state[i,4] = phase
    state[0, 0] = readScreen2.getUpperQlength()
    state[1,0] = readScreen2.getLowerQlength()
    state[2,0] = readScreen2.getRightQlength()
    state[3,0] = readScreen2.getLeftQlength()
    phase = traci.trafficlight.getPhase("0")
    state[4,0] = phase

    #print (state)

    return state



print("here")
import traci



def makeMove(state,action):

    traci.trafficlight.setPhase("0",action)

    # agent.simulateFrames(SIM_FRAMES)
    traci.simulationStep()
    traci.simulationStep()
    traci.simulationStep()
    traci.simulationStep()
    traci.simulationStep()
    traci.simulationStep()
    traci.simulationStep()
    traci.simulationStep()
    traci.simulationStep()

    newState = getState()

    return newState

def getReward(state,new_state):
    qLengths1 = state[:4]
    qLengths2 = new_state[:4]

    q1 = np.average(qLengths1)
    q2 = np.average(qLengths2)

    if q1>=q2:
        reward = -1
    elif q1<q2:
        reward = 1



    '''
    sum = np.sum(qLengths)
    if sum>=0 and sum <65:
        reward = 100
    elif sum>64 and sum<129:
        reward = 50
    elif sum>128 and sum<193:
        reward = 0
    elif sum>192 and sum<257:
        reward = -10
    elif sum>256 and sum<321:
        reward = -20'''


    return reward



from keras.models import Sequential
from keras.models import load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop,Adam

model = Sequential()
model.add(Dense(12, input_dim=5, init='uniform', activation='relu'))
model.add(Dense(24, init='uniform', activation='relu'))
#model.add(Dense(24, init='uniform', activation='relu'))
#model.add(Dense(12, init='uniform', activation='relu'))
model.add(Dense(4, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])



#model = load_model('traffic_model.h5')
#reset weights of neural network
epochs = 50
gamma = 0.975
epsilon = 1
batchSize = 40
buffer = 80
replay = []
#stores tuples of (S, A, R, S')
h = 0
generate_routefile()
traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])
actions = [0,1,2,3]

for i in range(epochs):


    print("Now starting TraCI")
    """execute the TraCI control loop"""


    traci.trafficlight.setPhase("0", 0)
    # for i in range(100):
    #     state = np.zeros((100, 5))
    #     state = getState(i)
    # print(state)
    # state = np.zeros((100, 5))
    state = getState()
    counter = 10000
    print("EPOCH # ", i)
    while traci.simulation.getMinExpectedNumber() > 0:

        qval = model.predict(state.reshape(1,5), batch_size=1)
        if (random.random() < epsilon): #choose random action
            action = np.random.choice(actions)
        else: #choose best action from Q(s,a) values
            action = (np.argmax(qval))
        #Take action, observe new state S'
        new_state = makeMove(state, action)

        #Observe reward
        reward = getReward(state,new_state)

        #Experience replay storage
        if (len(replay) < buffer): #if buffer not filled, add to it
            replay.append((state, action, reward, new_state))
        else: #if buffer full, overwrite old values
            if (h < (buffer-1)):
                h += 1
            else:
                h = 0
            replay[h] = (state, action, reward, new_state)
            #randomly sample our experience replay memory
            minibatch = random.sample(replay, batchSize)
            X_train = []
            y_train = []
            for memory in minibatch:
                #Get max_Q(S',a)
                old_state, action, reward, new_state = memory
                old_qval = model.predict(old_state.reshape(1,5), batch_size=1)
                newQ = model.predict(new_state.reshape(1,5), batch_size=1)
                maxQ = np.max(newQ)
                y = np.zeros((1,4))#changed here
                y[:] = old_qval[:]
                update = (reward + (gamma * maxQ))
                y[0][action] = update
                X_train.append(old_state.reshape(5,))
                y_train.append(y.reshape(4,))

            X_train = np.array(X_train)
            y_train = np.array(y_train)
            print("Epoch #: %s" % (i,))
            model.fit(X_train, y_train, batch_size=batchSize, nb_epoch=1, verbose=1)
            state = new_state
        #status += 1
    if epsilon > 0.1:
        #decrement epsilon over time
        epsilon -= (1/epochs)

    #print(counter)
    model.save('traffic_model_uj3.h5')
    print("Model saved for epoch # ",i)

    traci.load(["--start","-c", "data/cross.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])

    #traci.close()
    #print("on while over ",counter)
#sys.stdout.flush()




        #getState()

    #.curses.endwin()



