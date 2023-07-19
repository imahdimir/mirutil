"""


    """

import time

def time_a_feeded_function(func) :
    # Start timer
    start_time = time.time()

    # Code to be timed
    func()

    # End timer
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: " , elapsed_time)
