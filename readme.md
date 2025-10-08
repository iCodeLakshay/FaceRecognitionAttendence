
# FaceRecognitionAttendence

Small Python utility that uses a webcam to detect known faces and mark attendance in a CSV file named by the current date (YYYY-MM-DD.csv).

## What this does
- Loads face templates from the `faces/` folder (configure image file names in `main.py`).
- Starts the webcam and detects faces in real-time.
- When a known face is seen, the person's name and current time are appended to `YYYY-MM-DD.csv` (and the person is recorded only once per run).

## Requirements
- Python 3.10+ (3.13 used in development here).
- A working webcam.
- The project uses the `face_recognition` library which depends on `dlib` and other packages that can be tricky to install on Windows. Using the included virtual environment (recommended) or conda is easiest.

## Recommended setup (Windows / PowerShell)

1. Create and activate a virtual environment (optional but recommended):

```powershell
# create venv (if you don't have one yet)
python -m venv .venv
# activate it
& .\.venv\Scripts\Activate.ps1
```

2. Install required Python packages into the activated venv:

```powershell
python -m pip install --upgrade pip setuptools
python -m pip install face-recognition opencv-python numpy pillow
# If the program asks for face_recognition_models, install it too:
python -m pip install git+https://github.com/ageitgey/face_recognition_models
```

Note: On Windows you might hit build errors for `dlib`. If that happens, either use `pipwin` to install a prebuilt wheel or use Anaconda/Miniconda and install `dlib`/`face_recognition` from conda-forge. Tell me if you want step-by-step help for that.

## Configure known faces
- By default `main.py` expects image files under the `faces/` folder. Edit the `candidates` list in `main.py` to add your images and display names. Example entries:

```python
candidates = [
	(os.path.join("faces", "lakshay.jpg"), "Lakshay"),
	(os.path.join("faces", "ayush.png"), "Ayush"),
]
```

- Images should contain a single clear frontal face for best results.

## Run the program

Activate the venv (if used) and run:

```powershell
& .\.venv\Scripts\Activate.ps1
python main.py
```

- The webcam window will open. Press `q` to quit.
- Attendance is written to a CSV file in the project root with the current date as filename (e.g., `2025-10-08.csv`). The CSV has columns `Name,Time`.

## Ignore face images from Git
If you don't want the `faces/` folder to be tracked by Git, add `/faces/` to `.gitignore` (project root). If the images are already tracked, remove them from the index but keep them locally:

```powershell
Add-Content -Path .gitignore -Value "`n/faces/"
# remove tracked copies from git index but keep local files
git rm -r --cached faces
git commit -m "Stop tracking faces/ and add to .gitignore"
git push
```

## Troubleshooting
- If you see: "No module named 'face_recognition'" — make sure your venv is activated and that the venv's pip lists `face-recognition`.
- If you see: "Please install `face_recognition_models`..." — run the install command shown above.
- If `dlib` fails to build on Windows, use `pipwin` or conda:

pipwin (PowerShell):
```powershell
python -m pip install pipwin
python -m pipwin install dlib
python -m pip install face-recognition
```

conda (recommended if you already use conda):
```powershell
conda create -n fr python=3.10
conda activate fr
conda install -c conda-forge dlib face_recognition opencv numpy pillow
```

## Notes and improvements
- You can modify the code to automatically load all images from each subfolder under `faces/` and use folder names as labels. I can add that if you'd like.
- Consider doubling-checking privacy/legal requirements before storing or sharing face images.

If you'd like, I can also:
- Add automatic discovery of images in `faces/` and derive names from folder names.
- Add a `requirements.txt` with pinned versions.
- Add a simple UI to pick which images to include.

