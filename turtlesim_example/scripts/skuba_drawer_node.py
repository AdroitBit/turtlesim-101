import rospy
from turtlesim.srv import *




class SkubaDrawerNode:
    def __init__(self,turtle_name):
        self.turtle_name=turtle_name
        self.vel_pub=rospy.Publisher(f'{self.turtle_name}/cmd_vel')
        pass
    def set_pen(self,switch_on=True,r=255,g=255,b=255,width=2):
        srv_name=f'{self.turtle_name}/set_pen'
        rospy.wait_for_service(srv_name)
        try:
            set_pen=rospy.ServiceProxy(srv_name,SetPen)
            resp=set_pen(r,g,b,width,switch_on)
        except rospy.ServiceException as e:
            print("error motherfucker",e)
        pass
    def teleport(self,x,y,theta,absolute=True):#no pen setting for teleporting
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
        self.teleport(x,y)
        self.

        pass
    def draw_rectangle(self,cx,cy,w,h):

        pass
    def draw_triangle(self):
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
    