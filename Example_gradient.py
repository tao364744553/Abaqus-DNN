
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
d_U_D=[]

#open odb file
odb=['']
odb[0] = visualization.openOdb('Job-1.odb')
a = odb[0].steps['Step-1'].frames[-1]

#define the gradient name in the odb file
gradient_name_total = []
for int_point in range(number_integration_points):
	for index in range(number_variables):
		tmp = index_variables[index]
		gradient_name = 'd_U_D' + '_' +str(int_point) + '_' + str(tmp)
		gradient_name_total.append(gradient_name)

		
#access gradient
start = timeit.default_timer()

d_U_D_tmp = [a.fieldOutputs[gradient_name].getSubset(position=NODAL).values for gradient_name in gradient_name_total]
d_U_D = [d_U_D_tmp[field][node].data for node in observation_points for field in range(number_integration_points*number_variables)]
d_U_D = np.reshape(d_U_D, (observation_size,-1, number_U_direction))

#compute time cost
stop = timeit.default_timer()
time_count = stop - start
print(time_count)
