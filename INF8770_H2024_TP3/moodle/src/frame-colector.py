import os
import cv2

class FrameCollector:
    def __init__(self, video_path, output_parent_folder, frame_interval=1):
        self.video_path = video_path
        self.frame_interval = frame_interval
        self.video_name = os.path.splitext(os.path.basename(video_path))[0]
        self.output_folder = f"{output_parent_folder}/{self.video_name}_frames"
        os.makedirs(self.output_folder, exist_ok=True)

    def sample_frames(self):
        openedVideo = cv2.VideoCapture(self.video_path)
        if not openedVideo.isOpened():
            print("Error: Could not open video file")
            return

        total_frames = int(openedVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = range(0, total_frames, self.frame_interval)

        for frame_index in frame_indices:
            openedVideo.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = openedVideo.read()
            if not ret:
                print(f"Error: Could not read frame {frame_index}")
                continue
            
            frame_path = f"{self.output_folder}/frame_{frame_index}.jpeg"
            cv2.imwrite(frame_path, frame)

        openedVideo.release()

def main():
    video_dir = f"moodle/data/mp4"
    output_parent_folder = f"moodle/video_frames"
    frame_interval = 30
    for video_name in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_name)
        frame_collector = FrameCollector(video_path, output_parent_folder, frame_interval)
        frame_collector.sample_frames()

if __name__ == "__main__":
    main()
