import cv2

def change_fps(input_video_path, output_video_path, new_fps):
    # Capture the input video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the original video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))

    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(output_video_path, codec, new_fps, (width, height))

    # Read and write frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved with {new_fps} FPS at {output_video_path}")

# Usage example
"""input_video_path = './assets/khabib_vs_mcgregor.mp4'
output_video_path = './output.mp4'
new_fps = 5  # Desired new FPS
change_fps(input_video_path, output_video_path, new_fps)"""