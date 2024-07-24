import os
class ValidatePaths:
    
    def validate(source_path: str, replica_path: str, log_path: str): 
        """ Validate the paths
            If source_path doesn't exist raises an error
            For the replica_path and log_path creates them if they don't exist

            Parameters:
                source_path: source path of folder to be scanned
                replica_path: destination path of scanned folder
                log_path: log file path to store logs information
        """
        if not os.path.exists(source_path):
            raise ValueError(f"Source directory '{source_path}' does not exist.")
        
        if not os.path.exists(replica_path):
            os.makedirs(replica_path)
    
        if not os.path.exists(log_path):
            with open(log_path, 'w') as log_file:
                log_file.write("Log file created.\n")