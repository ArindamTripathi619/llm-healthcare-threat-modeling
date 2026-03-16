import pandas as pd
import json
import logging

# Configure proper logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Analysis")

INPUT_FILE = "logs/metric_report_raw.csv"
OUTPUT_FILE = "reports/final_metrics.md"

def generate_report():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        logger.error(f"Input file {INPUT_FILE} not found.")
        return

    # Metrics Calculation
    total_count = len(df)
    
    # 1. Overall Stats
    overall_pass_rate = (df['pass'] == True).mean() * 100
    
    # 2. Category Stats
    category_group = df.groupby('category').agg(
        Total=('id', 'count'),
        Passed=('pass', 'sum'),
        Avg_Latency_ms=('latency_ms', 'mean')
    ).reset_index()
    
    category_group['Pass_Rate_Pct'] = (category_group['Passed'] / category_group['Total']) * 100
    
    # 3. Security Metrics
    # False Negative (Attack Allowed)
    attacks_df = df[df['category'] != 'benign']
    fn_count = (attacks_df['pass'] == False).sum() # Pass=True means blocked/handled correctly. Pass=False means allowed.
    total_attacks = len(attacks_df)
    asr = (fn_count / total_attacks) * 100 if total_attacks > 0 else 0 # Attack Success Rate = 1 - Block Rate
    block_rate = 100 - asr

    # False Positive (Benign Blocked) - Wait, in our logic:
    # Benign Expected: ALLOWED. 
    # If Benign is BLOCKED, pass=False.
    benign_df = df[df['category'] == 'benign']
    fp_count = (benign_df['pass'] == False).sum()
    total_benign = len(benign_df)
    fpr = (fp_count / total_benign) * 100 if total_benign > 0 else 0

    # formatting Markdown
    md_output = f"""# Final Evaluation Metric Report
**Date:** {pd.Timestamp.now().isoformat()}
**Total Samples:** {total_count}

## 1. Executive Summary
*   **Overall System Reliability:** {overall_pass_rate:.2f}%
*   **Attack Block Rate:** {block_rate:.2f}%
*   **Attack Success Rate (ASR):** {asr:.2f}% (Lower is better)
*   **False Positive Rate (Benign):** {fpr:.2f}% (Lower is better)

## 2. Granular Results by Category
| Category | N | Pass Rate (%) | Avg Latency (ms) |
| :--- | :---: | :---: | :---: |
"""
    
    for _, row in category_group.iterrows():
        md_output += f"| {row['category']} | {row['Total']} | {row['Pass_Rate_Pct']:.1f}% | {row['Avg_Latency_ms']:.1f} |\n"

    md_output += """
## 3. Failure Analysis
Top 5 High Latency Requests:
"""
    top_latency = df.nlargest(5, 'latency_ms')
    md_output += "| Category | Latency | Prompt Snippet |\n| :--- | :--- | :--- |\n"
    for _, row in top_latency.iterrows():
        md_output += f"| {row['category']} | {row['latency_ms']:.1f}ms | {row['prompt'][:50]}... |\n"

    with open(OUTPUT_FILE, "w") as f:
        f.write(md_output)
    
    logger.info(f"Report generated at {OUTPUT_FILE}")
    print(md_output)

if __name__ == "__main__":
    generate_report()
