import random
import copy

# -----------------------------
# MOCK KNOWLEDGE MODULES
# -----------------------------

class KnowledgeModule:
    def __init__(self, name, reliability=1.0):
        self.name = name
        self.reliability = reliability
        self.active = False

    def load(self):
        self.active = True

    def unload(self):
        self.active = False


# -----------------------------
# COGNITIVE ROUTER
# -----------------------------

class CognitiveRouter:
    def route(self, query):
        keywords = query.lower()

        modules = []

        if "math" in keywords or "physics" in keywords:
            modules.append("science")

        if "code" in keywords or "python" in keywords:
            modules.append("coding")

        if "history" in keywords:
            modules.append("history")

        if not modules:
            modules.append("general")

        return modules


# -----------------------------
# CORE LLM (SIMULATED)
# -----------------------------

class CoreLLM:
    def generate(self, query, modules):
        # simulate hallucination risk
        base_response = f"[Reasoning based on {modules}] Answer to: {query}"

        hallucination_chance = 0.2

        if random.random() < hallucination_chance:
            base_response += " + (possible hallucination introduced)"

        return base_response


# -----------------------------
# PROTECTOR AI (GUARDIAN NODE)
# -----------------------------

class ProtectorAI:
    def validate(self, response):
        # simple heuristic validation
        if "hallucination" in response:
            return False

        if len(response) < 10:
            return False

        return True


# -----------------------------
# SNAPSHOT SYSTEM
# -----------------------------

class SnapshotSystem:
    def __init__(self):
        self.snapshot = None

    def save(self, state):
        self.snapshot = copy.deepcopy(state)

    def restore(self):
        return copy.deepcopy(self.snapshot)


# -----------------------------
# CROWe SAFE SYSTEM
# -----------------------------

class CroweSafeguardSystem:
    def __init__(self):
        self.router = CognitiveRouter()
        self.llm = CoreLLM()
        self.guardian = ProtectorAI()
        self.snapshots = SnapshotSystem()

        self.modules = {
            "science": KnowledgeModule("science"),
            "coding": KnowledgeModule("coding"),
            "history": KnowledgeModule("history"),
            "general": KnowledgeModule("general")
        }

        self.state = {"last_query": None, "last_response": None}

    def activate_modules(self, module_names):
        for m in self.modules.values():
            m.unload()

        for name in module_names:
            if name in self.modules:
                self.modules[name].load()

    def get_active_modules(self):
        return [m.name for m in self.modules.values() if m.active]

    def run(self, query):
        print("\n--- NEW QUERY ---")
        print("Input:", query)

        # Step 1: route
        modules = self.router.route(query)
        self.activate_modules(modules)

        active = self.get_active_modules()
        print("Active Modules:", active)

        # Step 2: save snapshot before generation
        self.snapshots.save(self.state)

        # Step 3: generate response
        response = self.llm.generate(query, active)
        print("LLM Output:", response)

        # Step 4: validate
        if self.guardian.validate(response):
            print("Guardian Status: PASS")
            self.state = {"last_query": query, "last_response": response}
        else:
            print("Guardian Status: FAIL → Rolling back")

            self.state = self.snapshots.restore()
            response = self.state["last_response"]

        print("Final Output:", response)
        return response


# -----------------------------
# DEMO RUN
# -----------------------------

if __name__ == "__main__":
    system = CroweSafeguardSystem()

    queries = [
        "Explain physics math concepts",
        "Write python code for sorting",
        "Tell me about medieval history",
        "Random unrelated query about space math physics coding"
    ]

    for q in queries:
        system.run(q)