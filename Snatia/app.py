import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import ttk, messagebox
import time
import psutil
import os
import threading

class OptimizedNoiseGenerator:
    """Optimized noise function implementations"""
    
    @staticmethod
    def perlin_noise(width, height, scale=0.1, octaves=1, persistence=0.5, lacunarity=2.0, seed=None):
        """Optimized Perlin noise implementation using vectorization"""
        if seed is not None:
            np.random.seed(seed)
        
        def fade(t):
            return t * t * t * (t * (t * 6 - 15) + 10)
        
        def lerp(a, b, t):
            return a + t * (b - a)
        
        # Generate coordinate grids
        x = np.linspace(0, width * scale, width)
        y = np.linspace(0, height * scale, height)
        X, Y = np.meshgrid(x, y)
        
        noise = np.zeros((height, width))
        
        # Create permutation table once
        p = np.arange(256, dtype=int)
        np.random.shuffle(p)
        p = np.tile(p, 2)
        
        for octave in range(octaves):
            freq = lacunarity ** octave
            amp = persistence ** octave
            
            # Scale coordinates
            x_scaled = X * freq
            y_scaled = Y * freq
            
            # Grid coordinates
            x0 = np.floor(x_scaled).astype(int) & 255
            x1 = (x0 + 1) & 255
            y0 = np.floor(y_scaled).astype(int) & 255
            y1 = (y0 + 1) & 255
            
            # Local coordinates
            dx0 = x_scaled - np.floor(x_scaled)
            dx1 = dx0 - 1
            dy0 = y_scaled - np.floor(y_scaled)
            dy1 = dy0 - 1
            
            # Simplified gradient calculation
            u = fade(dx0)
            v = fade(dy0)
            
            # Basic interpolation (simplified for performance)
            n00 = np.random.rand(*x0.shape) - 0.5
            n10 = np.random.rand(*x1.shape) - 0.5
            n01 = np.random.rand(*x0.shape) - 0.5
            n11 = np.random.rand(*x1.shape) - 0.5
            
            nx0 = lerp(n00, n10, u)
            nx1 = lerp(n01, n11, u)
            nxy = lerp(nx0, nx1, v)
            
            noise += nxy * amp
        
        return noise
    
    @staticmethod
    def simplex_noise(width, height, scale=0.1, octaves=1, persistence=0.5, lacunarity=2.0, seed=None):
        """Simplified and optimized Simplex-like noise"""
        if seed is not None:
            np.random.seed(seed)
        
        # Create coordinate grid
        x = np.linspace(0, width * scale, width)
        y = np.linspace(0, height * scale, height)
        X, Y = np.meshgrid(x, y)
        
        noise = np.zeros((height, width))
        
        for octave in range(octaves):
            freq = lacunarity ** octave
            amp = persistence ** octave
            
            # Create multiple offset grids for simplex-like effect
            offset1 = np.sin(X * freq) * np.cos(Y * freq)
            offset2 = np.cos(X * freq * 1.3) * np.sin(Y * freq * 1.7)
            offset3 = np.sin(X * freq * 0.7) * np.sin(Y * freq * 0.9)
            
            combined = (offset1 + offset2 + offset3) / 3.0
            noise += combined * amp
        
        return noise
    
    @staticmethod
    def worley_noise(width, height, scale=0.1, n_points=20, distance_func='euclidean', seed=None):
        """Optimized Worley noise using vectorization"""
        if seed is not None:
            np.random.seed(seed)
        
        # Generate random points
        points = np.random.rand(n_points, 2) * np.array([width, height])
        
        # Create coordinate grids
        x = np.arange(width)
        y = np.arange(height)
        X, Y = np.meshgrid(x, y)
        
        # Initialize with large values
        min_distances = np.full((height, width), float('inf'))
        
        # Calculate distances to all points
        for point in points:
            if distance_func == 'euclidean':
                distances = np.sqrt((X - point[0])**2 + (Y - point[1])**2)
            elif distance_func == 'manhattan':
                distances = np.abs(X - point[0]) + np.abs(Y - point[1])
            elif distance_func == 'chebyshev':
                distances = np.maximum(np.abs(X - point[0]), np.abs(Y - point[1]))
            else:
                distances = np.sqrt((X - point[0])**2 + (Y - point[1])**2)
            
            min_distances = np.minimum(min_distances, distances)
        
        # Apply scale and normalize
        noise = min_distances * scale
        noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
        return noise

