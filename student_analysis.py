"""
Student Performance Analysis – Python Tasks
============================================
Tasks covered:
  1. Load dataset using Pandas
  2. Create average_marks column
  3. Identify top-performing student
  4. Group data by department
  5. Calculate average marks by department
  6. Analyze relationship between attendance and marks
  7. Visualizations: bar chart, column chart, scatter plot
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
# 1. Load Dataset
# ─────────────────────────────────────────────
df = pd.read_csv("students.csv")

print("=" * 55)
print("  STUDENT PERFORMANCE ANALYSIS")
print("=" * 55)
print("\n📋 Task 1 — Raw Dataset")
print(df.to_string(index=False))

# ─────────────────────────────────────────────
# 2. Create average_marks column
# ─────────────────────────────────────────────
df["average_marks"] = df[["math", "science", "programming"]].mean(axis=1).round(2)

print("\n📊 Task 2 — Dataset with Average Marks")
print(df[["student_id","name","department","math","science","programming","attendance","average_marks"]]
      .to_string(index=False))

# ─────────────────────────────────────────────
# 3. Top-performing student
# ─────────────────────────────────────────────
top = df.loc[df["average_marks"].idxmax()]
print("\n🏆 Task 3 — Top-Performing Student")
print(f"   Name       : {top['name']}")
print(f"   Department : {top['department']}")
print(f"   Avg Marks  : {top['average_marks']}")
print(f"   Attendance : {top['attendance']}%")

# ─────────────────────────────────────────────
# 4 & 5. Group by department + avg marks
# ─────────────────────────────────────────────
dept_group = df.groupby("department").agg(
    Students     = ("name", "count"),
    Avg_Math     = ("math", "mean"),
    Avg_Science  = ("science", "mean"),
    Avg_Prog     = ("programming", "mean"),
    Overall_Avg  = ("average_marks", "mean"),
    Avg_Attend   = ("attendance", "mean")
).round(2).reset_index()

print("\n🏛️  Tasks 4 & 5 — Department-wise Analysis")
print(dept_group.to_string(index=False))

# ─────────────────────────────────────────────
# 6. Attendance vs Marks relationship
# ─────────────────────────────────────────────
correlation = df["attendance"].corr(df["average_marks"])
print("\n📈 Task 6 — Attendance vs Average Marks Relationship")
print(f"   Pearson Correlation: {correlation:.4f}")
if correlation > 0.7:
    strength = "Strong positive"
elif correlation > 0.4:
    strength = "Moderate positive"
else:
    strength = "Weak"
print(f"   Interpretation     : {strength} relationship")
print("\n   Student-level breakdown:")
print(df[["name","attendance","average_marks"]]
      .sort_values("attendance", ascending=False)
      .to_string(index=False))

at_risk = df[df["average_marks"] < 60]
print("\n⚠️  At-Risk Students (avg marks < 60)")
if len(at_risk):
    print(at_risk[["student_id","name","department","average_marks","attendance"]]
          .to_string(index=False))
else:
    print("   None")

# ─────────────────────────────────────────────
# 7. Visualizations
# ─────────────────────────────────────────────
COLORS = {
    "CS": "#2E75B6",
    "IT": "#ED7D31",
    "bar": ["#1F3864","#2E75B6","#3A9FD9","#ED7D31","#C00000"],
    "grid": "#E8E8E8",
    "bg":   "#F8F9FA",
}

fig = plt.figure(figsize=(18, 14))
fig.patch.set_facecolor(COLORS["bg"])
fig.suptitle("Student Performance Analysis Dashboard",
             fontsize=16, fontweight="bold", color="#1F3864", y=0.98)

# ── Plot 1: Bar Chart – Student Average Marks ──────────────
ax1 = fig.add_subplot(2, 2, 1)
sorted_df = df.sort_values("average_marks", ascending=False)
bars = ax1.barh(sorted_df["name"], sorted_df["average_marks"],
                color=[COLORS["CS"] if d == "CS" else COLORS["IT"]
                       for d in sorted_df["department"]],
                edgecolor="white", height=0.6)

for bar, val in zip(bars, sorted_df["average_marks"]):
    ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
             f"{val:.2f}", va="center", fontsize=11, fontweight="bold",
             color="#1F3864")

ax1.set_title("Student Average Marks", fontsize=13, fontweight="bold",
              color="#1F3864", pad=12)
ax1.set_xlabel("Average Marks", fontsize=11)
ax1.set_xlim(0, 105)
ax1.axvline(60, color="#C00000", linestyle="--", linewidth=1.5, alpha=0.7,
            label="Pass threshold (60)")
ax1.set_facecolor(COLORS["bg"])
ax1.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
ax1.spines[["top","right"]].set_visible(False)

patch_cs = mpatches.Patch(color=COLORS["CS"], label="CS")
patch_it = mpatches.Patch(color=COLORS["IT"], label="IT")
ax1.legend(handles=[patch_cs, patch_it,
                    plt.Line2D([0],[0], color="#C00000", linestyle="--",
                                linewidth=1.5, label="Pass (60)")],
           fontsize=9, loc="lower right")

# ── Plot 2: Column Chart – Department Performance ──────────
ax2 = fig.add_subplot(2, 2, 2)
subjects = ["Math","Science","Programming","Overall"]
cs_vals = [
    df[df.department=="CS"]["math"].mean(),
    df[df.department=="CS"]["science"].mean(),
    df[df.department=="CS"]["programming"].mean(),
    df[df.department=="CS"]["average_marks"].mean(),
]
it_vals = [
    df[df.department=="IT"]["math"].mean(),
    df[df.department=="IT"]["science"].mean(),
    df[df.department=="IT"]["programming"].mean(),
    df[df.department=="IT"]["average_marks"].mean(),
]

x = np.arange(len(subjects))
w = 0.35
b1 = ax2.bar(x - w/2, cs_vals, w, label="CS", color=COLORS["CS"],
             edgecolor="white", zorder=3)
b2 = ax2.bar(x + w/2, it_vals, w, label="IT", color=COLORS["IT"],
             edgecolor="white", zorder=3)

for bars in [b1, b2]:
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.8,
                 f"{bar.get_height():.1f}",
                 ha="center", va="bottom", fontsize=9, fontweight="bold")

ax2.set_title("Department Performance by Subject", fontsize=13,
              fontweight="bold", color="#1F3864", pad=12)
ax2.set_xticks(x); ax2.set_xticklabels(subjects, fontsize=11)
ax2.set_ylabel("Average Marks", fontsize=11)
ax2.set_ylim(0, 110)
ax2.set_facecolor(COLORS["bg"])
ax2.grid(axis="y", color=COLORS["grid"], linewidth=0.8, zorder=0)
ax2.spines[["top","right"]].set_visible(False)
ax2.legend(fontsize=10)

# ── Plot 3: Scatter – Attendance vs Average Marks ──────────
ax3 = fig.add_subplot(2, 2, 3)
for _, row in df.iterrows():
    color = COLORS["CS"] if row["department"] == "CS" else COLORS["IT"]
    ax3.scatter(row["attendance"], row["average_marks"],
                color=color, s=200, zorder=5, edgecolors="white", linewidths=1.5)
    ax3.annotate(row["name"],
                 (row["attendance"], row["average_marks"]),
                 textcoords="offset points", xytext=(8, 5),
                 fontsize=10, color="#1F3864", fontweight="bold")

# Trend line
m, b_line = np.polyfit(df["attendance"], df["average_marks"], 1)
x_line = np.linspace(df["attendance"].min()-2, df["attendance"].max()+2, 100)
ax3.plot(x_line, m * x_line + b_line, color="#C00000", linestyle="--",
         linewidth=2, label=f"Trend (r={correlation:.2f})", zorder=4)

ax3.set_title("Attendance vs Average Marks (Scatter)", fontsize=13,
              fontweight="bold", color="#1F3864", pad=12)
ax3.set_xlabel("Attendance (%)", fontsize=11)
ax3.set_ylabel("Average Marks", fontsize=11)
ax3.set_facecolor(COLORS["bg"])
ax3.grid(color=COLORS["grid"], linewidth=0.8)
ax3.spines[["top","right"]].set_visible(False)
ax3.legend(handles=[patch_cs, patch_it,
                    plt.Line2D([0],[0], color="#C00000", linestyle="--",
                                linewidth=2, label=f"Trend (r={correlation:.2f})")],
           fontsize=9)

# ── Plot 4: Subject-wise Heatmap ───────────────────────────
ax4 = fig.add_subplot(2, 2, 4)
heat_data = df[["math","science","programming"]].values
heat_df   = df[["math","science","programming"]]
im = ax4.imshow(heat_data, cmap="RdYlGn", aspect="auto", vmin=40, vmax=100)
ax4.set_xticks(range(3)); ax4.set_xticklabels(["Math","Science","Programming"], fontsize=11)
ax4.set_yticks(range(len(df))); ax4.set_yticklabels(df["name"], fontsize=11)
ax4.set_title("Subject-wise Marks Heatmap", fontsize=13,
              fontweight="bold", color="#1F3864", pad=12)
for i in range(len(df)):
    for j in range(3):
        val = heat_data[i, j]
        ax4.text(j, i, str(val), ha="center", va="center",
                 fontsize=12, fontweight="bold",
                 color="white" if val < 65 else "#1F3864")
plt.colorbar(im, ax=ax4, label="Marks")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("student_performance_charts.png", dpi=150,
            bbox_inches="tight", facecolor=COLORS["bg"])
print("\n✅ Charts saved as 'student_performance_charts.png'")
plt.show()

# ─────────────────────────────────────────────
# Summary Report
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  SUMMARY REPORT")
print("=" * 55)
print(f"  Total Students    : {len(df)}")
print(f"  Class Avg Marks   : {df['average_marks'].mean():.2f}")
print(f"  Top Performer     : {top['name']} ({top['average_marks']})")
print(f"  Best Department   : {dept_group.loc[dept_group.Overall_Avg.idxmax(),'department']}")
print(f"  Attendance-Marks  : Correlation = {correlation:.4f} ({strength})")
print(f"  At-Risk Students  : {len(at_risk)} ({', '.join(at_risk['name'].tolist()) if len(at_risk) else 'None'})")
print("=" * 55)
