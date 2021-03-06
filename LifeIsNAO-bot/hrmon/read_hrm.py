#!/usr/bin/env python

import max30100
import time
import os
import matplotlib.pyplot as plt

BUFFER_FILEPATH = '/var/lib/nao-debian/dev/shm/hrm_buffer.txt'
GRAFICO_FILEPATH = '/var/lib/nao-debian/dev/shm/grafico.png'
mx30 = max30100.MAX30100()

if not os.path.exists("/var/lib/nao-debian/"):
    os.mkdir("/var/lib/nao-debian")


def scrivi_grafico():
    
    # x = [1,2,3,4,5,6,7,8,9,10]
    # y = [1,2,3,4,5,6,7,8,9,10]

    y = mx30.buffer_ir[-10:]
    x = range(1, len(y)+1)

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='time (s)', ylabel='battiti (bpm)', title='Monitor cardiaco')
    ax.grid()

    fig.savefig(GRAFICO_FILEPATH)


while True:
    try:
        mx30.read_sensor()
        print("ir=%s red=%s" % (mx30.ir, mx30.red))
        if mx30.ir >= 1000:
            with open("/var/lib/nao-debian/dev/shm/hrm_instant.txt", "w") as f:
                f.write(str(mx30.ir))
            with open(BUFFER_FILEPATH, "w") as f:
                print(mx30.buffer_ir[-20:])
                f.write("\n".join(map(str, mx30.buffer_ir[-20:])))
            scrivi_grafico()
        else:
            with open("/var/lib/nao-debian/dev/shm/hrm_instant.txt", "w") as f:
                f.write("NODATA")

        time.sleep(0.5)
    except IOError as e:
        with open("/var/lib/nao-debian/dev/shm/hrm_instant.txt", "w") as f:
            f.write("ERROR")
