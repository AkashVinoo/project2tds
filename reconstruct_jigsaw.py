from PIL import Image
from sklearn.datasets import load_diabetes
import numpy as np

# Load the scrambled image
img = Image.open('jigsaw.webp')

piece_size = 100  # 500/5
N = 5

# Mapping: (original_row, original_col, scrambled_row, scrambled_col)
mapping = [
    (2,1,0,0), (1,1,0,1), (4,1,0,2), (0,3,0,3), (0,1,0,4),
    (1,4,1,0), (2,0,1,1), (2,4,1,2), (4,2,1,3), (2,2,1,4),
    (0,0,2,0), (3,2,2,1), (4,3,2,2), (3,0,2,3), (3,4,2,4),
    (1,0,3,0), (2,3,3,1), (3,3,3,2), (4,4,3,3), (0,2,3,4),
    (3,1,4,0), (1,2,4,1), (1,3,4,2), (0,4,4,3), (4,0,4,4)
]

# Create a blank image for the reconstructed output
out = Image.new('RGB', (piece_size*N, piece_size*N))

X, y = load_diabetes(return_X_y=True)
np.random.seed(0)

for orig_row, orig_col, scr_row, scr_col in mapping:
    left = scr_col * piece_size
    upper = scr_row * piece_size
    piece = img.crop((left, upper, left+piece_size, upper+piece_size))
    out.paste(piece, (orig_col*piece_size, orig_row*piece_size))

out.save('reconstructed_jigsaw.png')
print('Saved as reconstructed_jigsaw.png') 