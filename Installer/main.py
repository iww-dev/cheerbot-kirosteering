#!/usr/bin/env python3
import os
import sys
import re
import time
from pathlib import Path

NEW_VERSION = "0.0.1"

class Colors:
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GRAY = '\033[90m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class UI:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def header():
        print(f"{Colors.MAGENTA}{'═' * 50}")
        print(f"  ▸ Cheerbot Installer v0.0.2 ◂")
        print(f"{'═' * 50}{Colors.RESET}\n")

    @staticmethod
    def section(title):
        print(f"{Colors.MAGENTA}├─ {title} {Colors.RESET}")

    @staticmethod
    def item(text, status=None):
        if status == "ok":
            print(f"{Colors.MAGENTA}│  {Colors.GREEN}✓{Colors.RESET} {text}")
        elif status == "warn":
            print(f"{Colors.MAGENTA}│  {Colors.YELLOW}▲{Colors.RESET} {text}")
        elif status == "err":
            print(f"{Colors.MAGENTA}│  {Colors.RED}✗{Colors.RESET} {text}")
        else:
            print(f"{Colors.MAGENTA}│  {Colors.GRAY}•{Colors.RESET} {text}")

    @staticmethod
    def info(text):
        print(f"{Colors.GRAY}{text}{Colors.RESET}")

    @staticmethod
    def success(text):
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

    @staticmethod
    def error(text):
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")

    @staticmethod
    def warning(text):
        print(f"{Colors.YELLOW}▲ {text}{Colors.RESET}")

    @staticmethod
    def progress(percent):
        filled = percent // 5
        bar = f"  [{Colors.MAGENTA}{'█' * filled}{Colors.RESET}{'░' * (20 - filled)}] {percent}%"
        sys.stdout.write(f"\r{bar}")
        sys.stdout.flush()

    @staticmethod
    def footer():
        print(f"\n{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.GRAY}Press Enter to exit...{Colors.RESET}")

def run_diagnostics():
    UI.section("System Check")
    
    user_name = os.getenv('USERNAME')
    user_path = Path(f"C:\\Users\\{user_name}")
    kiro_path = user_path / ".kiro"

    if user_path.exists():
        UI.item(f"User path: {user_path}", "ok")
    else:
        UI.item(f"User path: NOT FOUND", "err")

    if kiro_path.exists():
        UI.item(".kiro folder: EXISTS", "ok")
    else:
        UI.item(".kiro folder: MISSING (will create)", "warn")

    try:
        test_file = Path(f"{Path.home()}/.chatbottify_test.tmp")
        test_file.write_text("test")
        test_file.unlink()
        UI.item("Permissions: OK", "ok")
    except:
        UI.item("Permissions: DENIED", "err")
        UI.warning("May need Administrator privileges")

    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

def extract_version(content):
    match = re.search(r'Chatbottify0\s*\(v([\d.]+)\)', content)
    return match.group(1) if match else "0.0.0"

def compare_versions(v1, v2):
    parts1 = [int(x) for x in v1.split('.')]
    parts2 = [int(x) for x in v2.split('.')]
    
    for p1, p2 in zip(parts1, parts2):
        if p1 > p2:
            return 1
        if p1 < p2:
            return -1
    
    if len(parts1) > len(parts2):
        return 1
    if len(parts1) < len(parts2):
        return -1
    
    return 0

def install_file(file_path):
    print()
    UI.section("Installation")
    
    for i in range(0, 101, 5):
        UI.progress(i)
        time.sleep(0.02)
    UI.progress(100)
    print()

    content = get_embedded_content()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')

    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("Installation complete!")
    UI.info(f"► {file_path}\n")

def delete_file(file_path):
    print()
    UI.section("Deletion")
    
    for i in range(0, 101, 20):
        UI.progress(i)
        time.sleep(0.05)
    UI.progress(100)
    print()

    file_path.unlink()
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("File deleted!\n")

def show_version_info(existing, new_ver):
    print()
    UI.section("Version Info")
    UI.item(f"Installed: {Colors.CYAN}{existing}{Colors.RESET}")
    UI.item(f"Available: {Colors.GREEN}{new_ver}{Colors.RESET}")
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

def show_error_solutions(ex):
    print()
    UI.section("Error Solutions")
    
    if isinstance(ex, PermissionError):
        UI.item("Run as Administrator")
        UI.item("Check file/folder permissions")
        UI.item("Ensure antivirus isn't blocking")
    elif isinstance(ex, FileNotFoundError):
        UI.item("User directory doesn't exist")
        UI.item("Check username is correct")
        UI.item("Verify C:\\Users\\ path exists")
    elif isinstance(ex, OSError):
        UI.item("File may be in use by another program")
        UI.item("Close Kiro IDE and try again")
        UI.item("Restart your computer if issue persists")
    else:
        UI.item(str(ex))
        UI.item("Try running as Administrator")
    
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

