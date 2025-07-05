import numpy as np

"""
Hyperparameter Setting
- Inertia (w)
- Cognition of particle (C1)
- Social influence of swarm (C2)
"""

"""
PSO INIT POPULATION
Partikel 1: x = (1.0, -2.0), v = (0.0, 0.0)
Partikel 2: x = (-3.0, 1.5), v = (0.0, 0.0)
Partikel 3: x = (0.5, 0.5), v = (0.0, 0.0)
Partikel 4: x = (4.0, -1.0), v = (0.0, 0.0)
Partikel 5: x = (-1.0, 3.0), v = (0.0, 0.0)
"""

"""
GWO INIT POPULATION
Serigala 1: x = (1.0, -2.0)
Serigala 2: x = (-3.0, 1.5)
Serigala 3: x = (0.5, 0.5)
Serigala 4: x = (4.0, -1.0)
Serigala 5: x = (-1.0, 3.0)
"""

w : float =  0.7
c1 : float = 2.0
c2 : float = 2.0

init_pos = np.array([
    [1.0, -2.0],
    [-3.0, 1.5],
    [0.5, 0.5],
    [4.0, -1.0],
    [-1.0, 3.0]
])



class Particle:
    def __init__(self, solution_dimension, init_pos):
        self.position = init_pos
        self.best_position = self.position
        self.best_score = float("inf")
        self.velocity =  np.zeros(solution_dimension)


def particle_swarm_optimizer(fitness_func, particle_population, max_iteration, solution_dimension, lb, ub):
    global_best_position = np.zeros(solution_dimension)
    global_best_score = float("inf")

    # v_max = 0.1 * np.abs(ub - lb)
    # v_min = -v_max
    
    particles = [Particle (solution_dimension, init_pos[i]) for i in range(particle_population)]

    
    fitness_history = []

    for i in range(particle_population):
        particles[i].best_score = fitness = fitness_func(particles[i].position)
        if fitness < global_best_score:
            global_best_score = fitness
            global_best_position = particles[i].position.copy()


    for t in range(max_iteration):
        """Get new velocity and update the position"""
        for i in range(particle_population):
            for j in range (solution_dimension):
                r1, r2 = np.random.rand(), np.random.rand()
                #update velocity of j particle
                particles[i].velocity[j] = (w * particles[i].velocity[j]) + (r1*c1*(particles[i].best_position[j] - particles[i].position[j])) + (r2*c2*(global_best_position[j] - particles[i].position[j]))

                #update position of j solution of i particle
                particles[i].position[j] += particles[i].velocity[j]
            particles[i].position = np.clip(particles[i].position, lb, ub)

        """Calculate best position"""
        for i in range(particle_population):
            fitness = fitness_func(particles[i].position)
            if fitness < particles[i].best_score:
                particles[i].best_score = fitness
                particles[i].best_position = particles[i].position.copy()
            if fitness < global_best_score:
                global_best_score = fitness
                global_best_position = particles[i].position.copy()

        fitness_history.append(global_best_score)
    
    return global_best_position, global_best_score, fitness_history


        
if __name__ == "__main__":
    # Test with a simple sphere function: f(x) = sum(x^2)
    def sphere_function(x):
        return np.sum(x**2)
    
    # Test with 2D problem
    best_pos, best_score, history = particle_swarm_optimizer(
        fitness_func=sphere_function,
        particle_population=5,
        max_iteration=5,
        solution_dimension=2,
        lb=-5.12,
        ub=5.12
    )
    
    print(f"Best position: {best_pos}")
    print(f"Best score: {best_score:.4f}")
    for i, fitness in enumerate(history):
        print(f"Iteration {i}: {fitness:.4f}")

