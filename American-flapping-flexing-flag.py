import cv2
import numpy as np
import os

# --- 1. CONFIGURATION ---
# Ensure you have an image named 'american_flag.png' in your folder
IMAGE_PATH = "american_flag.png" 
OUTPUT_VIDEO = "patriot_flex.mp4"
FRAME_COUNT = 90  # 3 seconds at 30fps
WIDTH, HEIGHT = 1280, 720 # Cinematic Widescreen

def generate_flag_wave(width, height, phase):
    """Creates horizontal ripples for a waving flag effect."""
    x = np.linspace(0, 10, width)
    y = np.linspace(0, 10, height)
    X, Y = np.meshgrid(x, y)
    
    # We combine horizontal waves (X) with time (phase) for the wave effect
    # and vertical waves (Y) for the 'muscle' ripple
    wave = np.sin(X * 0.5 - phase) * np.cos(Y * 0.3 + phase * 0.5)
    return wave.astype(np.float32)

def create_patriot_video():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: {IMAGE_PATH} not found. Add the flag image to your folder.")
        return

    # Use OpenCV to load and resize
    img = cv2.imread(IMAGE_PATH)
    img = cv2.resize(img, (WIDTH, HEIGHT))

    # Initialize Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, 30.0, (WIDTH, HEIGHT))

    print(f"[SYSTEM] Forging the Patriot Flex for {IMAGE_PATH}...")

    for i in range(FRAME_COUNT):
        # Calculate wave movement
        phase = (i / FRAME_COUNT) * 4 * np.pi
        
        # Intensity: How much the flag 'bulges' (the Flex)
        # We make it pulse slowly
        flex_intensity = (np.sin(phase * 0.5) + 1.5) * 8 
        
        # Create displacement maps
        noise = generate_flag_wave(WIDTH, HEIGHT, phase)
        
        # Build the coordinate maps (X and Y)
        map_x, map_y = np.meshgrid(np.arange(WIDTH), np.arange(HEIGHT))
        
        # APPLY THE DISPLACEMENT
        # We shift the X and Y coordinates by the noise * flex_intensity
        map_x = (map_x.astype(np.float32) + (noise * flex_intensity)).astype(np.float32)
        map_y = (map_y.astype(np.float32) + (noise * flex_intensity)).astype(np.float32)

        # remap the original pixels to the new waving coordinates
        wave_frame = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

        # Subtle lighting shimmer for the 'muscle' look
        shimmer = int((np.sin(phase) + 1) * 3)
        wave_frame = cv2.add(wave_frame, (shimmer, shimmer, shimmer, 0))

        out.write(wave_frame)
        
    out.release()
    print(f"[SYSTEM] Video saved as {OUTPUT_VIDEO}. Go get some sleep, Brandon.")

if __name__ == "__main__":
    create_patriot_video()