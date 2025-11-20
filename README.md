# Stromation - AI Automation Agency Website

A modern, highly-animated landing page for Stromation, an AI-powered automation agency for small businesses.

## Features

### 🎨 Design Elements
- **Brand Colors**: Primary (#00D2C6), Accent (#4AF2E8), Dark Background (#0B0F19)
- **Typography**: Inter Tight for headings, Inter for body text
- **Modern UI**: Glassmorphism effects, neon accents, gradient overlays

### ✨ Interactive Animations

#### Hero Section
- 3D animated particle background with mouse interaction
- Neural network nodes with pulsing connections
- Floating gradient orbs
- Animated workflow demonstration with connecting lines
- Smooth scroll indicator

#### Live Automations Showcase
- **AI Chatbot Demo**: Typing animation showing real-time conversation
- **Workflow Builder**: Animated blocks sliding and connecting
- **Phone System**: Missed call notification with auto-SMS response
- Card hover effects with glowing borders

#### Features Grid
- 9 automation services with glowing SVG icons
- Hover effects: lift, scale, and glow
- Icon pulse animations

#### Stats Banner
- Glassmorphism cards with backdrop blur
- Animated wave background
- Counters that animate on scroll into view
- 3 key metrics: Time Saved, Conversion Rate, ROI

#### Pricing Section
- Glass-style pricing cards
- 3D tilt effect on mouse move
- Recommended plan highlighted with special badge
- Neon accent borders

#### Final CTA
- Pulsing AI nodes background animation
- Large glowing call-to-action button

#### Footer
- Subtle neon grid background
- Animated dot map effect

### 🚀 Advanced JavaScript Features

1. **Particle Canvas**: 80 floating particles with mouse repulsion
2. **Neural Network**: 30 nodes with dynamic connections and data flow
3. **Scroll Animations**: Intersection Observer for fade-in effects
4. **Cursor Particles**: Magical particle trail following cursor
5. **Smooth Scroll**: Navigation links smoothly scroll to sections
6. **Header Effect**: Transparent to solid on scroll
7. **Button Ripples**: Material Design-style click effects
8. **Stats Counter**: Numbers animate from 0 to target value
9. **Card Tilt**: 3D perspective tilt on pricing cards
10. **Performance Optimization**: Reduced animations on low-end devices

## File Structure

```
Stromation/
├── index.html          # Main HTML structure
├── styles.css          # Complete styling with animations
├── script.js           # Interactive JavaScript features
├── logo.png            # Your company logo
└── README.md           # This file
```

## How to Use

### Local Development
1. Open `index.html` in a modern web browser
2. For best results, use Chrome, Firefox, or Edge
3. All assets are self-contained (no external dependencies except Google Fonts)

### Deployment
Upload all files to your web hosting:
- Works with any static hosting (Netlify, Vercel, GitHub Pages, etc.)
- No build process required
- No npm packages or dependencies

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Performance Features

- Optimized canvas animations (60 FPS)
- Intersection Observer for scroll animations (better than scroll events)
- Hardware acceleration enabled for transforms
- Automatic animation reduction on low-end devices
- Efficient particle systems with cleanup

## Customization

### Colors
Edit CSS custom properties in `styles.css`:
```css
:root {
    --primary: #00D2C6;
    --secondary: #0B0F19;
    --accent: #4AF2E8;
    --background: #FFFFFF;
}
```

### Content
Update text directly in `index.html`:
- Hero headline and subheadline
- Feature descriptions
- Pricing tiers and features
- Contact information

### Animations
Adjust animation timing in `styles.css`:
```css
--transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

## Animation Details

### On Load
- Hero content fades in with staggered timing
- Particles begin floating
- Neural network starts connecting

### On Scroll
- Sections fade in as they enter viewport
- Stats counter animates when visible
- Cards cascade in with delays

### On Hover
- Cards lift with shadow
- Icons glow turquoise
- Buttons shimmer with shine effect
- Pricing cards tilt in 3D

### Ambient
- Continuous particle movement
- Gradient orbs floating
- Neural network pulsing
- Connection lines flowing

## Technical Highlights

1. **Pure Vanilla JavaScript**: No frameworks required
2. **CSS Grid & Flexbox**: Fully responsive layout
3. **Canvas API**: High-performance 2D animations
4. **Intersection Observer**: Efficient scroll detection
5. **CSS Custom Properties**: Easy theming
6. **Glassmorphism**: Modern backdrop-blur effects
7. **Gradient Animations**: Smooth color transitions

## SEO Ready

- Semantic HTML5 markup
- Meta descriptions included
- Accessible navigation
- Fast loading time
- Mobile responsive

## Next Steps

To make this production-ready:

1. **Add Forms**: Connect CTA buttons to actual form submissions
2. **Analytics**: Add Google Analytics or similar
3. **CMS Integration**: Connect to backend if needed
4. **Email Service**: Set up email automation for lead capture
5. **A/B Testing**: Test different headlines and CTAs
6. **Live Chat**: Add Intercom, Drift, or custom chatbot

## Credits

Built for Stromation - AI Automation Agency
Design based on modern SaaS landing page best practices
Animations inspired by cutting-edge web experiences

---

**Need help customizing?** Contact your developer or refer to the inline code comments.
