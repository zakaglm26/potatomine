import cv2
from pathlib import Path

video_path = Path(__file__).resolve().parent / "potatos.mp4"


def open_video(path: Path) -> cv2.VideoCapture:
	cap = cv2.VideoCapture(str(path))
	if cap.isOpened():
		return cap

	# Fallback: try forcing a backend (helps on some Windows setups/codecs)
	for api in (getattr(cv2, "CAP_FFMPEG", None), getattr(cv2, "CAP_MSMF", None), getattr(cv2, "CAP_DSHOW", None)):
		if api is None:
			continue
		cap2 = cv2.VideoCapture(str(path), api)
		if cap2.isOpened():
			return cap2

	return cap


video = open_video(video_path)
if not video.isOpened():
	raise SystemExit(f"Could not open video: {video_path}")

# nombre total de frames
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# fps de la vidéo
fps = video.get(cv2.CAP_PROP_FPS)

duration = None
if fps and fps > 0:
	duration = total_frames / fps
else:
	# Best-effort fallback: seek to end and read timestamp.
	# Some files/codecs don't expose FPS via OpenCV.
	video.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
	pos_msec = video.get(cv2.CAP_PROP_POS_MSEC)
	if pos_msec and pos_msec > 0:
		duration = pos_msec / 1000.0

print("Nombre de frames :", total_frames)
print("FPS :", fps)
print("Durée (secondes) :", duration if duration is not None else "unknown")

video.release()