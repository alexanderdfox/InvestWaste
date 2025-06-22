import matplotlib.pyplot as plt
import numpy as np

def entropy_payoff_compound(debt_total, initial_entropy_rate, conversion_efficiency, systemic_loss, years=50, compound=False):
	net_efficiency = conversion_efficiency * (1 - systemic_loss)
	
	debt = debt_total
	entropy_rate = initial_entropy_rate
	debt_history = []

	for year in range(years + 1):
		debt_history.append(debt)
		if debt <= 0:
			# Debt fully paid off, stays at zero
			debt = 0
		else:
			annual_net = entropy_rate * net_efficiency
			debt -= annual_net
			if compound:
				entropy_rate += annual_net  # reinvest payoff to increase entropy harvesting
			if debt < 0:
				debt = 0
	return debt_history

# Parameters
debt_initial = 37_000_000_000_000        # $33 trillion
entropy_rate = 2_000_000_000_000         # $2 trillion/year entropy
efficiency = 0.20                        # 20% conversion efficiency
loss = 0.15                             # 15% systemic loss
years = 50

# Calculate debt over time
debt_no_compound = entropy_payoff_compound(debt_initial, entropy_rate, efficiency, loss, years, compound=False)
debt_compound = entropy_payoff_compound(debt_initial, entropy_rate, efficiency, loss, years, compound=True)

# Trump's Plan - assumed constant $775B increase per year
annual_increase = 775_000_000_000
debt_trump = [debt_initial + annual_increase * year for year in range(years + 1)]

# Plotting
plt.figure(figsize=(12, 7))
plt.plot(range(years + 1), np.array(debt_no_compound) / 1e12, label='Entropy Model (No Compounding)', linewidth=2)
plt.plot(range(years + 1), np.array(debt_compound) / 1e12, label='Entropy Model (With Compounding)', linewidth=2)
plt.plot(range(years + 1), np.array(debt_trump) / 1e12, label="Trump Plan Projection (Debt Increase)", linewidth=2)

plt.title('U.S. National Debt Projection Over 50 Years')
plt.xlabel('Years')
plt.ylabel('Debt (Trillions USD)')
plt.ylim(0, max(debt_trump[-1], debt_initial) / 1e12 * 1.2)
plt.grid(True)
plt.legend()
plt.show()
