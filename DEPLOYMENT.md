# Streamlit Cloud Deployment Guide

This guide provides step-by-step instructions for deploying the Smart Traffic Monitoring System on Streamlit Community Cloud.

## 📋 Prerequisites

Before deploying, ensure you have:

1. **GitHub Account** - Free account at https://github.com
2. **Streamlit Community Cloud Account** - Free account at https://share.streamlit.io
3. **Repository Access** - This repository pushed to your GitHub account
4. **Browser** - Modern browser (Chrome, Firefox, Safari, Edge)

## 🚀 Step 1: Prepare Your Repository

### 1.1 Fork or Clone the Repository

Option A - Fork (Recommended for keeping your own version):
```bash
# On GitHub, click "Fork" button
# Then clone your fork:
git clone https://github.com/YOUR_USERNAME/smart-trafffic-monitoring-system.git
cd smart-trafffic-monitoring-system
```

Option B - Clone and Push:
```bash
git clone https://github.com/3843-jp/smart-trafffic-monitoring-system.git
cd smart-trafffic-monitoring-system
git remote set-url origin https://github.com/YOUR_USERNAME/smart-trafffic-monitoring-system.git
git push -u origin main
```

### 1.2 Verify Required Files

Ensure these files exist in your repository root:

```
smart-trafffic-monitoring-system/
├── app.py                    # ✅ Main Streamlit application
├── requirements.txt          # ✅ Python dependencies
├── packages.txt              # ✅ System packages (tesseract-ocr)
├── .streamlit/config.toml   # ✅ Streamlit configuration
├── README.md                 # ✅ Documentation
└── .gitignore               # ✅ Git ignore rules
```

**Critical files for deployment:**
- `app.py` - Entry point (required)
- `requirements.txt` - Python packages (required)
- `packages.txt` - System packages (required for Tesseract)
- `.streamlit/config.toml` - Settings (optional but recommended)

### 1.3 Commit and Push All Changes

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

## ☁️ Step 2: Deploy on Streamlit Community Cloud

### 2.1 Sign Up / Log In

1. Go to https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub account
4. Allow Streamlit to install the GitHub app on your repositories

### 2.2 Create New App

1. Click the **"New app"** button
2. In the modal dialog, fill in:
   - **Repository**: Select `YOUR_USERNAME/smart-trafffic-monitoring-system`
   - **Branch**: Select `main`
   - **Main file path**: Enter `app.py`

3. Click **"Deploy"**

Streamlit will now:
- Clone your repository
- Install packages from `packages.txt` (Tesseract OCR)
- Install Python packages from `requirements.txt`
- Download YOLOv8 model on first run
- Start the application

### 2.3 Wait for Deployment

Deployment typically takes 2-5 minutes:

```
✓ Cloning repository...
✓ Installing system packages from packages.txt...
✓ Installing Python packages from requirements.txt...
✓ Building app cache...
✓ Starting app...
```

Once complete, you'll see: **"App is running"**

Your app will be available at:
```
https://share.streamlit.io/YOUR_USERNAME/smart-trafffic-monitoring-system
```

## 🔧 Step 3: Post-Deployment Configuration

### 3.1 View Your App

1. Your deployed app URL: `https://share.streamlit.io/YOUR_USERNAME/smart-trafffic-monitoring-system`
2. Share this URL with others
3. The app starts fresh on each user session

### 3.2 Check Deployment Logs

In Streamlit Cloud dashboard:
1. Find your app in "My apps"
2. Click the three dots (...) menu
3. Select "Manage app"
4. View logs in "Logs" tab

### 3.3 Configure Secrets (Optional)

If you need to store sensitive configuration:

1. In Streamlit Cloud, click "Manage app"
2. Click "Secrets" tab
3. Add configuration in TOML format
4. Access in app via `st.secrets`

## ✅ Step 4: Verify Deployment

### 4.1 Test Basic Functionality

1. Open your deployed app URL
2. Verify the interface loads correctly
3. Check sidebar configuration options
4. Ensure video upload works

### 4.2 Test Video Processing

1. **Prepare a small test video** (10-30 seconds, 480p)
   - Format: MP4, AVI, or MOV
   - Size: < 50 MB (smaller = faster)
2. **Upload the test video**
3. **Configure settings:**
   - Speed Limit: 60 km/h
   - Meters per Pixel: 0.05
4. **Click "Process Video"**
5. **Verify results:**
   - Processing messages appear
   - Video processes without errors
   - Results display correctly
   - Download works

### 4.3 Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| App won't start | Check app.py syntax, review logs |
| "Module not found" | Verify requirements.txt is complete |
| Tesseract error | Ensure packages.txt contains "tesseract-ocr" |
| Slow startup | First run downloads YOLOv8 model (~130 MB) |
| App timeout | Processing long videos may timeout; use shorter clips |
| "File too large" | Streamlit Cloud has 500 MB upload limit |

## 🌐 Step 5: Share Your App

### 5.1 Share Public Link

```
https://share.streamlit.io/YOUR_USERNAME/smart-trafffic-monitoring-system
```

### 5.2 Create GitHub Badge

Add to your README.md:

```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/YOUR_USERNAME/smart-trafffic-monitoring-system)
```

### 5.3 Social Media

Share on Twitter, LinkedIn, etc:

