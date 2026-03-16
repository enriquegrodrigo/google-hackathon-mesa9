import os

from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

FOCUS_COMPANY = "Telefonica"
AGENT_MISSION = (
	"Research external public information and help solve strategic and product "
	"problems for Telefonica with actionable, evidence-based recommendations."
)

# Flexible research policy defaults.
MIN_PUBLICATION_YEAR = 2025
PREFER_LAST_MONTHS = 6
MIN_SOURCES = 6

# Optional guidance only; not strict allowlist.
PREFERRED_DOMAINS = [
	"att.com",
	"verizon.com",
	"chinamobileltd.com",
	"telekom.com",
	"vodafone.com",
	"docomo.ne.jp",
	"gsma.com",
	"etno.eu",
	"ctia.org",
	"itu.int",
	"3gpp.org",
	"standards.ieee.org",
	"etsi.org",
	"ietf.org",
	"lightreading.com",
	"fierce-network.com",
	"telecoms.com",
	"reuters.com",
	"capacitymedia.com",
]
