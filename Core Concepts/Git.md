
# Here's a structured breakdown of **important Git topics**, from **introductory** to **advanced**, commonly covered in **interviews** and essential for **real-world use in development, DevOps, and infrastructure roles**:

---

## 🟢 **Beginner Git Topics**

### 1. **Git Basics**

* **What is Git?**
  A distributed version control system for tracking changes in source code during software development.
* **Key Concepts:**

  * Repository (repo)
  * Working directory
  * Staging area (index)
  * Commit

---

### 2. **Core Git Commands**

* `git init` – Initialize a repository
* `git clone` – Copy a remote repo
* `git add` – Stage changes
* `git commit` – Save changes to local repo
* `git status` – See the current state
* `git log` – View commit history

---

### 3. **Branching & Merging**

* `git branch` – List, create, or delete branches
* `git checkout` – Switch branches
* `git merge` – Merge branches
* **Fast-forward vs recursive merge**

  * Fast-forward: Linear history
  * Recursive: Merge commit created

---

### 4. **Remote Repositories**

* `git remote add origin <url>`
* `git push`, `git pull`, `git fetch`
* `origin` is the default name for your remote

---

## 🟡 **Intermediate Git Topics**

### 5. **Undoing Changes**

* `git reset` – Unstage or move HEAD
* `git revert` – Create a new commit that undoes a change
* `git checkout <file>` – Discard file changes
* `git clean -fd` – Remove untracked files and directories

---

### 6. **Stashing**

* `git stash` – Save dirty working directory
* `git stash pop` – Reapply stashed changes
* `git stash list`, `git stash apply`

---

### 7. **Rebasing**

* `git rebase` – Reapply commits on top of another base tip
* Used to **keep a clean linear history**
* Avoid rebasing public branches

---

### 8. **Cherry-pick**

* `git cherry-pick <commit>` – Apply a commit from another branch

---

### 9. **Tagging**

* Lightweight vs Annotated tags
* `git tag v1.0.0`
* `git push origin v1.0.0`

---

### 10. **Git Ignore & Attributes**

* `.gitignore` – Ignore specific files from being tracked
* `.gitattributes` – Manage end-of-line settings, language classification, merge strategies

---

## 🔴 **Advanced Git Topics**

### 11. **Interactive Rebase**

* `git rebase -i HEAD~n`
* Allows you to **squash**, **reword**, **drop**, or **reorder** commits

---

### 12. **Reflog**

* `git reflog` – View history of `HEAD`, useful for recovery
* You can recover lost commits using:

  ```bash
  git checkout <reflog-hash>
  ```

---

### 13. **Submodules**

* Manage repos within repos
* `git submodule add <repo-url>`
* Often used in mono-repos or vendoring

---

### 14. **Git Hooks**

* Scripts that run before/after Git commands
* Examples:

  * `pre-commit`
  * `pre-push`
  * `post-merge`
* Location: `.git/hooks`

---

### 15. **Rewriting History**

* `git commit --amend` – Modify the last commit
* `git rebase -i` – Rewrite multiple commits
* **Warning:** Don't rewrite public/shared history

---

### 16. **Advanced Merge Strategies**

* `git merge --no-ff` – Force a merge commit
* `git merge --squash` – Combine all changes into one commit

---

### 17. **Git Bisect**

* Binary search to find the commit that introduced a bug:

  ```bash
  git bisect start
  git bisect bad
  git bisect good <commit>
  ```

---

### 18. **Conflict Resolution**

* Manual: Edit files, then `git add`
* Tools: `git mergetool`, VS Code, Meld, etc.

---

### 19. **Git Internals**

* `.git` directory structure
* `objects`, `refs`, `HEAD`, `index`
* SHA-1 hashing, DAG (Directed Acyclic Graph)

---

### 20. **Large Repos and Performance**

* Git LFS (Large File Storage)
* Partial clone: `--depth`, `--filter=blob:none`

---

## 🚀 Bonus: Real-World Git Practices

* **Git Flow**, **GitHub Flow**, **Trunk-Based Development**
* **Feature branching**, **release tagging**, **hotfixes**
* CI/CD hooks for commit/push actions
* GitOps workflows in Infrastructure-as-Code

---