```
🚗 Check out my Smart Traffic Monitoring System built with Streamlit!
Upload a traffic video, detect vehicles, estimate speeds, and recognize license plates.

🔗 [App Link]
📦 [GitHub Repo]

#Streamlit #ComputerVision #YOLOv8 #Python
```

## 🔄 Step 6: Updates & Maintenance

### 6.1 Update Your App

1. Make changes locally:
```bash
git add .
git commit -m "Update feature description"
git push origin main
```

2. Streamlit automatically redeploys within seconds
3. Users see the updated version on refresh

### 6.2 Rerun/Restart

If app becomes unresponsive:

1. Go to Streamlit Cloud dashboard
2. Click three dots (...) on your app
3. Select "Restart" or "Settings"
4. Click "Reboot" if needed

### 6.3 Monitor Usage

Streamlit Community Cloud shows:
- Number of users
- App runtime
- Error logs
- Resource usage

## ⚠️ Streamlit Cloud Limitations & Workarounds

### Resource Limitations

| Resource | Limit | Impact |
|----------|-------|--------|
| Upload size | 500 MB | Use shorter/lower res videos |
| Memory | ~1 GB | Process one video at a time |
| Runtime | ~1 hour | Long videos may timeout |
| CPU | Shared | Slower processing on busy cloud |
| Threads | Limited | Sequential processing only |

### Workarounds

**For large videos:**
1. Split into shorter clips
2. Process multiple times
3. Use lower resolution
4. Increase timeouts in app

**For better performance:**
1. Use smaller video files
2. Request faster cloud instance (premium)
3. Process during off-peak hours
4. Optimize video codec (H.264)

## 🐛 Troubleshooting

### App Won't Deploy

**Error: "ModuleNotFoundError"**
```bash
# Solution: Verify requirements.txt
pip install -r requirements.txt  # Test locally first
git add requirements.txt
git push origin main
```

**Error: "tesseract-ocr not found"**
```bash
# Ensure packages.txt exists with:
# tesseract-ocr
git add packages.txt
git push origin main
```

### App Crashes During Processing

**Error: "Timeout after X seconds"**
- Use shorter video clips
- Reduce video resolution
- Deploy to Streamlit Community Cloud Plus (paid)

**Error: "Out of memory"**
- Process shorter videos
- Reduce processing batch size
- Clear cache between runs

### Slow Performance

**Processing is very slow:**
1. Check if video is high resolution (720p+)
2. Try 480p or lower resolution
3. Process in off-peak hours (fewer users)
4. Contact Streamlit about Premium tier

### Video Won't Process

**Error: "Cannot open video"**
- Verify video format (MP4/AVI/MOV)
- Check file isn't corrupted
- Try re-encoding: `ffmpeg -i input.mov -c:v h264 -c:a aac output.mp4`

**Error: "No vehicles detected"**
- Video too dark or low quality
- Vehicles too small in frame
- Try different speed limit settings
- Check CONF_THRESHOLD in app.py

## 📊 Performance Expectations

On Streamlit Community Cloud:

| Video Length | Resolution | Est. Time |
|--------------|------------|-----------|
| 10 seconds | 480p | 30-60 sec |
| 30 seconds | 480p | 1-2 min |
| 1 minute | 480p | 2-4 min |
| 5 minutes | 480p | 10-20 min |
| 10 seconds | 720p | 1-2 min |
| 1 minute | 720p | 5-10 min |

**First run:** Add 1-2 minutes for model download

## 🔐 Security Best Practices

### Data Privacy

- ✅ Videos are processed in-memory only
- ✅ No videos stored on cloud after processing
- ✅ User uploads not persisted
- ⚠️ Ensure compliance with local privacy laws

### GitHub Security

```bash
# Never commit sensitive data
echo "*.mp4" >> .gitignore          # Ignore video files
echo ".streamlit/secrets.toml" >> .gitignore  # Ignore secrets
git add .gitignore
git commit -m "Update gitignore"
git push origin main
```

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud
- **Ultralytics YOLOv8**: https://github.com/ultralytics/ultralytics
- **Tesseract OCR**: https://github.com/UB-Mannheim/tesseract/wiki
- **GitHub Docs**: https://docs.github.com

## ✨ Tips for Success

### Optimization

1. **Test locally first:**
   ```bash
   streamlit run app.py
   ```

2. **Use smaller test videos** before deploying
3. **Monitor app logs** for errors
4. **Restart app regularly** if it slows down
5. **Update dependencies** monthly

### User Experience

1. **Add instructions** in sidebar (done ✓)
2. **Set reasonable defaults** (done ✓)
3. **Show progress** during processing (done ✓)
4. **Handle errors gracefully** (done ✓)
5. **Enable video download** (done ✓)

### Community

1. Share your app on social media
2. Contribute improvements back to repo
3. Report bugs on GitHub Issues
4. Help other users in discussions
5. Showcase results with before/after videos

## 🎯 Next Steps

1. ✅ Deploy to Streamlit Cloud
2. ✅ Test with sample video
3. ✅ Share with friends/colleagues
4. ✅ Gather feedback
5. ✅ Iterate and improve
6. ✅ Consider premium features if needed

---

**Questions?** Open an issue on GitHub: https://github.com/3843-jp/smart-trafffic-monitoring-system/issues

**Ready to deploy?** Go to https://share.streamlit.io and create your app!
