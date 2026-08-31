"""
===============================================================================
Python Strings: Essential Production Practices & Real-World Patterns
===============================================================================
Level: Intermediate to Practical Production Code
===============================================================================
"""

s = "ali is good boy"

mystring = [ch.lower() for ch in s]
print(f"my lower string are \n {mystring}")

# =============================================================================
# 1. MODERN STRING FORMATTING (f-strings)
# =============================================================================
# f-strings (Python 3.6+) are faster, more readable, and standard in production.

name = "Alice"
score = 94.5678
total_users = 1250000

# A. Basic Variable Interpolation
print(f"User: {name}, Score: {score}")

# B. Number Formatting (Rounding floats & Thousand Separators)
print(f"Formatted Score : {score:.2f}")           # 94.57 (2 decimal places)
print(f"Total Users     : {total_users:,}")        # 1,250,000 (adds commas)

# C. Padding & Alignment (Great for logs and terminal reports)
print(f"{'Status':<10} | {'Count':>8}")            # Left & Right aligned
print(f"{'SUCCESS':<10} | {200:>8}")
print(f"Order ID: {42:06d}")                       # 000042 (zero-padded 6 digits)

# D. Debugging Flag (f"{var=}") - Python 3.8+
status_code = 404
print(f"Debugging: {status_code=}")                # Prints: Debugging: status_code=404


# =============================================================================
# 2. STRING SANITIZATION & STRIPPING
# =============================================================================
# Clean user inputs, API parameters, or database strings.

raw_user_input = "   john.doe@example.com  \n"

# A. Removing Leading / Trailing Whitespace
clean_email = raw_user_input.strip()
print(f"Cleaned Email: '{clean_email}'")

# B. Removing Specific Prefix/Suffix (Python 3.9+ removeprefix / removesuffix)
# Safer than .replace() because it only removes from the edges!
url = "https://api.example.com/v1/users/"
clean_url = url.removeprefix("https://").removesuffix("/")
print(f"Cleaned URL: '{clean_url}'")


# =============================================================================
# 3. CASE-INSENSITIVE COMPARISONS & SEARCHING
# =============================================================================
# Always normalize strings before comparing user input or search queries.

input_role = "Admin "
target_role = "admin"

# Case-insensitive check using .lower() or .casefold() (.casefold is stronger for international text)
if input_role.strip().lower() == target_role:
    print("Access Granted!")

# Substring Search: Use 'in' keyword (Pythonic & Readable)
user_bio = "Full-stack Python Developer specializing in backend APIs"

if "python" in user_bio.lower():
    print("Found Python in bio!")

# Check Start or End of a string (Supports tuples of options!)
filename = "invoice_2026_07.pdf"

if filename.startswith(("invoice", "bill")) and filename.endswith((".pdf", ".png")):
    print(f"Valid document file: {filename}")


# =============================================================================
# 4. SPLITTING, JOINING & PARTITIONING (Parsing Logs / CSVs)
# =============================================================================

# A. Splitting by Delimiter
log_line = "2026-07-29 | ERROR | Database connection failed"
parts = log_line.split(" | ")
date, log_level, message = parts
print(f"Parsed Log Level: {log_level}, Message: {message}")

# B. Joining Lists into Strings (Crucial: .join() takes a list of strings)
tags = ["python", "django", "fastapi"]
hashtag_string = " #".join(tags)
print(f"Hashtags: #{hashtag_string}")

# C. rsplit with maxsplit (Extracting file extensions or path parts)
file_path = "documents.backup.final.pdf"
name_part, extension = file_path.rsplit(".", maxsplit=1)
print(f"File Name: {name_part} | Extension: {extension}")

# D. partition() (Splits string into 3 parts: before, separator, after)
email = "user@domain.com"
username, sep, domain = email.partition("@")
print(f"User: {username}, Domain: {domain}")


# =============================================================================
# 5. STRING VALIDATION METHODS (Checking Input Integrity)
# =============================================================================

phone_num = "1234567890"
username_input = "user_99"

print(f"Is phone digits only? {phone_num.isdigit()}")        # True
print(f"Is username alphanumeric? {username_input.isalnum()}")# False (due to '_')


# =============================================================================
# 6. SLICING & TRUNCATION PATTERNS
# =============================================================================

sample_text = "Python Programming Language"

# A. Slicing Syntax: [start : stop : step]
print("First 6 chars :", sample_text[:6])              # 'Python'
print("Last 8 chars  :", sample_text[-8:])             # 'Language'
print("Reversed string:", sample_text[::-1])           # 'egaugnaL gnimmargorP nohtyP'

# B. Safe Truncation for Previews (UI / Logs)
def truncate_text(text: str, max_length: int = 20) -> str:
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text

long_description = "This is a very long log message that needs to be truncated for display."
print("Preview:", truncate_text(long_description, max_length=30))
