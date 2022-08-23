#/usr/bin/python3

#rosservice call /clear "{}"
#rosservice call /reset "{}"
#turtlesim world is around 0-100
from transformers import ALBERT_PRETRAINED_MODEL_ARCHIVE_LIST
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
    def draw_path(self,points):
        self.set_pen(switch_on=False)
        #sol1 : teleport continuously
        points+=[points[0]]
        for x,y in points:
            self.teleport(x,y,0)
            self.set_pen(switch_on=True)

        self.set_pen(switch_on=False)
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
    def draw_rectangle(self,bcx,bcy,w,h):
        points=[
            [bcx-w/2,bcy],#left of base
            [bcx+w/2,bcy],#right of base
            [bcx+w/2,bcy+h],#right of top
            [bcx-w/2,bcy+h],#left of top
        ]
        self.draw_path(points)

    def draw_triangle(self,bcx,bcy,bw,bh):
        points=[
            [bcx-bw/2,bcy],#left of base
            [bcx+bw/2,bcy],#right of base
            [bcx,bcy+bh],#top
        ]
        self.draw_path(points)

    def draw_christmas_tree(self,bcx,bcy,tree_w,tree_h):
        #christmas tree trunk
        points=[
            [bcx-tree_w*0.2/2,bcy],
            [bcx+tree_w*0.2/2,bcy],
            [bcx+tree_w*0.2/2,bcy+tree_h*0.2],
            [bcx-tree_w*0.2/2,bcy+tree_h*0.2],
        ]
        self.draw_path(points)
        #christmas tree leaves1
        points=[
            [bcx-tree_w/2,bcy+tree_h*0.2],
            [bcx+tree_w/2,bcy+tree_h*0.2],
            [bcx+tree_w*0.6/2,bcy+tree_h*(0.2+0.2)],
            [bcx-tree_w*0.6/2,bcy+tree_h*(0.2+0.2)],
        ]
        self.draw_path(points)
        #christmas tree leaves2
        points=[
            [bcx-tree_w*0.8/2,bcy+tree_h*(0.2+0.2)],
            [bcx+tree_w*0.8/2,bcy+tree_h*(0.2+0.2)],
            [bcx+tree_w*0.4/2,bcy+tree_h*(0.2+0.2+0.2)],
            [bcx-tree_w*0.4/2,bcy+tree_h*(0.2+0.2+0.2)],
        ]
        self.draw_path(points)
        #christmas tree leaves3
        points=[
            [bcx+tree_w*0.4/2,bcy+tree_h*(0.2+0.2+0.2)],
            [bcx-tree_w*0.4/2,bcy+tree_h*(0.2+0.2+0.2)],
            [bcx,bcy+tree_h*(0.2+0.2+0.2+0.3)],
        ]
        self.draw_path(points)
        #christmas tree star
        #star have 10 vertices,even then short dis,odd then long dis
        #it can have phase

        #christmas tree BALL and STICK
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
    #node.draw_circle(50,50,20);
    #node.draw_rectangle(50, 50, 40, 40)
    #node.draw_triangle(50, 50, 40, 40)
    node.draw_christmas_tree(50,0,25,50)
    
    #node.clear()
    #node.draw_circle(50, 50, 20)