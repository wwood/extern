
import sys
import multiprocessing as mp
import extern

class MultiRunner(object):
    def __init__(self, num_threads):
        self._num_threads = num_threads

    def __workerThread(self, queueIn, queueOut):
        """Process each data item in parallel."""
        while True:
            program_index, program = queueIn.get(block=True, timeout=None)
            if program == None:
                break
    
            # allow results to be processed or written to file
            queueOut.put((program_index, extern.run(program)))

    def __writerThread(self, numDataItems, writerQueue, resultQueue):
        """Store or write results of worker threads in a single thread."""
        processedItems = 0
        while True:
            result = writerQueue.get(block=True, timeout=None)
            if result[0] == None:
                break
            
            print result
            resultQueue.put(result)
    
            processedItems += 1
            statusStr = 'Finished processing %d of %d (%.2f%%) items.' % (processedItems, numDataItems, float(processedItems)*100/numDataItems)
            sys.stderr.write('%s\r' % statusStr)
            sys.stderr.flush()
    
        sys.stderr.write('\n')

    def run(self, programs):
        # populate worker queue with data to process
        workerQueue = mp.Queue()
        writerQueue = mp.Queue()
        resultQueue = mp.Queue()
        
        threads = self._num_threads

        for i, program in enumerate(programs):
            workerQueue.put((i, program))

        for _ in range(threads):
            workerQueue.put((None,None))

        try:
            workerProc = [mp.Process(target = self.__workerThread, args = (workerQueue, writerQueue)) for _ in range(threads)]
            writeProc = mp.Process(target = self.__writerThread, args = (len(programs), writerQueue, resultQueue))

            writeProc.start()
    
            for p in workerProc:
                p.start()
    
            for p in workerProc:
                p.join()

            writerQueue.put((None,None))
            writeProc.join()
            
            stdouts = []
            print resultQueue.get()
            for res in resultQueue:
                i = res[0]
                if stdouts[i]: raise Exception("Programming exception, duplicate program IDs detected")
                stdouts[i] = res[1]
            return stdouts
        except:
            for p in workerProc:
                p.terminate()

            writeProc.terminate()
            

