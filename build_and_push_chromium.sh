#!/bin/bash
set -e

# Chromium Build and Push Script
# This script automates the process of setting up the environment,
# fetching the Chromium source, building it, and preparing it for GitHub.

# Configuration
# Replace with your GitHub repository URL
GITHUB_REPO_URL="https://github.com/YOUR_USERNAME/my-chromium-fork.git"
BRANCH_NAME="my-feature-branch"

echo "Starting Chromium setup and build process..."

# 1. Install Prerequisites
echo "Installing system prerequisites..."
sudo apt-get update
sudo apt-get install -y git python3 curl

# 2. Install depot_tools
if [ ! -d "depot_tools" ]; then
    echo "Cloning depot_tools..."
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
else
    echo "depot_tools already exists. Updating..."
    cd depot_tools && git pull && cd ..
fi

# Add depot_tools to PATH for this session
export PATH="$PWD/depot_tools:$PATH"

# 3. Get the Code
mkdir -p chromium
cd chromium

if [ ! -d "src" ]; then
    echo "Fetching Chromium source (this may take a long time)..."
    # fetch --no-history chromium # Uncomment to save space/time if history isn't needed
    fetch chromium
else
    echo "Chromium source directory exists."
fi

cd src

# 4. Install Build Dependencies
echo "Installing build dependencies..."
./build/install-build-deps.sh --no-prompt

# 5. Synchronize and Run Hooks
echo "Running gclient hooks..."
gclient runhooks

# 6. Configure the Build
echo "Configuring build..."
gn gen out/Default --args="is_debug=false symbol_level=0 is_component_build=false"

# 7. Build Chromium
echo "Building Chromium (this will take hours)..."
autoninja -C out/Default chrome

echo "Build complete."

# 8. Package for Release
echo "Packaging release..."
cd out/Default
TAR_NAME="chromium-beta-linux.tar.gz"
tar -czvf "$TAR_NAME" chrome locales resources.pak icudtl.dat

# 9. Push to GitHub (Interactive/Requires Setup)
echo "To push to GitHub, execute the following commands:"
echo "---------------------------------------------------"
echo "cd ../.." # Go back to src root
echo "git remote add origin $GITHUB_REPO_URL"
echo "git checkout -b $BRANCH_NAME"
echo "git add ."
echo "git commit -m 'Initial fork customization'"
echo "git push -u origin $BRANCH_NAME"
echo "---------------------------------------------------"
echo "The release package is located at: $(pwd)/$TAR_NAME"
