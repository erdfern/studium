import math
import numpy as np
from matplotlib import pyplot as plt

# 1
def fac(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer `n`.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        return 1
    else:
        return n * fac(n - 1)


print(fac(4))
print(fac(5))
print(25)


# 2
def sin_approx(x: float, lim: int = 10) -> float:
    """
    Approximates sin(x) by calculating the sum representation of sin up to the given limit.
    """
    return sum(
        (-1) ** n * x ** (2 * n + 1) / fac(2 * n + 1) for n in range(0, lim)
    )


# 3

# Input values (in radians)
x_values = np.linspace(-2 * math.pi, 2 * math.pi, num=10)

sin_values = [math.sin(x) for x in x_values]

for x, y in zip(x_values, sin_values):
    print(f"sin({x:.2f}): {y:.4f}")

# 4
# Sample Input values
x_values = np.linspace(-2 * math.pi, 2 * math.pi, num=42)

# Compare for different 'limit' values
for limit in [5, 10, 25, 50]:
    print(f"\nComparison with limit = {limit}")
    errors = []
    for x in x_values:
        approx_value = sin_approx(x, limit)
        true_value = math.sin(x)
        error = abs(approx_value - true_value)
        errors.append(error)
        # print(f"x: {x:.2f}, Approx: {approx_value:.4f}, True: {true_value:.4f}, Error: {error:.5f}")
    print(f"Avg error: {np.average(errors)}, Median: {np.median(errors)}")

# 5
x = [i * 0.01 for i in range(1001)]
# 6
lim = 13
y = [sin_approx(x, lim) for x in x]

# 7 - Plotting the results
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.xlabel("x", fontsize=12)
plt.ylabel(f"sin_approx(x, {lim})", fontsize=12)
plt.title(f"Approximation of sin(x) using limit={lim}", fontsize=14)
plt.grid(True)
plt.show()

# 8 - Plotting for different limits and comparison
limits = [5, 10, 25]  # Limits to compare
colors = ["red", "green", "blue"]

plt.figure(figsize=(8, 6))
plt.plot(
    x, [math.sin(i) for i in x], label="sin(x)", color="black"
)  # Actual sin(x)

for lim, col in zip(limits, colors):
    y_approx = [sin_approx(i, lim) for i in x]
    plt.plot(x, y_approx, label=f"Limit {lim}", color=col)

plt.xlabel("x", fontsize=12)
plt.ylabel("sin(x) / Approximation", fontsize=12)
plt.title("Approximation of sin(x) for different limits", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

# 9 - Comparing two limits in different ranges
lim1, lim2 = 13, 11
x1 = x[: len(x) // 2]  # Range [0 to 5)
x2 = x[len(x) // 2 :-1]  # Range [5 to 10)

y1 = [sin_approx(i, lim1) for i in x1]
y2 = [sin_approx(i, lim2) for i in x2]

plt.figure(figsize=(8, 6))
plt.plot(x1, y1, label=f"Limit {lim1}", color="blue")
plt.plot(x2, y2, label=f"Limit {lim2}", color="red")
plt.xlabel("x", fontsize=12)
plt.ylabel("sin_approx(x)", fontsize=12)
plt.title(
    "Comparison of sin(x) approximation for different limits", fontsize=14
)
plt.xlim([0, 10])
plt.legend()
plt.grid(True)
plt.show()
