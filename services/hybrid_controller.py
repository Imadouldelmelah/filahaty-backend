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
        protected_keys=None,
        feature_name="HYBRID_DECISION"
    ):
        """
        Executes a hybrid flow.
        :param baseline_func: Callable that returns the agronomy baseline (must be synchronous).
        :param ai_func: Async Callable that attempts AI refinement.
        :param schema_repair_keys: List of keys to ensure exist in the final JSON.
        :param protected_keys: List of keys that MUST be preserved from the baseline (AI cannot overwrite).
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
            
            # TASK 1: Detect failure scenarios
            if not raw_ai_response or not isinstance(raw_ai_response, str) or raw_ai_response.strip() == "":
                raise ValueError("Empty or invalid AI response")
                
            if "AI_ERROR_FALLBACK" in raw_ai_response:
                raise ValueError("AI Service Credits Exhausted or Unauthorized")

            # Since GeminiService guarantees valid JSON (or fallback JSON), we can parse directly.
            try:
                refined_data = json.loads(raw_ai_response)
            except json.JSONDecodeError:
                logger.error(f"{feature_name}: JSONDecodeError trying to parse AI result. Fallback triggered. Content: {raw_ai_response[:100]}")
                raise ValueError("Malformed AI JSON: Parsing failed")

            # Merge AI refinement into base result
            if protected_keys:
                # Remove protected keys from AI data to prevent overwrite
                for p_key in protected_keys:
                    if p_key in refined_data:
                        logger.info(f"{feature_name}: Blocking AI overwrite of protected key '{p_key}'")
                        del refined_data[p_key]

            base_result.update(refined_data)
            base_result["status"] = "ai_optimized"
            
            logger.info(f"{feature_name}: AI Optimization Success")

        except Exception as e:
            logger.warning(f"{feature_name}_AI_SKIPPED: {str(e)}. Using safe baseline.")
            base_result["status"] = "offline_optimized"
            base_result["message"] = "Smart offline mode activated"

        # 4. Step 4: Final Schema Repair & Validation (Guaranteed No Nulls)
        if schema_repair_keys:
            for key in schema_repair_keys:
                # Catch both MISSING keys and NULL values
                if key not in base_result or base_result[key] is None:
                    logger.info(f"{feature_name}: Repairing missing or null key '{key}'")
                    base_result[key] = "System standard" if key not in ["alternatives", "alerts", "tasks"] else []
        
        # Final pass: Ensure NO Top-Level null values in the result
        for key, value in base_result.items():
            if value is None:
                base_result[key] = ""
        
        # Ensure status is always present
        if "status" not in base_result:
            base_result["status"] = "fallback"

        return base_result
