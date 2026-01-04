
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import r2_score

# 1. Read World bank CSV
df = pd.read_csv("WorldBank.csv")

# 2. Perform conditional selection
# Filter for Country: India and Indicator: Population ages 15-64 (% of total population)
indicator_name = "Population ages 15-64 (% of total population)"
df_india = df[(df["Country Name"] == "India") & (df["Indicator Name"] == indicator_name)]

# 3. Data Preprocessing
# Extract years and values
# Years are from columns 1960 to 2019 (2020 consists of NaN based on earlier view)
years = np.array([str(y) for y in range(1960, 2020)])
# Extract the values for these years. 
# We need to flatten values to match the years shape. 
# df_india[years] returns a dataframe, we want values.
values = df_india[years].values.flatten()


# Ensure we have numeric data and drop NaNs if any
# Convert years to integers for regression
X = years.astype(int).reshape(-1, 1)
y = values.astype(float).reshape(-1, 1)

# Handle potential NaNs at the end (2020 was NaN, let's remove any NaN in our chosen range)
mask = ~np.isnan(y).flatten()
X = X[mask]
y = y[mask]

print(f"Data shape after cleaning: X={X.shape}, y={y.shape}")

# 4. Feature Scaling (Mandatory for SVR)
sc_X = StandardScaler()
sc_y = StandardScaler()
X_scaled = sc_X.fit_transform(X)
y_scaled = sc_y.fit_transform(y)

print("Scaling Complete.")

# 5. Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# 6. Fitting SVR on 3 Different Kernels
kernels = ['linear', 'poly', 'rbf']
models = {}
results = {}

plt.figure(figsize=(15, 5))

for i, kernel in enumerate(kernels):
    # Train
    svr = SVR(kernel=kernel)
    svr.fit(X_train, y_train.ravel())
    models[kernel] = svr
    
    # Predict
    # We predict on the sorted X range for plotting smooth curves
    X_plot = np.sort(X_scaled, axis=0)
    y_pred_plot = svr.predict(X_plot)
    
    # Score
    train_score = svr.score(X_train, y_train.ravel())
    test_score = svr.score(X_test, y_test.ravel())
    results[kernel] = {'train': train_score, 'test': test_score}
    
    print(f"Kernel: {kernel}, Train R2: {train_score:.4f}, Test R2: {test_score:.4f}")

    # Visualization
    plt.subplot(1, 3, i+1)
    
    # Inverse transform for plotting to see real values
    X_plot_inv = sc_X.inverse_transform(X_plot)
    y_pred_plot_inv = sc_y.inverse_transform(y_pred_plot.reshape(-1, 1))
    X_inv = sc_X.inverse_transform(X_scaled)
    y_inv = sc_y.inverse_transform(y_scaled)
    
    plt.scatter(X_inv, y_inv, color='red', label='Data', s=10)
    plt.plot(X_plot_inv, y_pred_plot_inv, color='blue', label=f'SVR {kernel}')
    plt.title(f'SVR {kernel}\nTest R2: {test_score:.2f}')
    plt.xlabel('Year')
    plt.ylabel('Population % (15-64)')
    plt.legend()

plt.tight_layout()
plt.savefig('svr_results.png')
print("Plot saved to svr_results.png")
