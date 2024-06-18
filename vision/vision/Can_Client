#!/usr/bin/env python3


""" 
    @author Strix Elixel 
    @program can_client
    @brief Simple ROS2 Interface With Connor's CAN Driver  
"""


from enum                import Enum
from scion_types.srv     import SendFrame
from public_service_apis import Client
from public_service_apis import make_service_call
from helpers             import GENERATE_RANDOM_NODE_IDENTIFIER


#################################################
""" 
    Command Types Defined in CAN Driver
"""
class Command(Enum):

    SOFTKILL = 0x00
    CLEARERR = 0x0A
    MOTOR = 0x010
    STOW = 0x022

#################################################


##################################################################################
""" 
    Different CAN Frames Available 
"""

TURN_OFF_LIGHT =        [0x04, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00]
ENABLE_LIGHT =          [0x04, 0x00, 0x04, 0x00, 0x01, 0x00, 0x00, 0x00]
TURN_ON_LIGHT =         [0x04, 0x00, 0x04, 0x00, 0x64, 0x00, 0x00, 0x00]
SAFE_MODE =             [0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00]
ALL_CLEAR =             [0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
KILL =                  [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
NOTHING =               [0x65, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

###################################################################################


################################################################################################################
""" 
    Context of The CAN Client
"""

NO_RESPONSE                                         = -1
SEND_CAN_TOPIC_NAME                                 = 'send_can_raw'                                                # Defined in CAN Driver
CAN_TEMP_NODE_NAME                                  = 'can_temp_node_' + GENERATE_RANDOM_NODE_IDENTIFIER()          # We need a temp node to spin and process callback when we get response
CAN_CLIENT_INSTANTIATION_MESSAGE                    = "CAN CLIENT INSTANTIATED WITH ID: " + CAN_TEMP_NODE_NAME

################################################################################################################


class Can_Client():
    #########################################################

    def __init__(self):
        """ 
            We Will Create A Client Upon Instantiation with the appropriate topic name for 
            CAN Requests and a random name so it doesn't clash with other nodes on network
        """
        self.can_client = Client(SendFrame, CAN_TEMP_NODE_NAME, SEND_CAN_TOPIC_NAME)
        print("CAN CLIENT INSTANTIATED WITH ID: " + CAN_TEMP_NODE_NAME)

    #########################################################

    """
        The can client defines various functions to make it easy to utilize common features.
        This could be added to later with other frames.
    """ 
    def send_nothing(self):
        can_frame = SendFrame.Request()
        can_frame.can_id = Command.MOTOR.value
        can_frame.can_dlc = 1
        can_frame.can_data = NOTHING
        response = make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

    def set_bot_in_safe_mode(self):
        can_frame = SendFrame.Request()
        can_frame.can_id = Command.STOW.value
        can_frame.can_dlc = 5
        can_frame.can_data = SAFE_MODE
        response = make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

    def enable_light(self):
        can_frame = SendFrame.Request()
        can_frame.can_id = Command.STOW.value
        can_frame.can_dlc = 5
        can_frame.can_data = ENABLE_LIGHT
        response = make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

    def turn_on_light(self):
        can_frame = SendFrame.Request()
        can_frame.can_id = Command.STOW.value
        can_frame.can_dlc = 5
        can_frame.can_data = TURN_ON_LIGHT
        response = make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

    def turn_off_light(self):
        can_frame = SendFrame.Request()
        can_frame.can_id = Command.STOW.value
        can_frame.can_dlc = 5
        can_frame.can_data = TURN_OFF_LIGHT

        response = make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

    def kill_robot(self):
        can_frame = SendFrame.Request()
        can_frame.can_id = Command.SOFTKILL.value
        can_frame.can_dlc = 0
        can_frame.can_data = KILL
        response = make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

    def all_clear(self):
        can_frame = SendFrame.Request()
        can_frame.can_id = Command.CLEARERR.value
        can_frame.can_dlc = 0
        can_frame.can_data = ALL_CLEAR
        response = make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

    def make_motor_request(self, thrusts):
        convertedThrusts =              [int(thrust) for thrust in thrusts]
        byteThrusts =                   [thrust & 0xFF for thrust in convertedThrusts]
        can_frame =                     SendFrame.Request()
        can_frame.can_id =              int(Command.MOTOR.value)
        can_frame.can_dlc =             len(byteThrusts)
        can_frame.can_data =            byteThrusts
        response =                      make_service_call(self.can_client.node, self.can_client.client, can_frame)
        return response.status if response else NO_RESPONSE

####################################################################################################################