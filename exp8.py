from collections import deque
import random
print("Hasan Sayyed 232P003 32")


class Job:
    def __init__(self, job_id, duration):
        self.job_id = job_id
        self.duration = duration
        self.remaining_time = duration

    def __repr__(self):
        return f"Job({self.job_id}, rem={self.remaining_time})"


class Processor:
    def __init__(self, pid, threshold):
        self.pid = pid
        self.threshold = threshold
        self.queue = deque()
        self.running_job = None

    def total_load(self):
        load = sum(job.remaining_time for job in self.queue)
        if self.running_job:
            load += self.running_job.remaining_time
        return load

    def is_overloaded(self):
        return self.total_load() > self.threshold

    def is_underloaded(self):
        return self.total_load() < self.threshold

    def is_idle(self):
        return self.total_load() == 0

    def add_job(self, job):
        self.queue.append(job)

    def start_next_job(self):
        if not self.running_job and self.queue:
            self.running_job = self.queue.popleft()

    def execute(self):
        if self.running_job:
            self.running_job.remaining_time -= 1
            if self.running_job.remaining_time <= 0:
                self.running_job = None

    def __repr__(self):
        return f"Processor {self.pid} | Load: {self.total_load()}"


class LoadBalancer:
    def __init__(self, processors, preemptive=False):
        self.processors = processors
        self.preemptive = preemptive

    # Location Rule
    def find_underloaded_processors(self):
        return [p for p in self.processors if p.is_underloaded()]

    # Selection Rule
    def select_job(self, processor):
        if self.preemptive:
            # Can select running job (costly)
            if processor.running_job:
                print(
                    f"Preemptively migrating running job from P{processor.pid}")
                job = processor.running_job
                processor.running_job = None
                return job

        # Non-preemptive: pick from waiting queue
        if processor.queue:
            return processor.queue.pop()
        return None

    # Distribution Rule
    def balance_load(self):
        underloaded = self.find_underloaded_processors()

        for p in self.processors:
            while p.is_overloaded() and underloaded:
                target = min(underloaded, key=lambda x: x.total_load())
                job = self.select_job(p)

                if not job:
                    break

                target.add_job(job)
                print(
                    f"Migrated Job {job.job_id} from P{p.pid} to P{target.pid}")

                underloaded = self.find_underloaded_processors()


def simulate(preemptive=False):
    processors = [Processor(i, threshold=15) for i in range(4)]

    # Generate random jobs
    job_id = 1
    for _ in range(10):
        job = Job(job_id, random.randint(2, 8))
        random.choice(processors).add_job(job)
        job_id += 1

    balancer = LoadBalancer(processors, preemptive=preemptive)

    print("\nInitial State:")
    for p in processors:
        print(p)

    # Run simulation
    for step in range(10):
        print(f"\n--- Step {step+1} ---")
        for p in processors:
            p.start_next_job()
            p.execute()

        balancer.balance_load()

        for p in processors:
            print(p)


print("Running Non-Preemptive Load Balancing")
simulate(preemptive=False)

print("\nRunning Preemptive Load Balancing")
simulate(preemptive=True)
