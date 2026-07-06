import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Guides & Tutorials - Stromation</title>
    <meta name="description" content="In-depth guides on how to implement AI in your business. Learn automation, prompt engineering, and agent building.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles-news.css">
    <style>
        .guides-header {
            padding: 80px 0 40px;
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 64px;
        }
        
        .guides-header h1 {
            font-size: clamp(40px, 6vw, 64px);
            margin-bottom: 24px;
        }
        
        .guides-header p {
            font-size: 20px;
            color: var(--text-muted);
            max-width: 600px;
        }
        
        .guides-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 32px;
            margin-bottom: 80px;
        }
        
        .guide-card {
            background: var(--bg-panel);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            overflow: hidden;
            transition: transform 0.2s ease, border-color 0.2s ease;
            display: flex;
            flex-direction: column;
        }
        
        .guide-card:hover {
            transform: translateY(-4px);
            border-color: var(--border-focus);
        }
        
        .guide-image {
            aspect-ratio: 16/9;
            background: #1a1a1d;
            border-bottom: 1px solid var(--border-light);
            position: relative;
        }
        
        .guide-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        }
        
        .guide-card:hover .guide-image img {
            opacity: 1;
        }
        
        .guide-level {
            position: absolute;
            top: 16px;
            right: 16px;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(4px);
            padding: 4px 12px;
            border-radius: 100px;
            font-size: 12px;
            font-weight: 600;
            font-family: var(--font-mono);
            border: 1px solid var(--border-light);
        }
        
        .level-beginner { color: var(--accent-mint); }
        .level-intermediate { color: var(--accent-cyan); }
        .level-advanced { color: var(--accent-purple); }
        
        .guide-content {
            padding: 24px;
            display: flex;
            flex-direction: column;
            flex: 1;
        }
        
        .guide-meta {
            font-size: 12px;
            color: var(--text-dim);
            font-family: var(--font-mono);
            margin-bottom: 12px;
            display: flex;
            gap: 12px;
        }
        
        .guide-card h3 {
            font-size: 20px;
            margin-bottom: 12px;
            line-height: 1.3;
        }
        
        .guide-card p {
            color: var(--text-muted);
            font-size: 15px;
            margin-bottom: 24px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .guide-footer {
            margin-top: auto;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .guide-card:hover .guide-footer {
            color: var(--accent-cyan);
        }
        
        @media (max-width: 1024px) {
            .guides-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .guides-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <nav class="site-nav">
        <div class="container nav-container">
            <a href="index.html" class="logo">
                Stromation<span class="logo-dot"></span>
            </a>
            <div class="nav-links">
                <a href="index.html">News</a>
                <a href="tools.html">AI Tools</a>
                <a href="guides.html" class="text-main">Guides</a>
                <a href="about.html">About</a>
                <a href="advertise.html">Advertise</a>
                <a href="index.html#subscribe" class="btn-subscribe">Subscribe</a>
            </div>
        </div>
    </nav>

    <main>
        <section class="guides-header">
            <div class="container">
                <h1>AI <span class="text-gradient">Implementation</span> Guides</h1>
                <p>Step-by-step tutorials on how to build AI workflows, craft better prompts, and deploy agents in your business.</p>
            </div>
        </section>

        <section class="container">
            <div class="guides-grid">
                <!-- Guide 1 -->
                <a href="#" class="guide-card">
                    <div class="guide-image">
                        <div class="guide-level level-beginner">Beginner</div>
                        <img src="https://images.unsplash.com/photo-1655393001768-d946c98d6915?q=80&w=800&auto=format&fit=crop" alt="Prompt Engineering">
                    </div>
                    <div class="guide-content">
                        <div class="guide-meta">
                            <span>Prompting</span>
                            <span>10 min read</span>
                        </div>
                        <h3>The definitive guide to multi-shot prompting for Claude 3.5</h3>
                        <p>Stop getting generic outputs. Learn how to structure your prompts with XML tags, context framing, and few-shot examples to get exactly what you want.</p>
                        <div class="guide-footer">Read Guide →</div>
                    </div>
                </a>

                <!-- Guide 2 -->
                <a href="#" class="guide-card">
                    <div class="guide-image">
                        <div class="guide-level level-intermediate">Intermediate</div>
                        <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800&auto=format&fit=crop" alt="Automation">
                    </div>
                    <div class="guide-content">
                        <div class="guide-meta">
                            <span>Automation</span>
                            <span>15 min read</span>
                        </div>
                        <h3>How to build an automated AI news aggregator with n8n</h3>
                        <p>A complete walkthrough of building a system that scrapes RSS feeds, uses AI to summarize articles, and drafts a daily newsletter automatically.</p>
                        <div class="guide-footer">Read Guide →</div>
                    </div>
                </a>

                <!-- Guide 3 -->
                <a href="#" class="guide-card">
                    <div class="guide-image">
                        <div class="guide-level level-advanced">Advanced</div>
                        <img src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=800&auto=format&fit=crop" alt="AI Agents">
                    </div>
                    <div class="guide-content">
                        <div class="guide-meta">
                            <span>AI Agents</span>
                            <span>25 min read</span>
                        </div>
                        <h3>Building your first autonomous customer support agent</h3>
                        <p>Move beyond simple chatbots. Learn how to give an AI agent access to your internal documentation and API tools to actually resolve customer tickets.</p>
                        <div class="guide-footer">Read Guide →</div>
                    </div>
                </a>

                <!-- Guide 4 -->
                <a href="#" class="guide-card">
                    <div class="guide-image">
                        <div class="guide-level level-beginner">Beginner</div>
                        <img src="https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?q=80&w=800&auto=format&fit=crop" alt="AI Coding">
                    </div>
                    <div class="guide-content">
                        <div class="guide-meta">
                            <span>Coding</span>
                            <span>12 min read</span>
                        </div>
                        <h3>How to build a web app with Cursor (even if you can't code)</h3>
                        <p>The complete guide to "vibe coding." Learn how to use Cursor's Composer feature to build, debug, and deploy a functional web application from scratch.</p>
                        <div class="guide-footer">Read Guide →</div>
                    </div>
                </a>

                <!-- Guide 5 -->
                <a href="#" class="guide-card">
                    <div class="guide-image">
                        <div class="guide-level level-intermediate">Intermediate</div>
                        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop" alt="Data Analysis">
                    </div>
                    <div class="guide-content">
                        <div class="guide-meta">
                            <span>Data</span>
                            <span>18 min read</span>
                        </div>
                        <h3>Using ChatGPT Advanced Data Analysis for marketing reports</h3>
                        <p>Stop wrestling with Excel. Learn how to upload raw CSV exports from Google Analytics and Facebook Ads to generate boardroom-ready insights.</p>
                        <div class="guide-footer">Read Guide →</div>
                    </div>
                </a>

                <!-- Guide 6 -->
                <a href="#" class="guide-card">
                    <div class="guide-image">
                        <div class="guide-level level-intermediate">Intermediate</div>
                        <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop" alt="SEO">
                    </div>
                    <div class="guide-content">
                        <div class="guide-meta">
                            <span>Marketing</span>
                            <span>14 min read</span>
                        </div>
                        <h3>The AI SEO Playbook: Ranking in the era of AI Overviews</h3>
                        <p>Traditional SEO is dying. Learn how to optimize your content for Google's AI Overviews and Perplexity using information gain and entity relationships.</p>
                        <div class="guide-footer">Read Guide →</div>
                    </div>
                </a>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="index.html" class="logo">
                        Stromation<span class="logo-dot"></span>
                    </a>
                    <p>The signal in the noise. Daily AI news, tools, and insights for business leaders.</p>
                </div>
                <div class="footer-links">
                    <h4>Content</h4>
                    <ul>
                        <li><a href="index.html">News</a></li>
                        <li><a href="tools.html">AI Tools</a></li>
                        <li><a href="guides.html">Guides</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="about.html">About</a></li>
                        <li><a href="advertise.html">Advertise</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>Legal</h4>
                    <ul>
                        <li><a href="privacy.html">Privacy Policy</a></li>
                        <li><a href="terms.html">Terms of Service</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Stromation. All rights reserved.</p>
                <div class="social-links">
                    <a href="https://twitter.com/stromationhq">Twitter / X</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
"""

with open("guides.html", "w") as f:
    f.write(html_content)

print("guides.html generated successfully.")
