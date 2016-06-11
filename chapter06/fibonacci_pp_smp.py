import os, pp

input_list = [4, 3, 8, 6, 10]
result_dict = {}

def aggregate_results(result):
    print "Computing results with PID [%d]" % os.getpid()
    result_dict[result[0]] = result[1]

def fibo_task(value):
    a, b = 0, 1
    for item in range(value):
        a, b = b, a + b
    message = "the fibonacci calculated by pid %d was %d" \
        % (os.getpid(), a)
    return (value, message)


job_server = pp.Server()
for item in input_list:
    job_server.submit(fibo_task, (item,), modules=('os',), callback=aggregate_results)
  
job_server.wait()

print "Main process PID [%d]" % os.getpid() 
for key, value in result_dict.items():
    print "For input %d, %s" % (key, value)
