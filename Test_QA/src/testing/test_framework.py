import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from ..utils.config import load_config
from .data_collector import DataCollector
from .result_analyzer import ResultAnalyzer
from .visualizer import DataVisualizer
from src.utils.logger import TestLogger


class AmmeterTestFramework:
    def __init__(self, config_path: str = "config/test_config.yaml"):
        self.config = load_config(config_path)
        self.test_id = str(uuid.uuid4())
        self.logger = TestLogger(self.test_id)
        self.data_collector = DataCollector(self.config, self.logger)
        self.result_analyzer = ResultAnalyzer(self.config, self.logger)
        self.visualizer = DataVisualizer(self.config)
        self.logger.info(f"Framework initialized for Test ID: {self.test_id}")
        
    def run_test(self, ammeter_type: str) -> Dict:
        """
        הרצת בדיקה מלאה על אמפרמטר ספציפי
        """
        if ammeter_type not in self.config["ammeters"]:
            # זה יזרוק את השגיאה בthread המרכזי, והטסט יתפוס אותה מיד
            raise KeyError(f"Ammeter type '{ammeter_type}' not found in configuration.")
        # איסוף נתונים
        measurements = self.data_collector.collect_measurements(
            ammeter_type=ammeter_type,
            test_id=self.test_id
        )
        
        # ניתוח התוצאות
        analysis_results = self.result_analyzer.analyze(measurements)

        # יצירת ויזואליזציה
        if self.config["analysis"]["visualization"]["enabled"]:
            self.visualizer.create_visualizations(
                measurements,
                test_id=self.test_id,
                ammeter_type=ammeter_type
            )
            
        # הכנת המטא-דאטה
        metadata = {
            "test_id": self.test_id,
            "timestamp": datetime.now().isoformat(),
            "ammeter_type": ammeter_type,
            "test_duration": self.config["testing"]["sampling"]["total_duration_seconds"],
            "sampling_frequency": self.config["testing"]["sampling"]["sampling_frequency_hz"]
        }
        
        # שמירת התוצאות
        results = {
            "metadata": metadata,
            "measurements": measurements,
            "analysis": analysis_results
        }
        
        self._save_results(results)
        return results

    def _save_results(self, results: Dict) -> None:
        """
        שמירת תוצאות הבדיקה
        """
        import json
        import os
        
        # save_path = self.config["result_management"]["save_path"]
        # filename = f"{save_path}/{results['metadata']['test_id']}.json"
        #
        # os.makedirs(save_path, exist_ok=True)
        # with open(filename, 'w') as f:
        #     json.dump(results, f, indent=4)

        # 1. שליפת נתונים מהמטא-דאטה
        test_id = results['metadata']['test_id']
        ammeter_type = results['metadata']['ammeter_type']

        # 2. בניית נתיב דינמי ומאורגן: results/archive/greenlee/20240101_120000/
        base_path = self.config["result_management"]["save_path"]
        archive_dir = os.path.join(base_path, "archive", ammeter_type, test_id)

        # 3. יצירת כל התיקיות בבת אחת (כולל התיקיות הפנימיות)
        os.makedirs(archive_dir, exist_ok=True)

        # . שמירת ה-JSON בתוך התיקייה הנכונה
        filename = os.path.join(archive_dir, "statistical_report.json")

        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
