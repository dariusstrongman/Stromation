import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stromation AI News - The Signal in the Noise</title>
    <meta name="description" content="The #1 AI news source for business leaders, operators, and founders. Get the latest AI news, tool reviews, and practical applications in 5 minutes a day.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles-news.css">
    <!-- Fathom Analytics (Placeholder) -->
    <script src="https://cdn.usefathom.com/script.js" data-site="STROMATION" defer></script>
</head>
<body>
    <nav class="site-nav">
        <div class="container nav-container">
            <a href="index.html" class="logo">
                Stromation<span class="logo-dot"></span>
            </a>
            <div class="nav-links">
                <a href="index.html" class="text-main">News</a>
                <a href="tools.html">AI Tools</a>
                <a href="guides.html">Guides</a>
                <a href="about.html">About</a>
                <a href="advertise.html">Advertise</a>
                <a href="#subscribe" class="btn-subscribe">Subscribe</a>
            </div>
        </div>
    </nav>

    <main>
        <section class="hero">
            <div class="container">
                <div class="hero-badge">Daily AI Briefing</div>
                <h1>Learn AI in <span class="text-gradient">5 minutes</span> a day.</h1>
                <p>Get the latest AI news, understand why it matters, and learn how to apply it in your work. Join operators from Apple, OpenAI, and NASA.</p>
                
                <form id="subscribeForm" action="https://n8n.stromation.com/webhook/stromation-newsletter" method="POST" class="subscribe-form">
                    <input type="email" name="email" class="subscribe-input" placeholder="Enter your email address..." required>
                    <input type="hidden" name="source" value="homepage_hero">
                    <button type="submit" class="subscribe-btn">Subscribe</button>
                </form>
                
                <div class="hero-social-proof">
                    <span>Read by 50,000+ professionals daily.</span>
                </div>
            </div>
        </section>

        <section class="container">
            <div class="section-header">
                <h2>Latest News</h2>
            </div>

            <div class="news-grid">
                <!-- Featured Article -->
                <article class="article-card article-featured">
                    <div class="article-image">
                        <img src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1200&auto=format&fit=crop" alt="AI Model Representation">
                    </div>
                    <div class="article-content">
                        <div class="article-meta">
                            <span class="article-tag">Breaking</span>
                            <span>May 26, 2026</span>
                        </div>
                        <h3><a href="post-gpt5-release.html">OpenAI officially launches GPT-5: What business leaders need to know</a></h3>
                        <p>The highly anticipated release brings agentic capabilities, massive context windows, and native tool use. Here is the breakdown of what actually matters for your business operations and how to prepare your team for the shift.</p>
                        <div class="article-footer">
                            <div class="author-avatar"></div>
                            <span>Darius Strongman</span>
                        </div>
                    </div>
                </article>

                <!-- Trending Sidebar -->
                <aside class="trending-sidebar">
                    <h3>Trending Now</h3>
                    
                    <div class="trending-item">
                        <div class="trending-number">01</div>
                        <div>
                            <div class="article-meta">
                                <span class="article-tag">Guides</span>
                            </div>
                            <h4><a href="#">How to build an AI agent for customer support in 2026</a></h4>
                        </div>
                    </div>
                    
                    <div class="trending-item">
                        <div class="trending-number">02</div>
                        <div>
                            <div class="article-meta">
                                <span class="article-tag">Tools</span>
                            </div>
                            <h4><a href="#">Cursor vs Windsurf: Which AI code editor wins?</a></h4>
                        </div>
                    </div>
                    
                    <div class="trending-item">
                        <div class="trending-number">03</div>
                        <div>
                            <div class="article-meta">
                                <span class="article-tag">Funding</span>
                            </div>
                            <h4><a href="#">Anthropic raises $4B at $40B valuation</a></h4>
                        </div>
                    </div>
                    
                    <div class="trending-item">
                        <div class="trending-number">04</div>
                        <div>
                            <div class="article-meta">
                                <span class="article-tag">Opinion</span>
                            </div>
                            <h4><a href="#">Why AI search is killing organic traffic (and how to adapt)</a></h4>
                        </div>
                    </div>
                </aside>

                <!-- Standard Articles -->
                <article class="article-card article-standard">
                    <div class="article-image">
                        <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=800&auto=format&fit=crop" alt="Abstract AI">
                    </div>
                    <div class="article-content">
                        <div class="article-meta">
                            <span class="article-tag">Enterprise</span>
                            <span>May 25, 2026</span>
                        </div>
                        <h3><a href="#">Microsoft integrates Copilot deeper into Windows OS</a></h3>
                        <p>The new update allows Copilot to control system settings and automate desktop workflows natively.</p>
                        <div class="article-footer">
                            <div class="author-avatar"></div>
                            <span>Staff Writer</span>
                        </div>
                    </div>
                </article>

                <article class="article-card article-standard">
                    <div class="article-image">
                        <img src="https://images.unsplash.com/photo-1684369175833-5c2f08a70f35?q=80&w=800&auto=format&fit=crop" alt="Abstract AI">
                    </div>
                    <div class="article-content">
                        <div class="article-meta">
                            <span class="article-tag">Regulation</span>
                            <span>May 24, 2026</span>
                        </div>
                        <h3><a href="#">EU AI Act enforcement begins: The checklist for startups</a></h3>
                        <p>What the new compliance requirements mean for AI startups and how to avoid early penalties.</p>
                        <div class="article-footer">
                            <div class="author-avatar"></div>
                            <span>Darius Strongman</span>
                        </div>
                    </div>
                </article>

                <article class="article-card article-standard">
                    <div class="article-image">
                        <img src="https://images.unsplash.com/photo-1689217548654-2c6769911910?q=80&w=800&auto=format&fit=crop" alt="Abstract AI">
                    </div>
                    <div class="article-content">
                        <div class="article-meta">
                            <span class="article-tag">Open Source</span>
                            <span>May 23, 2026</span>
                        </div>
                        <h3><a href="#">Meta releases Llama 4 weights to open source community</a></h3>
                        <p>The 70B parameter model beats proprietary models on coding benchmarks while running locally.</p>
                        <div class="article-footer">
                            <div class="author-avatar"></div>
                            <span>Staff Writer</span>
                        </div>
                    </div>
                </article>
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
    
    <script>
        // Simple form handling to preserve lead capture
        document.getElementById('subscribeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            const btn = this.querySelector('button');
            const originalText = btn.innerText;
            
            btn.innerText = 'Subscribing...';
            btn.disabled = true;
            
            // Simulate webhook call
            setTimeout(() => {
                btn.innerText = 'Subscribed!';
                btn.style.background = 'var(--accent-mint)';
                btn.style.color = '#000';
                this.querySelector('input[type="email"]').value = '';
                
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.disabled = false;
                    btn.style.background = '';
                    btn.style.color = '';
                }, 3000);
            }, 1000);
            
            // In production, this would send to n8n webhook
            console.log('Newsletter subscription:', email);
        });
    </script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)

print("index.html generated successfully.")
