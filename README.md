# Kipply Website - Deployment Guide

This folder contains the complete website for kipplyapp.com including all App Store required pages.

## 📁 Files Included

### Main Pages
- `index.html` - Homepage/landing page
- `privacy.html` - Privacy Policy (required for App Store)
- `terms.html` - Terms of Service (required for App Store)
- `support.html` - Support page with FAQ
- `styles.css` - Complete stylesheet for all pages

### AdMob Files (for future use)
- `ads.txt` - AdMob verification file
- `app-ads.txt` - Mobile app ads verification file

## 🚀 Quick Deploy

### Option 1: Netlify (Recommended - Free & Easy)

1. **Sign up at** https://www.netlify.com
2. **Drag and drop** the entire `website` folder onto Netlify
3. **Add custom domain:**
   - In Netlify dashboard: Domain Settings → Add custom domain
   - Enter: `kipplyapp.com`
   - Follow DNS instructions below

4. **Configure DNS at your domain registrar:**
   ```
   Type    Name    Value
   A       @       75.2.60.5
   CNAME   www     [your-site].netlify.app
   ```

5. **Enable HTTPS** (automatic with Netlify)

### Option 2: Vercel (Free & Fast)

1. **Sign up at** https://vercel.com
2. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

3. **Deploy:**
   ```bash
   cd website
   vercel
   ```

4. **Add domain:**
   - Follow Vercel's domain setup instructions
   - Point `kipplyapp.com` to Vercel

### Option 3: GitHub Pages (Free)

1. **Create GitHub repo:**
   ```bash
   cd website
   git init
   git add .
   git commit -m "Initial commit"
   gh repo create kipply-website --public --push
   ```

2. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: Deploy from main branch
   - Custom domain: kipplyapp.com

3. **Add CNAME file:**
   ```bash
   echo "kipplyapp.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

### Option 4: Traditional Web Host

Upload all files via FTP/SFTP to your web host's public_html or www directory.

## 🔧 Post-Deployment Tasks

### 1. Verify URLs in App Settings

Update these files with your live URLs:

**In `Kipply/Views/Tabs/SettingsTabView.swift`:**
- Line 113: `https://kipplyapp.com/privacy`
- Line 134: `https://kipplyapp.com/terms`

### 2. Test All Pages

Visit and verify:
- ✅ https://kipplyapp.com
- ✅ https://kipplyapp.com/privacy.html
- ✅ https://kipplyapp.com/terms.html
- ✅ https://kipplyapp.com/support.html

### 3. SSL/HTTPS Setup

Ensure all pages load with HTTPS:
- Netlify/Vercel provide automatic HTTPS
- GitHub Pages provides automatic HTTPS
- Traditional hosts may require Let's Encrypt setup

### 4. App Store Connect

Add these URLs in App Store Connect:
- **Privacy Policy URL:** `https://kipplyapp.com/privacy.html`
- **Support URL:** `https://kipplyapp.com/support.html`
- **Marketing URL:** `https://kipplyapp.com` (optional)

## 📧 Email Setup

Set up email forwarding for support@kipplyapp.com:

### Option 1: Domain Registrar Email Forwarding
Most registrars offer free email forwarding:
- Forward `support@kipplyapp.com` → your personal email

### Option 2: Google Workspace (Paid)
- $6/month per user
- Professional email with Gmail interface
- Sign up: https://workspace.google.com/

### Option 3: Cloudflare Email Routing (Free)
1. Transfer domain DNS to Cloudflare
2. Enable Email Routing
3. Forward support@kipplyapp.com to your email

## 🔄 Future Updates

### When Integrating AdMob:

1. **Get AdMob Publisher ID:**
   - Sign up at https://admob.google.com
   - Create iOS app in AdMob dashboard
   - Find your Publisher ID (format: `pub-XXXXXXXXXXXXXXXX`)

2. **Update ads.txt and app-ads.txt:**
   ```
   google.com, pub-YOUR_ACTUAL_ID, DIRECT, f08c47fec0942fa0
   ```

3. **Verify files are accessible:**
   - https://kipplyapp.com/ads.txt
   - https://kipplyapp.com/app-ads.txt

4. **Update Privacy Policy:**
   - Add AdMob data collection details
   - Update "Third-Party Services" section

## 🎨 Customization

### Update App Store Links

When your app is live, replace `#` with actual App Store URL:

**In `index.html`:**
```html
<!-- Find and replace -->
href="#"
<!-- With -->
href="https://apps.apple.com/app/idYOUR_APP_ID"
```

### Add App Screenshots

Replace the placeholder in `index.html`:
```html
<div class="mockup-placeholder">
  <!-- Replace this with actual screenshot -->
  <img src="images/app-screenshot.png" alt="Kipply App">
</div>
```

### Update Footer Year

If deploying in a different year, update:
```html
<p>&copy; 2025 Kipply. All rights reserved.</p>
```

## 🔍 SEO & Meta Tags

The homepage includes basic SEO meta tags. For better App Store visibility, consider adding:

```html
<meta property="og:title" content="Kipply - Smart Photo Cleaner">
<meta property="og:description" content="Clean your photo library with simple swipes">
<meta property="og:image" content="https://kipplyapp.com/images/og-image.png">
<meta property="og:url" content="https://kipplyapp.com">
<meta name="twitter:card" content="summary_large_image">
```

## 📊 Analytics (Optional)

To track website visitors, add Google Analytics:

1. Create Google Analytics account
2. Get tracking ID
3. Add to all HTML files before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## ⚠️ Important Notes

### Before App Store Submission:
- ✅ All pages must be live and accessible via HTTPS
- ✅ Privacy Policy and Terms must match app functionality
- ✅ Support email must be monitored
- ✅ URLs in app settings must be updated

### Legal Disclaimer:
The provided Privacy Policy and Terms of Service are templates. Consider having them reviewed by a lawyer, especially if:
- You plan to collect user data
- You're launching in EU (GDPR compliance)
- You're targeting California users (CCPA compliance)

## 🆘 Troubleshooting

### "DNS not resolving"
- Wait 24-48 hours for DNS propagation
- Check DNS settings with https://dnschecker.org/

### "Privacy Policy not found (404)"
- Ensure file names are lowercase: `privacy.html` not `Privacy.html`
- Check file is uploaded to root directory

### "SSL certificate error"
- Most hosts provide automatic SSL
- For manual setup, use Let's Encrypt (free)

## 📞 Need Help?

If you have questions about deployment:
1. Check your hosting provider's documentation
2. Netlify Docs: https://docs.netlify.com/
3. Vercel Docs: https://vercel.com/docs
4. GitHub Pages: https://pages.github.com/

## ✅ Deployment Checklist

- [ ] All files uploaded to web host
- [ ] Domain DNS configured
- [ ] HTTPS/SSL enabled
- [ ] All pages accessible (test each URL)
- [ ] Email forwarding set up (support@kipplyapp.com)
- [ ] URLs updated in app settings
- [ ] Privacy Policy URL added to App Store Connect
- [ ] Support URL added to App Store Connect
- [ ] Test all links in footer and navigation

**Once complete, your website is ready for App Store submission! 🚀**
