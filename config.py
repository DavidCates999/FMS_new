# Configuration file for FMS Query Engine
# Loads sensitive data from environment variables

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (loaded from .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# MongoDB Configuration (loaded from .env or Streamlit secrets)
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "FMS")

# =============================================================================
# MULTI-DATABASE ARCHITECTURE
# =============================================================================
# The system supports multiple databases based on franchise location:
#
# Database: FMS
#   - Location: Boston Train-TAX
#
# Database: Austin
#   - Location: Austin
#
# Database: Boston (shared)
#   - Locations: Boston, Cleveland, Chicago, Columbia, Georgia, 
#                Maryland, Northern VA, Richmond
#
# Database: Broward
#   - Location: Broward
#
# Database: CentralAL
#   - Location: Central AL
#
# Database: CentralFlorida
#   - Location: Central Florida
#
# Database: Charleston
#   - Location: Charleston
#
# Database: Charlotte
#   - Location: Charlotte
#
# =============================================================================

# All available databases
AVAILABLE_DATABASES = [
    "FMS",
    "Austin",
    "Boston",
    "Broward",
    "CentralAL",
    "CentralFlorida",
    "Charleston",
    "Charlotte"
]

# Available Collections (common across databases)
COLLECTIONS = [
    "leads",
    "proposals", 
    "ServiceContracts",
    "rfps",
    "customers_activation",
    "customers_active",
    "customers_suspended",
    "customers_terminated",
    "serviceproviders",
    "spusers",
    "inspection_dashboard",
    "UsersInspection",
    "GeneralLedger"
]
