from time import time

from src.DTO.resolution import Resolution
from src.DTO.roi_absolute import RoiAbsolute
from src.display_adapter.cv2_adapter import Cv2DisplayAdapter
from src.multiprocessing_communication.sync_array_decorator_factory import SyncArrayDecoratorFactory
from src.tracker.tracker import Tracker
from src.video_capture_adapter.cv2_video_capture_adapter import Cv2VideoCaptureAdapter


class CameraWorker:
    def __init__(self, roi_to_capture_sync_array, captured_roi_sync_array):
        super().__init__()

        sync_array_decorator_factory = SyncArrayDecoratorFactory()
        self.__roi_to_capture_sync_array = sync_array_decorator_factory.create(roi_to_capture_sync_array)
        self.__captured_roi_sync_array = sync_array_decorator_factory.create(captured_roi_sync_array)

        self.__video_capture_adapter = Cv2VideoCaptureAdapter()
        self.__display_adapter = Cv2DisplayAdapter()
        self.__tracker = Tracker()

    def start(self) -> None:
        try:
            prev_frame_time = time()

            for frame in self.__video_capture_adapter.capture_continuous():
                roi_to_capture = None
                boarding_box = self.__roi_to_capture_sync_array.read()

                if boarding_box:
                    boarding_box = (int(boarding_box[0]), int(boarding_box[1]), int(boarding_box[2]), int(boarding_box[3]))
                    roi_to_capture = RoiAbsolute.from_boarding_box(boarding_box)

                captured_roi = self.__tracker.track(frame, roi_to_capture)

                if captured_roi:
                    self.__captured_roi_sync_array.write(
                        str(captured_roi.get_x_start()),
                        str(captured_roi.get_y_start()),
                        str(captured_roi.get_width()),
                        str(captured_roi.get_height())
                    )

                self.__display_adapter.display(frame)

                new_frame_time = time()
                fps = int(1 / (new_frame_time - prev_frame_time))
                prev_frame_time = new_frame_time
                print(fps)
        except Exception as exception:
            print(exception)

    def get_resolution(self) -> Resolution:
        return self.__video_capture_adapter.get_resolution()
