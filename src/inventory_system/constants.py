from enum import Enum

# Enum that matches 'code' column in 'cut_types' table
class CutTypeCode(str, Enum):
    NONE = "none"       # No cut
    FULL = "full"       # Full cut
    PARTIAL = "partial" # Partial cut

# Enum for column types (Balance, Fact, Cut)
class ColumnType(str, Enum):
    BALANCE = "BALANCE"  # Balance sheet quantity
    FACT = "FACT"        # Actual physical quantity
    CUT = "CUT"          # Quantity in cut/removed state