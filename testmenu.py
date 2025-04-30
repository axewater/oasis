import curses

# Placeholder functions for menu options
def function_dev_week_demo():
    print("You have selected 'dev-week-demo'.")

def function_merge_conflict_test():
    print("You have selected 'merge-conflict-test'.")

def function_dev_week_forking():
    print("You have selected 'dev-week-forking'.")

def function_electron():
    print("You have selected 'electron'.")

def function_vscode():
    print("You have selected 'vscode'.")

def function_gitkraken_client_docs_internal():
    print("You have selected 'gitkraken-client-docs-internal'.")

def function_libgit2():
    print("You have selected 'libgit2'.")

def function_git_integration_for_jira_self_managed_docs():
    print("You have selected 'git-integration-for-jira-self-managed-docs'.")

def function_monaco_editor():
    print("You have selected 'monaco-editor'.")

def function_gitlens_docs():
    print("You have selected 'gitlens-docs'.")

# Menu items mapped to their corresponding functions
menu_items = [
    ("dev-week-demo", function_dev_week_demo),
    ("merge-conflict-test", function_merge_conflict_test),
    ("dev-week-forking", function_dev_week_forking),
    ("electron", function_electron),
    ("vscode", function_vscode),
    ("gitkraken-client-docs-internal", function_gitkraken_client_docs_internal),
    ("libgit2", function_libgit2),
    ("git-integration-for-jira-self-managed-docs", function_git_integration_for_jira_self_managed_docs),
    ("monaco-editor", function_monaco_editor),
    ("gitlens-docs", function_gitlens_docs),
]
# The menu options and corresponding functions
menu_items = [
    ("dev-week-demo", function_dev_week_demo),
    ("merge-conflict-test", function_merge_conflict_test),
    ("dev-week-forking", function_dev_week_forking),
    # ... Add other menu items and their corresponding functions
]

# Function to display the menu and handle the user input
def run_menu(stdscr):
    curses.curs_set(0)  # Hide the cursor
    current_row = 0

    def print_menu(current_row):
        stdscr.clear()
        for idx, item in enumerate(menu_items):
            x = 0
            y = idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, item[0])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item[0])
        stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    print_menu(current_row)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            menu_items[current_row][1]()
            stdscr.getch()
            stdscr.clear()
            stdscr.refresh()
            print_menu(current_row)
            continue
        print_menu(current_row)

# Run the menu
curses.wrapper(run_menu)



