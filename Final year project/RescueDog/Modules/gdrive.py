from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

def upload_to_drive(filepath):
    f = drive.CreateFile({'title': os.path.basename(filepath)})
    f.SetContentFile(filepath)
    f.Upload()
    print(f"✅ Uploaded to Google Drive: {filepath}")
