import matplotlib.pyplot as plt


def plot_z_scores(z_a, z_b, dept_a, dept_b, r_val, output_path="motif_zscores.png"):
    """
    Generate grouped bar chart of Z-scores for Triad Classes 1-13
    comparing Department A and Department B, with dashed lines at +/-2
    and R included in the title.
    """
    classes = list(range(1, 14))
    width = 0.38

    x_a = [c - width / 2 for c in classes]
    x_b = [c + width / 2 for c in classes]

    plt.figure(figsize=(12, 6))
    plt.bar(x_a, z_a, width=width, label=f"Department {dept_a} (A)")
    plt.bar(x_b, z_b, width=width, label=f"Department {dept_b} (B)")

    plt.axhline(2, color="red", linestyle="--", linewidth=1.2, label="Motif threshold (+2)")
    plt.axhline(-2, color="blue", linestyle="--", linewidth=1.2, label="Anti-motif threshold (-2)")
    plt.axhline(0, color="black", linewidth=0.8)

    plt.xticks(classes)
    plt.xlabel("Triad Class (1-13)")
    plt.ylabel("Z-Score")
    plt.title(f"Network Motif Z-Scores: Dept {dept_a} vs Dept {dept_b} (R = {r_val})")
    plt.legend()
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved chart to {output_path}")