class NoiseComparatorGUI:
    """Main GUI class with Tkinter controls and Matplotlib display"""
    
    def __init__(self):
        self.generator = OptimizedNoiseGenerator()
        self.results = {}
        self.is_generating = False
        
        # Parameters
        self.size = 128  # Start with smaller size for performance
        self.scale = 0.1
        self.octaves = 2
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.n_points = 20
        self.distance_func = 'euclidean'
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI with Tkinter controls"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Optimized Noise Function Comparator")
        self.root.geometry("800x700")
        
        # Create control frame
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Size control
        ttk.Label(control_frame, text="Size:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.size_var = tk.StringVar(value=str(self.size))
        ttk.Entry(control_frame, textvariable=self.size_var, width=10).grid(row=0, column=1, padx=5)
        
        # Scale control
        ttk.Label(control_frame, text="Scale:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.scale_var = tk.StringVar(value=str(self.scale))
        ttk.Entry(control_frame, textvariable=self.scale_var, width=10).grid(row=0, column=3, padx=5)
        
        # Octaves control
        ttk.Label(control_frame, text="Octaves:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.octaves_var = tk.StringVar(value=str(self.octaves))
        ttk.Entry(control_frame, textvariable=self.octaves_var, width=10).grid(row=1, column=1, padx=5)
        
        # Persistence control
        ttk.Label(control_frame, text="Persistence:").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.persistence_var = tk.StringVar(value=str(self.persistence))
        ttk.Entry(control_frame, textvariable=self.persistence_var, width=10).grid(row=1, column=3, padx=5)
        
        # Lacunarity control
        ttk.Label(control_frame, text="Lacunarity:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.lacunarity_var = tk.StringVar(value=str(self.lacunarity))
        ttk.Entry(control_frame, textvariable=self.lacunarity_var, width=10).grid(row=2, column=1, padx=5)
        
        # Worley points control
        ttk.Label(control_frame, text="Worley Points:").grid(row=2, column=2, sticky=tk.W, padx=5)
        self.n_points_var = tk.StringVar(value=str(self.n_points))
        ttk.Entry(control_frame, textvariable=self.n_points_var, width=10).grid(row=2, column=3, padx=5)
        
        # Distance function dropdown
        ttk.Label(control_frame, text="Distance Function:").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.distance_var = tk.StringVar(value=self.distance_func)
        distance_combo = ttk.Combobox(control_frame, textvariable=self.distance_var, 
                                    values=['euclidean', 'manhattan', 'chebyshev'], width=12)
        distance_combo.grid(row=3, column=1, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Generate All", command=self.generate_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Benchmark", command=self.run_benchmark).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(control_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=4, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=4, sticky='ew', pady=5)
        
        # Results display frame
        self.results_frame = ttk.Frame(self.root, padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget for results
        self.results_text = tk.Text(self.results_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Setup matplotlib figure
        self.setup_matplotlib()
        
    def setup_matplotlib(self):
        """Setup matplotlib figure for visualization"""
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 10))
        self.fig.suptitle('Noise Function Comparison', fontsize=16)
        
        # Initialize empty plots
        self.images = {}
        noise_types = ['perlin', 'simplex', 'worley', 'comparison']
        positions = [(0,0), (0,1), (1,0), (1,1)]
        titles = ['Perlin Noise', 'Simplex Noise', 'Worley Noise', 'Performance Comparison']
        
        for i, (noise_type, pos, title) in enumerate(zip(noise_types, positions, titles)):
            ax = self.axes[pos[0], pos[1]]
            if i < 3:  # Noise visualizations
                self.images[noise_type] = ax.imshow(np.zeros((64, 64)), cmap='terrain')
                ax.set_title(title)
                ax.set_xticks([])
                ax.set_yticks([])
            else:  # Performance chart
                ax.set_title(title)
                ax.set_xlabel('Noise Type')
                ax.set_ylabel('Time (seconds)')
        
        plt.tight_layout()
        
    def get_parameters(self):
        """Get parameters from GUI inputs with validation"""
        try:
            size = int(self.size_var.get())
            scale = float(self.scale_var.get())
            octaves = int(self.octaves_var.get())
            persistence = float(self.persistence_var.get())
            lacunarity = float(self.lacunarity_var.get())
            n_points = int(self.n_points_var.get())
            distance_func = self.distance_var.get()
            
            # Validation
            if size < 32 or size > 1024:
                raise ValueError("Size must be between 32 and 1024")
            if scale <= 0 or scale > 1:
                raise ValueError("Scale must be between 0 and 1")
            if octaves < 1 or octaves > 10:
                raise ValueError("Octaves must be between 1 and 10")
            if persistence <= 0 or persistence > 1:
                raise ValueError("Persistence must be between 0 and 1")
            if lacunarity < 1 or lacunarity > 5:
                raise ValueError("Lacunarity must be between 1 and 5")
            if n_points < 5 or n_points > 100:
                raise ValueError("Worley points must be between 5 and 100")
                
            return {
                'size': size, 'scale': scale, 'octaves': octaves,
                'persistence': persistence, 'lacunarity': lacunarity,
                'n_points': n_points, 'distance_func': distance_func
            }
        except ValueError as e:
            messagebox.showerror("Parameter Error", str(e))
            return None
    
    def measure_performance(self, func, *args, **kwargs):
        """Measure function performance"""
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        
        return result, {
            'time': end_time - start_time,
            'memory': mem_after - mem_before,
            'peak_memory': mem_after
        }
    
    def generate_all(self):
        """Generate all noise types in separate thread"""
        if self.is_generating:
            return
            
        params = self.get_parameters()
        if params is None:
            return
        
        self.is_generating = True
        self.progress.start()
        self.status_var.set("Generating noise...")
        
        # Run generation in separate thread to avoid GUI freezing
        thread = threading.Thread(target=self._generate_worker, args=(params,))
        thread.daemon = True
        thread.start()
    
    def _generate_worker(self, params):
        """Worker thread for noise generation"""
        try:
            results = {}
            
            # Generate Perlin noise
            self.root.after(0, lambda: self.status_var.set("Generating Perlin noise..."))
            perlin_data, perlin_perf = self.measure_performance(
                self.generator.perlin_noise,
                params['size'], params['size'], params['scale'], 
                params['octaves'], params['persistence'], params['lacunarity']
            )
            results['perlin'] = {'data': perlin_data, 'perf': perlin_perf}
            
            # Generate Simplex noise
            self.root.after(0, lambda: self.status_var.set("Generating Simplex noise..."))
            simplex_data, simplex_perf = self.measure_performance(
                self.generator.simplex_noise,
                params['size'], params['size'], params['scale'],
                params['octaves'], params['persistence'], params['lacunarity']
            )
            results['simplex'] = {'data': simplex_data, 'perf': simplex_perf}
            
            # Generate Worley noise
            self.root.after(0, lambda: self.status_var.set("Generating Worley noise..."))
            worley_data, worley_perf = self.measure_performance(
                self.generator.worley_noise,
                params['size'], params['size'], params['scale'],
                params['n_points'], params['distance_func']
            )
            results['worley'] = {'data': worley_data, 'perf': worley_perf}
            
            # Update GUI in main thread
            self.root.after(0, lambda: self._update_results(results, params))
            
        except Exception as e:
            self.root.after(0, lambda: self._handle_error(str(e)))
    
    def _update_results(self, results, params):
        """Update GUI with results"""
        self.results = results
        
        # Update visualizations
        self.images['perlin'].set_data(results['perlin']['data'])
        self.images['simplex'].set_data(results['simplex']['data'])
        self.images['worley'].set_data(results['worley']['data'])
        
        # Update colormaps
        all_data = [r['data'] for r in results.values()]
        vmin = min(np.min(data) for data in all_data)
        vmax = max(np.max(data) for data in all_data)
        
        for img in self.images.values():
            if hasattr(img, 'set_clim'):
                img.set_clim(vmin=vmin, vmax=vmax)
        
        # Update performance chart
        ax = self.axes[1, 1]
        ax.clear()
        
        names = list(results.keys())
        times = [results[name]['perf']['time'] for name in names]
        
        bars = ax.bar(names, times, alpha=0.7, color=['blue', 'green', 'red'])
        ax.set_title('Generation Time Comparison')
        ax.set_ylabel('Time (seconds)')
        
        # Add value labels on bars
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{time_val:.4f}s', ha='center', va='bottom')
        
        # Update results text
        self._update_results_text(results, params)
        
        # Redraw plots
        self.fig.canvas.draw()
        
        # Update status
        self.progress.stop()
        self.status_var.set("Generation complete!")
        self.is_generating = False
    
    def _update_results_text(self, results, params):
        """Update results text widget"""
        self.results_text.delete(1.0, tk.END)
        
        # Parameters summary
        param_text = f"PARAMETERS:\n"
        param_text += f"Size: {params['size']}x{params['size']}\n"
        param_text += f"Scale: {params['scale']}\n"
        param_text += f"Octaves: {params['octaves']}\n"
        param_text += f"Persistence: {params['persistence']}\n"
        param_text += f"Lacunarity: {params['lacunarity']}\n"
        param_text += f"Worley Points: {params['n_points']}\n"
        param_text += f"Distance Function: {params['distance_func']}\n\n"
        
        # Results summary
        results_text = "RESULTS:\n"
        for name, result in results.items():
            data = result['data']
            perf = result['perf']
            results_text += f"\n{name.upper()} NOISE:\n"
            results_text += f"  Generation Time: {perf['time']:.4f} seconds\n"
            results_text += f"  Memory Usage: {perf['memory']:.2f} MB\n"
            results_text += f"  Data Statistics:\n"
            results_text += f"    Mean: {np.mean(data):.6f}\n"
            results_text += f"    Std Dev: {np.std(data):.6f}\n"
            results_text += f"    Min: {np.min(data):.6f}\n"
            results_text += f"    Max: {np.max(data):.6f}\n"
        
        self.results_text.insert(1.0, param_text + results_text)
    
    def _handle_error(self, error_msg):
        """Handle errors in generation"""
        self.progress.stop()
        self.status_var.set("Error occurred!")
        self.is_generating = False
        messagebox.showerror("Generation Error", f"Error generating noise: {error_msg}")
    
    def run_benchmark(self):
        """Run benchmark tests"""
        if self.is_generating:
            return
        
        self.status_var.set("Running benchmark...")
        self.progress.start()
        
        thread = threading.Thread(target=self._benchmark_worker)
        thread.daemon = True
        thread.start()
    
    def _benchmark_worker(self):
        """Worker thread for benchmark"""
        try:
            sizes = [64, 128, 256]
            scales = [0.05, 0.1, 0.2]
            
            benchmark_results = []
            
            for size in sizes:
                for scale in scales:
                    test_params = {
                        'size': size, 'scale': scale, 'octaves': 2,
                        'persistence': 0.5, 'lacunarity': 2.0,
                        'n_points': 20, 'distance_func': 'euclidean'
                    }
                    
                    test_result = {'params': test_params, 'results': {}}
                    
                    # Test each noise type
                    for noise_type in ['perlin', 'simplex', 'worley']:
                        try:
                            if noise_type == 'perlin':
                                _, perf = self.measure_performance(
                                    self.generator.perlin_noise,
                                    size, size, scale, 2, 0.5, 2.0
                                )
                            elif noise_type == 'simplex':
                                _, perf = self.measure_performance(
                                    self.generator.simplex_noise,
                                    size, size, scale, 2, 0.5, 2.0
                                )
                            else:  # worley
                                _, perf = self.measure_performance(
                                    self.generator.worley_noise,
                                    size, size, scale, 20, 'euclidean'
                                )
                            
                            test_result['results'][noise_type] = perf
                        except Exception as e:
                            test_result['results'][noise_type] = {'error': str(e)}
                    
                    benchmark_results.append(test_result)
            
            # Update GUI with benchmark results
            self.root.after(0, lambda: self._update_benchmark_results(benchmark_results))
            
        except Exception as e:
            self.root.after(0, lambda: self._handle_error(f"Benchmark error: {str(e)}"))
    
    def _update_benchmark_results(self, benchmark_results):
        """Update GUI with benchmark results"""
        self.results_text.delete(1.0, tk.END)
        
        benchmark_text = "BENCHMARK RESULTS:\n\n"
        
        for i, test in enumerate(benchmark_results):
            params = test['params']
            results = test['results']
            
            benchmark_text += f"Test {i+1}: {params['size']}x{params['size']}, Scale: {params['scale']}\n"
            
            for noise_type, perf in results.items():
                if 'error' in perf:
                    benchmark_text += f"  {noise_type}: ERROR - {perf['error']}\n"
                else:
                    benchmark_text += f"  {noise_type}: {perf['time']:.4f}s, {perf['memory']:.2f}MB\n"
            
            benchmark_text += "\n"
        
        self.results_text.insert(1.0, benchmark_text)
        
        self.progress.stop()
        self.status_var.set("Benchmark complete!")
    
    def clear_results(self):
        """Clear all results"""
        self.results_text.delete(1.0, tk.END)
        
        # Clear visualizations
        for img in self.images.values():
            if hasattr(img, 'set_data'):
                img.set_data(np.zeros((64, 64)))
        
        # Clear performance chart
        self.axes[1, 1].clear()
        self.axes[1, 1].set_title('Performance Comparison')
        self.axes[1, 1].set_xlabel('Noise Type')
        self.axes[1, 1].set_ylabel('Time (seconds)')
        
        self.fig.canvas.draw()
        self.status_var.set("Results cleared")
    
    def run(self):
        """Start the GUI"""
        # Show matplotlib figure
        plt.show(block=False)
        
        # Start Tkinter main loop
        self.root.mainloop()

def main():
    """Main function"""
    print("Starting Optimized Noise Function Comparison Tool...")
    print("Features:")
    print("- Precise parameter input fields")
    print("- Optimized noise algorithms")
    print("- Threaded generation (no GUI freezing)")
    print("- Real-time performance monitoring")
    print("- Comprehensive benchmarking")
    
    try:
        app = NoiseComparatorGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()