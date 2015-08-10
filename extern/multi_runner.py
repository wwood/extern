
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
            try:
                stdout = extern.run(program)
                queueOut.put((program_index, stdout))
            except extern.ExternCalledProcessError as e:
                # command, returncode, stderr, stdout
                queueOut.put((program_index, None, e.command,
                                                   e.returncode,
                                                   e.stderr,
                                                   e.stdout))
                break

    def __writerThread(self, numDataItems, writerQueue, resultQueue, progress_stream):
        """Store or write results of worker threads in a single thread."""
        processedItems = 0
        while True:
            result = writerQueue.get(block=True, timeout=None)
            if result[0] == None:
                break
            
            resultQueue.put(result)
    
            processedItems += 1
            if progress_stream:
                statusStr = 'Finished processing %d of %d (%.2f%%) items.' % (processedItems, numDataItems, float(processedItems)*100/numDataItems)
                progress_stream.write('%s\r' % statusStr)
                progress_stream.flush()
    
        if progress_stream: progress_stream.write('\n')

    def run(self, programs, progress_stream=None):
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
            writeProc = mp.Process(target = self.__writerThread, args = (len(programs), writerQueue, resultQueue, progress_stream))
    
            writeProc.start()
    
            for p in workerProc:
                p.start()
    
            for p in workerProc:
                p.join()
    
            writerQueue.put((None,None))
            writeProc.join()
        except Exception as e:
            for p in workerProc:
                p.terminate()
 
            writeProc.terminate()
            raise e
        
        
        stdouts = [None]*len(programs)
        #sequential here so there is no producer-consumer race condition possible
        while resultQueue.empty() is not True:
            res = resultQueue.get()
            i = res[0]
            stdout = res[1]
            if stdout is None:
                raise extern.ExternCalledProcessError(*res[2:])
            elif stdouts[i] is not None:
                raise Exception("extern Programming exception, duplicate program IDs detected")
            stdouts[i] = stdout
        return stdouts