def get_embedded_content():
    return """You're a helpful AI assistant with a friendly, conversational tone. Be ChatGPT-like but with genuine warmth and personality. Keep things light and approachable.

When communicating:
• Talk like a modern AI assistant, not a robot
• Use Kiro IDE features when it makes sense
• Be efficient - don't over-explain
• Remember: users read and write fast, so be concise
• Give direct answers, skip the fluff
• Be genuinely helpful and a bit playful

---

Cheerbot (v0.0.1)
Author: warwakei
A steering rule for Kiro IDE to make Claude AI more like ChatGPT - simple, fast, and friendly
Repository: https://github.com/warwakei/cheerbot-kirosteering
"""

def get_ext_content():
    return """You're a helpful AI assistant with a friendly, conversational tone. Be ChatGPT-like but with a bit more personality and warmth. Keep things light and approachable while maintaining focus on code quality and efficiency.

When writing code:
• Validate syntax before suggesting (nobody wants production bugs)
• Use type annotations (TypeScript, Python type hints, etc.) - types are your friends
• Comments only for complex logic, not the obvious stuff
• Minimize comments - good code explains itself
• Follow language conventions (camelCase, snake_case, PascalCase)
• Suggest optimizations when you spot inefficiency
• Minimize dependencies, prefer built-in solutions

When evaluating code quality:
• Good code: readable, typed, logically structured
• Bad code: spaghetti logic, duplication, magic numbers, unclear names
• When you spot bad code, show the problem first, then the solution
• Don't mix good and bad code in the same file
• Refactor bad code to good, don't leave it as-is

When helping with bugs:
• Reproduce the problem logically before answering
• Show the exact error location with context (2-3 lines around it)
• Explain the cause in one line max
• Provide a ready-made solution with brief explanation
• If there are multiple options, show the best one

When refactoring:
• Keep functionality at 100%
• Don't overcomplicate without reason
• Remove dead code and duplication
• Group similar logic together
• Improve readability over performance (unless critical)

---

Extension1 (v0.0.1)
Author: warwakei
Extends: Cheerbot v0.0.1+
Focus: Code Quality & Efficiency
Repository: https://github.com/warwakei/cheerbot-kirosteering
"""

def get_ext1_content():
    return """You're a helpful AI assistant with a friendly, conversational tone. Be ChatGPT-like but with a bit more personality and warmth. Keep things light and approachable while maintaining focus on code quality and efficiency.

When writing code:
• Validate syntax before suggesting (nobody wants production bugs)
• Use type annotations (TypeScript, Python type hints, etc.) - types are your friends
• Comments only for complex logic, not the obvious stuff
• Minimize comments - good code explains itself
• Follow language conventions (camelCase, snake_case, PascalCase)
• Suggest optimizations when you spot inefficiency
• Minimize dependencies, prefer built-in solutions

When evaluating code quality:
• Good code: readable, typed, logically structured
• Bad code: spaghetti logic, duplication, magic numbers, unclear names
• When you spot bad code, show the problem first, then the solution
• Don't mix good and bad code in the same file
• Refactor bad code to good, don't leave it as-is

When helping with bugs:
• Reproduce the problem logically before answering
• Show the exact error location with context (2-3 lines around it)
• Explain the cause in one line max
• Provide a ready-made solution with brief explanation
• If there are multiple options, show the best one

When refactoring:
• Keep functionality at 100%
• Don't overcomplicate without reason
• Remove dead code and duplication
• Group similar logic together
• Improve readability over performance (unless critical)

---

Extension1 (v0.0.1)
Author: warwakei
Extends: Cheerbot v0.0.1+
Focus: Code Quality & Efficiency
Repository: https://github.com/warwakei/cheerbot-kirosteering
"""

def get_ext2_content():
    return """You're a helpful AI assistant with a friendly, conversational tone. Be ChatGPT-like but with a bit more personality and warmth. Keep things light and approachable while maintaining focus on dependencies, testing, and documentation.

When working with dependencies:
• Check version compatibility before suggesting (conflicts are no fun)
• Document why a specific version is needed
• Prefer stable versions over experimental ones
• Avoid beta/alpha unless absolutely necessary
• Minimize the number of dependencies
• Check licenses before adding anything

When writing tests:
• Tests should be clear and fast
• One test = one thing to check
• Use descriptive names that explain what's being tested
• Don't test the obvious
• Tests should be independent of each other
• Cover edge cases and error scenarios

When documenting:
• Keep READMEs short and to the point
• Code examples should work as copy-paste
• Explain the "why", not just the "what"
• Link to additional resources when helpful
• Structure documentation logically
• Update docs when you update code

When versioning:
• Use semantic versioning (major.minor.patch)
• Document breaking changes in CHANGELOG
• Tag releases in git
• Write clear commit messages

When optimizing:
• Profile before optimizing (don't guess)
• Don't optimize prematurely
• Document why optimization is needed
• Verify that optimization actually helps

---

Extension2 (v0.0.1)
Author: warwakei
Extends: Cheerbot v0.0.1+
Focus: Dependencies, Testing & Documentation
Repository: https://github.com/warwakei/cheerbot-kirosteering
"""

