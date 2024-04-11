def error(actual_output,true_output):
    return actual_output-true_output
def reading(error,true_output):
    if error == 0 or true_output == 0:
        return 0
    else:
        return error/true_output * 100
def hysteresis(increasing,decreasing,fso):
    if increasing-decreasing == 0:
        return 0
    else:
        return abs(increasing-decreasing)/fso * 100
def linearity(error,fso):
    if error == 0:
        return 0
    else:
        return error/fso*100
def zero_drift(output1,output2,temperature1,temperature2):
    return (output1-output2)/(temperature1-temperature2) * 100
def sensitivity_drift(sensitivity1,sensitivity2,temperature1,temparature2):
    return (sensitivity1-sensitivity2)/(temperature1-temparature2)
def range_to_spam(range):
    return range*2
def span_to_range(span):
    return span/2
def worst_case_error(error_list):
    sum_of_errors = 0
    for error in error_list:
        sum_of_errors += abs(error)
    return sum_of_errors
def root_of_sum_square(error_list):
    sum = 0
    for error in error_list:
        sum += error**2
    sum = sum**1/2
    return sum
def fso(increasing_decreasing):
    fso = 0
    for n in increasing_decreasing:
        if n["increasing"] > fso:
            fso = n["increasing"]
        if n["decreasing"] > fso:
            fso = n["decreasing"]
    return fso