# Here are **detailed notes** on two advanced Git topics: **Git Submodules** and **Git Hooks** — commonly used in large repositories and automation workflows, and often discussed in advanced Git interviews or DevOps tooling discussions.

---

## 🔷 **Git Submodules**

### 📌 What are Git Submodules?

Git Submodules allow you to include **one Git repository inside another**, at a specific commit. It’s useful when:

* You need to vendor a third-party dependency.
* You want to include reusable components (like libraries) that live in separate repos.

---

### 🛠️ Common Use Cases

* Shared libraries across microservices.
* Embedding external tools/components (e.g., an SDK).
* Separating frontend/backend while keeping them in sync.

---

### 📦 How to Add a Submodule

```bash
git submodule add https://github.com/example/libfoo.git path/to/libfoo
git commit -m "Add libfoo submodule"
```

---

### 📤 Cloning with Submodules

After cloning a repo with submodules:

```bash
git clone --recurse-submodules <repo-url>
# OR if already cloned:
git submodule init
git submodule update
```

---

### 🔁 Updating a Submodule

To get the latest changes from a submodule's upstream repo:

```bash
cd path/to/submodule
git checkout main
git pull origin main
cd ../
git add path/to/submodule
git commit -m "Updated submodule to latest commit"
```

---

### 🧹 Removing a Submodule

```bash
git submodule deinit -f path/to/submodule
git rm -f path/to/submodule
rm -rf .git/modules/path/to/submodule
```

---

### ⚠️ Submodule Gotchas

* Submodules point to **specific commit**, not branches.
* Require explicit update (`git submodule update`).
* CI/CD systems need extra setup to fetch them.
* Can cause headaches in mono-repo workflows if not managed properly.

---

## 🔷 **Git Hooks**

### 📌 What are Git Hooks?

Git Hooks are **scripts that Git executes automatically** at certain points in the Git workflow. They're stored in `.git/hooks/` and can be used to:

* Enforce code quality (linters, formatters).
* Prevent bad commits.
* Automate deployment steps.

---

### 📁 Hook Script Location

* Default folder: `.git/hooks/`
* Hooks are shell scripts (Bash, Python, etc.)
* Default scripts exist but are named with `.sample`.

---

### 🔧 Common Git Hooks and Use Cases

| Hook                 | When It Runs                 | Use Case Example                                              |
| -------------------- | ---------------------------- | ------------------------------------------------------------- |
| `pre-commit`         | Before a commit is made      | Run linters, check formatting                                 |
| `prepare-commit-msg` | Before commit message editor | Pre-fill commit messages, issue numbers                       |
| `commit-msg`         | After message written        | Enforce commit message convention (e.g. Conventional Commits) |
| `post-commit`        | After a commit is done       | Notify tools, logging                                         |
| `pre-push`           | Before push to remote        | Run tests, enforce branch rules                               |
| `post-merge`         | After a merge                | Reinstall dependencies if needed                              |

---

### 🧪 Example: `pre-commit` Hook to Check Code Format

```bash
#!/bin/bash
black --check .
if [ $? -ne 0 ]; then
  echo "Please format code with black before committing."
  exit 1
fi
```

Save as `.git/hooks/pre-commit` and make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

---

### 🔁 Hook Execution is Local

* Git hooks are **not version-controlled** by default.
* To share hooks, use tools like:

  * `husky` (for JS/Node projects)
  * `lefthook`
  * Custom script: copy hooks from a shared folder during repo setup

---

### 🚀 Pro Tips

