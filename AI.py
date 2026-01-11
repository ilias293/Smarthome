from data import energie_totaal, douche_minuten, lamp_minuten

def cor(x, y): #Correlatie functie van AI OPDR2

    gemiddeldex = sum(x) / len(x)
    gemiddeldey = sum(y) / len(y)

    teller = 0
    for xi, yi in zip(x, y):
        teller += (xi - gemiddeldex) * (yi - gemiddeldey)

    kwadraatx = 0
    kwadraaty = 0

    for xi in x:
        kwadraatx += (xi - gemiddeldex) ** 2

    for yi in y:
        kwadraaty += (yi - gemiddeldey) ** 2

    if kwadraatx == 0 or kwadraaty == 0:
        return 0.0

    r = teller / ((kwadraatx * kwadraaty) ** 0.5)
    return r

r_douche = cor(douche_minuten, energie_totaal)
r_lampen = cor(lamp_minuten, energie_totaal)

print("Correlatie douche vs energie:", r_douche)
print("Correlatie lampen vs energie:", r_lampen)

import matplotlib.pyplot as plt

# Scatterplot: douche vs energie
plt.figure(figsize=(8, 5))
plt.scatter(douche_minuten, energie_totaal, color='blue', alpha=0.7)
plt.xlabel("Douche minuten per dag")
plt.ylabel("Energieverbruik per dag (kWh)")
plt.title("Spreidingsdiagram: Douchegebruik vs Energieverbruik")
plt.grid(True)
plt.show()

# Scatterplot: lampen vs energie
plt.figure(figsize=(8, 5))
plt.scatter(lamp_minuten, energie_totaal, color='green', alpha=0.7)
plt.xlabel("Lampen minuten per dag")
plt.ylabel("Energieverbruik per dag (kWh)")
plt.title("Spreidingsdiagram: Lampgebruik vs Energieverbruik")
plt.grid(True)
plt.show()

#Gradient_descent functie
def gradient_descent(x, y, num_iterations=1000, learning_rate=0.00001):
    n = len(x)
    coefficients = [0, 0]
    for _ in range(num_iterations):
        grad_a = 0
        grad_b = 0
        for i in range(n):
            error = (coefficients[0] + coefficients[1] * x[i]) - y[i]
            grad_a += 2 * error
            grad_b += 2 * error * x[i]

        coefficients[0] -= learning_rate * grad_a / n
        coefficients[1] -= learning_rate * grad_b / n

    return coefficients

coeffs = gradient_descent(douche_minuten, energie_totaal,
                          num_iterations=20000,
                          learning_rate=0.0001)

a = coeffs[0]
b = coeffs[1]

print("Intercept (a):", a)
print("Helling (b):", b)

import matplotlib.pyplot as plt

def predict(x, a, b):
    return a + b * x

plt.figure(figsize=(8, 5))
plt.scatter(douche_minuten, energie_totaal, color='blue', alpha=0.7, label='Data')

min_x = min(douche_minuten)
max_x = max(douche_minuten)
line_xs = [min_x, max_x]
line_ys = [predict(min_x, a, b), predict(max_x, a, b)]

plt.plot(line_xs, line_ys, color='red', label='Regressielijn')

plt.xlabel("Douche minuten per dag")
plt.ylabel("Energieverbruik per dag (kWh)")
plt.title("Lineaire regressie: Douchegebruik vs Energieverbruik")
plt.grid(True)
plt.legend()
plt.show()

