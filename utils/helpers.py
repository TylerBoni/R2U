import signal
import json

class TimeoutError(Exception):
    pass

# def input_with_timeout(prompt, timeout):
#     def timeout_handler(signum, frame):
#         raise TimeoutError()

#     # Set the signal handler for the alarm signal
#     signal.signal(signal.SIGALRM, timeout_handler)
#     signal.alarm(timeout)  # Start the timer

#     try:
#         result = input(prompt)
#         signal.alarm(0)  # Cancel the timer
#         return result
#     except TimeoutError:
#         print("Input timed out.")
#         return None
    
def getJsonFromFile(path):
    # read the contents of the JSON file
    with open(path, 'r') as f:
        obj = json.load(f)
    return obj
    
