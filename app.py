import streamlit as st
import pandas as pd
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()

# ---- Configuration ----
TOGETHER_API_KEY = os.getenv("API_KEY")  # Add API key
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K"
SAFETY_MODEL = "meta-llama/Meta-Llama-Guard-3-8B"
MAX_TOKENS = 4000

# Initialize Together AI client
client = Together(api_key=TOGETHER_API_KEY)

# ---- Function: Classify Medical Conditions Using Optimized Prompt ----
def classify_medical_condition(vartext):
    """Uses LLaMA to classify medical conditions into ICD-10 codes (supports German)."""
    
    prompt = f"""
    Du bist ein spezialisierter KI-Assistent für medizinische Klassifikationen, insbesondere das ICD-10-System.

    Deine Aufgabe ist es, die folgende medizinische Bedingung in den **genauesten ICD-10-Code(s)** einzustufen.

    **Regeln:**
    - Falls eine **spezifische Unterkategorie existiert**, verwende diese (z. B. "Asthma" → "J45.9" statt nur "J45").
    - Falls mehrere Bedingungen existieren, **gib alle relevanten Codes** an (z. B. "ADHS und Asthma" → "F98.80, J45.9").
    - Gib das Ergebnis ausschließlich im **folgenden Format** zurück:

    **Format:**
    ```
    ICD-10 Code(s): [Code1, Code2, ...]
    ```

    **Jetzt klassifiziere diese Bedingung:**
    **Bedingung:** "{vartext}"
    """

    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content.strip()

# ---- Streamlit UI ----
st.title("📄 ICD-10 Medical Condition Classifier (Multilingual)")
st.write("Upload a CSV file containing medical conditions (`vartext` column) to classify them into ICD-10 codes.")

# ---- File Upload ----
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    st.write("📂 **Processing File...**")

    # Load CSV
    df = pd.read_csv(uploaded_file)

    # Ensure 'vartext' column exists
    if "Condition" not in df.columns:
        st.error("CSV must contain a 'vartext' column!")
    else:
        st.write("🔄 **Classifying medical conditions... This may take a while.**")

        # Apply classification function and overwrite `vartext` column
        df["Vorschlag_ICD10"] = df["Condition"].apply(lambda x: classify_medical_condition(str(x)))

        # ---- Display Results ----
        st.write("✅ **Classification Completed!** Here are the results:")
        st.dataframe(df)

        # ---- Provide Download Button ----
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Processed File",
            data=csv,
            file_name="classified_medical_conditions.csv",
            mime="text/csv"
        )
