# Guide to Forking and Building Chromium on Linux

This guide outlines the steps to create a fork of the Chromium browser, build it on a Linux Virtual Machine (VM), and release a beta build on GitHub.

**Note:** Building Chromium requires significant hardware resources (at least 16GB RAM, >100GB disk space) and time.

## Prerequisites

Ensure you are running a 64-bit Linux distribution (Ubuntu 20.04 or later is recommended).

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install git and python
sudo apt-get install -y git python3 curl
```

## Step 1: Install depot_tools

Chromium uses a custom set of tools for code management and building called `depot_tools`.

```bash
# Clone the depot_tools repository
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

# Add depot_tools to your PATH
export PATH="$PATH:/path/to/depot_tools"

# It is recommended to add this to your .bashrc or .zshrc
echo 'export PATH="$PATH:$PWD/depot_tools"' >> ~/.bashrc
source ~/.bashrc
```

## Step 2: Get the Code

Create a directory for the source code and fetch it. This process can take a long time as it downloads roughly 20GB+ of data.

```bash
mkdir chromium && cd chromium

# Fetch the chromium source code (including history)
# Use --no-history to save space if you don't need full git history,
# but for a fork you usually want history.
fetch chromium

# Enter the source directory
cd src
```

## Step 3: Install Build Dependencies

Chromium provides a script to install all necessary development packages for Debian/Ubuntu.

```bash
# Run the install-build-deps script
./build/install-build-deps.sh
```

## Step 4: Synchronize and Run Hooks

Ensure all dependencies and toolchains are up to date.

```bash
gclient runhooks
```

## Step 5: Configure the Build

Use `gn` (Generate Ninja) to create the build files. You can customize the build arguments to create a release build.

```bash
# Generate build files in out/Default
gn gen out/Default

# To customize the build (e.g., for release), run:
gn args out/Default
```

In the editor that opens, add the following for a release build:

```text
is_debug = false
symbol_level = 0
is_component_build = false
```

## Step 6: Build Chromium

Use `autoninja` (a wrapper around ninja) to compile the browser. This will take several hours depending on your CPU.

```bash
autoninja -C out/Default chrome
```

## Step 7: Verify the Build

Once the build completes, you can run your custom browser:

```bash
./out/Default/chrome
```

## Step 8: Create a GitHub Repository and Push

1.  Create a new repository on GitHub (e.g., `my-chromium-fork`).
2.  Link your local repository to GitHub.

```bash
# If you want to push the entire chromium history (very large), or just your changes:
git remote add origin https://github.com/YOUR_USERNAME/my-chromium-fork.git

# Create a new branch for your changes
git checkout -b my-feature-branch

# Commit your changes
git add .
git commit -m "Initial fork customization"

# Push to GitHub
git push -u origin my-feature-branch
```

*Note: Because the Chromium repo is massive, it is often better to maintain a patchset or use a repo tool manifest rather than pushing the full history to a new generic git remote, unless you have Large File Storage (LFS) and high limits.*

## Step 9: Create a Beta Build (Release)

To distribute your build (the binary):

1.  **Package the binary**:
    ```bash
    # Create a zip or tarball of the output
    cd out/Default
    tar -czvf chromium-beta-linux.tar.gz chrome locales resources.pak icudtl.dat
    ```

2.  **Create a Release on GitHub**:
    *   Go to your GitHub repository.
    *   Click "Releases" -> "Draft a new release".
    *   Tag the version (e.g., `v1.0.0-beta`).
    *   Upload the `chromium-beta-linux.tar.gz` file as an asset.
    *   Publish the release.

## Automation (Optional)

For continuous integration, consider setting up a self-hosted GitHub Actions runner, as the standard GitHub runners may not have enough disk space or time to build Chromium.
