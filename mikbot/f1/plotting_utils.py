from io import BytesIO
from matplotlib import pyplot as plt


def fig_to_file(fig) -> BytesIO:
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer


def create_plot(
        data: list[tuple],
        title: str,
        x_label: str,
        y_label: str,
) -> tuple:
    fig, ax = plt.subplots()
    for x, y, label in data:
        ax.plot(x, y, label=label)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    return fig, ax
