import json
import streamlit as st

def parse_and_display_risk(json_str):
    try:
        # Strip markdown backticks if present
        clean_json = json_str.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        
        risk_score = data.get("risk_score", 0)
        risk_level = data.get("risk_level", "Unknown")
        indicators_found = data.get("indicators_found", [])
        indicators_not_found = data.get("indicators_not_found", [])
        verdict = data.get("verdict", "")
        recommendation = data.get("recommendation", "")
        
        # Display badge based on score
        if risk_score <= 39:
            st.success(f"Risk Level: {risk_level} (Score: {risk_score})")
        elif risk_score <= 69:
            st.warning(f"Risk Level: {risk_level} (Score: {risk_score})")
        else:
            st.error(f"Risk Level: {risk_level} (Score: {risk_score})")
            
        st.progress(risk_score / 100.0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Indicators Found")
            if indicators_found:
                for ind in indicators_found:
                    st.write(f"❌ {ind}")
            else:
                st.write("None")
                
        with col2:
            st.subheader("Indicators Not Found")
            if indicators_not_found:
                for ind in indicators_not_found:
                    st.write(f"✅ {ind}")
            else:
                st.write("None")
                
        st.subheader("Verdict")
        st.write(verdict)
        
        st.subheader("Recommendation")
        st.write(recommendation)
        
        return data
    except json.JSONDecodeError:
        st.error("Analysis failed. Please try again.")
        return None
