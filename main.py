import sys
from synchronization import Synchronization
from validate_paths import ValidatePaths
from log_config import LogConfiguration
def main():

    source_path      = sys.argv[1]
    replica_path     = sys.argv[2]
    synchro_interval = sys.argv[3]
    log_path         = sys.argv[4]

    # Configure log file
    LogConfiguration.config(log_path)
    # Validate paths
    ValidatePaths.validate(source_path, replica_path, log_path)

    sync = Synchronization(source_path, replica_path, int(synchro_interval), log_path)
    sync.start_periodic_synchronization()

if __name__ == '__main__':
    main()