# Navigate to the frontend directory
cd ./frontend

# Build the Next.js project
Write-Host "Building the Next.js project..."
npm run build

# Check if the build was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Exiting..." -ForegroundColor Red
    exit $LASTEXITCODE
}

# Define the source and destination paths
$nextSourcePath = ".\.next"
$nextDestinationPath = "..\backend\static\.next"
$publicSourcePath = ".\public"
$publicDestinationPath = "..\backend\static\media"

# Remove the existing .next folder in the backend/static directory if it exists
if (Test-Path $nextDestinationPath) {
    Write-Host "Removing existing .next folder in backend/static..."
    Remove-Item -Recurse -Force $nextDestinationPath
}

# Copy the .next folder to the backend/static directory
Write-Host "Copying .next folder to backend/static..."
Copy-Item -Recurse -Force $nextSourcePath $nextDestinationPath

# Remove the existing media folder in the backend/static directory if it exists
if (Test-Path $publicDestinationPath) {
    Write-Host "Removing existing media folder in backend/static..."
    Remove-Item -Recurse -Force $publicDestinationPath
}

# Copy the contents of the public folder to the backend/static/media directory
Write-Host "Copying public folder contents to backend/static/media..."
Copy-Item -Recurse -Force $publicSourcePath $publicDestinationPath

Write-Host "Build and copy completed successfully!" -ForegroundColor Green

cd ..