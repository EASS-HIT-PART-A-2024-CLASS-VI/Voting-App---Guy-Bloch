import subprocess


def test_integration():
    """
    Run unit tests as part of integration testing.
    """
    try:
        # Run pytest on unit tests
        result = subprocess.run(
            ["pytest", "app/unit_tests.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Integration Test Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Integration Test Failed:\n", e.stdout)
        print("Integration Test Errors:\n", e.stderr)
        raise
