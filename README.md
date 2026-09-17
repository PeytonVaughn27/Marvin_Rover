BEFORE WORKING GET THE NEWEST MAIN:
git status
git switch main
git pull origin main
git switch feature-peyton
git merge main

AFTER CHANGE SAVE AND PUSH:
git status
git add .
git commit -m "Description of what changed"
git push
git pull

AFTER PUSHING UPDATE MAIN:
git switch main
git pull origin main
git switch feature-peyton
git merge main


FOR FIRST PUSH:
git push -u origin feature-peyton

commit
Saves your changes locally.

push
Uploads your commits to GitHub.

pull
Downloads changes from GitHub to your computer.

pull request
Asks teammates to review and merge your branch into another branch.

merge
Combines the approved changes into the target branch, usually main.

fetch
Checks GitHub for updates without necessarily applying them to your current files.
