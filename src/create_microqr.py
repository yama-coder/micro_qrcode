import segno
import argparse
import os

def encode_microqr(string, save_path):
    """
    Encode the string to a Micro QR Code and save it to the save_path.
    """
    micro_qr = segno.make_micro(string)
    micro_qr.save(save_path, scale=20)
    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str,
                        help='The string to encode to a Micro QR Code.')
    parser.add_argument('--save_dir', type=str, default='./data/qrcode/',
                        help='The directory to save the Micro QR Code.')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    save_path = os.path.join(args.save_dir, args.string + '.png')
    encode_microqr(args.string, save_path)