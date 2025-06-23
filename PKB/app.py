import streamlit as st
import matplotlib.pyplot as plt
from gwo import gwo_optimize
from objective import shifted_sphere_function, rosenbrock

st.title("🐺Grey Wolf Optimization - Two Objective Comparison")

wolf_population = st.number_input("Jumlah Serigala", min_value=5, value=5)
max_iteration = st.number_input("Jumlah Iterasi", min_value=10, value=10)
solution_dimention = st.number_input("Dimensi Solusi", min_value=2, value=2)

if st.button("Jalankan Optimasi"):
    st.subheader("1. Shifted Sphere Function")
    best_pos1, best_fit1, history1 = gwo_optimize(shifted_sphere_function, wolf_population, max_iteration, solution_dimention)
    st.write(f"Nilai terbaik: {best_fit1:.4f}")

    st.subheader("2. Rosenbrock Function")
    best_pos2, best_fit2, history2 = gwo_optimize(rosenbrock, wolf_population, max_iteration, solution_dimention)
    st.write(f"Nilai terbaik: {best_fit2:.4f}")

    fig, ax = plt.subplots()
    ax.plot(history1, label="Shifted Sphere")
    ax.plot(history2, label="Rosenbrock")
    ax.set_xlabel("Iterasi")
    ax.set_ylabel("Fitness")
    ax.set_title("Konvergensi GWO")
    ax.legend()
    st.pyplot(fig)
