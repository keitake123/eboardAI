# Netlify Deployment Guide

## Overview
This guide explains how to deploy the Teacher AI Support App to Netlify with proper configuration for the Gemini AI integration.

## Prerequisites
1. A Netlify account (free tier is sufficient)
2. A Google Gemini API key
3. Git repository with your code

## Deployment Steps

### 1. Connect Repository to Netlify
1. Log in to [Netlify](https://netlify.com)
2. Click "New site from Git"
3. Connect your GitHub/GitLab/Bitbucket repository
4. Select this repository

### 2. Build Configuration
Netlify will automatically detect the `netlify.toml` configuration file. The deployment settings are:
- **Build command**: (none needed - static site)
- **Publish directory**: `.` (root directory)
- **Functions directory**: `netlify/functions`

### 3. Set Environment Variables
1. In Netlify dashboard, go to **Site settings** → **Environment variables**
2. Add the following variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your Google Gemini API key

### 4. Deploy
1. Click **Deploy site**
2. Wait for the build to complete
3. Your site will be available at `https://[site-name].netlify.app`

## Environment Variables Required

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI responses | Yes |

## Troubleshooting

### Common Issues

**1. Function not working**
- Check environment variables are set correctly
- Verify `GEMINI_API_KEY` is valid and has proper permissions
- Check function logs in Netlify dashboard

**2. Subtitle files not loading**
- Ensure `vtt_files/` directory is in repository
- Check file names match the video IDs in CSV
- Verify file paths in console logs

**3. CSV data not loading**
- Ensure CSV files are included in deployment
- Check file encoding (should be UTF-8)
- Verify column structure matches expected format 