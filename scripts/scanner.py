import cv2
import numpy as np
import os
import time
from collections import defaultdict
from scripts.constants import verbose

def load_reference_images(directory):
    reference_images = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):

            img_path = os.path.join(directory, filename)
            image = cv2.imread(img_path)

            if image is None:
                continue

            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            h, _ = image_gray.shape
            image_gray = image_gray[:h//2, :]

            reference_images[filename] = image_gray

    return reference_images


def detect_card(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    card_contour = None
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 1000:
            continue

        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and area > max_area:
            max_area = area
            card_contour = approx

    if card_contour is not None:
        x, y, w, h = cv2.boundingRect(card_contour)
        cropped_card = gray[y:y+h, x:x+w]

        cropped_card = cropped_card[:h//2, :]

        return cropped_card, (x, y, w, h)
    
    return None, None

def run(interface=1):
    cap = cv2.VideoCapture(interface)
    if not cap.isOpened():
        print("[scanner::error] could not open video capture")
        return
    
    reference_images = load_reference_images("sources")
    match_counts = defaultdict(int)
    past_detections = []
    tracking_active = False
    start_time = None
    display_text = "Press 's' to start matching and 'q' to quit."
    price_text = ""

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        height, _, _ = frame.shape
        frame = frame[0:int(height*0.8), :]

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            tracking_active = True
            match_counts.clear()
            start_time = time.time()
            display_text = "Loading..."
            price_text = "$0.00"
        
        if tracking_active:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, 5 - elapsed_time)
            display_text = f"Loading... {remaining_time:.1f}s"
            price_text = "..."

            detected_card, bbox = detect_card(frame)

            if bbox is not None:
                x, y, w, h = bbox
                overlay = frame.copy()
                cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 255, 0), -1)
                alpha = 0.3
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
            
            if detected_card is not None and detected_card.size > 0:
                match, kp1, kp2, matches = compare_images_advanced(detected_card, reference_images)

                if match:
                    if verbose:
                        print("[scanner::verbose] detected:", match)
                    match_counts[match] += 1

                    if kp1 and kp2 and matches:
                        ref_image = reference_images[match]
                        matched_image = cv2.drawMatches(detected_card, kp1, ref_image, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

                        cv2.imshow("Matches", matched_image)
            
            if elapsed_time >= 5:
                if match_counts:
                    best_match = max(match_counts, key=match_counts.get)
                    display_text = f"Detected: {best_match.split('.')[0]}"
                    price_text = get_price(best_match.split('.')[0])
                    past_detections.append((best_match.split('.')[0], price_text))
                else:
                    display_text = "No matches found."
                    price_text = "NA"

                match_counts.clear()
                tracking_active = False
        
        cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, price_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Video Output", frame)

        history_frame = np.zeros((500, 400, 3), dtype=np.uint8)
        for i, (card, price) in enumerate(past_detections[-10:]):
            cv2.putText(history_frame, f"{card}: {price}", (10, 30 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Detected Cards", history_frame)

        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def compare_images_advanced(image, reference_images):
    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(image, None)
    
    best_match = None
    best_inliers = 0
    best_kp1, best_kp2, best_matches = None, None, None
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    
    for name, ref_image in reference_images.items():
        if ref_image is None:
            continue
        
        kp2, des2 = orb.detectAndCompute(ref_image, None)

        if des2 is None:
            continue
        
        raw_matches = matcher.knnMatch(des1, des2, k=2)
        
        good_matches = []
        for m, n in raw_matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        
        inliers = 0

        if len(good_matches) >= 4:
            pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
            pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])
            _, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
            if mask is not None:
                inliers = int(mask.sum())
        
        if inliers > best_inliers:
            best_inliers = inliers
            best_match = name
            best_kp1, best_kp2, best_matches = kp1, kp2, good_matches

    return best_match, best_kp1, best_kp2, best_matches

def get_price(match):
    try:
        with open(f"sources/{match}.txt", "r") as f:
            price = f.read().strip()
            return price
        
    except FileNotFoundError:
        return "Price not available"