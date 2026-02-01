import time
from typing import List, Dict
import threading
import queue
from Ammeters.client import request_current_from_ammeter
from src.utils.logger import TestLogger


class DataCollector:
    def __init__(self, config: Dict, logger: TestLogger):
        self.config = config
        self.measurement_queue = queue.Queue()
        self.logger = logger
        
    def collect_measurements(self, ammeter_type: str, test_id: str) -> List[Dict]:
        """
        איסוף מדידות מהאמפרמטר
        """
        measurements = []
        sampling_config = self.config["testing"]["sampling"]
        
        # חישוב מרווח הזמן בין דגימות
        interval = 1.0 / sampling_config["sampling_frequency_hz"]
        total_measurements = sampling_config["measurements_count"]
        
        # הפעלת תהליכון נפרד לדגימה
        sampling_thread = threading.Thread(
            target=self._sampling_worker,
            args=(ammeter_type, interval, total_measurements)
        )
        sampling_thread.start()
        
        # איסוף התוצאות
        for _ in range(total_measurements):
            measurement = self.measurement_queue.get()
            measurements.append({
                "timestamp": time.time(),
                "value": measurement,
                "test_id": test_id
            })
            
        sampling_thread.join()
        return measurements
        
    def _sampling_worker(self, ammeter_type: str, interval: float, total_measurements: int):
        """
        עובד שאוסף את המדידות בתהליכון נפרד
        """
        ammeter_config = self.config["ammeters"][ammeter_type]

        for _ in range(total_measurements):
            start_time = time.time()
            
            # קבלת מדידה מהאמפרמטר
            # כאן צריך להשתמש בקוד הקיים של האמפרמטרים
            measurement = self._get_measurement(ammeter_type, ammeter_config)
            self.logger.debug(f"Successfully received data from {ammeter_type}: {measurement}A")

            self.measurement_queue.put(measurement)
            
            # המתנה עד לדגימה הבאה
            elapsed = time.time() - start_time
            if elapsed < interval:
                time.sleep(interval - elapsed)
                self.logger.debug(f"Sleep for: {interval - elapsed} seconds")

    def _get_measurement(self, ammeter_type: str, config: Dict) -> float:
        """
        קבלת מדידה מהאמפרמטר הספציפי
        """
        # כאן צריך לממש את הקריאה לאמפרמטר הספציפי
        # using existing ammeter code

        port = config['port']
        command = config['command'].encode('utf-8')

        try:
            value_str = request_current_from_ammeter(port, command)

            if value_str:
                return float(value_str)
            return 0.0
        except Exception as e:
            self.logger.error(f"Error collecting measurement from {ammeter_type}: {e}")
            return 0.0
