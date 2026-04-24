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
        Executes a hybrid flow. PRIORITIZES AI first.
        """
        # 1. Attempt AI Refinement FIRST
        try:
            logger.info(f"{feature_name}: Ensuring AI is called first...")
            # Relaxed timeout for better normal response flow
            response = await asyncio.wait_for(ai_func(), timeout=20)
            
            if response and len(response) > 0:
                refined_data = None
                try:
                    # 1. Clean response (Strip potential markdown code blocks)
                    cleaned_response = response.strip()
                    if cleaned_response.startswith("```"):
                        # Remove first line if it's a fence
                        lines = cleaned_response.split("\n")
                        if lines[0].startswith("```"): lines = lines[1:]
                        if lines and lines[-1].startswith("```"): lines = lines[:-1]
                        cleaned_response = "\n".join(lines).strip()
                    
                    # 2. Try direct parse
                    try:
                        refined_data = json.loads(cleaned_response)
                    except json.JSONDecodeError:
                        # 3. Safe Extraction: Find first '{' and last '}'
                        start_idx = cleaned_response.find("{")
                        end_idx = cleaned_response.rfind("}")
                        
                        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                            json_str = cleaned_response[start_idx:end_idx + 1]
                            refined_data = json.loads(json_str)
                except Exception as parse_error:
                    logger.warning(f"{feature_name}: JSON Extraction failed: {str(parse_error)}")
                    refined_data = None
                
                if refined_data:
                    # Get baseline only to fill missing fields if needed, but return AI result
                    try:
                        base_result = baseline_func()
                    except:
                        base_result = {}
                        
                    # Merge and protect keys
                    if protected_keys:
                        for p_key in protected_keys:
                            if p_key in refined_data: del refined_data[p_key]
                    
                    base_result.update(refined_data)
                    base_result["status"] = "ai_optimized"
                    return base_result

            raise Exception("AI response empty or invalid")

        except Exception as e:
            # 2. ONLY fallback if REAL EXCEPTION
            logger.warning(f"{feature_name}_AI_FAILover: {str(e)}. Falling back to local rules.")
            try:
                base_result = baseline_func()
                # Status and internal logging should be enough for debugging
                base_result["status"] = "rule_based_fallback"
            except Exception as inner_e:
                logger.error(f"{feature_name}_CRITICAL_FAIL: {str(inner_e)}")
                base_result = {"status": "error", "error_type": "logic_failure"}

        # 3. Final Schema Repair
        if schema_repair_keys:
            for key in schema_repair_keys:
                if key not in base_result or base_result[key] is None:
                    base_result[key] = "System standard" if key not in ["alternatives", "alerts", "tasks"] else []
        
        for key, value in base_result.items():
            if value is None: base_result[key] = ""
            
        if "status" not in base_result: base_result["status"] = "fallback"

        return base_result
