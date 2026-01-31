@echo off
REM Automated GitHub Setup Script for Windows
REM For: Tanzanian Rent Invoice Processor
REM Repository: http://github.com/jmaccoe/tanzanian-rent-processor

setlocal enabledelayedexpansion

echo ==================================================
echo GitHub Setup - Tanzanian Rent Invoice Processor
echo ==================================================
echo.

REM Configuration
set GITHUB_USER=jmaccoe
set REPO_NAME=tanzanian-rent-processor
set REPO_URL=https://github.com/%GITHUB_USER%/%REPO_NAME%.git

REM Check if git is installed
echo Checking prerequisites...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed!
    echo Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)
echo [OK] Git is installed
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo [ERROR] app.py not found!
    echo Please run this script from the project directory
    pause
    exit /b 1
)
echo [OK] Project files found
echo.

REM Initialize git repository if not already initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo [OK] Git repository initialized
) else (
    echo [WARNING] Git repository already exists
)
echo.

REM Configure git user if not set
for /f "delims=" %%i in ('git config user.name') do set GIT_USER=%%i
if "!GIT_USER!"=="" (
    set /p GIT_USERNAME="Enter your Git username: "
    git config user.name "!GIT_USERNAME!"
    echo [OK] Git username configured
)

for /f "delims=" %%i in ('git config user.email') do set GIT_EMAIL=%%i
if "!GIT_EMAIL!"=="" (
    set /p GIT_USEREMAIL="Enter your Git email: "
    git config user.email "!GIT_USEREMAIL!"
    echo [OK] Git email configured
)
echo.

REM Use GitHub-optimized README
if exist "README_GITHUB.md" (
    echo Using GitHub-optimized README...
    if exist "README.md" (
        copy /Y README.md README_DETAILED.md >nul 2>&1
    )
    copy /Y README_GITHUB.md README.md >nul
    echo [OK] README prepared for GitHub
)
echo.

REM Add all files
echo Adding files to Git...
git add .
echo [OK] Files staged
echo.

REM Create initial commit
git log --oneline >nul 2>&1
if errorlevel 1 (
    echo Creating initial commit...
    git commit -m "Initial commit: Tanzanian rent invoice processor with WHT calculations"
    echo [OK] Initial commit created
) else (
    echo [WARNING] Repository already has commits
    set /p CREATE_COMMIT="Create a new commit with current changes? (y/n): "
    if /i "!CREATE_COMMIT!"=="y" (
        set /p COMMIT_MSG="Enter commit message: "
        git commit -m "!COMMIT_MSG!" 2>nul || echo [WARNING] No changes to commit
    )
)
echo.

REM Check if remote exists
git remote get-url origin >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Remote 'origin' already exists
    for /f "delims=" %%i in ('git remote get-url origin') do set CURRENT_URL=%%i
    echo Current URL: !CURRENT_URL!
    set /p UPDATE_REMOTE="Update to %REPO_URL%? (y/n): "
    if /i "!UPDATE_REMOTE!"=="y" (
        git remote set-url origin %REPO_URL%
        echo [OK] Remote URL updated
    )
) else (
    echo Adding GitHub remote...
    git remote add origin %REPO_URL%
    echo [OK] Remote added: %REPO_URL%
)
echo.

REM Set main branch
echo Setting up main branch...
git branch -M main
echo [OK] Branch set to 'main'
echo.

REM Display remote info
echo Remote repository:
git remote -v
echo.

REM Ask before pushing
echo ==================================================
echo Ready to push to GitHub!
echo ==================================================
echo Repository: %REPO_URL%
echo.
echo [WARNING] Make sure you have created the repository on GitHub first!
echo If not, go to: https://github.com/new
echo Repository name: %REPO_NAME%
echo.
set /p DO_PUSH="Push to GitHub now? (y/n): "

if /i "%DO_PUSH%"=="y" (
    echo.
    echo Pushing to GitHub...
    echo.
    echo If prompted, use your GitHub username and Personal Access Token
    echo Create token at: https://github.com/settings/tokens
    echo.
    
    git push -u origin main
    if errorlevel 1 (
        echo.
        echo [ERROR] Push failed!
        echo.
        echo Common issues and solutions:
        echo 1. Repository doesn't exist on GitHub
        echo    ^> Create it at: https://github.com/new
        echo.
        echo 2. Authentication failed
        echo    ^> Use Personal Access Token instead of password
        echo    ^> Create at: https://github.com/settings/tokens
        echo.
        echo 3. Permission denied
        echo    ^> Verify you own the repository
        echo    ^> Check your username is correct: %GITHUB_USER%
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo [OK] Successfully pushed to GitHub!
    echo.
    echo Your repository is now available at:
    echo https://github.com/%GITHUB_USER%/%REPO_NAME%
    echo.
    echo Next steps:
    echo 1. Visit your repository on GitHub
    echo 2. Add topics/tags (tanzania, tax-calculator, streamlit, etc.)
    echo 3. Update repository description
    echo 4. Consider adding a screenshot
    echo.
) else (
    echo.
    echo [INFO] Push cancelled
    echo You can push manually later with:
    echo   git push -u origin main
    echo.
)

echo.
echo ==================================================
echo Setup Complete!
echo ==================================================
echo.

pause
