from enum import Enum

# Enum that matches 'code' column in 'cut_types' table
class CutTypeCode(str, Enum):
    NONE = "none"       # No cut
    FULL = "full"       # Full cut
    PARTIAL = "partial" # Partial cut