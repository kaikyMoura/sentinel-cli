from enum import Enum


class AnalysisTask(str, Enum):
            IMPROVEMENTS = "improvements"
            DOCUMENTATION = "documentation"
            COMMITS = "commits"
            APPLY_IMPROVEMENTS = "apply-improvements"