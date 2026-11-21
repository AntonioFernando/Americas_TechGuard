
import matplotlib.pyplot as plt

stats = [
    {
        'label': 'Recife',
        'med': 0.2573,
        'q1': 0.1226,
        'q3': 0.5669,
        'whislo': -0.2781,
        'whishi': 0.8487
    },
    {
        'label': 'Fort Lauderdale',
        'med': 0.5422,
        'q1': 0.3201,
        'q3': 0.7511,
        'whislo': 0.1227,
        'whishi': 0.8665
    }
]

fig, ax = plt.subplots(figsize=(8, 5))

ax.bxp(stats, showfliers=False)

ax.set_ylabel("NDVI")
ax.set_title("Comparative Analysis of NDVI Distributions")
ax.grid(True)

plt.tight_layout()
plt.show()
