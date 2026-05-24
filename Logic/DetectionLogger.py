from datetime import datetime

class DetectionLogger:

    def write_log(self, message, log_file="network.log"):
        """
        logs threat predictions to a text file with a timestamp.

        Args:
            message (str): The log message.
            log_file (str): Name of the log file.
        """
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as file:
            file.write(f"[{timestamp}] {message}\n")