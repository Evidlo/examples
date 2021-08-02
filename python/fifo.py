import os, stat, time

fifo_file = 'test.fifo'

# remove old fifo
if os.path.exists(fifo_file) and stat.S_ISFIFO(os.stat(fifo_file).st_mode):
    print('deleting old fifo')
    os.remove(fifo_file)

os.mkfifo(fifo_file)

# open a fifo in non-blocking mode
f = os.open(fifo_file, os.O_RDWR)
os.write(f, b'foobar')

time.sleep(10)

# cleanup
os.remove(fifo_file)
