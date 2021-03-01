"""
Note: This code is written horribly inefficient and absolutely not recommended for production, but rather just for a
cheap laugh.

written by alyaeanyx
"""

import cv2
import sys
import numpy as np

DOTS = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 0), (3, 1)]

chars = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
for i in range(256):
    num = 0
    pattern = np.zeros((4, 2))
    for b in range(8):
        if i & 2**b:
            num += 1
            pattern[DOTS[b]] = 1
    chars[num].append((chr(0x2800+i), pattern))


def brailleize(img, width):
    ratio = width/img.shape[1]
    scaled_img = cv2.cvtColor(cv2.resize(img, (0, 0), fx=ratio*2, fy=ratio/2*4), cv2.COLOR_BGR2GRAY)

    text = ""
    for x in range(scaled_img.shape[0]//4):
        for y in range(scaled_img.shape[1]//2):
            tile = scaled_img[x*4:(x+1)*4, y*2:(y+1)*2].astype(float)
            avg = np.average(tile)
            num_dots = int(float(avg)*8/255 + 0.5)
            shifted = tile - avg
            norm = shifted / (max(1, np.abs(shifted).max())) / 2 + 0.5
            errors = []
            for char, pattern in chars[num_dots]:
                error = np.linalg.norm(pattern-norm)
                errors.append((char, error))
            char = sorted(errors, key=lambda x: x[1])[0][0]
            text += char
        text += "\n"
    return text

if __name__ == "__main__":
    img = cv2.imread(sys.argv[1])
    width = int(sys.argv[2])
    print(brailleize(img, width))