"""Word lists used by the quality linter.

Gendered lists are based on Gaucher, Friesen and Kay (2011), "Evidence That
Gendered Wording in Job Advertisements Exists and Sustains Gender
Inequality". Entries ending in `*` are prefix matches. The lists are a
screening aid, not proof of bias.
"""

MASCULINE_CODED = (
    "active", "adventurous", "aggress*", "ambitio*", "assert*", "athlet*",
    "autonom*", "boast*", "challeng*", "compet*", "confident", "courag*",
    "decisive", "determin*", "dominant", "domina*", "driven", "fearless",
    "fight*", "force*", "greedy", "headstrong", "hierarch*", "hostil*",
    "impulsive", "independen*", "individual*", "intellect*", "masculine",
    "objective", "outspoken", "persist*", "principle*", "reckless",
    "stubborn", "superior", "self-confiden*", "self-reliant", "self-sufficien*",
)

FEMININE_CODED = (
    "affectionate", "cheer*", "collab*", "commit*", "communal", "compassion*",
    "connect*", "considerate", "cooperat*", "co-operat*", "depend*",
    "emotiona*", "empath*", "feminine", "gentle", "honest", "interpersonal",
    "interdependen*", "kind", "kinship", "loyal*", "modesty", "nurtur*",
    "pleasant*", "polite", "quiet*", "responsive", "sensitiv*", "submissive",
    "support*", "sympath*", "tender*", "together*", "trust*", "understand*",
    "warm*", "yield*",
)

# Phrases that discourage older applicants (UCI/NBER 2022 ageist-language study, AARP).
AGE_CODED_PHRASES = (
    "digital native", "recent graduate", "recent grad", "young and dynamic",
    "young team", "young, energetic", "high energy", "energetic team",
    "fresh graduate", "fresh out of", "junior mindset", "born after",
    "youthful",
)

# Hype words that add noise and put off many candidates.
FILLER_PHRASES = (
    "rockstar", "rock star", "ninja", "guru", "wizard", "superhero",
    "work hard play hard", "fast-paced environment", "fast paced environment",
    "self-starter", "go-getter", "hit the ground running", "wear many hats",
    "thrive in chaos", "passionate about", "dynamic environment",
    "synergy", "results-driven", "team player", "think outside the box",
)

EXCLUSIONARY_PHRASES = (
    "native english speaker", "native speaker", "must be able to lift",
    "clean-cut", "culture fit", "manpower", "salesman", "chairman",
    "he or she", "guys", "foreman", "stewardess", "workman",
)

PAY_MARKERS = (
    "$", "usd", "eur", "gbp", "cad", "salary", "compensation", "per hour",
    "per year", "/hr", "/yr", "annual", "base pay", "pay range",
)
