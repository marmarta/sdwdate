#!/usr/bin/python3 -u

## Copyright (C) 2015 troubadour <trobador@riseup.net>
## Copyright (C) 2015 - 2020 ENCRYPTED SUPPORT LP <adrelanos@riseup.net>
## See the file COPYING for copying conditions.

import sys
import gevent
from gevent.subprocess import Popen, PIPE

def get_time_from_servers(remotes, ip_address, port_number):
    url_to_unixtime_path = '/usr/lib/sdwdate/url_to_unixtime'

    threads = []
    urls = []
    unix_times = []
    seconds = 50
    do_exit = False

    ### Clear lists.
    del threads[:]
    del urls[:]
    del unix_times[:]

    for i in range(len(remotes)):
        threads.append(Popen([url_to_unixtime_path,
                              ip_address,
                              port_number,
                              remotes[i],
                              '80',
                              '0'], stdout=PIPE))

    try:
       gevent.wait(timeout=seconds)
    except KeyboardInterrupt:
       do_exit = True
       print("remotes.py: KeyboardInterrupt received.")
    except SystemExit:
       do_exit = True
       print("remotes.py: sigterm received.")
    except:
       print("Unexpected error:", sys.exc_info()[0])
       pass

    if do_exit == True:
       for i in range(len(threads)):
           try:
               threads[i].terminate()
           except:
               pass
       urls.append(remotes[i])
       unix_times.append('sigterm')
       return urls, unix_times

    for i in range(len(threads)):
        if threads[i].poll() is not None:
            urls.append(remotes[i])
            msg = threads[i].stdout.read()
            # Sanitize response. Log if response causes error. This can be placed in a separate file/process
            try:
                msg = msg.strip()
                unix_times.append(msg)
            except:
                #Log
                unix_times.append('Error sanitizing output!')
        else:
            urls.append(remotes[i])
            unix_times.append('Timeout')
        try:
           threads[i].terminate()
        except:
           pass

    return urls, unix_times

if __name__ == "__main__":
    get_time_from_servers(remotes)
