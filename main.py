from src.multiprocessing_communication.sync_array_factory import SyncArrayFactory
from src.worker.camera_worker import CameraWorker
from src.worker.flight_control_worker import FlightControlWorker
from src.worker.trigger_worker import TriggerWorker


def main():
    sync_array_factory = SyncArrayFactory()
    roi_to_capture_sync_array = sync_array_factory.create()
    captured_roi_sync_array = sync_array_factory.create()

    camera_worker = CameraWorker(
        roi_to_capture_sync_array=roi_to_capture_sync_array,
        captured_roi_sync_array=captured_roi_sync_array
    )
    resolution = camera_worker.get_resolution()

    flight_control_worker = FlightControlWorker(captured_roi_sync_array=captured_roi_sync_array, resolution=resolution)
    flight_control_worker.daemon = True

    trigger_worker = TriggerWorker(roi_to_capture_sync_array=roi_to_capture_sync_array, resolution=resolution)
    trigger_worker.daemon = True

    try:
        trigger_worker.start()
        flight_control_worker.start()
        camera_worker.start()
    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    main()
