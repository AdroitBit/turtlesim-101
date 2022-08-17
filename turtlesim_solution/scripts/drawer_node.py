import rospy
from turtlesim.srv import *

class DrawerNode:
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
    def draw_circle(self):
        pass
    def draw_rectangle(self):
        pass
    def draw_triangle(self):
        pass

    def draw_christmas_tree(self):
        pass

if __name__=='__main__':
    node=DrawerNode('turtle1')
    