"""
Neuraluxe-Lite
Premium Community Tab (Full Version)
--------------------------------------
- View all posts with pagination
- Search and filter by user or keyword
- Create, like, comment on posts
- Free vs Paid access limits
- Recent activity timestamps
- Quick tips
- Logging & timestamps
"""

import json
import os
from datetime import datetime

# -----------------------------
# Configurations
# -----------------------------
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
COMMUNITY_JSON = "community.json"
POSTS_PER_PAGE = 5  # pagination chunk size

# -----------------------------
# Helper Functions
# -----------------------------
def load_community():
    if not os.path.exists(COMMUNITY_JSON):
        with open(COMMUNITY_JSON, "w") as f:
            json.dump({}, f)
    with open(COMMUNITY_JSON, "r") as f:
        return json.load(f)

def save_community(data):
    with open(COMMUNITY_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def display_quick_tips():
    tips = [
        "Free users have limited posting capabilities.",
        "Check community posts for updates and discussions.",
        "Like and comment to engage with others.",
        "Posts are saved automatically.",
        "Use pagination to navigate through all posts.",
        "Search posts by user or keyword to find content quickly."
    ]
    print("\n✨ Community Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# View Posts with Pagination
# -----------------------------
def view_posts_paginated(posts_list):
    if not posts_list:
        print("- No posts to display.")
        return

    total_posts = len(posts_list)
    total_pages = (total_posts + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
    page = 1

    while True:
        start_idx = (page - 1) * POSTS_PER_PAGE
        end_idx = min(start_idx + POSTS_PER_PAGE, total_posts)
        print(f"\n📢 Community Posts (Page {page}/{total_pages}):")
        for idx, post in enumerate(posts_list[start_idx:end_idx], start_idx + 1):
            print(f"{idx}. [{post['timestamp']}] {post['user']}: {post['content']} "
                  f"(Likes: {post['likes']}, Comments: {len(post['comments'])})")
        print("\nCommands: [n] Next Page | [p] Previous Page | [e] Exit")
        cmd = input("Select command: ").strip().lower()
        if cmd == "n":
            if page < total_pages:
                page += 1
            else:
                print("Already at the last page.")
        elif cmd == "p":
            if page > 1:
                page -= 1
            else:
                print("Already at the first page.")
        elif cmd == "e":
            break
        else:
            print("Invalid command. Use n/p/e.")

# -----------------------------
# Search / Filter Posts
# -----------------------------
def search_posts(community_data):
    all_posts = community_data.get("posts", [])
    if not all_posts:
        print("- No posts to search.")
        return

    term = input("Enter keyword or user to search: ").strip().lower()
    filtered = [
        post for post in all_posts
        if term in post["content"].lower() or term in post["user"].lower()
    ]

    if not filtered:
        print(f"- No posts found for '{term}'.")
    else:
        print(f"\n🔍 Search Results for '{term}':")
        view_posts_paginated(filtered)

# -----------------------------
# Create Post
# -----------------------------
def create_post(user_email, community_data):
    full_access = (user_email == FREE_USER_EMAIL)
    if not full_access and len(community_data.get("posts", [])) >= 2:
        print("Free users can only post up to 2 times. Upgrade for full access.")
        return
    content = input("Enter your post content: ").strip()
    if not content:
        print("Post cannot be empty.")
        return
    post_entry = {
        "user": user_email,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "likes": 0,
        "comments": []
    }
    community_data.setdefault("posts", []).append(post_entry)
    save_community(community_data)
    print("✅ Post created!")

# -----------------------------
# Like Post
# -----------------------------
def like_post(community_data):
    posts = community_data.get("posts", [])
    if not posts:
        print("No posts to like.")
        return
    view_posts_paginated(posts)
    idx = input("Enter post number to like: ").strip()
    if idx.isdigit() and 1 <= int(idx) <= len(posts):
        posts[int(idx)-1]["likes"] += 1
        save_community(community_data)
        print("✅ Post liked!")
    else:
        print("Invalid selection.")

# -----------------------------
# Comment Post
# -----------------------------
def comment_post(user_email, community_data):
    posts = community_data.get("posts", [])
    if not posts:
        print("No posts to comment.")
        return
    view_posts_paginated(posts)
    idx = input("Enter post number to comment on: ").strip()
    if idx.isdigit() and 1 <= int(idx) <= len(posts):
        comment = input("Enter your comment: ").strip()
        if comment:
            posts[int(idx)-1]["comments"].append({
                "user": user_email,
                "comment": comment,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_community(community_data)
            print("✅ Comment added!")
        else:
            print("Comment cannot be empty.")
    else:
        print("Invalid selection.")

# -----------------------------
# Community Tab Main
# -----------------------------
def community_tab_ui(user_email):
    print("\n==============================")
    print("        COMMUNITY TAB         ")
    print("==============================\n")

    log_activity(user_email, "Opened Community Tab")
    community_data = load_community()

    display_quick_tips()

    while True:
        print("\nOptions:")
        print("1. View Posts (Paginated)")
        print("2. Search / Filter Posts")
        print("3. Create Post")
        print("4. Like Post")
        print("5. Comment on Post")
        print("6. Exit Community Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            view_posts_paginated(community_data.get("posts", []))
        elif choice == "2":
            search_posts(community_data)
        elif choice == "3":
            create_post(user_email, community_data)
        elif choice == "4":
            like_post(community_data)
        elif choice == "5":
            comment_post(user_email, community_data)
        elif choice == "6":
            log_activity(user_email, "Closed Community Tab")
            print("Exiting Community Tab...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    community_tab_ui(email)