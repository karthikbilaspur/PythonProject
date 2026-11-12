
import streamlit as st
import datetime
import ast
import operator
from typing import Callable, cast

st.set_page_config(page_title="LIFECODE — You, Translated", page_icon="🧬", layout="wide")

# ---------- Helpers ----------
DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Number = int | float


def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    if base < 2 or base > 36:
        return "?"
    neg = n < 0
    n = abs(n)
    out = ""
    while n > 0:
        out = DIGITS[n % base] + out
        n //= base
    return ("-" if neg else "") + out


def to_base_frac(value: float, base: int, precision: int = 6) -> str:
    if base < 2 or base > 36:
        return "?"
    neg = value < 0
    value = abs(value)
    integer = int(value)
    frac = value - integer
    int_part = to_base(integer, base)
    if frac < 1e-9:
        return ("-" if neg else "") + int_part
    frac_digits = ""
    for _ in range(precision):
        frac *= base
        d = int(frac)
        frac_digits += DIGITS[d]
        frac -= d
        if frac < 1e-9:
            break
    return ("-" if neg else "") + int_part + "." + frac_digits


def parse_date_flexible(text: str):
    text = text.strip()
    # Try ISO first, then common formats, then dateparser if available
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y", "%d-%b-%Y"):
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except Exception:
            pass
    try:
        import dateparser  # pyright: ignore[reportMissingModuleSource]

        dt = dateparser.parse(text)
        if dt:
            return dt.date()
    except Exception:
        pass
    return None


def safe_eval(expr: str, variables: dict[str, Number]) -> Number:
    # Safe calculator - no eval(), only ast
    binary_op: Callable[[Number, Number], Number] = cast(Callable[[Number, Number], Number], operator.add)
    binary_sub: Callable[[Number, Number], Number] = cast(Callable[[Number, Number], Number], operator.sub)
    binary_mul: Callable[[Number, Number], Number] = cast(Callable[[Number, Number], Number], operator.mul)
    binary_div: Callable[[Number, Number], Number] = lambda a, b: a / b
    binary_mod: Callable[[Number, Number], Number] = cast(Callable[[Number, Number], Number], operator.mod)
    binary_pow: Callable[[Number, Number], Number] = lambda a, b: a ** b
    unary_neg: Callable[[Number], Number] = cast(Callable[[Number], Number], operator.neg)
    unary_pos: Callable[[Number], Number] = cast(Callable[[Number], Number], operator.pos)

    allowed_ops: dict[type[ast.AST], Callable[..., Number]] = {
        ast.Add: binary_op,
        ast.Sub: binary_sub,
        ast.Mult: binary_mul,
        ast.Div: binary_div,
        ast.Mod: binary_mod,
        ast.Pow: binary_pow,
        ast.USub: unary_neg,
        ast.UAdd: unary_pos,
    }

    def _eval(node: ast.AST) -> Number:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return node.value
            raise ValueError("Only numbers allowed")
        if isinstance(node, ast.Name):
            if node.id in variables:
                value = variables[node.id]
                return value
            raise ValueError(f"Unknown variable: {node.id}")
        if isinstance(node, ast.BinOp):
            op = allowed_ops.get(type(node.op))
            if op is not None:
                left = _eval(node.left)
                right = _eval(node.right)
                return op(left, right)
        if isinstance(node, ast.UnaryOp):
            op = allowed_ops.get(type(node.op))
            if op is not None:
                operand = _eval(node.operand)
                return op(operand)
        raise ValueError("Not allowed in this calculator")

    tree = ast.parse(expr, mode="eval")
    return _eval(tree)

def next_birthday(birthdate: datetime.date, today: datetime.date) -> datetime.date:
    # Feb 29 safe
    try:
        nb = datetime.date(today.year, birthdate.month, birthdate.day)
    except ValueError:
        nb = datetime.date(today.year, 2, 28)
    if nb < today:
        try:
            nb = datetime.date(today.year + 1, birthdate.month, birthdate.day)
        except ValueError:
            nb = datetime.date(today.year + 1, 2, 28)
    return nb

# ---------- State ----------
if "history" not in st.session_state:
    st.session_state["history"] = []
history: list[str] = cast(list[str], st.session_state["history"])

# ---------- UI ----------
st.title("🧬 LIFECODE")
st.caption("Don't just calculate your age. Translate your life — into every base, planet, and system.")

with st.sidebar:
    st.header("👤 You")
    birth_input = st.text_input("Birthdate (try: 1994-01-12 or 12 Jan 1994)", value="1994-01-12")
    st.divider()
    st.header("🧍 Body")
    weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
    height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0)
    st.divider()
    st.header("⚙️ Display Base")
    display_base = st.slider("Show age also in base", 2, 36, 16)
    st.caption("2=Binary, 8=Octal, 16=Hex, 36=Base36")

birthdate = parse_date_flexible(birth_input)
today = datetime.date.today()

if not birthdate:
    st.error("Couldn't understand that birthdate. Try YYYY-MM-DD or '12 Jan 1994'")
    st.stop()
if birthdate > today:
    st.error("That birthdate is in the future — are you a time traveller? 👀")
    st.stop()

