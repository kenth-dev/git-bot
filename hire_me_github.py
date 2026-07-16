import os
import subprocess
import random
from datetime import datetime, timedelta

# --- Configuration ---
GITHUB_USERNAME = "kenth-dev"

# Commit intensity levels - all higher than 13 (your current max) for visibility
# Level 3 = darkest green, Level 2 = medium, Level 1 = lighter but still visible
INTENSITY = {
    3: (35, 50),   # Front face - very dark green (way above your 13 max)
    2: (20, 30),   # Shadow - clearly visible medium green
    1: (14, 19),   # Edge/depth - just above your current max of 13
    0: (0, 0),     # Empty - no commits
}

# "HIRE ME" in clean 5-column wide font that fits perfectly in 7 rows
# With 3D shading: 3=front, 2=shadow, 1=depth
# Each letter is carefully designed to be exactly 7 rows tall
LETTERS = {
    'H': [
        [3,2,0,3,2],
        [3,2,0,3,2],
        [3,2,0,3,2],
        [3,3,3,3,2],
        [3,2,0,3,2],
        [3,2,0,3,2],
        [1,1,0,1,1],
    ],
    'I': [
        [3,3,3],
        [1,3,1],
        [0,3,0],
        [0,3,0],
        [0,3,0],
        [1,3,1],
        [3,3,3],
    ],
    'R': [
        [3,3,3,2],
        [3,0,0,3],
        [3,0,0,3],
        [3,3,3,2],
        [3,0,3,1],
        [3,0,0,3],
        [1,0,0,1],
    ],
    'E': [
        [3,3,3,2],
        [3,1,1,1],
        [3,0,0,0],
        [3,3,3,0],
        [3,0,0,0],
        [3,1,1,1],
        [3,3,3,2],
    ],
    ' ': [
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
    ],
    'M': [
        [3,2,0,0,2,3],
        [3,3,0,0,3,3],
        [3,2,3,3,2,3],
        [3,0,2,2,0,3],
        [3,0,0,0,0,3],
        [3,0,0,0,0,3],
        [1,0,0,0,0,1],
    ],
}


def build_grid(text):
    """Converts text into a 7-row pixel grid with intensity values."""
    grid = [[] for _ in range(7)]
    for i, char in enumerate(text.upper()):
        if char in LETTERS:
            letter = LETTERS[char]
            for row in range(7):
                grid[row].extend(letter[row])
                # Add 1-column spacing between letters
                if i < len(text) - 1:
                    grid[row].append(0)
    return grid


def get_start_date(grid_width):
    """
    Position text in 2025 (Jan-Oct area).
    Jan 5, 2025 is a Sunday - first full week.
    Center the text within Jan-Oct (~43 weeks).
    """
    jan_start = datetime(2025, 1, 5)

    # Center within Jan-Oct (about 43 weeks available)
    available_weeks = 43
    offset_weeks = (available_weeks - grid_width) // 2
    start_date = jan_start + timedelta(weeks=max(0, offset_weeks))

    return start_date


def preview_grid(grid):
    """Prints a styled preview of the 3D art in the terminal."""
    shade_chars = {0: " ", 1: "░", 2: "▒", 3: "█"}
    grid_width = len(grid[0])
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    print("    ┌" + "─" * grid_width + "┐")
    for i, row in enumerate(grid):
        line = "".join([shade_chars[cell] for cell in row])
        print(f" {days[i]} │{line}│")
    print("    └" + "─" * grid_width + "┘")


def main():
    text = "HIRE ME"
    grid = build_grid(text)
    grid_width = len(grid[0])  # number of columns (weeks)

    print("╔══════════════════════════════════════════════╗")
    print("║   🎨 GitHub 3D Contribution Art Maker        ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"\n  Text: '{text}'")
    print(f"  Grid size: 7 rows x {grid_width} columns")
    print(f"  Target: Jan - Oct 2025 (centered in your graph)")
    print(f"  Min commits/day: 14 (above your current max of 13)")
    print("\n  3D Preview (█=front ▒=shadow ░=depth):\n")
    preview_grid(grid)

    # Estimate total commits
    total_pixels = sum(cell for row in grid for cell in row if cell > 0)
    avg_commits = sum((INTENSITY[i][0] + INTENSITY[i][1]) // 2 for i in range(1, 4)) // 3
    estimated_total = total_pixels * avg_commits

    start_date = get_start_date(grid_width)
    end_date = start_date + timedelta(weeks=grid_width - 1, days=6)
    print(f"\n  Date range: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
    print(f"  Estimated total commits: ~{estimated_total}")
    print(f"\n  ⚠️  Username: '{GITHUB_USERNAME}'")

    input("\n  Press Enter to start generating commits (or Ctrl+C to cancel)...")

    # Work in the current directory (existing repo)

    # Create commits for each "pixel"
    commit_count = 0
    for col in range(grid_width):
        for row in range(7):
            intensity = grid[row][col]
            if intensity > 0:
                # col = week offset, row = day of week (0 = Sunday)
                commit_date = start_date + timedelta(weeks=col, days=row)
                date_str = commit_date.strftime("%Y-%m-%dT12:00:00")

                min_c, max_c = INTENSITY[intensity]
                num_commits = random.randint(min_c, max_c)

                for i in range(num_commits):
                    with open("contribution.txt", "a") as f:
                        f.write(f"{date_str} commit {i}\n")

                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run(
                        ["git", "commit", "-m", "contribution",
                         "--date", date_str],
                        check=True,
                        env={
                            **os.environ,
                            "GIT_AUTHOR_DATE": date_str,
                            "GIT_COMMITTER_DATE": date_str,
                        }
                    )
                    commit_count += 1

        print(f"  ▓ Column {col+1}/{grid_width} done ({commit_count} commits)")

    print(f"\n  {'═'*50}")
    print(f"  ✅ DONE! Created {commit_count} commits.")
    print(f"  {'═'*50}")
    print(f"\n  Next steps:")
    print(f"    git push origin master")
    print(f"")
    print(f"  Visit your profile → 2025 contribution graph")
    print(f"  Your 3D 'HIRE ME' will be there! 🔥")


if __name__ == "__main__":
    main()
