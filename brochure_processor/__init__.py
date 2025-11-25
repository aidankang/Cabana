"""
Brochure Processor Package

A comprehensive toolkit for converting static brochure images 
into crawlable, SEO-friendly web content.
"""

__version__ = "1.0.0"
__author__ = "Coastal Cabana Project"

# Make main classes available at package level
from .scripts.brochure_processor import BrochureProcessor
from .scripts.batch_processor import ResumableBatchProcessor, BatchProgressTracker

__all__ = [
    "BrochureProcessor", 
    "ResumableBatchProcessor", 
    "BatchProgressTracker"
]