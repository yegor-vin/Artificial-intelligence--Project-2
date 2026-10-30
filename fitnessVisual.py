import matplotlib.pyplot as plt


def plotFitness(histories, maxFitness, selection, mutation,  saveTo=None):
    n = len(histories)
    fig, axes = plt.subplots(n, 1, figsize=(9, 3.5 * n), squeeze=False)

    for ax, (popSize, (minArr, meanArr, maxArr)) in zip(axes[:, 0], histories.items()):
        gens = range(len(maxArr))
        ax.plot(gens, maxArr, label="max")
        ax.plot(gens, meanArr, label="mean")
        ax.plot(gens, minArr, label="min", alpha=0.5)
        ax.axhline(maxFitness, linestyle="-", color="gray", label="optimum")
        ax.set_title(f"Population {popSize} ({selection}), ({mutation})")
        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness")
        ax.legend()
        ax.grid(alpha=0.3)

    fig.tight_layout()
    if saveTo:
        fig.savefig(saveTo, dpi=150)


def plotComparison(histories, maxFitness, selection, mutation, saveTo=None):
    fig, (axMax, axMean) = plt.subplots(1, 2, figsize=(12, 4))

    for popSize, (minArr, meanArr, maxArr) in histories.items():
        axMax.plot(maxArr, label=f"pop {popSize}")
        axMean.plot(meanArr, label=f"pop {popSize}")

    for ax, title in ((axMax, "Max fitness"), (axMean, "Mean fitness")):
        ax.axhline(maxFitness, linestyle="-", color="gray")
        ax.set_title(f"{title} ({selection}) ({mutation})")
        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness")
        ax.legend()
        ax.grid(alpha=0.3)

    fig.tight_layout()
    if saveTo:
        fig.savefig(saveTo, dpi=150)
