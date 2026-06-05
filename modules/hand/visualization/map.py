import matplotlib.pyplot as plt
import contextily as cx


def plot(gdf, title="Mapa"):
    fig, ax = plt.subplots(figsize=(10, 10))

    gdf.to_crs(3857).plot(
        ax=ax,
        edgecolor="black",
        alpha=0.6
    )

    cx.add_basemap(ax)

    ax.set_axis_off()
    ax.set_title(title)

    plt.show()