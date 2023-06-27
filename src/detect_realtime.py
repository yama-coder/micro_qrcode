import numpy as np
import pyboof as pb
import cv2
import os
import argparse

def detect_microqr_through_camera():
    """
    Detects Micro QR codes through camera.
    Display the decoded message and the bounding box on the camera feed.
    """
    detector = pb.FactoryFiducial(np.uint8).microqr()
    
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # TODO: Remove temporal file using pb.ndarray_to_boof
            # The return value of pb.ndarray_to_boof is diffrent from the one of pb.load_single_band
            # Need to check the source code of pb.ndarray_to_boof
            cv2.imwrite('tmp.png', frame)
            pb_img = pb.load_single_band('tmp.png', np.uint8)
            # pb_img = pb.ndarray_to_boof(frame)
            
            detector.detect(pb_img)
            for qr in detector.detections:
                decoded_msg = qr.message
                # qr.bounds is a list of 4 object: Polybon2D,
                # so we need to convert it to a list of 4 tuples
                qr_bounds = qr.bounds.convert_tuple()
                qr_bounds = list(map(lambda x: (int(x[0]), int(x[1])), qr_bounds))
                pts = np.array(qr_bounds, np.int32)
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                cv2.putText(frame, decoded_msg, qr_bounds[0], cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5, (255, 0, 0), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.realase()
        
if __name__ == '__main__':
    detect_microqr_through_camera()