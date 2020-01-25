# Creating and uploading my first iteration of this project
# Create the folder where your project files are
cd C:/Main/NYCDSA/Web_Scraping_Project
git init
git status
git add --all
# Save your file snapshot locally on your computer
git commit --all -m "Details of your first snapshot of your project blah blah"
git log --oneline

# I created a repo on my Github named Web_Scraping_Project
git remote add origin https://github.com/jzl4/Web_Scraping_Project
# Upload your files to github; save them online
git push origin master

# To save changes to your project to both your local repo and pushing it online
git status
git add --all
git commit --all -m "WHATEVER CHANGE YOU MADE"
git log --oneline
git push origin master