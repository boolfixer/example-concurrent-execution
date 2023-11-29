from multiprocessing import Process

from pymavlink import mavutil

from config.mavlink_connection_config import MavlinkConnectionConfig
from src.DTO.resolution import Resolution
from src.DTO.roi_absolute import RoiAbsolute
from src.deviation_calculator import DeviationCalculator
from src.multiprocessing_communication.sync_array_decorator_factory import SyncArrayDecoratorFactory


class FlightControlWorker(Process):
    def __init__(self, captured_roi_sync_array, resolution: Resolution):
        super().__init__()

        self.__captured_roi_sync_array = SyncArrayDecoratorFactory().create(captured_roi_sync_array)
        self.__resolution = resolution

        self.__deviation_calculator = DeviationCalculator(self.__resolution)

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
                boarding_box = self.__captured_roi_sync_array.read()

                if not boarding_box:
                    continue

                boarding_box = (int(boarding_box[0]), int(boarding_box[1]), int(boarding_box[2]), int(boarding_box[3]))
                roi_absolute = RoiAbsolute.from_boarding_box(boarding_box)

                deviation = self.__deviation_calculator.calculate(roi_absolute)

                self.__mavlink_connection.mav.manual_control_send(
                    self.__mavlink_connection.target_system,
                    x=deviation.delta_x,
                    y=deviation.delta_y,
                    z=500,
                    r=0,
                    buttons=0
                )

            except Exception as exception:
                print(exception)
