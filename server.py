from pyrow import pyrow
from pyrow.ergmanager import ErgManager

from datetime import datetime, time, timedelta, date
import random
import sys
import json

import socket
import websockets
import asyncio

data = {}
ergman = None

port = 5353
if len(sys.argv) > 1: port = int(sys.argv[1])

hostname = sys

async def get_erg_update(erg):
    desc = erg.get_erg()
    monitor = erg.get_monitor()
    workout = erg.get_workout()
    return {
        "serial": desc["serial"],
        "status": desc["status"],
        "time": monitor["time"],
        "distance": monitor["distance"],
        "interval_count": workout["intcount"],
        "workout_state": workout["state"],
        "pace": monitor["pace"],
        "rate": monitor["spm"]
    }

async def main():
    while True:
        try:
            async with websockets.connect('ws://localhost:5000/erg/' + socket.gethostname()) as ws:
                erg = None
                while erg is None:
                    ergs = [pyrow.PyErg(e) for e in pyrow.find()]
                    erg = ergs[0] if len(ergs) > 0 else None
                    await asyncio.sleep(1)
                
                while True:
                    data = await asyncio.gather(*map(get_erg_update, ergs))
                    print(data)
                    await ws.send(json.dumps(data))
                    await asyncio.sleep(1)
        except:
            pass
        await asyncio.sleep(5)


asyncio.run(main())