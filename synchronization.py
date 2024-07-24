import os
import shutil
import logging
from time import sleep
import stat

from validate_paths import ValidatePaths
from log_config import LogConfiguration

class Synchronization:

    def __init__(self, source_path : str, replica_path : str, synchro_interval : int, log_path : str):
        """ Constructor of class Synchronization stores the paths
        
            Parameters:
                source_path: source path of folder to be scanned
                replica_path: destination path of scanned folder
                synchro_interval: interval that the folder is going to be synchronized in seconds
                log_path: log file path to store logs information
        """
        self.source_path      = source_path
        self.replica_path     = replica_path
        self.synchro_interval = synchro_interval
        self.log_path         = log_path

    #class main
    def start_periodic_synchronization(self):
        """ Cycle that allows of the folder be synchronize with a respective interval """
        while True:
            self.synchronize()   
            sleep(self.synchro_interval)

    def synchronize(self):
        """ Synchronize the respective folder to the replica
            implies create and delete files and folders """
        try:
            # Synchronize files and directories
            self.sync_directory(self.source_path, self.replica_path)
            
        
        except Exception as e:
            raise ValueError(f"Error during synchronization cycle: {e}")
        try:
            # Synchronize files and directories
            self.remove_extraneous_files_and_dirs(self.source_path, self.replica_path)
            
        
        except Exception as e:
            raise ValueError(f"Error during synchronization cycle removal: {e}")

            

    def sync_directory(self, source: str, replica: str):
        """
        Sync files and directories from source to replica.

        Parameters:
            source: source path of folder to be scanned
            source: destination path of scanned folder
        """
        if not os.path.exists(replica):
            os.makedirs(replica)
            self.display_info(f"Created directory '{replica}'")

        for item in os.listdir(source):
            source_item = os.path.join(source, item)
            replica_item = os.path.join(replica, item)

            if os.path.isdir(source_item):
                self.sync_directory(source_item, replica_item)
            else:
                self.sync_file(source_item, replica_item)

    def sync_file(self, source_file: str, replica_file: str):
        """
        Sync a single file from source to replica.

        Parameters:
            source_file: source path of file to be scanned
            replica_file: destination path of scanned file
        """
        if not os.path.exists(replica_file) or \
           os.path.getmtime(source_file) > os.path.getmtime(replica_file) or \
           os.path.getsize(source_file) != os.path.getsize(replica_file):
            shutil.copy2(source_file, replica_file)
            self.display_info(f"Copied file '{source_file}' to '{replica_file}'")
            

    

    def remove_extraneous_files_and_dirs(self, source: str, replica: str):
        """
        Remove files and directories from replica that are not in the source.
        Parameters:
                    source: source path of external files and directories to be scanned
                    replica: destination path of scanned files and directories
        
        """
        for item in os.listdir(replica):
            replica_item = os.path.join(replica, item)
            source_item = os.path.join(source, item)

            if not os.path.exists(source_item):
                try:
                    if os.path.isdir(replica_item):
                        shutil.rmtree(replica_item, onerror=self.remove_readonly)
                        self.display_info(f"Removed directory '{replica_item}'")
                    else:
                        os.remove(replica_item)
                        self.display_info(f"Removed file '{replica_item}'")
                except PermissionError as e:
                    raise ValueError(f"Permission error: {e}")
                except Exception as e:
                    raise ValueError(f"Error: {e}")


    #Util methods
    def remove_readonly(self, func, path, exc_info):
        """ Removes the access of read-only"""
        if exc_info[0] is PermissionError:
            os.chmod(path, stat.S_IWRITE)
            func(path)

    def display_info(self,string: str):
        """
            Prints string to console
            Logs information to log file
        """
        print(string)
        logging.info(string)
        

