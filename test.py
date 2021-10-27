#from __future__ import print_function
from math import sin, cos, radians
import timeit
import os


'''
if __name__ == '__main__':
    
    result = timeit.repeat('bench.bench()', setup='import bench', number=10, repeat=10)
    print(result)
    result = list(sorted(result))
    avg = 0

    for i in result:
        avg += i
    
    avgFinal = (avg/3) * 1000

    print("BENCH SCORE: " + str(avgFinal))

'''


from time import perf_counter as time
import sys

def write_test(file, block_size, blocks_count):

    try:
        with open(f"{file}", 'r+') as f:
            f.truncate(0)
        
    except:
        pass


    #f = os.open(file, os.O_CREAT|os.O_WRONLY, 0o777) # low-level I/O

    took = []

    for i in range(blocks_count):
        #buff = os.urandom(block_size) # get random bytes
        #print(sys.getsizeof(buff))
        start = time()
        #os.write(f, buff)

        fo = open(file, "wb")
        fo.write(b'00000000000000000' * int(block_size))

        # Close opend file
        fo.close()

        #os.fsync(f) # force write to disk
        t = time() - start
        took.append(t)

    #os.close(f)

    #os.remove(f"{file}") 

    return took

def read_test(file, itr):
    print("Reading file")

    times = []

    for i in range(itr):
        #f = os.open(file, os.O_RDONLY, 0o777) # low-level I/O
        start = time()


        #fileContent = open(file)



        #ret = os.read(f,1024)

        fo = open(file, "r+")
        x = fo.read();



        #print(x)
        # Close opend file
        fo.close()

        t = time() - start

        times.append(t)

        #os.close(f)

        

        print(sys.getsizeof(x))


    #os.close(f)


    #os.remove(f"{file}") 

    return times


byteSize = 1048576/17
dataToWrite_MB = 100 # 100 MB
itr = 5
fileName = 'disk_bench_temp.dat'

print("Running write test")
results = write_test(fileName, byteSize * dataToWrite_MB, itr)
read_test = read_test(fileName, itr)

print(results)

avgTotal = 0
avgReadTime = 0

print(read_test)

for readTime in read_test:
    avgReadTime += readTime

print("READ TEST: " + str((dataToWrite_MB*itr)/(avgReadTime)) + " MB/s")

for result in results:
    avgTotal += result


print("WRITE TEST: " + str(((dataToWrite_MB*itr)/(avgTotal))) + " MB/s")

