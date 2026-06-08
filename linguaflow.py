import streamlit as st
import random
import json
from datetime import datetime

st.set_page_config(
    page_title="LinguaFlow — ინგლისური ადაპტურად",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Noto Sans Georgian', sans-serif;
    background: #0a0e1a;
    color: #e2e8f8;
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #0f1f3d 0%, #0a0e1a 50%, #060810 100%);
    min-height: 100vh;
}

/* Hide streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 2rem 1rem 4rem 1rem !important; max-width: 720px !important; }

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
}
.hero-logo {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #60a5fa);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s ease infinite;
    letter-spacing: -1px;
}
@keyframes shimmer { 0%,100%{background-position:0%} 50%{background-position:100%} }
.hero-sub {
    font-size: 1rem;
    color: #64748b;
    margin-top: 0.5rem;
    letter-spacing: 0.05em;
}
.hero-tagline {
    font-size: 0.85rem;
    color: #334155;
    margin-top: 0.3rem;
}

/* ── CARDS ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(96,165,250,0.4), transparent);
}

/* ── LEVEL BADGE ── */
.level-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.pill-a1 { background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.35); color: #4ade80; }
.pill-a2 { background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.35); color: #60a5fa; }
.pill-b1 { background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.35); color: #c084fc; }
.pill-b2 { background: rgba(249,115,22,0.15); border: 1px solid rgba(249,115,22,0.35); color: #fb923c; }

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #e2e8f8;
    margin-bottom: 0.4rem;
}
.section-sub {
    font-size: 0.88rem;
    color: #475569;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

/* ── QUESTION TEXT ── */
.q-text {
    font-size: 1.12rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin-bottom: 1.4rem;
    padding: 1rem 1.2rem;
    background: rgba(96,165,250,0.05);
    border-left: 3px solid rgba(96,165,250,0.4);
    border-radius: 0 10px 10px 0;
}

/* ── ANSWER OPTIONS ── */
.stButton > button {
    width: 100%;
    background: rgba(255,255,255,0.04) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.2rem !important;
    font-family: 'Noto Sans Georgian', sans-serif !important;
    font-size: 0.92rem !important;
    text-align: left !important;
    transition: all 0.2s !important;
    margin-bottom: 2px;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: rgba(96,165,250,0.12) !important;
    border-color: rgba(96,165,250,0.45) !important;
    color: #e2e8f8 !important;
    transform: translateX(4px);
}

/* ── TEXT INPUT ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f8 !important;
    font-family: 'Noto Sans Georgian', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(96,165,250,0.5) !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.1) !important;
}

/* ── FEEDBACK ── */
.fb-correct {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #4ade80;
    font-weight: 600;
    margin-top: 0.8rem;
}
.fb-wrong {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #f87171;
    font-weight: 600;
    margin-top: 0.8rem;
}
.fb-explain {
    color: #94a3b8;
    font-size: 0.88rem;
    margin-top: 0.5rem;
    font-weight: 400;
    line-height: 1.6;
}

/* ── PROGRESS ── */
.progress-wrap { margin: 1.2rem 0; }
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #475569;
    margin-bottom: 0.4rem;
}
.stProgress > div > div > div { background: linear-gradient(90deg,#3b82f6,#8b5cf6) !important; border-radius: 4px !important; }
.stProgress > div > div { background: rgba(255,255,255,0.06) !important; border-radius: 4px !important; }

/* ── STEP DOTS ── */
.step-dots {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin-bottom: 1.5rem;
}
.dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.12);
    transition: all 0.3s;
}
.dot.active { background: #60a5fa; width: 24px; border-radius: 4px; }
.dot.done { background: rgba(96,165,250,0.4); }

/* ── VOCAB CARD ── */
.vocab-card {
    background: rgba(96,165,250,0.06);
    border: 1px solid rgba(96,165,250,0.15);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.vocab-word { font-size: 1.1rem; color: #93c5fd; font-weight: 600; min-width: 140px; }
.vocab-meaning { font-size: 0.9rem; color: #64748b; }
.vocab-example { font-size: 0.82rem; color: #334155; font-style: italic; margin-top: 0.2rem; }

/* ── STREAK / STATS ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.2rem;
}
.stat-box {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
}
.stat-val { font-size: 1.8rem; font-weight: 700; color: #60a5fa; }
.stat-lbl { font-size: 0.75rem; color: #475569; margin-top: 0.2rem; }

/* ── RESULT ── */
.result-hero {
    text-align: center;
    padding: 2rem 0;
}
.result-score {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    color: #60a5fa;
    font-weight: 700;
}
.result-level {
    font-size: 1.1rem;
    color: #8b5cf6;
    margin-top: 0.5rem;
    font-weight: 600;
}
.result-msg { font-size: 0.95rem; color: #64748b; margin-top: 0.8rem; line-height: 1.6; }

/* ── NAV TAB ── */
.nav-tabs {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    background: rgba(255,255,255,0.03);
    padding: 0.4rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.07);
}
.nav-tab {
    flex: 1;
    text-align: center;
    padding: 0.6rem;
    border-radius: 10px;
    font-size: 0.85rem;
    cursor: pointer;
}
.nav-tab.active {
    background: rgba(96,165,250,0.15);
    color: #60a5fa;
    font-weight: 600;
}
.nav-tab.inactive { color: #475569; }

/* ── DAILY LESSON SECTION ── */
.lesson-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.lesson-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}
.icon-test { background: rgba(59,130,246,0.15); }
.icon-vocab { background: rgba(168,85,247,0.15); }
.icon-grammar { background: rgba(34,197,94,0.15); }
.icon-writing { background: rgba(249,115,22,0.15); }
.lesson-title { font-size: 1.1rem; font-weight: 600; color: #e2e8f8; }
.lesson-desc { font-size: 0.82rem; color: #475569; margin-top: 0.2rem; }

/* ── GRAMMAR HIGHLIGHT ── */
.grammar-box {
    background: rgba(168,85,247,0.06);
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 1rem;
    font-size: 0.92rem;
    color: #c4b5fd;
    line-height: 1.7;
}
.grammar-box b { color: #a78bfa; }

/* ── SENTENCE BUILD ── */
.word-chip {
    display: inline-block;
    background: rgba(96,165,250,0.12);
    border: 1px solid rgba(96,165,250,0.25);
    border-radius: 8px;
    padding: 0.3rem 0.75rem;
    margin: 0.2rem;
    font-size: 0.9rem;
    color: #93c5fd;
    font-family: 'DM Mono', monospace;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f8 !important;
}

/* ── RADIO ── */
.stRadio > div { gap: 0.5rem !important; }
.stRadio label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.1rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: #94a3b8 !important;
}
.stRadio label:hover {
    border-color: rgba(96,165,250,0.4) !important;
    color: #e2e8f8 !important;
}

/* divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ────────────────────────────────────────────────────────────────────

PLACEMENT_QUESTIONS = [
    {
        "level_target": "A1",
        "q": "Choose the correct sentence:",
        "options": ["I am a student.", "I are a student.", "I is a student.", "Me am student."],
        "correct": "I am a student.",
        "explain": "'I am' — პირველი პირის ერთობითი ფორმა to be ზმნისთვის."
    },
    {
        "level_target": "A1",
        "q": "What is the plural of 'cat'?",
        "options": ["cates", "cats", "cat's", "catz"],
        "correct": "cats",
        "explain": "უმეტეს არსებით სახელებს ემატება -s."
    },
    {
        "level_target": "A2",
        "q": "She ___ to the market yesterday.",
        "options": ["go", "goes", "went", "gone"],
        "correct": "went",
        "explain": "'go'-ს წარსული დრო არის 'went' — Past Simple."
    },
    {
        "level_target": "A2",
        "q": "Which sentence is correct?",
        "options": [
            "He don't like coffee.",
            "He doesn't likes coffee.",
            "He doesn't like coffee.",
            "He not like coffee."
        ],
        "correct": "He doesn't like coffee.",
        "explain": "მესამე პირში გამოიყენება 'doesn't' + ზმნის საწყისი ფორმა."
    },
    {
        "level_target": "B1",
        "q": "By the time she arrived, we ___ dinner.",
        "options": ["finish", "finished", "had finished", "have finished"],
        "correct": "had finished",
        "explain": "Past Perfect გამოიყენება, როდესაც ერთი მოქმედება მოხდა მეორეზე ადრე."
    },
    {
        "level_target": "B1",
        "q": "Choose the correct passive form: 'Someone stole my bag.'",
        "options": [
            "My bag stolen.",
            "My bag was stolen.",
            "My bag is stolen.",
            "My bag has steal."
        ],
        "correct": "My bag was stolen.",
        "explain": "Past Simple Passive = was/were + Past Participle."
    },
    {
        "level_target": "B2",
        "q": "If I ___ more time, I would have studied abroad.",
        "options": ["had had", "have", "had", "would have"],
        "correct": "had had",
        "explain": "Third Conditional: If + Past Perfect → would have + PP. გამოხატავს შეუსრულებელ წარსულ პირობას."
    },
    {
        "level_target": "B2",
        "q": "The report, ___ was submitted late, caused major delays.",
        "options": ["that", "which", "who", "whose"],
        "correct": "which",
        "explain": "Non-defining relative clause-ში გამოიყენება 'which', არ გამოიყენება 'that'."
    },
]

DAILY_CONTENT = {
    "A1": {
        "vocab": [
            {"word": "hello", "meaning": "გამარჯობა", "example": "Hello! How are you?"},
            {"word": "house", "meaning": "სახლი", "example": "I live in a big house."},
            {"word": "water", "meaning": "წყალი", "example": "Can I have some water?"},
            {"word": "friend", "meaning": "მეგობარი", "example": "She is my best friend."},
        ],
        "grammar_rule": "სახელწოდება <b>Present Simple</b> — გამოიყენება ჩვეულებრივი ქმედებების აღსაწერად.\n\n📌 ფორმა: I/You/We/They + ზმნა | He/She/It + ზმნა + <b>-s</b>\n\n✦ I eat breakfast every day.\n✦ She works at a school.",
        "grammar_q": "She ___ to school every morning.",
        "grammar_opts": ["go", "goes", "going", "gone"],
        "grammar_ans": "goes",
        "grammar_exp": "მესამე პირის ერთობითში (he/she/it) ემატება -s.",
        "mcq_q": "What does 'big' mean?",
        "mcq_opts": ["პატარა", "დიდი", "ლამაზი", "სწრაფი"],
        "mcq_ans": "დიდი",
        "mcq_exp": "'Big' ნიშნავს 'დიდი' — ზომის აღმნიშვნელი ზედსართავი სახელია.",
        "sentence_words": ["I", "have", "a", "black", "cat"],
        "sentence_answer": "I have a black cat",
        "sentence_hint": "ააგეთ წინადადება ამ სიტყვებიდან:",
    },
    "A2": {
        "vocab": [
            {"word": "journey", "meaning": "მოგზაურობა", "example": "The journey took three hours."},
            {"word": "market", "meaning": "ბაზარი", "example": "We buy vegetables at the market."},
            {"word": "favourite", "meaning": "საყვარელი", "example": "Pizza is my favourite food."},
            {"word": "weather", "meaning": "ამინდი", "example": "The weather is nice today."},
        ],
        "grammar_rule": "სახელწოდება <b>Past Simple</b> — გამოიყენება დასრულებული წარსული ქმედებებისთვის.\n\n📌 წესიერი ზმნები: ზმნა + <b>-ed</b> | მოურიგე: went, saw, had...\n\n✦ I visited Paris last year.\n✦ She went to the cinema yesterday.",
        "grammar_q": "They ___ football last Saturday.",
        "grammar_opts": ["play", "plays", "played", "playing"],
        "grammar_ans": "played",
        "grammar_exp": "წარსული დრო Regular ზმნებში = ზმნა + -ed.",
        "mcq_q": "Which word means 'very happy'?",
        "mcq_opts": ["sad", "angry", "delighted", "tired"],
        "mcq_ans": "delighted",
        "mcq_exp": "'Delighted' ნიშნავს ძალიან ბედნიერს. 'Sad'=მოწყენილი, 'angry'=გაბრაზებული.",
        "sentence_words": ["She", "bought", "a", "red", "dress", "yesterday"],
        "sentence_answer": "She bought a red dress yesterday",
        "sentence_hint": "ააგეთ წარსულ დროში:",
    },
    "B1": {
        "vocab": [
            {"word": "ambitious", "meaning": "მიზანდასახული", "example": "She is very ambitious and works hard."},
            {"word": "efficient", "meaning": "ეფექტიანი", "example": "The new system is more efficient."},
            {"word": "negotiate", "meaning": "მოლაპარაკება", "example": "They negotiated a better deal."},
            {"word": "opportunity", "meaning": "შესაძლებლობა", "example": "This is a great opportunity."},
        ],
        "grammar_rule": "სახელწოდება <b>Present Perfect</b> — გამოიყენება, როდესაც წარსული ქმედება კვლავ აქვს კავშირი აწმყოსთან.\n\n📌 ფორმა: have/has + <b>Past Participle</b>\n\n✦ I have lived here for 5 years.\n✦ She has just finished the report.",
        "grammar_q": "He ___ three books this month.",
        "grammar_opts": ["read", "reads", "has read", "had read"],
        "grammar_ans": "has read",
        "grammar_exp": "Present Perfect: has + Past Participle. 'this month' = კავშირი აწმყოსთან.",
        "mcq_q": "Choose the correct meaning of 'despite':",
        "mcq_opts": ["იმიტომ რომ", "მიუხედავად", "თუ", "სანამ"],
        "mcq_ans": "მიუხედავად",
        "mcq_exp": "'Despite' = მიუხედავად. მაგ: Despite the rain, we went out.",
        "sentence_words": ["I", "have", "never", "been", "to", "Japan"],
        "sentence_answer": "I have never been to Japan",
        "sentence_hint": "Present Perfect-ით ააგეთ:",
    },
    "B2": {
        "vocab": [
            {"word": "pragmatic", "meaning": "პრაგმატული", "example": "We need a pragmatic approach."},
            {"word": "leverage", "meaning": "გამოყენება/ბერკეტი", "example": "They leveraged their network effectively."},
            {"word": "inevitable", "meaning": "გარდაუვალი", "example": "Change is inevitable in life."},
            {"word": "nuance", "meaning": "ნიუანსი", "example": "The nuance of the argument was lost."},
        ],
        "grammar_rule": "სახელწოდება <b>Third Conditional</b> — გამოხატავს შეუსრულებელ წარსულ პირობასა და მის შედეგს.\n\n📌 ფორმა: If + <b>Past Perfect</b>, would/could have + <b>Past Participle</b>\n\n✦ If she had studied, she would have passed.\n✦ If I had known, I could have helped.",
        "grammar_q": "If they ___ earlier, they ___ the flight.",
        "grammar_opts": [
            "left / wouldn't miss",
            "had left / wouldn't have missed",
            "leave / won't miss",
            "had left / won't miss"
        ],
        "grammar_ans": "had left / wouldn't have missed",
        "grammar_exp": "Third Conditional: had + PP → would have + PP. ორივე ნაწილი წარსულზე.",
        "mcq_q": "Which sentence uses 'although' correctly?",
        "mcq_opts": [
            "Although she was tired, but she continued.",
            "Although she was tired, she continued.",
            "She continued although but tired.",
            "She was tired, although continued."
        ],
        "mcq_ans": "Although she was tired, she continued.",
        "mcq_exp": "'Although' არ გამოიყენება 'but'-თან ერთად. სწორი სტრუქტურა: Although + clause, main clause.",
        "sentence_words": ["Had", "I", "known", "the", "truth", "I", "would", "have", "acted", "differently"],
        "sentence_answer": "Had I known the truth I would have acted differently",
        "sentence_hint": "Inversion Third Conditional:",
    },
}

LEVEL_INFO = {
    "A1": {"label": "A1 — Beginner", "css": "pill-a1", "emoji": "🌱", "desc": "საბაზისო ინგლისური — მისალმება, ოჯახი, ყოველდღიური სიტყვები"},
    "A2": {"label": "A2 — Elementary", "css": "pill-a2", "emoji": "📘", "desc": "ელემენტარული — მარტივი საუბარი, ყოველდღიური სიტუაციები"},
    "B1": {"label": "B1 — Intermediate", "css": "pill-b1", "emoji": "⚡", "desc": "საშუალო — თავისუფალი საუბარი, ახალი ამბები, სამუშაო"},
    "B2": {"label": "B2 — Upper-Intermediate", "css": "pill-b2", "emoji": "🔥", "desc": "ზედა-საშუალო — კომპლექსური გრამატიკა, ბიზნეს ინგლისური"},
}

# ── SESSION STATE ─────────────────────────────────────────────────────────
def init():
    defs = {
        "screen": "home",          # home | placement | result | lesson
        "pl_idx": 0,               # placement question index
        "pl_correct": 0,
        "pl_history": [],          # list of level_target where answered correctly
        "pl_answered": False,
        "pl_last_correct": None,
        "user_level": None,
        "lesson_tab": "vocab",     # vocab | grammar | mcq | writing
        "lesson_grammar_answered": False,
        "lesson_grammar_correct": None,
        "lesson_mcq_answered": False,
        "lesson_mcq_correct": None,
        "lesson_writing_submitted": False,
        "lesson_writing_correct": None,
        "lesson_writing_input": "",
        "xp": 0,
        "streak": 1,
        "lessons_done": 0,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()
S = st.session_state

# ── HELPERS ──────────────────────────────────────────────────────────────
def go(screen):
    S.screen = screen

def level_pill(level):
    info = LEVEL_INFO[level]
    return f'<span class="level-pill {info["css"]}">{info["emoji"]} {info["label"]}</span>'

def dot_nav(total, current):
    dots = ""
    for i in range(total):
        if i < current:
            dots += '<div class="dot done"></div>'
        elif i == current:
            dots += '<div class="dot active"></div>'
        else:
            dots += '<div class="dot"></div>'
    return f'<div class="step-dots">{dots}</div>'

def compute_level():
    h = S.pl_history
    if not h:
        return "A1"
    b2 = h.count("B2")
    b1 = h.count("B1")
    a2 = h.count("A2")
    a1 = h.count("A1")
    if b2 >= 1 and b1 >= 1:
        return "B2"
    elif b1 >= 1 or (a2 >= 2 and b2 >= 1):
        return "B1"
    elif a2 >= 1:
        return "A2"
    return "A1"

# ════════════════════════════════════════════════════════════════════════════
# SCREEN: HOME
# ════════════════════════════════════════════════════════════════════════════
if S.screen == "home":
    st.markdown("""
    <div class="hero">
        <div class="hero-logo">LinguaFlow</div>
        <div class="hero-sub">ადაპტური ინგლისური — CEFR A1 → B2</div>
        <div class="hero-tagline">BKT · IRT · Adaptive Learning · ბაკალავრის ნაშრომი</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="section-title">გამარჯობა! 👋</div>
        <div class="section-sub">
            LinguaFlow ჯერ განსაზღვრავს შენს ინგლისურის დონეს (Placement Test),
            შემდეგ კი ყოველდღიურად გთავაზობს პერსონალიზებულ გაკვეთილებს —
            ლექსიკა, გრამატიკა, ტესტები და წინადადების აგება.
        </div>
        <div class="divider"></div>
        <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.2rem;">
            <div style="flex:1; min-width:140px; text-align:center; padding:1rem; background:rgba(96,165,250,0.06); border-radius:12px; border:1px solid rgba(96,165,250,0.15);">
                <div style="font-size:1.6rem;">🎯</div>
                <div style="font-size:0.82rem; color:#60a5fa; margin-top:0.4rem; font-weight:600;">Placement Test</div>
                <div style="font-size:0.75rem; color:#475569; margin-top:0.2rem;">8 კითხვა, 4 დონე</div>
            </div>
            <div style="flex:1; min-width:140px; text-align:center; padding:1rem; background:rgba(168,85,247,0.06); border-radius:12px; border:1px solid rgba(168,85,247,0.15);">
                <div style="font-size:1.6rem;">📚</div>
                <div style="font-size:0.82rem; color:#c084fc; margin-top:0.4rem; font-weight:600;">ყოველდღიური გაკვეთილი</div>
                <div style="font-size:0.75rem; color:#475569; margin-top:0.2rem;">4 სექცია</div>
            </div>
            <div style="flex:1; min-width:140px; text-align:center; padding:1rem; background:rgba(34,197,94,0.06); border-radius:12px; border:1px solid rgba(34,197,94,0.15);">
                <div style="font-size:1.6rem;">⚡</div>
                <div style="font-size:0.82rem; color:#4ade80; margin-top:0.4rem; font-weight:600;">ადაპტური სისტემა</div>
                <div style="font-size:0.75rem; color:#475569; margin-top:0.2rem;">BKT · IRT მოდელი</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🎯  Placement Test-ის დაწყება", key="start_placement"):
            S.screen = "placement"
            S.pl_idx = 0
            S.pl_correct = 0
            S.pl_history = []
            S.pl_answered = False
            st.rerun()
    with col2:
        if S.user_level and st.button("📚  გაკვეთილი", key="go_lesson_home"):
            S.screen = "lesson"
            st.rerun()

    if S.user_level:
        st.markdown(f"""
        <div class="card" style="margin-top:0.8rem;">
            <div style="font-size:0.8rem; color:#475569; margin-bottom:0.5rem;">შენი დონე</div>
            {level_pill(S.user_level)}
            <div style="font-size:0.85rem; color:#64748b; margin-top:0.5rem;">{LEVEL_INFO[S.user_level]['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SCREEN: PLACEMENT TEST
# ════════════════════════════════════════════════════════════════════════════
elif S.screen == "placement":
    total_q = len(PLACEMENT_QUESTIONS)

    if S.pl_idx >= total_q:
        S.user_level = compute_level()
        S.screen = "result"
        st.rerun()

    q = PLACEMENT_QUESTIONS[S.pl_idx]
    pct = S.pl_idx / total_q

    st.markdown(f"""
    <div class="hero" style="padding:2rem 1rem 1rem;">
        <div class="hero-logo" style="font-size:2rem;">Placement Test</div>
        <div class="hero-sub">განსაზღვრე შენი CEFR დონე</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(dot_nav(total_q, S.pl_idx), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label">
            <span>კითხვა {S.pl_idx + 1} / {total_q}</span>
            <span style="color:#60a5fa;">{int(pct*100)}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(pct)

    st.markdown(f"""
    <div class="card">
        <div style="font-size:0.78rem; color:#475569; margin-bottom:0.8rem; text-transform:uppercase; letter-spacing:0.1em;">
            დონე: {q['level_target']}
        </div>
        <div class="q-text">{q['q']}</div>
    </div>
    """, unsafe_allow_html=True)

    if not S.pl_answered:
        cols = st.columns(2)
        for i, opt in enumerate(q["options"]):
            with cols[i % 2]:
                if st.button(opt, key=f"popt_{S.pl_idx}_{i}"):
                    S.pl_answered = True
                    S.pl_last_correct = (opt == q["correct"])
                    if S.pl_last_correct:
                        S.pl_correct += 1
                        S.pl_history.append(q["level_target"])
                    st.rerun()
    else:
        if S.pl_last_correct:
            st.markdown(f'<div class="fb-correct">✓ სწორია!<div class="fb-explain">{q["explain"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="fb-wrong">✗ მცდარია — სწორი: <b>{q["correct"]}</b><div class="fb-explain">{q["explain"]}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("შემდეგი →", key="pl_next"):
            S.pl_idx += 1
            S.pl_answered = False
            S.pl_last_correct = None
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# SCREEN: RESULT
# ════════════════════════════════════════════════════════════════════════════
elif S.screen == "result":
    lvl = S.user_level
    info = LEVEL_INFO[lvl]
    score_pct = int(S.pl_correct / len(PLACEMENT_QUESTIONS) * 100)

    st.markdown(f"""
    <div class="card">
        <div class="result-hero">
            <div style="font-size:3rem; margin-bottom:0.5rem;">{info['emoji']}</div>
            <div class="result-score">{score_pct}%</div>
            <div class="result-level">{info['label']}</div>
            <div class="result-msg">{info['desc']}</div>
        </div>
        <div class="divider"></div>
        {level_pill(lvl)}
        <div style="font-size:0.88rem; color:#475569; margin-top:0.5rem; line-height:1.7;">
            სწორი პასუხები: <b style="color:#60a5fa;">{S.pl_correct} / {len(PLACEMENT_QUESTIONS)}</b><br>
            სისტემამ განსაზღვრა შენი CEFR დონე ადაპტური BKT ალგორითმის გამოყენებით.
            ახლა შეგიძლია დაიწყო ყოველდღიური პერსონალიზებული გაკვეთილი.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚  გაკვეთილის დაწყება", key="go_lesson"):
            S.screen = "lesson"
            S.lesson_tab = "vocab"
            S.lesson_grammar_answered = False
            S.lesson_mcq_answered = False
            S.lesson_writing_submitted = False
            st.rerun()
    with col2:
        if st.button("🔄  Placement-ის გამეორება", key="redo_pl"):
            S.screen = "placement"
            S.pl_idx = 0
            S.pl_correct = 0
            S.pl_history = []
            S.pl_answered = False
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# SCREEN: DAILY LESSON
# ════════════════════════════════════════════════════════════════════════════
elif S.screen == "lesson":
    lvl = S.user_level or "A1"
    content = DAILY_CONTENT[lvl]
    info = LEVEL_INFO[lvl]

    # Header
    st.markdown(f"""
    <div class="hero" style="padding:1.5rem 1rem 0.5rem; text-align:left;">
        <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem;">
            <div>
                <div class="hero-logo" style="font-size:1.6rem;">ყოველდღიური გაკვეთილი</div>
                {level_pill(lvl)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # XP / Stats
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box"><div class="stat-val">{S.xp}</div><div class="stat-lbl">XP</div></div>
        <div class="stat-box"><div class="stat-val">{S.streak}</div><div class="stat-lbl">🔥 streak</div></div>
        <div class="stat-box"><div class="stat-val">{S.lessons_done}</div><div class="stat-lbl">გაკვეთილი</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Tab selector
    tabs = [("📖", "vocab", "ლექსიკა"), ("📝", "grammar", "გრამატიკა"), ("✔", "mcq", "ტესტი"), ("✏️", "writing", "წინადადება")]
    tab_html = '<div class="nav-tabs">'
    for icon, key, label in tabs:
        cls = "active" if S.lesson_tab == key else "inactive"
        tab_html += f'<div class="nav-tab {cls}">{icon} {label}</div>'
    tab_html += '</div>'
    st.markdown(tab_html, unsafe_allow_html=True)

    tcols = st.columns(4)
    tab_keys = ["vocab", "grammar", "mcq", "writing"]
    tab_labels = ["📖 ლექსიკა", "📝 გრამატიკა", "✔ ტესტი", "✏️ წინადადება"]
    for i, (tk, tl) in enumerate(zip(tab_keys, tab_labels)):
        with tcols[i]:
            if st.button(tl, key=f"tab_{tk}"):
                S.lesson_tab = tk
                st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── VOCAB TAB ──
    if S.lesson_tab == "vocab":
        st.markdown("""
        <div class="lesson-header">
            <div class="lesson-icon icon-vocab">📖</div>
            <div>
                <div class="lesson-title">დღის ლექსიკა</div>
                <div class="lesson-desc">4 ახალი სიტყვა შენი დონისთვის</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for v in content["vocab"]:
            st.markdown(f"""
            <div class="vocab-card">
                <div>
                    <div class="vocab-word">{v['word']}</div>
                    <div class="vocab-meaning">{v['meaning']}</div>
                    <div class="vocab-example">"{v['example']}"</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("გრამატიკაზე გადასვლა →", key="to_grammar"):
            S.lesson_tab = "grammar"
            st.rerun()

    # ── GRAMMAR TAB ──
    elif S.lesson_tab == "grammar":
        st.markdown("""
        <div class="lesson-header">
            <div class="lesson-icon icon-grammar">📝</div>
            <div>
                <div class="lesson-title">გრამატიკის წესი</div>
                <div class="lesson-desc">წესი + პრაქტიკული სავარჯიშო</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        rule_lines = content["grammar_rule"].replace("\n", "<br>")
        st.markdown(f'<div class="grammar-box">{rule_lines}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="q-text">🧩 &nbsp;{content["grammar_q"]}</div>', unsafe_allow_html=True)

        if not S.lesson_grammar_answered:
            gcols = st.columns(2)
            for i, opt in enumerate(content["grammar_opts"]):
                with gcols[i % 2]:
                    if st.button(opt, key=f"gopt_{i}"):
                        S.lesson_grammar_answered = True
                        S.lesson_grammar_correct = (opt == content["grammar_ans"])
                        if S.lesson_grammar_correct:
                            S.xp += 15
                        st.rerun()
        else:
            if S.lesson_grammar_correct:
                st.markdown(f'<div class="fb-correct">✓ სწორია! +15 XP<div class="fb-explain">{content["grammar_exp"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="fb-wrong">✗ მცდარია — სწორი: <b>{content["grammar_ans"]}</b><div class="fb-explain">{content["grammar_exp"]}</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ტესტზე გადასვლა →", key="to_mcq"):
                S.lesson_tab = "mcq"
                st.rerun()

    # ── MCQ TAB ──
    elif S.lesson_tab == "mcq":
        st.markdown("""
        <div class="lesson-header">
            <div class="lesson-icon icon-test">✔</div>
            <div>
                <div class="lesson-title">გამგებლობის ტესტი</div>
                <div class="lesson-desc">შეამოწმე ლექსიკის ცოდნა</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="q-text">❓ &nbsp;{content["mcq_q"]}</div>', unsafe_allow_html=True)

        if not S.lesson_mcq_answered:
            mcols = st.columns(2)
            for i, opt in enumerate(content["mcq_opts"]):
                with mcols[i % 2]:
                    if st.button(opt, key=f"mopt_{i}"):
                        S.lesson_mcq_answered = True
                        S.lesson_mcq_correct = (opt == content["mcq_ans"])
                        if S.lesson_mcq_correct:
                            S.xp += 20
                        st.rerun()
        else:
            if S.lesson_mcq_correct:
                st.markdown(f'<div class="fb-correct">✓ სწორია! +20 XP<div class="fb-explain">{content["mcq_exp"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="fb-wrong">✗ მცდარია — სწორი: <b>{content["mcq_ans"]}</b><div class="fb-explain">{content["mcq_exp"]}</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("წინადადებაზე გადასვლა →", key="to_writing"):
                S.lesson_tab = "writing"
                st.rerun()

    # ── WRITING / SENTENCE BUILD TAB ──
    elif S.lesson_tab == "writing":
        st.markdown("""
        <div class="lesson-header">
            <div class="lesson-icon icon-writing">✏️</div>
            <div>
                <div class="lesson-title">წინადადების აგება</div>
                <div class="lesson-desc">დაწერე სწორი წინადადება</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="q-text">🔤 &nbsp;{content["sentence_hint"]}</div>', unsafe_allow_html=True)

        # Show word chips
        chips = "".join([f'<span class="word-chip">{w}</span>' for w in content["sentence_words"]])
        st.markdown(f'<div style="margin-bottom:1.2rem; line-height:2.2;">{chips}</div>', unsafe_allow_html=True)

        if not S.lesson_writing_submitted:
            user_input = st.text_input("შენი პასუხი:", placeholder="ჩაწერე წინადადება...", key="writing_input")
            if st.button("✓  შემოწმება", key="check_writing"):
                if user_input.strip():
                    correct_clean = content["sentence_answer"].lower().strip().rstrip(".")
                    user_clean = user_input.lower().strip().rstrip(".")
                    S.lesson_writing_correct = (user_clean == correct_clean)
                    S.lesson_writing_submitted = True
                    if S.lesson_writing_correct:
                        S.xp += 25
                        S.lessons_done += 1
                    st.rerun()
        else:
            if S.lesson_writing_correct:
                st.markdown(f'<div class="fb-correct">✓ სწორია! +25 XP 🎉<div class="fb-explain">სწორი: <b>{content["sentence_answer"]}</b></div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="fb-wrong">✗ თითქმის! სწორია: <b>{content["sentence_answer"]}</b></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">🎓</div>
                <div style="font-size:1.1rem; color:#60a5fa; font-weight:600;">გაკვეთილი დასრულდა!</div>
                <div style="font-size:0.88rem; color:#475569; margin-top:0.5rem;">
                    მოპოვებული XP: <b style="color:#60a5fa;">{S.xp}</b> &nbsp;|&nbsp; გაკვეთილები: <b style="color:#c084fc;">{S.lessons_done}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠  მთავარი", key="done_home"):
                    S.screen = "home"
                    st.rerun()
            with col2:
                if st.button("🔄  კიდევ ერთხელ", key="done_retry"):
                    S.lesson_grammar_answered = False
                    S.lesson_grammar_correct = None
                    S.lesson_mcq_answered = False
                    S.lesson_mcq_correct = None
                    S.lesson_writing_submitted = False
                    S.lesson_writing_correct = None
                    S.lesson_tab = "vocab"
                    st.rerun()

    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← მთავარი გვერდი", key="back_home"):
        S.screen = "home"
        st.rerun()
