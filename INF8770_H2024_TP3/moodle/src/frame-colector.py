import cv2

class FrameCollector:
    def __init__(self, video_path, output_folder, frame_interval=1):
        self.video_path = video_path
        self.output_folder = output_folder
        self.frame_interval = frame_interval

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
            
            frame_path = f"{self.output_folder}/frame_{frame_index}.jpg"
            cv2.imwrite(frame_path, frame)

        openedVideo.release()

def main():
    video_path = r'moodle\data\mp4\v001.mp4'
    output_folder = f"moodle/video_frames"
    frame_interval = 30
    frame_collector = FrameCollector(video_path, output_folder, frame_interval)

    frame_collector.sample_frames()

if __name__ == "__main__":
    main()
