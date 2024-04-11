import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import time

import KOM2731_functions as f
import serial_read


serial_read.openport()
step = 0
increasing = []
decreasing = []
true_output = []

load_unit_weight = int(input("load unit weight : "))
load_unit_quantity = int(input("load unit quantity : "))
starting_load = 0

#weight is added,step by step
while step < load_unit_quantity + 1:
    #without any weight
    if step == 0:
        print("You are calculating 'increasing' please make sure no weight is present at first step.")
        input("press any key after step is done.\n")
        increasing.append({"load":0,"increasing":serial_read.read()})
    #with weight
    else:
        print("You are calculating 'increasing' please add one weight unit.")
        input("press any key after step is done.\n")
        increasing.append({"load":increasing[step-1]["load"]+load_unit_weight,"increasing":serial_read.read()})
    step += 1

step = 0

while step < load_unit_quantity + 1:
    #with all the weights
    if step == 0:
        print("You are calculating 'decreasing' please make sure all available weight is present at first step.")
        input("press any key after step is done.\n")
        decreasing.append({"load":load_unit_quantity*load_unit_weight,"decreasing":serial_read.read()})
    #with weight
    else:
        print("You are calculating 'decreasing' please remove one weight unit.")
        input("press any key after step is done.\n")
        decreasing.append({"load":decreasing[step-1]["load"]-load_unit_weight,"decreasing":serial_read.read()})
    step += 1

#Decreasing list begins at max load,we have to reverse it
decreasing=decreasing[::-1]

#Combines increasing and decreasing lists into a single lists
increasing_decreasing = increasing
for n in range(len(increasing_decreasing)):
    increasing_decreasing[n]["decreasing"] = decreasing[n]["decreasing"]

fso = f.fso(increasing_decreasing)
hysteresis = [{"load": n["load"],"hysteresis":f.hysteresis(n["increasing"],n["decreasing"],fso)} for n in increasing_decreasing]

voltage_per_unit = 7 #idk
true_and_actual_output = [{"load": n["load"],"true_output":voltage_per_unit*n["load"],"actual_output":n["increasing"]} for n in increasing_decreasing]

error = [{"load": n["load"],"error":f.error(n["actual_output"],n["true_output"])} for n in true_and_actual_output]

reading = [{"load": true_and_actual_output[n]["load"],"reading":f.reading(error[n]["error"],true_and_actual_output[n]["true_output"])} for n in range(len(true_and_actual_output))]

ee_range = fso
span = f.range_to_spam(ee_range)

linearity = [{"load":n["load"],"linearity":f.linearity(n["error"],fso)} for n in error]

error_without_load = [n["error"] for n in error]
worst_case_error = [{"load":error[n]["load"],"worst_case_error": f.worst_case_error(error_without_load[:n+1])}for n in range(len(error))]
root_of_sum_square = [{"load":error[n]["load"],"root_of_sum_square": f.root_of_sum_square(error_without_load[:n+1])}for n in range(len(error))]



fig, axs = plt.subplots(3, 2,figsize=(16,10))
plt.subplots_adjust(hspace=0.5)

increasing_decreasing_df=pd.DataFrame(increasing_decreasing)
axs[0,0].plot(increasing_decreasing_df["load"],increasing_decreasing_df["increasing"],color="blue",label="Increasing")
axs[0,0].plot(increasing_decreasing_df["load"],increasing_decreasing_df["decreasing"],color="red",label="Decreasing")
axs[0,0].set_xticks(increasing_decreasing_df["load"])
axs[0,0].set_xlabel("Load")
axs[0,0].set_ylabel("Voltage")
axs[0,0].set_title("Increasing/Decreasing")
axs[0,0].legend()


hysteresis_df=pd.DataFrame(hysteresis)
axs[0,1].plot(hysteresis_df["load"],hysteresis_df["hysteresis"],color="green",label="Hysteresis")
axs[0,1].set_xticks(hysteresis_df["load"])
axs[0,1].set_xlabel("Load")
axs[0,1].set_ylabel("%FSO")
axs[0,1].set_title("Hysteresis")
axs[0,1].legend()

linearity_df=pd.DataFrame(linearity)
axs[1,0].plot(linearity_df["load"],linearity_df["linearity"],color="purple",label="Linearity")
axs[1,0].set_xticks(linearity_df["load"])
axs[1,0].set_xlabel("Load")
axs[1,0].set_ylabel("%FSO")
axs[1,0].set_title("linearity")
axs[1,0].legend()

true_and_actual_output_df=pd.DataFrame(true_and_actual_output)
axs[1,1].plot(true_and_actual_output_df["load"],true_and_actual_output_df["actual_output"],color="orange",label="Actual Output")
axs[1,1].plot(true_and_actual_output_df["load"],true_and_actual_output_df["true_output"],color="black",label="True Output")
axs[1,1].set_xticks(true_and_actual_output_df["load"])
axs[1,1].set_xlabel("Load")
axs[1,1].set_ylabel("Voltage")
axs[1,1].set_title("True/Actual Output")
axs[1,1].legend()

reading_df=pd.DataFrame(reading)
axs[2,0].plot(reading_df["load"],reading_df["reading"],color="cyan",label="Reading")
axs[2,0].set_xticks(reading_df["load"])
axs[2,0].set_xlabel("Load")
axs[2,0].set_ylabel("Reading")
axs[2,0].set_title("Reading")
axs[2,0].legend()

worst_case_error_df=pd.DataFrame(worst_case_error)
root_of_sum_square_df=pd.DataFrame(root_of_sum_square)
axs[2,1].plot(worst_case_error_df["load"],worst_case_error_df["worst_case_error"],color="yellow",label="Worst Case Error")
axs[2,1].plot(worst_case_error_df["load"],root_of_sum_square_df["root_of_sum_square"],color="blue",label="Root of Sum Square")
axs[2,1].set_xticks(worst_case_error_df["load"])
axs[2,1].set_xlabel("Load")
axs[2,1].set_ylabel("Error")
axs[2,1].set_title("Worst Case Error/Root of Sum Square")
axs[2,1].legend()


plt.suptitle("Calibration Graphs")
plt.show()

increasing_decreasing_df.to_excel("increasing_decreasing.xlsx", index=False)
hysteresis_df.to_excel("hysteresis.xlsx", index=False)
linearity_df.to_excel("linearity.xlsx", index=False)
true_and_actual_output_df.to_excel("true_actual_output.xlsx", index=False)
reading_df.to_excel("reading.xlsx", index=False)
worst_case_error_df.to_excel("worst_case_error.xlsx", index=False)
root_of_sum_square_df.to_excel("root_of_sum_square.xlsx", index=False)















