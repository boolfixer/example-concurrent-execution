from multiprocessing import Process

from pymavlink import mavutil

from config.mavlink_connection_config import MavlinkConnectionConfig
from src.DTO.resolution import Resolution
from src.DTO.roi_relative import RoiRelative
from src.multiprocessing_communication.sync_array_decorator_factory import SyncArrayDecoratorFactory


class TriggerWorker(Process):
    def __init__(self, roi_to_capture_sync_array, resolution: Resolution):
        super().__init__()

        self.__roi_to_capture_sync_array = SyncArrayDecoratorFactory().create(roi_to_capture_sync_array)
        self.__resolution = resolution

        mavlink_connection_configuration = MavlinkConnectionConfig()
        self.__mavlink_connection = mavutil.mavlink_connection(
            device=mavlink_connection_configuration.device,
            baud=mavlink_connection_configuration.baud
        )
        self.__mavlink_connection.wait_heartbeat()
        self.__mavlink_connection.arducopter_arm()
        self.__mavlink_connection.motors_armed_wait()

    def run(self) -> None:
        while True:
            try:
                msg = self.__mavlink_connection.recv_match(type='STATUSTEXT', blocking=True)
                msg = msg.to_dict()

                roi_relative = RoiRelative.from_mavlink_message(msg['text'])
                roi_absolute = roi_relative.to_roi_absolute(resolution=self.__resolution)

                self.__roi_to_capture_sync_array.write(
                    str(roi_absolute.get_x_start()),
                    str(roi_absolute.get_y_start()),
                    str(roi_absolute.get_width()),
                    str(roi_absolute.get_height())
                )

            except Exception as exception:
                print(exception)
