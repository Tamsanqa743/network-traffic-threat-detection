from datetime import datetime
import random

class DetectionLogger:

    def write_log(self, message, log_id, log_file="network.log"):

        """
        logs threat predictions to a text file with a timestamp.

        Args:
            message (str): The log message.
            log_file (str): Name of the log file.
        """
        ip = f"{random.randint(100, 192)}.{random.randint(1, 169)}.{random.randint(1, 80)}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as file:
            file.write(f"[{timestamp}] {log_id}      {message} {ip}\n")