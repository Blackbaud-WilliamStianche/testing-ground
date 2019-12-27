import cProfile
import csv
from time import sleep
import threading
import queue

mxg = 8
queues = dict()


def one_thread(file_handle):
    items = csv.reader(file_handle)
    for item in items:
        (_, time) = item
        seconds = int(time)
        one_item(seconds)


def two_threads(file_handle1, file_handle2):
    t1 = threading.Thread(target=one_thread, args=(file_handle1,))
    t2 = threading.Thread(target=one_thread, args=(file_handle2,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def one_item(seconds):
    sleep(seconds)


def generate_queues(file_handle):
    for i in range(mxg):
        queues[i+1] = queue.Queue()
    items = csv.reader(file_handle)
    for item in items:
        (g, time) = item
        queues[int(g)].put(int(time))


def one_worker(myqueue):
    while not myqueue.empty():
        item = myqueue.get()
        one_item(item)
        myqueue.task_done()


def process_queues():
    threads = list()
    for q in range(len(queues.keys())):
        threads.append(threading.Thread(name=str(q+1), target=one_worker, args=(queues[q+1],)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    with open('infile.csv', 'r') as infile:
        cProfile.run('one_thread(infile)')

    with open('infile1.csv', 'r') as infile1, open('infile2.csv', 'r') as infile2:
        cProfile.run('two_threads(infile1, infile2)')

    with open('infile.csv', 'r') as infile:
        cProfile.run('generate_queues(infile)')

    cProfile.run('process_queues()')