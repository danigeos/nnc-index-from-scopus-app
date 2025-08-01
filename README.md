readme_content = """# 📊 NNC Calculator for Scopus Author Profiles

This Streamlit app calculates the **Número Normalizado de Citas (NNC)** for an author based on their publication list exported from a Scopus author profile.

---

## 📘 What is NNC?

**NNC (Número Normalizado de Citas)** is a metric that estimates an author's contribution to each publication, taking into account:

- The number of citations (NC)
- The author's position in the author list (n)
- The total number of authors (N)

### 📐 Formula

The NNC for a publication is calculated as:

\\[
\\text{NNC} = \\frac{NC \\cdot (2 - \\sum_{i=1}^{N} 2^{-i})}{2^n}
\\]

Where:
- `NC`: Number of citations (from Scopus)
- `n`: Position of the author in the list (1-based)
- `N`: Total number of authors

---

## 🚀 Features

- 📥 Upload one or more CSV files exported from a Scopus **author profile** ("Export all").
- 🔍 Automatically detects the most frequent author in each file.
- 📈 Calculates:
  - Number of citations (Scopus)
  - Author position and number of co-authors
  - NNC for each publication
  - Total NNC for the author
- 📊 Displays a comparative summary table across authors.
- 📄 Shows the list of publications for the last uploaded file.
- 💾 Allows downloading the results as a CSV file.

---

## 🖥️ Local Setup

1. Clone this repository:


