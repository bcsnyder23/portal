import sys
from PIL import Image

def get_bboxes(img_path):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    
    colors = {
        'red': (255, 0, 0),
        'green': (0, 128, 0), # typical green
        'yellow': (255, 215, 0), # gold
        'blue': (0, 0, 255)
    }
    
    def color_dist(c1, c2):
        return sum((a-b)**2 for a,b in zip(c1,c2))

    # we just need approximate bounds
    bboxes = {}
    for name in colors:
        bboxes[name] = [w, h, 0, 0] # minx, miny, maxx, maxy
        
    for y in range(h):
        for x in range(w):
            p = img.getpixel((x,y))
            # simple closest color, but we only care if it's very close
            for name, c in colors.items():
                if color_dist(p, c) < 5000: # tolerance
                    bboxes[name][0] = min(bboxes[name][0], x)
                    bboxes[name][1] = min(bboxes[name][1], y)
                    bboxes[name][2] = max(bboxes[name][2], x)
                    bboxes[name][3] = max(bboxes[name][3], y)
    
    print(f"--- {img_path} ---")
    for name in colors:
        if bboxes[name][0] <= bboxes[name][2]:
            print(f"{name}: x={bboxes[name][0]}..{bboxes[name][2]}, y={bboxes[name][1]}..{bboxes[name][3]} (w={bboxes[name][2]-bboxes[name][0]}, h={bboxes[name][3]-bboxes[name][1]})")

get_bboxes('images/example6.png')
get_bboxes('images/example1.png')
get_bboxes('images/example1-halfway.png')
get_bboxes('images/example2.png')
get_bboxes('images/example3.png')
get_bboxes('images/example4.png')
