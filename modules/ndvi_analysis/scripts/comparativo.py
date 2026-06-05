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
        'med': 0.4023,
        'q1': 0.2380,
        'q3': 0.5923,
        'whislo': 0.0919,
        'whishi': 0.7397
    }
]

fig, ax = plt.subplots()

ax.bxp(stats, showfliers=False)

ax.set_ylabel("NDVI")
ax.set_title("Comparative Analysis of NDVI Distributions")
ax.grid(True)

plt.show()