from random import uniform


def linspace(start, stop, n):
    """Like numpy.linspace, generate a list of <n> values from <start> to <stop>.

    Arguments:
        start (Number): Minimum value of sequence.
        stop (Number): Maximum value of sequence.
        n (int): Number of values to produce between start and stop (inclusive).

    Returns:
        List of values.
    """

    total = stop - start
    step = total / (n - 1)
    results = []
    for i in range(n):
        results.append(start + i * step)
    return results


def randomize(values, amount):
    """Randomize the values in a list by <amount>.

    Arguments:
        values (list): List of numbers to randomize.
        amount (Number): Amount to vary numbers by

    Returns:
        List of randomized values.
    """

    return [v + uniform(-amount, amount) * 0.5 for v in values]
