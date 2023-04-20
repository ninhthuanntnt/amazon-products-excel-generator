import threading
import queue

class Threadpool:
    def __init__(self, num_threads):
        self.tasks = queue.Queue()
        self.workers = []
        self.num_threads = num_threads
        for _ in range(self.num_threads):
            worker = threading.Thread(target=self.worker)
            self.workers.append(worker)
            worker.start()

    def worker(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def wait_completion(self):
        self.tasks.join()