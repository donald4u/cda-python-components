#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

import logging
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

class MqttClientConnector(IPubSubClient):
    """
    MQTT client connector using paho-mqtt library.
    """

    def __init__(self, clientID: str = None):
        self.config = ConfigUtil()
        self.dataMsgListener = None
        
        self.host = self.config.getProperty(
            ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
        
        self.port = self.config.getInteger(
            ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
        
        self.keepAlive = self.config.getInteger(
            ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
        
        self.defaultQos = self.config.getInteger(
            ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
        
        if not clientID:
            clientID = self.config.getProperty(
                ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY, "CDAMqttClient")
        
        self.mc = mqttClient.Client(client_id=clientID, clean_session=True)
        self.mc.on_connect = self.onConnect
        self.mc.on_disconnect = self.onDisconnect
        self.mc.on_message = self.onMessage
        self.mc.on_publish = self.onPublish
        self.mc.on_subscribe = self.onSubscribe
        
        logging.info(f"MQTT client created. Broker: {self.host}:{self.port}")

    def connectClient(self) -> bool:
        if not self.mc:
            logging.warning("MQTT client not initialized.")
            return False
        
        try:
            logging.info(f"Connecting to MQTT broker at {self.host}:{self.port}...")
            self.mc.connect(self.host, self.port, self.keepAlive)
            self.mc.loop_start()
            return True
        except Exception as e:
            logging.error(f"Failed to connect to MQTT broker: {e}")
            return False
        
    def disconnectClient(self) -> bool:
        if not self.mc:
            logging.warning("MQTT client not initialized.")
            return False
        
        try:
            self.mc.loop_stop()
            self.mc.disconnect()
            logging.info("Disconnected from MQTT broker.")
            return True
        except Exception as e:
            logging.error(f"Failed to disconnect from MQTT broker: {e}")
            return False
        
    def onConnect(self, client, userdata, flags, rc):
        logging.info(f"Connected to MQTT broker. Result code: {rc}")
        
    def onDisconnect(self, client, userdata, rc):
        logging.info(f"Disconnected from MQTT broker. Result code: {rc}")
        
    def onMessage(self, client, userdata, msg):
        logging.info(f"Message received on topic {msg.topic}: {msg.payload.decode('utf-8')}")
        
        if self.dataMsgListener:
            # TODO: Parse message and call appropriate listener method
            pass
            
    def onPublish(self, client, userdata, mid):
        logging.debug(f"Message published. Message ID: {mid}")
    
    def onSubscribe(self, client, userdata, mid, granted_qos):
        logging.info(f"Subscribed to topic. Message ID: {mid}, QoS: {granted_qos}")
    
    def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
        """
        Publish a message to the specified topic with optional QoS level.
        
        @param resource: The topic resource to publish to
        @param msg: The message payload to publish
        @param qos: QoS level (0, 1, or 2). If invalid, defaults to ConfigConst.DEFAULT_QOS
        @return: True if publish was successful, False otherwise
        """
        # check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot publish message.')
            return False
        
        # check validity of message
        if not msg:
            logging.warning('No message specified. Cannot publish message to topic: ' + resource.value)
            return False
        
        # check validity of QoS - set to default if necessary
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        
        # publish message, and wait for publish to complete before returning
        logging.info(f'Publishing message to topic {resource.value} with QoS {qos}')
        msgInfo = self.mc.publish(topic=resource.value, payload=msg, qos=qos)
        msgInfo.wait_for_publish()
        
        return True
    
    def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
        """
        Subscribe to the specified topic with optional callback and QoS level.
        
        @param resource: The topic resource to subscribe to
        @param callback: Optional custom callback for messages on this topic
        @param qos: QoS level (0, 1, or 2). If invalid, defaults to ConfigConst.DEFAULT_QOS
        @return: True if subscription was successful, False otherwise
        """
        # check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot subscribe.')
            return False
        
        # check validity of QoS - set to default if necessary
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        
        # subscribe to topic
        logging.info(f'Subscribing to topic {resource.value} with QoS {qos}')
        self.mc.subscribe(resource.value, qos)
        
        # add custom callback if provided
        if callback:
            self.mc.message_callback_add(resource.value, callback)
        
        return True
    
    def unsubscribeFromTopic(self, resource: ResourceNameEnum = None) -> bool:
        """
        Unsubscribe from the specified topic.
        
        @param resource: The topic resource to unsubscribe from
        @return: True if unsubscribe was successful, False otherwise
        """
        # check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot unsubscribe.')
            return False
        
        logging.info(f'Unsubscribing from topic {resource.value}')
        self.mc.unsubscribe(resource.value)
        
        return True

    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
        return False