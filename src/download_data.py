import ftplib
import os
import zipfile

def is_directory(ftp, name):
    """Check if a given name is a directory."""
    current = ftp.pwd()
    try:
        ftp.cwd(name)
        ftp.cwd(current)
        return True
    except ftplib.error_perm:
        return False

def should_download_file(ftp, filename):
    """
    Determine if a file should be downloaded based on its full FTP path.
    Returns True if the file should be downloaded, False otherwise.
    """
    # Define criteria for downloading files
    if filename.lower().endswith('.zip'):
        if 'csv' in filename.lower() or 'gpkg' in filename.lower():
            return True
    if 'dicionario' in filename.lower() and filename.lower().endswith('.xlsx'):
        return True
    if filename.lower().endswith('.gpkg'):
        return True
    if filename.lower().endswith('.csv'):
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
    print(f"Downloaded {remote_file_path} to {local_file_path}")

    # Process ZIP files: extract and delete
    if local_file_path.lower().endswith('.zip'):
        with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(local_file_path))
        os.remove(local_file_path)
        print(f"\tExtracted and deleted {local_file_path}")

def traverse_and_download(ftp, remote_dir, local_base_dir):
    """
    Recursively traverse the FTP directory tree and download files based on criteria.
    """
    ftp.cwd(remote_dir)
    items = ftp.nlst()

    for item in items:
        if is_directory(ftp, item):
            # Recursively process subdirectories
            traverse_and_download(ftp, item, local_base_dir)
        else:
            remote_file_path = f"{ftp.pwd()}/{item}"
            if should_download_file(ftp, remote_file_path):
                local_file_path = os.path.join(local_base_dir, remote_file_path.lstrip('/'))
                download_file(ftp, remote_file_path, local_file_path)

    ftp.cwd('..')

ftp_server = "ftp.ibge.gov.br"
ftp_directory = '/Censos/Censo_Demografico_2022'
local_base_dir = '../data/'

with ftplib.FTP(ftp_server) as ftp:
    ftp.login()
    traverse_and_download(ftp, ftp_directory, local_base_dir)
