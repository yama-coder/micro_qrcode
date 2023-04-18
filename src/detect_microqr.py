import numpy as np
import pyboof as pb

data_path = "./data/images/microqr1.jpg"
detector = pb.FactoryFiducial(np.uint8).microqr()
image = pb.load_single_band(data_path, np.uint8)

detector.detect(image)
print("Detected a total of {} Micro QR Codes".format(len(detector.detections)))

for qr in detector.detections:
    print("Found a Micro QR Code with message: {}".format(qr.message))
    print("  at location: {}".format(qr.bounds))