#/usr/bin/python3

#rosservice call /clear "{}"
#rosservice call /reset "{}"
#turtlesim world is around 0-100
import rospy
from turtlesim.srv import *
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Vector3
from std_srvs.srv import Empty
import time
import math

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)



class SkubaDrawerNode:
    def __init__(self,turtle_name):
        rospy.init_node('skuba_drawer_node')
        self.turtle_name=turtle_name
        self.vel_pub=rospy.Publisher(f'{self.turtle_name}/cmd_vel',Twist,queue_size=1)

        rospy.wait_for_service(f'clear')
        try:
            clear=rospy.ServiceProxy(f'clear',Empty)
            resp=clear()
        except rospy.ServiceException as e:
            print(e)

    def set_pen(self,switch_on=True,r=255,g=255,b=255,width=2):
        srv_name=f'{self.turtle_name}/set_pen'
        rospy.wait_for_service(srv_name)
        try:
            set_pen=rospy.ServiceProxy(srv_name,SetPen)
            resp=set_pen(r,g,b,width,not switch_on)
        except rospy.ServiceException as e:
            print("error motherfucker",e)
        pass
    def teleport(self,x,y,theta=0,absolute=True):#no pen setting for teleporting
        x=translate(x,0,100,0,12)
        y=translate(y,0,100,0,12)
        if absolute==True:
            srv_name=f'{self.turtle_name}/teleport_absolute'
            rospy.wait_for_service(srv_name)
            try:
                tp_absolute=rospy.ServiceProxy(srv_name,TeleportAbsolute)
                resp=tp_absolute(x,y,theta)
            except rospy.ServiceException as e:
                print("error motherfucker",e)
        pass
        
    def walk_to(self,x,y,absolute=True):#no pen setting for teleporting

        pass
    def draw_circle(self,x,y,r):
        self.set_pen(switch_on=False)
        
        #sol1 : teleport continuously in circle
        for ang in range(0,360,int(50/r)):
            rad=ang/180*math.pi
            self.teleport(x+r*math.cos(rad), y+r*math.sin(rad),rad+math.pi/2)
            self.set_pen(switch_on=True)
#while not rospy.is_shutdown():
#            self.vel_pub.publish(Twist(linear=Vector3(x=1),angular=Vector3(z=0.1)))
#            time.sleep(0.1)
        #sol2 : pid

        
        #    time.sleep(0.1)
        #    self.vel_pub.publish(Twist(linear=Vector3(x=-r),angular=Vector3(z=0)))
        #    time.sleep(0.1)
        #    pass
        

        pass
    def draw_rectangle(self,cx,cy,w,h):
        self.set_pen(switch_on=False)
        points=[
            [cx-w/2,cy+h/2],
            [cx+w/2,cy+h/2],
            [cx+w/2,cy-h/2],
            [cx-w/2,cy-h/2],
            [cx-w/2,cy+h/2]
        ]
        for xi,yi in points:
            self.teleport(xi,yi)
            self.set_pen(switch_on=True)

    def draw_triangle(self,bcx,bcy,bw,bh):
        self.set_pen(switch_on=False)
        points=[
            [bcx-bw/2,bcy+bh/2],
            [bcx+bw/2,bcy+bh/2],
            [bcx,bcy-bh/2],
            [bcx-bw/2,bcy+bh/2]
        ]
        for xi,yi in points:
            self.teleport(xi,yi)
            self.set_pen(switch_on=True)
        pass

    def draw_christmas_tree(self):
        pass
    def draw(self):
        self.draw_circle(100,100,100);
        self.draw_rectangle(100,100,200,200);
        self.draw_triangle(x,y,w,h);
        self.draw_christmas_tree(100,100,200,200);

if __name__=='__main__':
    node=SkubaDrawerNode('turtle1')

    #node.set_pen(switch_on=False)
    #node.teleport(50,50,0)
    node.draw_circle(50,50,20);
    node.draw_rectangle(50, 50, 40, 40)
    node.draw_triangle(50, 50, 40, 40)
    #node.clear()
    #node.draw_circle(50, 50, 20)