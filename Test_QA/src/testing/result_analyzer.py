import numpy as np
from typing import List, Dict
from scipy import stats

from src.utils.logger import TestLogger


class ResultAnalyzer:
    def __init__(self, config: Dict, logger: TestLogger):
        self.config = config
        self.metrics = config["analysis"]["statistical_metrics"]
        self.logger = logger

    def analyze(self, measurements: List[Dict]) -> Dict:
        """
        ניתוח סטטיסטי של המדידות
        """
        self.logger.info("Starting statistical analysis of measurements...")
        values = [m["value"] for m in measurements]

        if not values:
            self.logger.error("No measurements found to analyze!")
            return {}

        results = {}

        # חישוב מדדים סטטיסטיים בסיסיים
        if "mean" in self.metrics:
            results["mean"] = float(np.mean(values))
        if "median" in self.metrics:
            results["median"] = float(np.median(values))
        if "std_dev" in self.metrics:
            results["std_dev"] = float(np.std(values))
        if "min" in self.metrics:
            results["min"] = float(np.min(values))
        if "max" in self.metrics:
            results["max"] = float(np.max(values))

        self.logger.debug(f"Basic metrics calculated: Mean={results.get('mean')}, STD={results.get('std_dev')}")
        # ניתוח מתקדם
        results.update(self._advanced_analysis(values))
        
        return results

    def _advanced_analysis(self, values: List[float]) -> Dict:
        """
        ניתוח סטטיסטי מתקדם
        """
        self.logger.debug("Running advanced analysis...")
        advanced_results = {
            "skewness": float(stats.skew(values)),  # א-סימטריה
            "kurtosis": float(stats.kurtosis(values)),  # התפלגות
            "confidence_interval_95": list(stats.t.interval(
                confidence=0.95,
                df=len(values)-1,
                loc=np.mean(values),
                scale=stats.sem(values)
            )),
        }

        # בדיקת נורמליות
        _, normality_p_value = stats.normaltest(values)
        advanced_results["is_normal_distribution"] = bool(normality_p_value > 0.05)

        # זיהוי חריגים
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        outlier_bounds = (q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        outliers = [v for v in values if v < outlier_bounds[0] or v > outlier_bounds[1]]
        advanced_results["outliers_count"] = len(outliers)
        
        return advanced_results

    def identify_best_device(self, all_results: Dict[str, Dict]) -> Dict:
        """
         : זיהוי המכשיר הכי אמין לפי שקלול של דיוק, עקביות וחריגים
        """
        self.logger.info(f"Identifying best device")
        comparison = {}

        for name, report in all_results.items():

            # . עקביות (Precision) - סטיית התקן
            precision_error = report['analysis']['std_dev']

            # 3. אמינות (Reliability) - כמות חריגים
            outlier_penalty = report['analysis']["outliers_count"] * 0.1  # הוספת "קנס" על כל חריג

            # ציון משוקלל (ככל שנמוך יותר - המכשיר טוב יותר)
            total_score = precision_error + outlier_penalty

            comparison[name] = {
                "total_score": total_score,
                "precision": precision_error,
                "outliers": report['analysis']["outliers_count"]
            }
            self.logger.debug(
                f"Device '{name}' Score: {total_score:.4f}, STD: {precision_error:.4f})")
        # המנצח הוא זה עם הציון הנמוך ביותר
        best_device = min(comparison, key=lambda k: comparison[k]["total_score"])
        self.logger.info(f"Winner identified: {best_device} with best overall reliability score.")
        return {"best_device": best_device, "full_comparison": comparison}
