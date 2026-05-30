"""event-safety-cad — Event Safety Planning and DXF generation.

Public API:
    from generator import load_standards, load_event, analyze, build_dxf
"""

from .standards import Standards, load_standards
from .models import EventPlan, SafetyReport, load_event
from .analysis import analyze
from .dxf_builder import build_dxf

__all__ = [
    "Standards",
    "load_standards",
    "EventPlan",
    "SafetyReport",
    "load_event",
    "analyze",
    "build_dxf",
]

__version__ = "0.1.0"
