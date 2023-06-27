import os
import pyboof as pb
import cv2
import argparse

def encode_microqr(msg, output_dir):
    """Encode message into a Micro QR code and save it to output_path.

    Args:
        msg (str): The message to encode
        output_dir (str): The directory to save the micro qr code 
    """
    generator = pb.MicroQrCodeGenerator(pixels_per_module=20)
    generator.set_message(msg)
    boof_gray_img = generator.generate()
    np_gray_img = pb.boof_to_ndarray(boof_gray_img)
    
    save_path = os.path.join(output_dir, f'{msg}.png')
    cv2.imwrite(save_path, np_gray_img)
    print(f"Saved Micro QR code to {save_path}")
    
def get_args():
    parser = argparse.ArgumentParser(description='Encode message into a Micro QR code')
    parser.add_argument('msg', help='Message to encode')
    parser.add_argument('-d', '--output_dir', dest='out_dir', type=str, default='data/qrcodes')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    encode_microqr(args.msg, args.out_dir)
    