import numpy as np
def gwo_optimize(fitness_func, wolf_population, max_iteration, solution_dimention, lb, ub):
    alpha_positon = np.zeros(solution_dimention)
    alpha_score = float("inf")
    beta_positon = np.zeros(solution_dimention)
    beta_score = float("inf")
    delta_positon = np.zeros(solution_dimention)
    delta_score = float("inf")

    positions = np.random.uniform(lb, ub, (wolf_population, solution_dimention))
    fitness_history = []

    for t in range(max_iteration):
        
        #pengecekan nilai fitness posisi setiap serigala terhadap fungsi objective
        for i in range(wolf_population):
            fitness = fitness_func(positions[i])

            #memilih alpha, beta, dan delta baru
            if fitness < alpha_score:
                alpha_score = fitness
                alpha_positon = positions[i].copy()
            elif fitness < beta_score:
                beta_score = fitness
                beta_positon = positions[i].copy()
            elif fitness < delta_score:
                delta_score = fitness
                delta_positon = positions[i].copy()
        
        #variabel "a" dikurangi secara linear dari 2 hingga bernilai 0 seiring iterasi
        a = 2 - t * (2 / max_iteration)

        #proses merubah posisi setiap serigala
        for i in range(wolf_population):
            for j in range(solution_dimention):
                r1, r2 = np.random.rand(), np.random.rand() #randomisasi nilai r1 dan r2 dalam range [0,1]
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha_positon[j] - positions[i][j]) #jarak serigala ke-i dengan Alpha dalam dimensi j
                X1 = alpha_positon[j] - A1 * D_alpha #posisi serigala ke-i baru berdasarkan pengaruh Alpha

                r1, r2 = np.random.rand(), np.random.rand()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta_positon[j] - positions[i][j]) #jarak serigala ke-i dengan Beta dalam dimensi j
                X2 = beta_positon[j] - A2 * D_beta #posisi serigala ke-i baru berdasarkan pengaruh Beta

                r1, r2 = np.random.rand(), np.random.rand()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta_positon[j] - positions[i][j]) #jarak serigala ke-i dengan Delta dalam dimensi j
                X3 = delta_positon[j] - A3 * D_delta #posisi serigala ke-i baru berdasarkan pengaruh Delta

                #merubah posisi ke-j dari serigala ke-i dari rata-rata posisi yang disarankan/dipengaruhi oleh Alpha, Beta, Delta
                positions[i][j] = (X1 + X2 + X3) / 3

            #menetapkan posisi serigala agar tetap pada range boundarie
            positions[i] = np.clip(positions[i], lb, ub)

        #mencatat nilai fitness terbaik setiap iterasi
        fitness_history.append(alpha_score)

    return alpha_positon, alpha_score, fitness_history