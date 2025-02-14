import time
import os
import logging

class ContainerMetrics:
    def __init__(self):
        self.cgroup_path = '/sys/fs/cgroup'
        
    def read_memory_usage(self):
        """Read container memory usage in MB"""
        try:
            with open(os.path.join(self.cgroup_path, 'memory.current'), 'r') as f:
                return float(f.read()) / (1024 * 1024)  # Convert to MB
        except Exception:
            return None
            
    def read_cpu_usage(self):
        """Read container CPU usage in seconds"""
        try:
            with open(os.path.join(self.cgroup_path, 'cpu.stat'), 'r') as f:
                for line in f:
                    if line.startswith('usage_usec'):
                        return float(line.split()[1]) / 1_000_000  # Convert to seconds
        except Exception:
            return None

class PerformanceMonitor:
    def __init__(self, db_type: str):
        """Initialize performance monitor for the specified database type."""
        self.db_type = db_type
        self.start_time = None
        self.start_cpu = None
        self.start_memory = None
        self.metrics = ContainerMetrics()
        
        # Setup simple logging without timestamps
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"{db_type.lower()}_performance.log")
        formatter = logging.Formatter('%(message)s')
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger = logging.getLogger(db_type)
        self.logger.setLevel(logging.INFO)
        self.logger.handlers = []  # Remove any existing handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def start_operation(self, operation_name: str):
        """Start monitoring an operation."""
        self.start_time = time.time()
        self.start_cpu = self.metrics.read_cpu_usage()
        self.start_memory = self.metrics.read_memory_usage()
        self.logger.info(f"\n[{self.db_type}] {operation_name}")

    def end_operation(self, operation_name: str):
        """End monitoring an operation and log results."""
        if not self.start_time:
            return

        end_time = time.time()
        end_cpu = self.metrics.read_cpu_usage()
        end_memory = self.metrics.read_memory_usage()

        execution_time = end_time - self.start_time
        
        # Log only the changes and percentages
        if end_memory is not None and self.start_memory is not None:
            memory_change = end_memory - self.start_memory
            self.logger.info(f"Memory Change: {memory_change:+.2f} MB")
                
        if end_cpu is not None and self.start_cpu is not None:
            cpu_time = end_cpu - self.start_cpu
            cpu_percent = (cpu_time / execution_time) * 100 if execution_time > 0 else 0
            self.logger.info(f"CPU Usage: {cpu_percent:.2f}%")
            
        self.logger.info(f"Time: {execution_time:.2f} seconds")
        

        # Reset start values
        self.start_time = None
        self.start_cpu = None
        self.start_memory = None
