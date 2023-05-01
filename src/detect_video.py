import argparse
import os

import cv2
import numpy as np
import pyboof as pb

def detect_microqr_through_video(input_path, mode='v', output_dir='data/resutlts'):
    """Detects Micro QR codes in a video.
    Detected bounding boxes are drawn on the video and saved to the output directory.

    Args:
        input_path (str): Path to input video
        mode (str, optional): v for viewing the video while detecting, s for saving the video while detecting. Defaults to 'v'. 
        output_dir (str, optional): Path to output directory. Defaults to 'data/results'.
    """
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File {input_path} not found")
    
    detector = pb.FactoryFiducial(np.uint8).microqr()    
    cap = cv2.VideoCapture(input_path)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    msec = 0
    frames_to_save = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # TODO: Remove temporal file using pb.ndarray_to_boof
        # The return value of pb.ndarray_to_boof is diffrent from the one of pb.load_single_band
        # Need to check the source code of pb.ndarray_to_boof
        cv2.imwrite('tmp.png', frame)
        pb_img = pb.load_single_band('tmp.png', np.uint8)
        
        detector.detect(pb_img)
        for qr in detector.detections:
            decoded_msg = qr.message
            qr_bounds = qr.bounds.convert_tuple()
            qr_bounds = list(map(lambda x: (int(x[0]), int(x[1])), qr_bounds))
            pts = np.array(qr_bounds, np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            cv2.putText(frame, decoded_msg, qr_bounds[0], cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 0), 2)
        if mode == 'v':
            cv2.imshow('frame', frame)
            
            # Press 'f' to forward 1 second
            # Press 'b' to backward 1 second
            # Press 'j' to jump to a specific time
            # Press 'q' to quit
            key = cv2.waitKey(0)
            if key & 0xFF == ord('f'):
                msec += 1000
            elif key & 0xFF == ord('b'):
                msec -= 1000
            elif key & 0xFF == ord('j'):
                print(f"Current time: {msec / 1000} s.")
                print(f"Where to jump to? (in seconds) --> ", end='')
                msec = int(input()) * 1000
            elif key & 0xFF == ord('q'):
                break
            cap.set(cv2.CAP_PROP_POS_MSEC, msec)
            
        if mode == 's':
            frames_to_save.append(frame)

    if mode == 's':
        video_name = os.path.basename(input_path)
        output_path = os.path.join(output_dir, video_name)
        size = (frames_to_save[0].shape[1], frames_to_save[0].shape[0])
        video_writer = cv2.VideoWriter(
            output_path, cv2.VideoWriter_fourcc(*'MP4'), FPS, size)
        
        for frame in frames_to_save:
            video_writer.write(frame)
        print(f"Video saved to {output_path}")
    
    cap.release()
    

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='Path to input video')
    parser.add_argument('-m', '--mode', type=str, choices=['v', 's'],
                        default='v', help='v for viewing the video while detecting, s for saving the video while detecting')
    parser.add_argument('-o', '--output_dir', type=str, default='data/results')
    
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    detect_microqr_through_video(args.input_path, args.mode, args.output_dir)
    print('Done')