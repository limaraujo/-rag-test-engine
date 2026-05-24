from agents.test_generator import (
    TestGeneratorAgent
)


def main():

    agent = TestGeneratorAgent()

    response = agent.generate(
        "def soma(a, b): return a + b"
    )

    print(response)


if __name__ == "__main__":
    main()