def show_recommendation():
    print()
    UI.section("Available Extensions")
    UI.item("cheerbot-ext1: Code Quality & Efficiency", "ok")
    UI.item("cheerbot-ext2: Dependencies, Testing & Docs", "ok")
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")
    
    print(f"  {Colors.MAGENTA}[1]{Colors.RESET} Install ext1  {Colors.MAGENTA}[2]{Colors.RESET} Install ext2")
    print(f"  {Colors.MAGENTA}[B]{Colors.RESET} Install both  {Colors.MAGENTA}[S]{Colors.RESET} Skip")
    action = input(f"\n{Colors.MAGENTA}›{Colors.RESET} ").upper()
    
    if action == "1":
        try:
            install_ext1()
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    elif action == "2":
        try:
            install_ext2()
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    elif action == "B":
        try:
            install_ext1()
            install_ext2()
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    else:
        UI.info("Skipped")

def install_ext1():
    user_name = os.getenv('USERNAME')
    kiro_path = Path(f"C:\\Users\\{user_name}\\.kiro\\steering")
    ext_path = kiro_path / "cheerbot-ext1.md"
    
    print()
    UI.section("Installing Extension1")
    
    for i in range(0, 101, 5):
        UI.progress(i)
        time.sleep(0.02)
    UI.progress(100)
    print()
    
    content = get_ext1_content()
    ext_path.write_text(content, encoding='utf-8')
    
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("Extension1 installed!")
    UI.info(f"► {ext_path}\n")

def install_ext2():
    user_name = os.getenv('USERNAME')
    kiro_path = Path(f"C:\\Users\\{user_name}\\.kiro\\steering")
    ext_path = kiro_path / "cheerbot-ext2.md"
    
    print()
    UI.section("Installing Extension2")
    
    for i in range(0, 101, 5):
        UI.progress(i)
        time.sleep(0.02)
    UI.progress(100)
    print()
    
    content = get_ext2_content()
    ext_path.write_text(content, encoding='utf-8')
    
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("Extension2 installed!")
    UI.info(f"► {ext_path}\n")

def handle_existing_file(file_path, comparison):
    show_version_info(extract_version(file_path.read_text(encoding='utf-8')), NEW_VERSION)
    
    if comparison > 0:
        UI.warning("Current version is newer!")
    elif comparison < 0:
        print(f"{Colors.CYAN}► New version available!{Colors.RESET}")
    else:
        UI.info("Same version installed")

    if comparison > 0:
        print(f"\n  {Colors.MAGENTA}[U]{Colors.RESET}pdate  {Colors.MAGENTA}[D]{Colors.RESET}elete  {Colors.MAGENTA}[C]{Colors.RESET}ancel")
    elif comparison < 0:
        print(f"\n  {Colors.MAGENTA}[U]{Colors.RESET}pdate  {Colors.MAGENTA}[D]{Colors.RESET}elete  {Colors.MAGENTA}[C]{Colors.RESET}ancel")
    else:
        print(f"\n  {Colors.MAGENTA}[R]{Colors.RESET}einstall  {Colors.MAGENTA}[D]{Colors.RESET}elete  {Colors.MAGENTA}[C]{Colors.RESET}ancel")
    
    action = input(f"\n{Colors.MAGENTA}›{Colors.RESET} ").upper()

    if action == "U" or action == "R":
        try:
            install_file(file_path)
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    elif action == "D":
        try:
            delete_file(file_path)
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    else:
        UI.info("Cancelled")

def main():
    UI.clear()
    UI.header()
    run_diagnostics()

    try:
        user_name = os.getenv('USERNAME')
        kiro_path = Path(f"C:\\Users\\{user_name}\\.kiro\\steering")
        file_path = kiro_path / "cheerbot.md"

        UI.section("Target")
        UI.item(f"Path: {kiro_path}")
        UI.item(f"File: cheerbot.md")
        print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

        if file_path.exists():
            existing_version = extract_version(file_path.read_text(encoding='utf-8'))
            comparison = compare_versions(existing_version, NEW_VERSION)
            handle_existing_file(file_path, comparison)
        else:
            if not kiro_path.exists():
                try:
                    kiro_path.mkdir(parents=True, exist_ok=True)
                except PermissionError:
                    UI.error("Permission Denied!")
                    show_error_solutions(PermissionError())
                    UI.footer()
                    input()
                    return

            install_file(file_path)

        show_recommendation()

    except Exception as ex:
        UI.error(f"Error: {type(ex).__name__}")
        show_error_solutions(ex)
        UI.footer()
        input()

if __name__ == "__main__":
    main()
