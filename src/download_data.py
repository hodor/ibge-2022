import ftplib
import os
import zipfile
import json
from tqdm import tqdm

cache_file = '../files_to_download.json' # takes a while to browse data from FTP
download_gpkg = True
download_csv = True
download_xlsx = False
download_dictionaries = True

def is_directory(ftp, name):
    """Check if a given name is a directory."""
    current = ftp.pwd()
    try:
        ftp.cwd(name)
        ftp.cwd(current)
        return True
    except ftplib.error_perm:
        return False

def should_download_file(filename):
    """
    Determine if a file should be downloaded based on its full FTP path.
    Returns True if the file should be downloaded, False otherwise.
    """
    # Define criteria for downloading files
    if filename.lower().endswith('.zip'):
        if (download_csv and 'csv' in filename.lower()) or (download_gpkg and 'gpkg' in filename.lower())\
                or (download_xlsx and 'xlsx' in filename.lower()):
            return True
    if download_dictionaries and 'dicionario' in filename.lower() and filename.lower().endswith('.xlsx'):
        return True
    if download_gpkg and filename.lower().endswith('.gpkg'):
        return True
    if download_csv and filename.lower().endswith('.csv'):
        return True
    if download_xlsx and filename.lower().endswith('.xlsx'):
        return True
    return False

def download_file(ftp, remote_file_path, local_file_path):
    """
    Download a file from the FTP server and process it if necessary.
    """
    # Ensure the local directory exists
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    # Download the file
    with open(local_file_path, 'wb') as local_file:
        ftp.retrbinary(f'RETR {remote_file_path}', local_file.write)

    # Process ZIP files: extract and delete
    if local_file_path.lower().endswith('.zip'):
        with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(local_file_path))
        os.remove(local_file_path)

def traverse_and_collect_files(ftp, remote_dir):
    """
    Recursively traverse the FTP directory tree and collect files to download.
    """
    files_to_download = []
    ftp.cwd(remote_dir)
    items = ftp.nlst()

    for item in items:
        if is_directory(ftp, item):
            # Recursively process subdirectories
            files_to_download.extend(traverse_and_collect_files(ftp, item))
        else:
            remote_file_path = f"{ftp.pwd()}/{item}"
            if should_download_file(remote_file_path):
                files_to_download.append(remote_file_path)

    ftp.cwd('..')
    return files_to_download

def main():
    ftp_server = "ftp.ibge.gov.br"
    ftp_directory = '/Censos/Censo_Demografico_2022'
    local_base_dir = '../data/'

    if os.path.exists(cache_file):
        print(f"Loading list of files to download from {cache_file}...")
        with open(cache_file, 'r') as f:
            files_to_download = json.load(f)
    else:
        with ftplib.FTP(ftp_server) as ftp:
            ftp.login()
            print("Collecting all files that should be downloaded...")
            files_to_download = traverse_and_collect_files(ftp, ftp_directory)
            with open(cache_file, 'w') as f:
                json.dump(files_to_download, f, indent=4)
            ftp.close()

    total_files = len(files_to_download)
    print(f"Total files to download: {total_files}")

    with ftplib.FTP(ftp_server) as ftp:
        ftp.login()
        for remote_file_path in tqdm(files_to_download, desc="Downloading files", unit="file"):
            local_file_path = os.path.join(local_base_dir, remote_file_path.lstrip('/'))
            download_file(ftp, remote_file_path, local_file_path)
        ftp.close()

if __name__ == "__main__":
    main()