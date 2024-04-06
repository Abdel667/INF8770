import os
import time
import cv2
import logging

logging.basicConfig(level=logging.INFO)

class FrameCollector:
    def __init__(self, video_path, output_parent_folder, frame_interval=1):
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file {video_path} does not exist")
        self.video_path = video_path
        self.frame_interval = frame_interval
        self.video_name = os.path.splitext(os.path.basename(video_path))[0]
        self.output_folder = f"{output_parent_folder}/{self.video_name}"
        os.makedirs(self.output_folder, exist_ok=True)

    def sample(self):
        openedVideo = cv2.VideoCapture(self.video_path)
        if not openedVideo.isOpened():
            logging.error("Could not open video file")
            return

        try:
            total_frames = int(openedVideo.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_indices = range(10, total_frames, self.frame_interval)

            for frame_index in frame_indices:
                openedVideo.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                ret, frame = openedVideo.read()
                if not ret:
                    logging.error(f"Could not read frame {frame_index}")
                    continue
                timestamp_msec = openedVideo.get(cv2.CAP_PROP_POS_MSEC)
                timestamp_sec = timestamp_msec / 1000

                frame_path = f"{self.output_folder}/{timestamp_sec}.jpeg"
                cv2.imwrite(frame_path, frame)
        finally:
            openedVideo.release()

def sample_frames(video_dir, output_parent_folder, frame_interval):
    start_time = time.time()
    for video_name in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_name)
        frame_collector = FrameCollector(video_path, output_parent_folder, frame_interval)
        frame_collector.sample()
    end_time = time.time()
    execution_time = end_time - start_time
    performance = f"Execution time of frame sampling is : {execution_time} seconds with frame interval of {frame_interval}"
    logging.info(performance)
    return performance

if __name__ == "__main__":
    video_dir = f"moodle/data/mp4"
    output_parent_folder = f"moodle/video_frames"
    frame_interval = 15
    sample_frames(video_dir, output_parent_folder, frame_interval)