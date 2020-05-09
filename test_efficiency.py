#import necessary modules
from abaqus import *
from abaqusConstants import *
import visualization
import numpy as np
import timeit

#model information
number_integration_points = 98
number_U_direction = 2
observation_points =  list(range(0,231))
del_indices = [0, 21, 42, 63, 84, 105, 126, 147, 168, 188, 210]
observation_points = [i for j, i in enumerate(observation_points) if j not in del_indices]
observation_points = observation_points[0:-1:40]
observation_size = np.size(observation_points)
number_variables = 4
index_variables = [11,12,22,44]

#define the container for the fields outputs
disp=[]
stress = []
strain = []
d_U_D=[]

a = odb[0].steps['Step-1'].frames[-1]

#least efficient style to access displacement 
start = timeit.default_timer()
for obs_opoint in observation_points:
	disp_tmp = a.fieldOutputs['U'].getSubset(position=NODAL).values[obs_opoint].data 
	disp.append(disp_tmp)

stop = timeit.default_timer()
time_count = stop - start
print(time_count)

#intemediate efficient style to access displacement 
start = timeit.default_timer()
disp_tmp = 	a.fieldOutputs['U'].getSubset(position=NODAL).values
for obs_opoint in observation_points:
    disp_tmp1 = disp_tmp[obs_opoint].data
    disp.append(disp_tmp1)

stop = timeit.default_timer()
time_count = stop - start
print(time_count) 

#Most efficient style to access displacement 
start = timeit.default_timer()
disp_tmp = a.fieldOutputs['U'].getSubset(position=NODAL).values
disp = [disp_tmp[obs_opoint].data for obs_opoint in observation_points]
stop = timeit.default_timer()
time_count = stop - start
print(time_count)

