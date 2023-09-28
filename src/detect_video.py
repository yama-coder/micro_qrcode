import argparse
import os

import json
import cv2
import numpy as np
import pyboof as pb
from PIL import Image
from tqdm import tqdm

def detect_microqr_through_video(input_path, mode='v', output_dir='data/resutlts', alignment_file=None):
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
    FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    msec = 0
    frames_to_save = []
    
    if mode == 's':
        # TODO: Accelerate the process of Reading video
        # Bottle neck: saving temporary image files
        # This is meaningless: ndarray -> PIL Image -> temporal file -> pb_img
        # Can I convert frame -> BytesIO -> pb_img?
        for _ in tqdm(range(FRAMES), desc="Reading video"):
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imwrite('tmp.png', frame)
            pb_img = pb.load_single_band('tmp.png', np.uint8)
            frame = detect_in_one_frame(frame, pb_img, detector, alignment_file)
            frames_to_save.append(frame)
            
        video_name = os.path.basename(input_path)
        output_path = os.path.join(output_dir, video_name)
        size = (frames_to_save[0].shape[1], frames_to_save[0].shape[0])
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_writer = cv2.VideoWriter(
            output_path, fourcc, FPS, size)
        for frame in tqdm(frames_to_save, desc="Saving video"):
            video_writer.write(frame)
            
    if mode == 'v':
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # TODO: Remove temporal file using pb.ndarray_to_boof
            # The return value of pb.ndarray_to_boof is diffrent from the one of pb.load_single_band
            # Need to check the source code of pb.ndarray_to_boof
            cv2.imwrite('tmp.png', frame)
            pb_img = pb.load_single_band('tmp.png', np.uint8)
            frame = detect_in_one_frame(frame, pb_img, detector, alignment_file)
            
            # Press 'f' to forward 1 second
            # Press 'b' to backward 1 second
            # Press 'j' to jump to a specific time
            # Press 'q' to quit
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.imshow('frame', frame)
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
        
    cap.release()
    
    
def detect_in_one_frame(frame, pb_img, detector, alignment_file=None):
    detector.detect(pb_img)
    if alignment_file is not None:
        with open(alignment_file, 'r') as f:
            bne_qr_alignment_dict = json.load(f)
    for qr in detector.detections:
        decoded_msg = qr.message
        if decoded_msg not in bne_qr_alignment_dict:
            continue
        else:
            qr_label = bne_qr_alignment_dict[decoded_msg]
        qr_bounds = qr.bounds.convert_tuple()
        qr_bounds = list(map(lambda x: (int(x[0]), int(x[1])), qr_bounds))
        pts = np.array(qr_bounds, np.int32)
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        cv2.putText(frame, qr_label, qr_bounds[0], cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)
    return frame

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='Path to input video')
    parser.add_argument('-m', '--mode', type=str, choices=['v', 's'],
                        default='v', help='v for viewing the video while detecting, s for saving the video while detecting')
    parser.add_argument('-o', '--output_dir', type=str, default='data/results')
    parser.add_argument('--alignment_file', type=str, default=None,
                        help='Path to alignment file of Micro QR code labels')
    
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    detect_microqr_through_video(args.input_path, args.mode, args.output_dir, args.alignment_file)
    print('Done')