import threading
import queue
import time

def console(q):
    while 1:
        cmd = input('> ')
        q.put(cmd)
        if cmd == 'quit':
            break

def action_foo():
    print('--> action foo')

def action_bar():
    print('--> action bar')

def invalid_input():
    print('---> Unknown command')

def main():
    cmd_actions = {'foo': action_foo, 'bar': action_bar}
    cmd_queue = queue.Queue()

    dj = threading.Thread(target=console, args=(cmd_queue,))
    dj.start()

    while True:
      print("hello")
      time.sleep(1)

main()