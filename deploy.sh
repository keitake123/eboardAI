#!/bin/bash

# Netlify Deployment Script for Teacher AI Support App
echo "🚀 Starting Netlify deployment preparation..."

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Check if required files exist
echo "📁 Checking required files..."

required_files=("index.html" "netlify.toml" "netlify/functions/getairesponse.js" "package.json")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    printf '   - %s\n' "${missing_files[@]}"
    exit 1
fi

echo "✅ All required files present"

# Check VTT files
vtt_count=$(find vtt_files -name "*.vtt" 2>/dev/null | wc -l)
echo "📹 Found $vtt_count VTT subtitle files"

# Check CSV files
csv_count=$(find . -maxdepth 1 -name "*.csv" 2>/dev/null | wc -l)
echo "📊 Found $csv_count CSV data files"

echo ""
echo "🔧 Configuration Summary:"
echo "   - Functions: netlify/functions/"
echo "   - Publish directory: . (root)"
echo "   - VTT files: $vtt_count files in vtt_files/"
echo "   - CSV files: $csv_count files"

echo ""
echo "⚠️  Important: Make sure to set the GEMINI_API_KEY environment variable in Netlify!"
echo ""

# Offer to deploy or just prepare
read -p "Would you like to deploy now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Deploying to Netlify..."
    netlify deploy --prod
    echo "✅ Deployment complete!"
    echo "🌐 Your app should be available at your Netlify URL"
else
    echo "📋 Ready for deployment. Run 'netlify deploy --prod' when ready."
fi

echo ""
echo "📖 For detailed instructions, see README_NETLIFY_DEPLOYMENT.md" 