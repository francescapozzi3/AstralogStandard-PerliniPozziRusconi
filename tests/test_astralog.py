import pytest
import os
from src.astralog_mock import AstraLogHPC

@pytest.fixture
def mission_env(tmp_path):
    """
    Fixture to set up a mock mission environment using a temporary directory.
    Creates minimal rules and telemetry files for testing purposes.
    """
    rules_file = tmp_path / "rules.json"
    rules_file.write_text("[]")
    
    input_file = tmp_path / "telemetry_cleaned.csv"
    input_file.write_text("2025-11-15T12:00:00Z;TEMP-01;25.5;LOW")
    
    output_dir = tmp_path / "results"
    
    return str(rules_file), str(input_file), str(output_dir)

def test_engine_initialization(mission_env):
    """Verifies that the engine initializes correctly when files exist."""
    r_path, i_path, o_dir = mission_env
    engine = AstraLogHPC(r_path, i_path, o_dir)
    assert engine.initialize() is True
    assert engine.is_initialized is True

def test_engine_initialization_fail():
    """Verifies that the engine raises an error if the rules file is missing."""
    engine = AstraLogHPC("missing_rules.json", "data.csv", "out")
    with pytest.raises(FileNotFoundError):
        engine.initialize()

def test_analysis_execution(mission_env):
    """Verifies full analysis execution and output file generation."""
    r_path, i_path, o_dir = mission_env
    engine = AstraLogHPC(r_path, i_path, o_dir)
    engine.initialize()
    
    success = engine.run_analysis()
    assert success is True
    assert os.path.exists(os.path.join(o_dir, "valid_data.csv"))
    assert os.path.exists(os.path.join(o_dir, "alarms.log"))

def test_analysis_without_init(mission_env):
    """Verifies that analysis fails if initialization was skipped."""
    r_path, i_path, o_dir = mission_env
    engine = AstraLogHPC(r_path, i_path, o_dir)
    assert engine.run_analysis() is False

def test_analysis_missing_input(tmp_path):
    """Verifies engine behavior when the telemetry input file is missing."""
    rules = tmp_path / "rules.json"
    rules.write_text("[]")
    engine = AstraLogHPC(str(rules), "non_existent_telemetry.csv", str(tmp_path / "out"))
    engine.initialize()
    
    with pytest.raises(FileNotFoundError):
        engine.run_analysis()