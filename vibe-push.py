import os
import sys
import time
import subprocess

# Безопасное включение ANSI-цветов для Windows
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# ANSI-цвета
CYAN = "\033[38;5;51m"
PURPLE = "\033[38;5;141m"
GREEN = "\033[38;5;119m"
GRAY = "\033[38;5;245m"
YELLOW = "\033[38;5;226m"
RED = "\033[38;5;196m"
BOLD = "\033[1m"
RESET = "\033[0m"

def get_emoji(msg):
    msg_lower = msg.lower()
    if any(word in msg_lower for word in ["fix", "баг", "исправ", "пофикс", "ошибк"]):
        return "🐛"
    elif any(word in msg_lower for word in ["feat", "add", "добав", "нов", "фич"]):
        return "✨"
    elif any(word in msg_lower for word in ["upd", "update", "обнов"]):
        return "🔄"
    elif any(word in msg_lower for word in ["doc", "док"]):
        return "📚"
    elif any(word in msg_lower for word in ["style", "ui", "стил", "дизайн", "css"]):
        return "🎨"
    elif any(word in msg_lower for word in ["refactor", "рефактор"]):
        return "♻️"
    elif any(word in msg_lower for word in ["del", "remov", "удал", "чист"]):
        return "🔥"
    return "🚀"

def run_cmd(args):
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8')
    return result.returncode == 0, result.stdout, result.stderr

def spinner(text, duration=1.5):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{CYAN}├── {PURPLE}{chars[i % len(chars)]}{RESET} {GRAY}{text}{RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r{' ' * (len(text) + 15)}\r")

def main():
    print(f"\n{CYAN}╭── {BOLD}Git Vibe Push{RESET}")
    
    if not os.path.exists(".git"):
        print(f"{CYAN}╰── ❯ {RED}❌ Бро, это не Git-репозиторий!{RESET}\n")
        return

    message = input(f"{CYAN}├── {GRAY}Что сделали? {RESET}❯ ")
    if not message.strip():
        print(f"{CYAN}╰── ❯ {RED}❌ Пустой коммит отменен.{RESET}\n")
        return

    emoji = get_emoji(message)
    full_message = f"{emoji} {message}"
    
    spinner("Добавляем файлы (git add .)...", 1)
    success, out, err = run_cmd(["git", "add", "."])
    if not success:
         print(f"{CYAN}├── ❯ {RED}❌ Ошибка при добавлении файлов.{RESET}")
         return
    print(f"{CYAN}├── {GREEN}✔{RESET} {GRAY}Файлы собраны{RESET}")

    spinner("Создаем коммит...", 1)
    success, out, err = run_cmd(["git", "commit", "-m", full_message])
    
    if "nothing to commit" in out or "nothing to commit" in err:
        print(f"{CYAN}╰── ❯ {YELLOW}⚠️ Нет изменений для коммита.{RESET}\n")
        return
        
    print(f"{CYAN}├── {GREEN}✔{RESET} {GRAY}Закоммичено:{RESET} {full_message}")

    spinner("Отправляем в космос (git push)...", 2)
    success, out, err = run_cmd(["git", "push"])
    
    if success or "Everything up-to-date" in err or "Everything up-to-date" in out:
         print(f"{CYAN}╰── ❯ {GREEN}✨ Успешно запушено! Вайб сохранен.{RESET}\n")
    else:
         print(f"{CYAN}╰── ❯ {RED}❌ Ошибка при пуше. (Может ветка не привязана?){RESET}\n")
         print(f"{GRAY}{err.strip()}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{CYAN}╰── ❯ {YELLOW}Отменено пользователем.{RESET}\n")