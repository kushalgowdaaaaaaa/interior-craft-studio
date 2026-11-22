# Interior Craft Studio website

A one-page static site: plain HTML with the CSS and JavaScript inside `index.html`. There's no framework and no build step, so it deploys on Vercel's free (Hobby) plan as-is.

- About 160 KB in total on first load: two self-hosted fonts (41 KB), the logo (62 KB) and small images
- Lighthouse on mobile, tested locally: Performance 99, Accessibility 100, Best Practices 100, SEO 100
- The logo intro plays for about 2 seconds while the page loads underneath it. Tapping it skips the intro. Visitors who have turned on "reduce motion" see a short fade, and visitors without JavaScript see the page straight away.

## 1. Add your details (5 minutes)

Open `index.html` in any text editor and use **Find and Replace** for each line below. Each spot is also marked with an `<!-- EDIT -->` comment.

| Find | Replace with | Example |
|---|---|---|
| `+910000000000` | your number for tap-to-call: country code, no spaces | `+919876543210` |
| `+91 00000 00000` | your number as people should read it | `+91 98765 43210` |
| `your.instagram` | your Instagram handle, without the @ | `interiorcraftstudio` |
| `Studio address line` | first line of your address | `12, MG Road` |
| `Area, City 000 000` | the rest of your address | `Indiranagar, Bengaluru 560038` |
| `https://your-domain.vercel.app` | your live web address, after the first deploy | `https://interiorcraftstudio.vercel.app` |

**Map link:** on Google Maps, open your studio's pin, tap **Share** and copy the link. In `index.html`, find `https://www.google.com/maps/search/?api=1&amp;query=Interior+Craft+Studio` and paste your link in its place. The "Visit" row will then open your exact pin.

Also update the address in the `<script type="application/ld+json">` block near the top of the file (`streetAddress`, `addressLocality`, `postalCode`). Google uses it for local search.

## 2. Add or update your project photos

The site comes pre-loaded with photorealistic, high-end interior architecture photos tailored to each section.

To replace any photo with your own project shots, you can either:

### Method A: Automated Optimizer (Recommended)
1. Drop your high-res original photos (JPG, PNG, WebP) into `images-raw/` with these names:
   - `hero.jpg` (Hero top section)
   - `work-living.jpg` (Recent work: Living room)
   - `work-kitchen.jpg` (Recent work: Kitchen)
   - `work-wardrobe.jpg` (Recent work: Bedroom / Wardrobe)
   - `work-entrance.jpg` (Recent work: Entrance / Foyer)
2. Run the optimizer script:
   ```bash
   python scripts/optimize-images.py
   ```
   The script automatically center-crops to the ideal aspect ratio, optimizes compression with WebP, and saves directly into `images/` (cutting file sizes by ~90-95% to preserve Vercel free-tier bandwidth).

### Method B: Manual replacement
Overwrite the files in `/images` directly using the same file names:

| File | Where it shows | Best shape | Target Size |
|---|---|---|---|
| `images/hero.webp` | Large image at the top | Portrait (4:5 or 1000x1250) | ~30-60 KB |
| `images/work-living.webp` | Recent work, 1st | Portrait (8:11 or 800x1100) | ~40-80 KB |
| `images/work-kitchen.webp` | Recent work, 2nd | Landscape (3:2 or 1200x800) | ~40-70 KB |
| `images/work-wardrobe.webp` | Recent work, 3rd | Square (1:1 or 900x900) | ~30-50 KB |
| `images/work-entrance.webp` | Recent work, 4th | Square (1:1 or 900x900) | ~30-50 KB |

Then, in `index.html`, update the `alt="..."` text and the `<figcaption>` text under each photo to describe your project.

## 3. Deploy on Vercel (free)

**Option A: GitHub (recommended, because every later change redeploys automatically)**
1. Create a new repository on GitHub and upload all the files in this folder.
2. On vercel.com, sign in with GitHub and choose **Add New… → Project**.
3. Import the repository. Set the Framework Preset to **Other** and leave the build settings empty.
4. Click **Deploy**. Your site will be live at `your-project.vercel.app` in under a minute.

**Option B: the command line**
```bash
npm i -g vercel
cd interior-craft-studio
vercel          # first time: answer the questions, accept the defaults
vercel --prod   # publish to your live address
```

To use your own domain, open the project on Vercel and go to **Settings → Domains**.

## Files

```
index.html          the whole site (HTML, CSS, JS)
404.html            "page not found" page
vercel.json         caching and security headers for Vercel
assets/logo-*.webp  logo, split into the house mark and the wordmark
assets/fonts/       Marcellus + Jost (SIL Open Font License, see licence files)
images/             photos (replace with your own)
favicon.*, apple-touch-icon.png, og-image.jpg   browser icons and the link preview image
```

## Changing colours or fonts

All colours are set at the top of the `<style>` block in `index.html`:

```css
--linen:#F6F1EA;  /* page background */
--chalk:#FDFBF8;  /* lighter sections */
--sand:#ECE3D6;   /* beige band + footer */
--oat:#D9CCBA;    /* thin lines */
--umber:#6B5C4E;  /* secondary text */
--walnut:#2F261F; /* main text + buttons */
--brass:#9A7B4F;  /* drawing lines + step numbers */
```

To preview the site on your own computer, run `npx serve .` in this folder and open the address it prints.
