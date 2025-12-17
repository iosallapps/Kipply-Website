# 🚀 Kipply Website - Quick Start Guide

**Congratulations on purchasing kipplyapp.com!** Here's everything you need to get your website live in 5-10 minutes.

---

## ⭐ RECOMMENDED: GitHub Pages (Easiest!)

**Since you're already using GitHub, GitHub Pages is the simplest option!**

📖 **See DEPLOY_GITHUB_PAGES.md for complete step-by-step guide**

### Ultra-Quick Deploy:
```bash
cd /path/to/Kipply
git add website/
git commit -m "Add website for kipplyapp.com"
echo "kipplyapp.com" > website/CNAME
git add website/CNAME
git commit -m "Add custom domain"
git push
```

Then in GitHub: **Settings → Pages** → Enable (main branch, /website folder)

**Done! Site deploys automatically on every `git push`! 🚀**

---

## Alternative: Netlify (If you prefer drag & drop)

### Step 1: Sign Up (2 minutes)
1. Go to https://www.netlify.com
2. Click "Sign up" → Use GitHub, GitLab, or Email
3. Verify your email

### Step 2: Deploy (3 minutes)
1. Click "Add new site" → "Deploy manually"
2. **Drag the entire `website` folder** onto the upload area
3. Wait for deployment (30 seconds)
4. Your site is live at: `random-name-12345.netlify.app`

### Step 3: Add Your Domain (5 minutes)
1. In Netlify dashboard: **Domain management** → "Add custom domain"
2. Enter: `kipplyapp.com`
3. Netlify will show DNS instructions

### Step 4: Configure DNS (5 minutes)
Go to where you purchased kipplyapp.com and add these DNS records:

```
Type    Name    Value
A       @       75.2.60.5
CNAME   www     [your-site-name].netlify.app
```

**Common Registrars:**
- **Namecheap**: Advanced DNS → Add New Record
- **GoDaddy**: DNS Management → Add Record
- **Cloudflare**: DNS → Add record

### Step 5: Enable HTTPS (Automatic)
- Netlify automatically enables HTTPS
- Wait 10-20 minutes for SSL certificate
- Your site will be available at `https://kipplyapp.com`

---

## ✅ Verify Everything Works

Visit these URLs and check they load:
- ✅ https://kipplyapp.com
- ✅ https://kipplyapp.com/privacy.html
- ✅ https://kipplyapp.com/terms.html
- ✅ https://kipplyapp.com/support.html

---

## 📧 Set Up Support Email

### Option 1: Email Forwarding (Free & Easy)

Most domain registrars offer free email forwarding:

**Namecheap:**
1. Dashboard → Your domain → Email Forwarding
2. Create: `support@kipplyapp.com` → Forward to your personal email
3. Test by sending email to support@kipplyapp.com

**Cloudflare Email Routing (Free):**
1. Transfer DNS to Cloudflare
2. Email Routing → Enable
3. Add route: support@kipplyapp.com → your email

**Google Workspace ($6/month - Professional):**
- Get support@kipplyapp.com with full Gmail interface
- Sign up: https://workspace.google.com/

---

## 🔧 Update App Settings

### Critical: Replace Placeholder URLs

**File:** `Kipply/Views/Tabs/SettingsTabView.swift`

**Find and replace:**
```swift
// Line 113
"https://kipply.app/privacy"  →  "https://kipplyapp.com/privacy.html"

// Line 134
"https://kipply.app/terms"  →  "https://kipplyapp.com/terms.html"

// Line 68 & 238
"YOUR_APP_ID"  →  Your actual App Store ID (after approval)
```

---

## 📱 Add to App Store Connect

When submitting your app:

1. **App Privacy URL:** `https://kipplyapp.com/privacy.html`
2. **Support URL:** `https://kipplyapp.com/support.html`
3. **Marketing URL:** `https://kipplyapp.com` (optional)

---

## 🎯 When You Add AdMob (Future)

### After creating AdMob account:

1. Get your Publisher ID from https://admob.google.com
2. Update these files:

**ads.txt:**
```
google.com, pub-YOUR_ACTUAL_ID, DIRECT, f08c47fec0942fa0
```

**app-ads.txt:**
```
google.com, pub-YOUR_ACTUAL_ID, DIRECT, f08c47fec0942fa0
```

3. Re-upload to Netlify (drag & drop again)
4. Verify: https://kipplyapp.com/ads.txt

---

## 🆘 Troubleshooting

### "Domain not working after 24 hours"
1. Check DNS with https://dnschecker.org/
2. Verify you added BOTH A record (@) and CNAME (www)
3. Clear browser cache or try incognito mode

### "HTTPS not working"
1. Wait 20-30 minutes for SSL certificate
2. In Netlify: Domain Settings → HTTPS → Verify DNS configuration
3. Force HTTPS redirect should be ON

### "Privacy policy shows 404"
1. Check file name is lowercase: `privacy.html`
2. Re-upload entire website folder to Netlify
3. Clear Netlify cache: Deploys → Trigger deploy → Clear cache

---

## 📝 Before App Store Submission Checklist

- [ ] Website is live at kipplyapp.com
- [ ] All pages load with HTTPS
- [ ] Privacy Policy accessible
- [ ] Terms of Service accessible
- [ ] Support page accessible
- [ ] support@kipplyapp.com email works (test it!)
- [ ] URLs updated in SettingsTabView.swift
- [ ] Tested all links in footer and navigation

---

## 🎨 Optional: Add App Screenshots

**Replace placeholder in index.html:**

```html
<!-- Find this section -->
<div class="mockup-placeholder">
  <p>📸</p>
  <p>App Screenshot</p>
</div>

<!-- Replace with -->
<img src="images/iphone-screenshot.png"
     alt="Kipply App Screenshot"
     style="width: 100%; height: 100%; object-fit: cover;">
```

**Then:**
1. Create `website/images/` folder
2. Add your screenshot as `iphone-screenshot.png`
3. Re-upload to Netlify

---

## 💡 Pro Tips

### Update App Store Link After Approval
When your app is approved, update homepage:

```html
<!-- Replace all instances of href="#" with -->
href="https://apps.apple.com/app/id[YOUR_APP_ID]"
```

### Add Analytics (Optional)
Track visitors with Google Analytics:
1. Create GA4 account
2. Add tracking code to all HTML files
3. Monitor traffic in GA dashboard

### Improve SEO
- Add more keywords to meta descriptions
- Create blog posts about photo organization
- Share on social media

---

## 📞 Need Help?

**Netlify Support:**
- Docs: https://docs.netlify.com/
- Community: https://answers.netlify.com/

**DNS Issues:**
- Check propagation: https://dnschecker.org/
- Wait 24-48 hours max for full propagation

**Email Setup:**
- Contact your domain registrar's support
- Most have live chat or tutorials

---

## ✅ You're Done!

Your website is ready for App Store submission! 🎉

**Next Steps:**
1. ✅ Test all URLs one final time
2. ✅ Send a test email to support@kipplyapp.com
3. ✅ Update app settings with live URLs
4. ✅ Submit to App Store!

**Your live site:** https://kipplyapp.com

Good luck with your app launch! 🚀
