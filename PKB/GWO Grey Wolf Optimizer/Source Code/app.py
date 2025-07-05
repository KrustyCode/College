import streamlit as st
import matplotlib.pyplot as plt
from gwo import gwo_optimize
from objective import shifted_sphere_function, rosenbrock_function, shifted_sphere_boundaries, rosenbrock_boundaries

st.title("🐺Grey Wolf Optimization - Two Objective Comparison")

wolf_population = st.number_input("Jumlah Serigala", min_value=5, value=5)
max_iteration = st.number_input("Jumlah Iterasi", min_value=10, value=10)
solution_dimention = st.number_input("Dimensi Solusi", min_value=1, value=1)

objective_options = ["Rosenbrock", "Shifted Sphere", "Keduanya"]
selected_objective = st.selectbox("Pilih Fungsi Objektif yang ingin dijalankan", objective_options)

shifted_sphere_lb, shifted_sphere_ub = shifted_sphere_boundaries()
rosenbrock_lb, rosenbrock_ub = rosenbrock_boundaries()

if st.button("Jalankan Optimasi"):
    if selected_objective in ["Shifted Sphere", "Keduanya"]:
        st.subheader("1. Shifted Sphere Function")
        best_pos1, best_fit1, history1 = gwo_optimize(shifted_sphere_function, wolf_population, max_iteration, solution_dimention, shifted_sphere_lb, shifted_sphere_ub)
        st.write(f"Nilai terbaik: {best_fit1:.4f}")
        with st.container(height=300):
            st.markdown("Fitness tiap iterasi:")
            st.code("\n".join(f"Iterasi {i+1}: {val:.6f}" for i, val in enumerate(history1)), language="text")

    if selected_objective in ["Rosenbrock", "Keduanya"]:
        st.subheader("2. Rosenbrock Function")
        best_pos2, best_fit2, history2 = gwo_optimize(rosenbrock_function, wolf_population, max_iteration, solution_dimention, rosenbrock_lb, rosenbrock_ub)
        st.write(f"Nilai terbaik: {best_fit2:.4f}")
        with st.container(height=300):
            st.markdown("Fitness tiap iterasi:")
            st.code("\n".join(f"Iterasi {i+1}: {val:.6f}" for i, val in enumerate(history2)), language="text")

    fig, ax = plt.subplots()
    if selected_objective in ["Shifted Sphere", "Keduanya"]:
        ax.plot(history1, label="shifted Sphere")
    if selected_objective in ["Rosenbrock", "Keduanya"]:
        ax.plot(history2, label="Rosenbrock")

    ax.set_xlabel("Iterasi")
    ax.set_ylabel("Fitness")
    ax.set_title("Konvergensi GWO")
    ax.legend()
    st.pyplot(fig)


