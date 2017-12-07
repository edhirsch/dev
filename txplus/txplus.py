import os, sys, subprocess
import random
from txplus.constants import *
from time import sleep

class TxPlus(object):
    def __init__(self,
                 download_app=None,
                 download_args=None,
                 download_folder = None,
                 download_port = None,
                 upload_time = None,
                 scan_folder = None,
                 scan_interval = None,
                 ):

            self.download_folder = download_folder or DEFAULT_DOWNLOAD_FOLDER
            self.download_app = download_app or DEFAULT_DOWNLOAD_APP
            self.download_args = download_args or DEFAULT_DOWNLOAD_APP_ARGS
            self.download_port = download_port
            self.upload_time = upload_time or DEFAULT_UPLOAD_TIME
            self.scan_folder = scan_folder or DEFAULT_SCAN_FOLDER
            self.scan_interval = scan_interval or DEFAULT_SCAN_INTERVAL

            self.torrent = None


    def download(self,
                 torrent_path
                 ):

        self.torrent = torrent_path

        print("Building the download command..")
        command = "{} -w {} -p {} {} {} 2>&1".format(self.download_app,
                                          self.download_folder,
                                          self.download_port or str(random.randint(33000,55000)),
                                          self.download_args or "",
                                          self.torrent
        )
        print(command)
        command_l = command.split()
        process = subprocess.Popen(command_l, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        last_line = ""
        for line in iter(process.stdout.readline, ""):
            line = line.replace('\n', '')
            if line[:14] != last_line[:14]: # Check and print line if the progress percentage changed
                print(line)
            if line.__contains__("Seeding, uploading to"):
                print("Download finished. Uploading for {} seconds "
                      "and stopping the process.".format(self.upload_time))
                sleep(self.upload_time)
                break
            last_line = line
        process.kill()




