import time
from multiprocessing import Manager, Process

def get_data():
    """ Does the actual work of getting the updating value. """

def update_the_data(shared_dict):
    while not shared_dict.get('server_started'):
        time.sleep(.1)
    while True:
        shared_dict['data'] = get_data()
        shared_dict['data_timestamp'] = time.time()
        time.sleep(3)


def serve_the_data(shared_dict):
    server = initialize_server() # whatever this looks like
    shared_dict['server_started'] = True
    while True:
        server.serve_with_timeout()
        if time.time() - shared_dict['data_timestamp'] > 30:
            # child hasn't updated data for 30 seconds; problem?
            handle_child_problem()


if __name__ == '__main__':
    manager = Manager()
    shared_dict = manager.dict()
    processes = [Process(target=update_the_data, args=(shared_dict,)),
        Process(target=serve_the_data, args=(shared_dict,))]
    for process in processes:
        process.start()
    for process in processes:
        process.join()