import numpy as np
import pyboof as pb
import cv2
import os
import argparse

def detect_microqr_in_image(input_path, output_dir):
    """
    input_path: Path to input image
    output_dir: Path to output directory
    Detects Micro QR codes in a single image.
    Detected bounding boxes are drawn on the image and saved to the output directory. 
    """
    detector = pb.FactoryFiducial(np.uint8).microqr()
    pb_img = pb.load_single_band(input_path, np.uint8)
    detector.detect(pb_img)
    
    num_microqr = len(detector.detections)
    print(f"Detected {num_microqr} microqr codes")
    
    img = cv2.imread(input_path)
    for qr in detector.detections:
       decoded_msg = qr.message
       # qr.bounds is a list of 4 object: Polybon2D,
       # so we need to convert it to a list of 4 tuples
       qr_bounds = qr.bounds.convert_tuple()
       qr_bounds = list(map(lambda x: (int(x[0]), int(x[1])), qr_bounds))
       pts = np.array(qr_bounds, np.int32)
       cv2.polylines(img, [pts], True, (0, 255, 0), 2)
       cv2.putText(img, decoded_msg, qr_bounds[0], cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, (0, 255, 0), 2)
    
    output_path = os.path.join(output_dir, os.path.basename(input_path))
    cv2.imwrite(output_path, img)
    
def detect_microqr_in_dir(input_dir, output_dir):
    """
    input_dir: Path to input directory
    output_dir: Path to output directory
    Detects Micro QR codes in all images in a directory.
    Detected bounding boxes are drawn on the images and saved to the output directory. 
    """
    for file in os.listdir(input_dir):
        if file.endswith('.png'):
            input_path = os.path.join(input_dir, file)
            detect_microqr_in_image(input_path, output_dir)

def get_args():
    parser = argparse.ArgumentParser(description='Detect Micro QR codes in images')
    parser.add_argument('input_path', help='Path to input image or dir')
    parser.add_argument('-o', '--output_dir', dest='out_dir', type=str, default='data/results')
    parser.add_argument('-d', '--direcotry', dest='using_dir', action='store_true', 
                        help='Input is a directory')
    
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    
    if args.using_dir:
        detect_microqr_in_dir(args.input_path, args.out_dir)
    else:
        detect_microqr_in_image(args.input_path, args.out_dir)