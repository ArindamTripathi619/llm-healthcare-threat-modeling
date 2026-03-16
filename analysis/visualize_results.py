import pandas as pd
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt
import os
import sys

# Increase recursion depth just in case (though venv_new might solve it)
sys.setrecursionlimit(10000)

# Paths
INPUT_CSV = "logs/metric_report_raw.csv"
OUTPUT_DIR = "../"

def add_labels(ax):
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='center', 
                   xytext=(0, 9), 
                   textcoords='offset points',
                   fontsize=10, fontweight='bold')

def visualize():
    print("Loading data...")
    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} not found.")
        return

    df = pd.read_csv(INPUT_CSV)
    
    # FIG 5: Defense Effectiveness across categories
    print("Generating Figure 5...")
    attack_df = df[df['category'] != 'benign']
    # Use explicit ordering to match final_metrics.md
    categories = ['direct_injection', 'indirect_injection', 'medical_safety', 'role_confusion']
    category_group = attack_df.groupby('category')['pass'].mean() * 100
    category_group = category_group.reindex(categories).fillna(0)
    
    plt.figure(figsize=(10, 6))
    ax = category_group.plot(kind='bar', color=['#2E7D32', '#C62828', '#C62828', '#C62828'])
    add_labels(ax)
    
    plt.title("Defense Effectiveness Across Attack Categories (Block Rate %)")
    plt.ylabel("Block Rate (%)")
    plt.xlabel("Attack Category")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylim(0, 110) # Room for labels
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "figure_5.png"), dpi=300)
    plt.close()
    print("Saved figure_5.png")

    # FIG 6: Semantic Camouflage / Signal Dilution Effect
    print("Generating Figure 6...")
    dilution_data = {
        "Direct Probe\n(N=6)": 80.0,
        "Polymorphic Payload\n(N=100)": 21.33
    }
    
    plt.figure(figsize=(8, 6))
    names = list(dilution_data.keys())
    values = list(dilution_data.values())
    bars = plt.bar(names, values, color=['#1976D2', '#D32F2F'])
    
    # Add labels for plt.bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.2f}%', 
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title("Semantic Camouflage Effect (Signal Dilution)")
    plt.ylabel("Block Rate (%)")
    plt.ylim(0, 110)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "figure_6.png"), dpi=300)
    plt.close()
    print("Saved figure_6.png")

if __name__ == "__main__":
    visualize()
