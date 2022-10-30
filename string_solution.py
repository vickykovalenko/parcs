from os import stat
from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

    	strings = self.read_input()
    	n = len(strings)
    	step = n / len(self.workers)

    	mapped = []
    	for i in xrange(0, len(self.workers)):
        	mapped.append(self.workers[i].mymap(i*step, (i+1)*step, strings, i))

    	reduced = self.myreduce(mapped)
    	self.write_output(reduced)
    	print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b, strings, i):
        print(a, b)
        
        res = [str(i)]
        for i in xrange(a, b):
        	for j in xrange(i+1, len(strings)):
        		check_str = strings[i] + strings[j]
        		if(check_str == check_str[::-1]):
        			res.append(check_str)	
        
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        res = []
        for chunk in mapped:
            for s in chunk.value:
                res.append(s)
        
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        return [line.strip() for line in f.readlines()]

    def write_output(self, output):
        f = open(self.output_file_name, 'w')

        for s in output:
            f.write(s + '\n')

        f.close()




