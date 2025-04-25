# 🏥✨ ICD-10 Medical Condition Classifier

**Automate the coding of free-text medical conditions into accurate ICD-10 codes—turning messy healthcare text into structured, analysis-ready data.**

---

## 🤔 Why This Project?

In healthcare, patient and clinician notes about medical conditions are rarely standardized. These free-text descriptions make it hard to:
- Compare or aggregate data
- Integrate with billing, analytics, or research systems
- Keep up with custom codeplans that change over time

Manual coding is time-consuming and inconsistent, especially as clients’ codeplans frequently evolve.  
To address this, I built a tool that leverages the **universal ICD-10 system**—an internationally accepted standard for disease classification.

---

## ℹ️ What is ICD-10?

**ICD-10** (International Classification of Diseases, 10th Revision) is the global standard for coding diseases, symptoms, and health conditions.  
- Every concept, from broad to ultra-specific, has its own code (e.g., “J45” for Asthma, “J45.9” for Asthma, unspecified).
- The **tree-like hierarchy** makes it possible to code anything from general categories to precise subtypes—enabling robust analytics and easy mapping to local codeplans.

---

## 🧩 Why Was This Challenging?

ICD-10 is not just a list—it’s a **complex, multi-level tree structure**. For example:
- Codes branch out into subcategories and sub-subcategories.
- A precise diagnosis often sits several layers deep in the tree.

**Challenge for Small LLMs:**  
- **Navigating the Hierarchy:**  
  Small and medium language models (LLMs) often struggle to “walk the tree” and choose the *most specific* applicable code.  
  They may:
  - Stick to broad, parent categories (e.g., “J45” instead of “J45.9”)
  - Miss subtypes, making the data less useful for analytics and mapping
- **Ambiguous or Multi-condition Inputs:**  
  Patients often list several issues together, use abbreviations, or describe symptoms vaguely.
  LLMs must **split**, **understand**, and **assign** multiple codes correctly.
- **Prompt Limitations:**  
  Even with engineered prompts, smaller models have limited memory/context and can lose detail when faced with messy, real-world answers.

**Example:**  
> “ADHS und Asthma” (ADHD and asthma)

Ideal model output:  
```
ICD-10 Code(s): [F98.80, J45.9]
```
A weaker model may only output:  
```
ICD-10 Code(s): [F98, J45]
```
(losing critical detail).

---

## 🚦 Project Solution: How I Solved It

1. **LLM-Powered Classification:**  
   Used the Meta-Llama-3.1-8B model with carefully crafted prompts to:
   - Encourage selection of *the most specific* ICD-10 code(s)
   - Support multiple codes for answers with more than one condition
   - Handle both German and English input
2. **Smart Batch Processing:**  
   - Users upload a CSV with `"Condition"` or `"vartext"` columns.
   - The app processes each entry, returning the best-match ICD-10 codes in a new `Vorschlag_ICD10` column.
3. **Accessible UI:**  
   - Streamlit web app makes file upload, processing, and download simple—no coding required.
4. **Ready for Codeplan Mapping:**  
   - ICD-10 serves as a stable “bridge”—easy to re-map as custom codeplans evolve.

---

## 🌟 Features

- **Handles entire datasets**—no manual entry
- **Supports multilingual, complex input**
- **Outputs precise ICD-10 codes for each answer**
- **Plug-and-play: CSV in, CSV out**
- **Ready for integration with downstream analytics or mapping**

---

## 🧑‍💻 How to Use

```sh
git clone https://github.com/yourusername/icd10-medical-condition-classifier.git
cd icd10-medical-condition-classifier
pip install -r requirements.txt
# Add your Together API key to .env
streamlit run app.py
```
1. Upload your CSV (`Condition` or `vartext` column required)
2. See instant ICD-10 suggestions in the `Vorschlag_ICD10` column
3. Download your labeled file for further analysis or mapping

---

## 💡 Example

**Input:**

| Condition                  |
|----------------------------|
| ADHS und Asthma            |
| Diabetes mellitus Typ 2    |
| Rückenschmerzen            |

**Output:**

| Condition                  | Vorschlag_ICD10       |
|----------------------------|-----------------------|
| ADHS und Asthma            | [F98.80, J45.9]       |
| Diabetes mellitus Typ 2    | [E11.9]               |
| Rückenschmerzen            | [M54.9]               |

---

## ⚖️ Why Use ICD-10 as a Bridge?

- **Universal:** Globally recognized and accepted
- **Granular:** Covers both broad and specific categories
- **Adaptable:** Easy mapping to any internal or client codeplan—even as codeplans change

---

## 🚩 Project Status

**Production-ready:**  
A robust, accessible solution for converting free-text medical answers into structured, ICD-10-coded data, fit for mapping and analytics.