# Calculations
age_years = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
total_days = (today - birthdate).days
total_hours = total_days * 24
total_minutes = total_hours * 60
total_seconds = total_minutes * 60
months = (today.year - birthdate.year) * 12 + today.month - birthdate.month
if today.day < birthdate.day:
    months -= 1
weeks = total_days // 7
nb = next_birthday(birthdate, today)
days_to_bday = (nb - today).days

height_m = height_cm / 100
bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0
if bmi < 18.5:
    bmi_cat, bmi_emoji = "Underweight", "🩵"
elif bmi < 25:
    bmi_cat, bmi_emoji = "Normal", "💚"
elif bmi < 30:
    bmi_cat, bmi_emoji = "Overweight", "🧡"
else:
    bmi_cat, bmi_emoji = "Obese", "❤️"

planets = [
    ("Earth 🌍", 365.25, 1.0),
    ("Mercury ☿️", 88.0, 0.38),
    ("Venus ♀️", 224.7, 0.91),
    ("Mars ♂️", 687.0, 0.38),
    ("Jupiter ♃", 4331.0, 2.34),
    ("Saturn ♄", 10747.0, 1.06),
    ("Moon 🌙", 27.3, 0.166),
]

tab1, tab2, tab3 = st.tabs(["⏳ TIME", "🧍 BODY", "🌌 UNIVERSE CALCULATOR"])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Age", f"{age_years} years")
    c2.metric("Days Alive", f"{total_days:,}")
    c3.metric("Next Birthday", nb.strftime("%d %b %Y"))
    c4.metric("Days to Birthday", f"{days_to_bday} days")

    st.subheader(f"Your age in Base {display_base} and friends")
    cols = st.columns(4)
    for i, b in enumerate([2, 8, 16, display_base]):
        with cols[i]:
            st.code(f"Base {b}: {to_base(age_years, b)}", language="text")
    st.info(f"In Base {display_base}, your {total_days:,} days alive = **{to_base(total_days, display_base)}**")

    st.subheader("Detailed Age")
    st.write(f"**Months:** {months:,} | **Weeks:** {weeks:,} | **Days:** {total_days:,} | **Hours:** {total_hours:,} | **Minutes:** {total_minutes:,} | **Seconds:** {total_seconds:,}")
    st.progress(min(days_to_bday / 365, 1.0), text=f"{days_to_bday} days until you turn {age_years + 1}")

    st.subheader("Age on Other Planets")
    for name, orbital_days, _g in planets:
        p_age = total_days / orbital_days
        st.write(f"**{name}:** {p_age:.2f} years old")

with tab2:
    c1, c2, c3 = st.columns(3)
    c1.metric("BMI", f"{bmi:.1f}")
    c2.metric("Category", f"{bmi_emoji} {bmi_cat}")
    c3.metric("Height", f"{height_cm:.0f} cm / {height_cm/30.48:.1f} ft")
    st.caption(f"Weight in lbs: {weight_kg*2.20462:.1f} lbs | BMI in Hex: {to_base_frac(bmi, 16, 2)} | BMI in Binary: {to_base_frac(bmi, 2, 4)}")
    st.subheader("Your weight elsewhere")
    for name, _orb, gravity in planets:
        st.write(f"**{name}:** {weight_kg * gravity:.1f} kg")

with tab3:
    st.write("Use variables: `age`, `days`, `bmi`, `days_to_bday`, `months`, `seconds`. Try: `age * 2 + bmi` or `days in binary?` — use the converter below.")
    expr = st.text_input("Expression", value="age * 2 + bmi", key="expr")
    col_a, col_b = st.columns([1, 2])
    if col_a.button("Calculate", type="primary"):
        variables = {"age": age_years, "days": total_days, "bmi": round(bmi, 2), "days_to_bday": days_to_bday, "months": months, "seconds": total_seconds, "weeks": weeks}
        try:
            result = safe_eval(expr, variables)
            st.success(f"= {result}")
            history.append(f"{expr} = {result}")
        except Exception as e:
            st.error(f"Error: {e}")
    with col_b:
        st.markdown("**Available variables:** `age`, `days`, `months`, `weeks`, `seconds`, `bmi`, `days_to_bday`")

    st.subheader("Any Number → Any Base")
    n1, n2 = st.columns(2)
    num_to_convert = n1.text_input("Number (decimal)", value=str(age_years))
    base_to = n2.slider("Convert to base", 2, 36, 16, key="conv_base")
    try:
        val = float(num_to_convert)
        st.code(f"{val} in Base {base_to} = {to_base_frac(val, base_to, 6)}")
    except:
        st.error("Enter a valid number")

    st.subheader("History")
    if history:
        for h in reversed(history[-10:]):
            st.write(f"• {h}")
        if st.button("Clear History"):
            st.session_state["history"] = []
            st.rerun()
    else:
        st.caption("No calculations yet. Your history lives here, in this session.")

st.divider()
st.caption("LIFECODE • Built from your Age + Base-N + BMI + Flask calculators — now safe (no eval), Feb 29 safe, and multilingual-date friendly.")
