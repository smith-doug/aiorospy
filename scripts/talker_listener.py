#!/usr/bin/env python3.7

import asyncio
import rospy 
from aiorospy import AsyncSubscriber
from std_msgs.msg import String


pub = rospy.Publisher('chatter', String, queue_size=1)

async def talker():
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        pub.publish(hello_str)
        await asyncio.sleep(1)


sub = AsyncSubscriber('chatter', String)

async def listener():
    while not rospy.is_shutdown():
        message = await sub.get()
        print(f'I heard: %s'% message.data)

if __name__ == '__main__':
    rospy.init_node('example_pubsub', disable_signals=True)
    try:
        asyncio.get_event_loop().run_until_complete(asyncio.gather(talker(),
                                                                   listener()))
    except KeyboardInterrupt:
        pass
    finally:
        print(f'\nShutting Down')

