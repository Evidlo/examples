import time
import pyfldigi
import subprocess
import string
import re

c = pyfldigi.Client()

# time to clear commands queue if no new data received
data_timeout = 5

partial_command = b''
commands = []
last_data_time = time.time()

def make_printable(bytestring):
    processed = []
    for b in bytestring:
        if b >= 32 and b <= 127 or b == 10:
            processed.append(b)
        elif b == 13:
            pass
        else:
            # processed.append(63)
            pass

    return bytes(processed)

while True:
    rxdata_raw = c.text.get_rx_data()

    # filter out nonprinting chars
    # rxdata = ''.join(filter(lambda x: x in string.printable, rxdata))
    rxdata = make_printable(rxdata_raw)

    # lowercase so we can use modes with caps only characters
    rxdata = rxdata.lower()

    # parsing incoming data into separate commands.
    if len(rxdata) > 0:
        print('--------')
        print(rxdata_raw)
        print(partial_command, commands)

        partial_command += rxdata
        c.text.clear_rx()

        match = re.match(b'.*\.\.\.(.*)\.\.\..*', partial_command)
        if match is not None:
            commands.append(match.groups()[0])
            partial_command = b''
        # if b'\n' in rxdata:
        #     rx_lines = rxdata.split(b'\n')
        #     commands.append(partial_command + rx_lines[0])
        #     commands += rx_lines[1:-1]
        #     partial_command = rx_lines[-1]
        # else:
        #     partial_command += rxdata

        last_data_time = time.time()

    if len(partial_command) > 0 and time.time() - last_data_time > data_timeout:
        partial_command = b''
        print(partial_command, commands)

    if len(commands) > 0:
        for command in commands:
            print('Executing:', command)
            # TODO: execute all commands in same shell
            output = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()
            # trim output chars and send
            output = b'\n'.join(output)[:100]
            print('Result:', output)

            # sometimes pyfldigi times out after sending.  catch that
            # also fldigi gets stuck in tx mode.  abort() afterwards
            # to prevent his
            try:
                c.main.send(output)
                c.main.abort()
            except TimeoutError:
                pass

        commands = []

    time.sleep(1)
