import threading
import time

from uwb_mqtt.constants import *
from uwb_mqtt.data_position import init_data_managers as idmPositions
from uwb_mqtt.data_raw_distance import init_data_managers as idmDistance
from uwb_mqtt.data_individual_distance import init_data_managers as idmIndivDistance
from uwb_mqtt.db.init_db import create_db_and_tables
from uwb_mqtt.manager import MQTTManager
from uwb_mqtt.visualization import InteractivePlot


def main():
    create_db_and_tables()

    position_data_managers = idmPositions(n_tags=N_TAGS)
    distance_data_managers = idmDistance(n_tags=N_TAGS)
    indiv_distance_data_managers = idmIndivDistance(n_tags=N_TAGS)

    topics = [MQTT_TOPIC_POSITION, MQTT_TOPIC_RAW_DISTANCE, MQTT_TOPIC_INDIVIDUAL_DISTANCE]

    mqtt_manager = MQTTManager(
        MQTT_SERVER,
        MQTT_PORT,
        MQTT_USER,
        MQTT_PASS,
        topics=topics,
        position_manager=position_data_managers,
        distance_manager=distance_data_managers,
        indiv_distance_manager= indiv_distance_data_managers
    )
    

    plotter = InteractivePlot(anchors, position_data_managers, distance_data_managers,indiv_distance_data_managers)
    

    mqtt_thread = threading.Thread(target=mqtt_manager.start)

    mqtt_thread.start()


    plotter.start_plotting()
  
    mqtt_manager.stop()
    mqtt_thread.join()


if __name__ == "__main__":
    main()