* For CI/CD validation, mirror Git hook logic in pipelines.
* Prefer `pre-push` over `pre-commit` for time-consuming checks (e.g., tests).
* Enforce team-wide hooks via tools like [Husky](https://github.com/typicode/husky) or `git config core.hooksPath`.

---

## ✅ Summary Table

| Topic          | Git Submodules                     | Git Hooks                                  |
| -------------- | ---------------------------------- | ------------------------------------------ |
| Purpose        | Embed one Git repo inside another  | Automate custom actions in Git lifecycle   |
| Config File    | `.gitmodules`                      | `.git/hooks/*`                             |
| Tracked Commit | Yes, points to specific commit     | No, hooks are not version-controlled       |
| Use Cases      | Shared libs, vendored dependencies | Linting, testing, enforcing policies       |
| Risks          | Version drift, manual updates      | Can block workflow if not managed properly |

---

Would you like examples using **GitHub Actions to simulate Git Hooks**, or a **step-by-step CI/CD pipeline** that uses hooks and submodules?

# Here is a **Git Interview Q\&A set**, structured in a **question-answer** format for real-world, interview-relevant scenarios. These cover beginner to advanced topics frequently asked in DevOps, SRE, backend, and platform engineering roles.

---

### 🔹 **1. How do you work on a peer's remote branch and add changes on top of their work?**

**Answer:**

```bash
git fetch origin peer-branch
git checkout -b my-feature origin/peer-branch
# Make changes
git add .
git commit -m "Added enhancements on peer's work"
git push origin my-feature
```

---

### 🔹 **2. How can you make changes to an older commit on `master`?**

**Answer:**

```bash
git checkout -b fix-legacy <old-commit-hash>
# Make edits
git add .
git commit -m "Fixes for legacy commit"
git push origin fix-legacy
```

---

### 🔹 **3. How do you update your local branch with the latest `master` and replay your commits on top?**

**Answer:**

```bash
git checkout my-branch
git fetch origin
git rebase origin/master
# Resolve conflicts if any
git push origin my-branch --force-with-lease
```

---

### 🔹 **4. You accidentally committed to the wrong branch. How do you fix it?**

**Answer:**

```bash
git branch correct-branch
git reset HEAD~ --soft  # Moves commit out of wrong branch
git checkout correct-branch
git commit -m "Moved commit to correct branch"
git push origin correct-branch
```

---

### 🔹 **5. How do you squash all your commits into one before creating a pull request?**

**Answer:**

```bash
git rebase -i HEAD~<number-of-commits>
# Change "pick" to "squash" for all but the first commit
git push origin your-branch --force-with-lease
```

---

### 🔹 **6. How do you delete a file from Git history but keep it locally?**

**Answer:**

```bash
git rm --cached file.txt
echo "file.txt" >> .gitignore
git commit -m "Removed from repo but kept locally"
```

---

### 🔹 **7. You committed secrets. How do you remove them from the entire Git history?**

**Answer:**

```bash
# Use BFG Repo Cleaner or filter-branch
git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch secrets.txt" \
--prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

---

### 🔹 **8. How do you undo the last commit but keep the changes in your working directory?**

**Answer:**

```bash
git reset HEAD~1
```

---

### 🔹 **9. How do you delete a remote branch?**

**Answer:**

```bash
git push origin --delete old-branch
```

---

### 🔹 **10. How do you rename both a local and remote branch?**

**Answer:**

```bash
git branch -m old-name new-name
git push origin new-name
git push origin --delete old-name
```

---

### 🔹 **11. How do you stash changes and apply them later?**

**Answer:**

```bash
git stash
# Work or switch branch
git stash pop
```

---

### 🔹 **12. How do you see differences between two branches?**

**Answer:**

```bash
git diff branchA..branchB
```

---

### 🔹 **13. How do you cherry-pick a commit from one branch to another?**

**Answer:**

```bash
git checkout target-branch
git cherry-pick <commit-hash>
```

---

### 🔹 **14. You pulled from remote and messed up local changes. How do you revert?**

**Answer:**

```bash
git reset --hard HEAD~1
```

---

### 🔹 **15. How do you track a remote branch locally?**

**Answer:**

```bash
git checkout -b local-branch origin/remote-branch
```

---

### 🔹 **16. How do you clean up local branches that are already merged to `master`?**

**Answer:**

```bash
git checkout master
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d
```

---

### 🔹 **17. How do you apply only parts of your change (a few lines from a file)?**

**Answer:**

```bash
git add -p filename
# Choose hunks interactively
```

---

### 🔹 **18. How do you clone a repo with a single branch only?**

**Answer:**

```bash
git clone --branch branch-name --single-branch https://github.com/repo.git
```

---

### 🔹 **19. How do you see who last modified each line of a file?**

**Answer:**

```bash
git blame file.txt
```

---

### 🔹 **20. How do you pull changes without affecting your local uncommitted changes?**

**Answer:**

```bash
git stash
git pull origin branch
git stash pop
```

---

Would you like a **printable PDF**, **flashcards**, or **practice quiz format** for these questions?
