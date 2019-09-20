import asyncio

def helloWorld(loop, nbre):
    while nbre < 10:
        nbre += 1
        print(nbre)
    loop.stop()


loop = asyncio.new_event_loop()
loop.call_soon(helloWorld, loop, 0)


loop.run_forever()
loop.close()