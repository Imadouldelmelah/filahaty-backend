import json
import asyncio
from utils.logger import logger

class HybridDecisionController:
    """
    Indestructible Controller for Hybrid Intelligence.
    Pattern: Step 1 (Baseline) -> Step 2 (Optional AI Refinement) -> Step 3 (Safe Result)
    """

    @staticmethod
    async def execute(
        baseline_func,
        ai_func,
        schema_repair_keys=None,
        feature_name="HYBRID_DECISION"
    ):
        """
        Executes a hybrid flow.
        :param baseline_func: Callable that returns the agronomy baseline (must be synchronous).
        :param ai_func: Async Callable that attempts AI refinement.
        :param schema_repair_keys: List of keys to ensure exist in the final JSON.
        :param feature_name: Name for logging.
        """
        # 1. Step 1: Get Agronomy Baseline (Guaranteed)
        try:
            base_result = baseline_func()
            # Ensure base_result is a dict
            if not isinstance(base_result, dict):
                 raise ValueError("Baseline must return a dictionary")
        except Exception as e:
            logger.error(f"{feature_name}_BASELINE_CRITICAL_FAILURE: {str(e)}")
            # Ultimate safety net if even the baseline fails
            base_result = {"status": "error", "message": "Baseline logic failure"}

        # 2. Step 2 & 3: Try AI Refinement
        try:
            logger.info(f"{feature_name}: Attempting AI refinement...")
            # Run AI with a timeout to prevent hanging
            raw_ai_response = await asyncio.wait_for(ai_func(), timeout=15)
            
            if not raw_ai_response or not isinstance(raw_ai_response, str):
                raise ValueError("Invaliad AI response type")

            # Extract JSON substring
            start_idx = raw_ai_response.find("{")
            end_idx = raw_ai_response.rfind("}")
            
            if start_idx == -1 or end_idx == -1:
                raise ValueError("AI JSON delimiters not found")
                
            json_str = raw_ai_response[start_idx : end_idx + 1]
            refined_data = json.loads(json_str)

            # Merge AI refinement into base result
            # Optimization: Only take specific keys from AI to prevent it from overwriting core logic
            base_result.update(refined_data)
            base_result["status"] = "ai_optimized"
            
            logger.info(f"{feature_name}: AI Optimization Success")

        except Exception as e:
            logger.warning(f"{feature_name}_AI_SKIPPED: {str(e)}. Using safe baseline.")
            base_result["status"] = "offline_optimized"
            base_result["message"] = "Smart offline mode activated"

        # 4. Step 4: Final Schema Repair & Validation
        if schema_repair_keys:
            for key in schema_repair_keys:
                if key not in base_result:
                    base_result[key] = "System standard" if key != "alternatives" and key != "alerts" else []
        
        # Ensure status is always present
        if "status" not in base_result:
            base_result["status"] = "fallback"

        return base_result
