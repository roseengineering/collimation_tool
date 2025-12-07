#!/usr/bin/env -S uv run --with opencv-python,pygame,numpy
"exec" "uv" "run" "--with" "opencv-python,pygame,numpy" "$0" "$@"

import cv2
import pygame
import argparse
import numpy as np
import sys

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def parse_args():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=formatter_class,
        description="collimation circle tool")
    parser.add_argument('--device', type=int, default=0, help='video device number')
    return parser.parse_args()

def main():
    args = parse_args()
    cap = cv2.VideoCapture(args.device)
    if not cap.isOpened():
        return

    # Native Camera Resolution
    cam_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cam_x = cam_w // 2
    cam_y = cam_h // 2

    pygame.init()
    pygame.display.set_caption("Collimation Helper")
    
    # Window settings (Resizable)
    win_w, win_h = 800, 600
    screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    color = (0, 255, 0)
    pan_x = 0         # Offset from center X (pixels)
    pan_y = 0         # Offset from center Y (pixels)
    pan_speed = 1     # Speed of panning
    zoom_speed = 0.1  # Speed of zooming
    scale_factor = 5
    running = True
    last_pos = None
    zoom_level = 2.0  # 1.0 = 100%, 2.0 = 200%

    while running:
        min_zoom = win_h / win_w * cam_w / cam_h
        min_zoom = max(min_zoom, 1 / min_zoom)
        zoom_level = max(zoom_level, min_zoom)

        view_w = int(cam_w / zoom_level)
        view_h = int(win_h / win_w * view_w)
        view_w = min(view_w, cam_w)
        view_h = min(view_h, cam_h)

        keys = pygame.key.get_pressed()
        scale = scale_factor if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1

        if keys[pygame.K_LEFT]:   pan_x += pan_speed * scale
        if keys[pygame.K_RIGHT]:  pan_x -= pan_speed * scale
        if keys[pygame.K_UP]:     pan_y += pan_speed * scale
        if keys[pygame.K_DOWN]:   pan_y -= pan_speed * scale
        if keys[pygame.K_EQUALS]: zoom_level += zoom_speed * scale
        if keys[pygame.K_MINUS]:  zoom_level -= zoom_speed * scale

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # X button on window
                running = False
            
            elif event.type == pygame.VIDEORESIZE:
                zoom_level *= win_w / event.w
                win_w, win_h = event.w, event.h
                # screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r:
                    zoom_level = 1.0
                    pan_x = 0
                    pan_y = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    last_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left mouse button
                    last_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if last_pos:
                    pan_x += (last_pos[0] - event.pos[0]) / zoom_level
                    pan_y += (last_pos[1] - event.pos[1]) / zoom_level
                    last_pos = event.pos

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom_level += zoom_speed * scale
                else:
                    zoom_level -= zoom_speed * scale

        zoom_level = clamp(zoom_level, 1.0, 100.0)

        ret, frame = cap.read()
        if ret:
            # prepare cam surface
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_transposed = np.transpose(frame_rgb, (1, 0, 2))
            raw_surface = pygame.surfarray.make_surface(frame_transposed)

            # determine top-left position of view within cam image
            view_x = (cam_x - (view_w // 2)) + int(pan_x)
            view_y = (cam_y - (view_h // 2)) + int(pan_y)

            # keep view within cam image
            view_x = clamp(view_x, 0, cam_w - view_w)
            view_y = clamp(view_y, 0, cam_h - view_h)

            # crop subsurface
            roi_rect = pygame.Rect(view_x, view_y, view_w, view_h)
            cropped_surface = raw_surface.subsurface(roi_rect)

            # scale to Window
            final_surface = pygame.transform.scale(
                cropped_surface, (win_w, win_h))
            screen.blit(final_surface, (0, 0))

            # draw info text
            font = pygame.font.SysFont(None, 24)
            img = font.render(f"Zoom: {zoom_level:.1f}x | Pan: {pan_x:.0f},{pan_y:.0f}", True, color)
            screen.blit(img, (10, 10))
            
            # draw Reticle
            pygame.draw.line(screen, color, (win_w//2, 0), (win_w//2, win_h), 1)
            pygame.draw.line(screen, color, (0, win_h//2), (win_w, win_h//2), 1)

            radius = max(100, min(win_w, win_h) // 2)
            steps = 10
            for r in range(radius // steps, radius, radius // steps):
                pygame.draw.circle(screen, color, (win_w//2, win_h//2), r, 1)

            pygame.display.flip()
        
        clock.tick(60)

    cap.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


