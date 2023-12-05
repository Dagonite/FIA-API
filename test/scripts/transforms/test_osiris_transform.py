"""
Test for Osiris transform
"""
from unittest.mock import Mock

from ir_api.scripts.pre_script import PreScript
from ir_api.scripts.transforms.osiris_transform import OsirisTransform

SCRIPT = """from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np


def generate_input_path_for_run(run_number, cycle):
    return f"/archive/ndxosiris/Instrument/data/{cycle}/OSI{run_number}.nxs"

# To change by automatic script
input_runs = ["108538"]
# This needs to be loaded from a shared repository of files
calibration_file_path = "/home/sam/Downloads/osi92682_multi_graphite002_calib.nxs"
cycle = "cycle_14_1"
analyser = "graphite"
reflection = "002"
spectroscopy_reduction = True
diffraction_reduction = True

# Defaults
instrument = "OSIRIS"
workspace_start_of_file = ""
efixed = 1.845
spectra_range = "963,1004"
# Grouping string is for 14 groups, and generated by the UI for indirect data reduction and based on spectra_range
grouping_string = "963-965,966-968,969-971,972-974,975-977,978-980,981-983,984-986,987-989,990-992,993-995,996-998,999-1001,1002-1004"
unit_x = "DeltaE"
fold_multiple_frames = False

# Generated
sum_runs = len(input_runs) > 1

input_file_paths = ""
for input_run in input_runs:
    input_file_paths += ", " + generate_input_path_for_run(input_run, cycle)
input_file_paths = input_file_paths[2:]
print(input_file_paths)

output_workspace_prefix = instrument + input_runs[0]

# Perform the reduction
if spectroscopy_reduction:
    # Load calibration workspace
    calibration_workspace = Load(calibration_file_path)
    
    print("Reducing all")
    output_ws_all = ISISIndirectEnergyTransferWrapper(OutputWorkspace=output_workspace_prefix + "-all", GroupingMethod="All", InputFiles=input_file_paths, SumFiles=sum_runs, CalibrationWorkspace=calibration_workspace, Instrument=instrument, Analyser=analyser, Reflection=reflection, EFixed=efixed, SpectraRange=spectra_range, FoldMultipleFrames=fold_multiple_frames, UnitX=unit_x)

    print("Reducing using groups")
    output_ws_grouping = ISISIndirectEnergyTransferWrapper(OutputWorkspace=output_workspace_prefix + "-groups", GroupingMethod="Custom", GroupingString=grouping_string, InputFiles=input_file_paths, SumFiles=sum_runs, CalibrationWorkspace=calibration_workspace, Instrument=instrument, Analyser=analyser, Reflection=reflection, EFixed=efixed, SpectraRange=spectra_range, FoldMultipleFrames=fold_multiple_frames, UnitX=unit_x)

    print("Reducing individual")
    output_ws_individual = ISISIndirectEnergyTransferWrapper(OutputWorkspace=output_workspace_prefix + "-individual", GroupingMethod="Individual", InputFiles=input_file_paths, SumFiles=sum_runs, CalibrationWorkspace=calibration_workspace, Instrument=instrument, Analyser=analyser, Reflection=reflection, EFixed=efixed, SpectraRange=spectra_range, FoldMultipleFrames=fold_multiple_frames, UnitX=unit_x)

if diffratcion_reduction:
    pass"""


def create_expected_script(
    cycle_string: str, input_runs: str, reflection: str, diffraction: str, spectroscopy: str
) -> str:
    return f"""from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np


def generate_input_path_for_run(run_number, cycle):
    return f"/archive/ndxosiris/Instrument/data/{{cycle}}/OSI{{run_number}}.nxs"

# To change by automatic script
input_runs = {input_runs}
# This needs to be loaded from a shared repository of files
calibration_file_path = "/home/sam/Downloads/osi92682_multi_graphite002_calib.nxs"
cycle = {cycle_string}
analyser = "graphite"
reflection = {reflection}
spectroscopy_reduction = {spectroscopy}
diffraction_reduction = {diffraction}

# Defaults
instrument = "OSIRIS"
workspace_start_of_file = ""
efixed = 1.845
spectra_range = "963,1004"
# Grouping string is for 14 groups, and generated by the UI for indirect data reduction and based on spectra_range
grouping_string = "963-965,966-968,969-971,972-974,975-977,978-980,981-983,984-986,987-989,990-992,993-995,996-998,999-1001,1002-1004"
unit_x = "DeltaE"
fold_multiple_frames = False

# Generated
sum_runs = len(input_runs) > 1

input_file_paths = ""
for input_run in input_runs:
    input_file_paths += ", " + generate_input_path_for_run(input_run, cycle)
input_file_paths = input_file_paths[2:]
print(input_file_paths)

output_workspace_prefix = instrument + input_runs[0]

# Perform the reduction
if spectroscopy_reduction:
    # Load calibration workspace
    calibration_workspace = Load(calibration_file_path)
    
    print("Reducing all")
    output_ws_all = ISISIndirectEnergyTransferWrapper(OutputWorkspace=output_workspace_prefix + "-all", GroupingMethod="All", InputFiles=input_file_paths, SumFiles=sum_runs, CalibrationWorkspace=calibration_workspace, Instrument=instrument, Analyser=analyser, Reflection=reflection, EFixed=efixed, SpectraRange=spectra_range, FoldMultipleFrames=fold_multiple_frames, UnitX=unit_x)

    print("Reducing using groups")
    output_ws_grouping = ISISIndirectEnergyTransferWrapper(OutputWorkspace=output_workspace_prefix + "-groups", GroupingMethod="Custom", GroupingString=grouping_string, InputFiles=input_file_paths, SumFiles=sum_runs, CalibrationWorkspace=calibration_workspace, Instrument=instrument, Analyser=analyser, Reflection=reflection, EFixed=efixed, SpectraRange=spectra_range, FoldMultipleFrames=fold_multiple_frames, UnitX=unit_x)

    print("Reducing individual")
    output_ws_individual = ISISIndirectEnergyTransferWrapper(OutputWorkspace=output_workspace_prefix + "-individual", GroupingMethod="Individual", InputFiles=input_file_paths, SumFiles=sum_runs, CalibrationWorkspace=calibration_workspace, Instrument=instrument, Analyser=analyser, Reflection=reflection, EFixed=efixed, SpectraRange=spectra_range, FoldMultipleFrames=fold_multiple_frames, UnitX=unit_x)

if diffratcion_reduction:
    pass"""


def test_osiris_transform_spectroscopy():
    """Test spectroscopy transform"""
    reduction = Mock()
    reduction.reduction_inputs = {
        "mode": "spectroscopy",
        "cycle_string": "cycle_20_1",
        "runno": [123, 124],
        "analyser": "004",
    }
    script = PreScript(value=SCRIPT)
    OsirisTransform().apply(script, reduction)

    assert script.value == create_expected_script("cycle_20_1", "[123, 124]", "004", "False", "True")
