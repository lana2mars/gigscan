"""
GigScan - Autonomous Gig Opportunity Detection Agent
Built for AGENTIC 3.0 Hackathon | Track 4: The Scholar

An economic intent detection agent that autonomously monitors opportunity streams,
qualifies leads based on budget/urgency signals, and generates strategic outreach.
"""

from google import genai
import json
import os
import time
import argparse
from datetime import datetime

# ============================================================
# CONFIGURATION - Edit these to match your profile
# ============================================================

YOUR_SKILLS = """
- Ghostwriting for Web3 founders (threads, posts, long-form)
- Narrative strategy and positioning
- GTM (go-to-market) strategy
- Brand architecture and messaging
- Fractional CMO services
- Community building and ecosystem design
"""

YOUR_OFFERS = [
    {
        "name": "Ghostwriting Retainer",
        "description": "4 posts/week for Web3 founders who want consistent presence without the time drain",
        "price": "$1,500/month",
        "ideal_for": "Funded founders, protocols with treasury, busy builders"
    },
    {
        "name": "Narrative Sprint",
        "description": "2-week intensive to nail your positioning, messaging, and launch narrative",
        "price": "$2,000",
        "ideal_for": "Pre-launch projects, teams preparing for fundraise or token launch"
    },
    {
        "name": "Clarity Session",
        "description": "60-min deep dive to get your core story, GTM, and positioning right",
        "price": "$150",
        "ideal_for": "Early founders who need direction fast"
    }
]

YOUR_STYLE = """
Strategic but approachable. Not salesy. Lead with insight, not pitch.
Show you understand their problem before offering help.
Keep it short - 2-3 sentences max for initial outreach.
"""

# ============================================================
# GEMINI SETUP
# ============================================================

def setup_gemini(api_key: str):
    """Initialize Gemini client"""
    client = genai.Client(api_key=api_key)
    return client

# ============================================================
# CORE ANALYSIS ENGINE
# ============================================================

ANALYSIS_PROMPT = """
You are GigScan, an autonomous economic intent detection agent that identifies high-value opportunities for freelancers.

## YOUR USER'S PROFILE:
Skills: {skills}

Available Offers:
{offers}

Response Style: {style}

## YOUR TASK:
Perform deep analysis on the following post/message:
1. Detect economic intent signals (hiring, seeking help, budget indicators)
2. Assess urgency and timeline
3. Evaluate budget capacity based on contextual clues
4. Match to optimal offer from user's menu
5. Generate strategic outreach if opportunity qualifies

## POST TO ANALYZE:
{post_text}

## RESPOND IN THIS EXACT JSON FORMAT (no markdown, just raw JSON):
{{
    "is_opportunity": true,
    "confidence": 0.85,
    "signal_type": "content_need",
    "signals_detected": ["signal1", "signal2"],
    "budget_indicator": "high",
    "urgency": "high",
    "reply_speed_likelihood": "fast",
    "reasoning": "Detailed analysis explanation",
    "matched_offer": "Offer name or null",
    "match_reason": "Why this offer fits",
    "draft_response": "Ready-to-send outreach or null",
    "pass_reason": null
}}

Apply strict qualification criteria. Only flag genuine opportunities with clear economic intent.
Return ONLY valid JSON, no markdown code blocks.
"""

def analyze_post(client, post_text: str) -> dict:
    """Analyze a single post for gig potential using Gemini"""
    
    offers_text = "\n".join([
        f"- {o['name']}: {o['description']} ({o['price']}) - Ideal for: {o['ideal_for']}"
        for o in YOUR_OFFERS
    ])
    
    prompt = ANALYSIS_PROMPT.format(
        skills=YOUR_SKILLS,
        offers=offers_text,
        style=YOUR_STYLE,
        post_text=post_text
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        result = json.loads(text.strip())
        return result
    except json.JSONDecodeError as e:
        return {"error": f"Parse error: {e}", "raw": response.text}
    except Exception as e:
        return {"error": str(e)}

# ============================================================
# OUTPUT FORMATTING
# ============================================================

def print_opportunity(opp: dict, index: int = 0):
    """Pretty print a detected opportunity"""
    print(f"\n{'='*60}")
    print(f"🎯 OPPORTUNITY DETECTED")
    print(f"{'='*60}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📊 Confidence: {opp.get('confidence', 0)*100:.0f}%")
    print(f"🏷️  Signal: {opp.get('signal_type', 'unknown')}")
    print(f"💰 Budget: {opp.get('budget_indicator', 'unclear')} | ⚡ Urgency: {opp.get('urgency', 'unknown')}")
    print(f"🚀 Reply Speed: {opp.get('reply_speed_likelihood', 'unknown')}")
    print(f"\n📝 Original Post:")
    print(f"   {opp.get('original_post', 'N/A')}")
    print(f"\n🧠 Analysis:")
    print(f"   {opp.get('reasoning', 'N/A')}")
    print(f"\n🎁 Matched Offer: {opp.get('matched_offer', 'None')}")
    print(f"   Why: {opp.get('match_reason', 'N/A')}")
    print(f"\n✉️  Draft Response:")
    print(f"   {opp.get('draft_response', 'N/A')}")
    print(f"{'='*60}\n")

def print_rejection(post: str, reason: str):
    """Print rejection for non-opportunities"""
    print(f"\n❌ [{datetime.now().strftime('%H:%M:%S')}] Not an opportunity")
    print(f"   Post: {post[:50]}...")
    print(f"   Reason: {reason}\n")

# ============================================================
# AUTONOMOUS WATCH MODE
# ============================================================

def watch_file(client, filepath: str, interval: int = 5):
    """
    Autonomous monitoring mode - watches a file for new posts
    and analyzes them automatically without human intervention.
    
    This demonstrates the agent's ability to:
    1. Observe: Monitor data streams continuously
    2. Reason: Apply economic intent detection
    3. Plan: Match opportunities to offers
    4. Execute: Generate ready-to-send outreach
    """
    print(f"\n{'='*60}")
    print(f"🤖 GIGSCAN AUTONOMOUS MODE ACTIVATED")
    print(f"{'='*60}")
    print(f"📁 Watching: {filepath}")
    print(f"⏱️  Check interval: {interval}s")
    print(f"🛑 Press Ctrl+C to stop\n")
    
    processed_posts = set()
    opportunities_found = 0
    posts_analyzed = 0
    
    # Create file if doesn't exist
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write("")
        print(f"📄 Created empty watch file: {filepath}\n")
    
    try:
        while True:
            try:
                with open(filepath, 'r') as f:
                    lines = [line.strip() for line in f if line.strip()]
                
                new_posts = [p for p in lines if p not in processed_posts]
                
                for post in new_posts:
                    processed_posts.add(post)
                    posts_analyzed += 1
                    
                    print(f"🔍 [{datetime.now().strftime('%H:%M:%S')}] Analyzing new post...")
                    
                    result = analyze_post(client, post)
                    result["original_post"] = post[:200] + "..." if len(post) > 200 else post
                    
                    if result.get("is_opportunity"):
                        opportunities_found += 1
                        print_opportunity(result)
                        
                        # Save to opportunities log
                        with open("opportunities.json", "a") as f:
                            result["timestamp"] = datetime.now().isoformat()
                            f.write(json.dumps(result) + "\n")
                    else:
                        print_rejection(post, result.get('pass_reason', result.get('reasoning', 'No economic intent detected')))
                    
                    # Rate limit protection
                    time.sleep(2)
                
                # Status update every interval
                if not new_posts:
                    print(f"👀 [{datetime.now().strftime('%H:%M:%S')}] Watching... (analyzed: {posts_analyzed}, opportunities: {opportunities_found})", end='\r')
                
                time.sleep(interval)
                
            except FileNotFoundError:
                print(f"⚠️  File not found, creating: {filepath}")
                with open(filepath, 'w') as f:
                    f.write("")
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print(f"\n\n{'='*60}")
        print(f"📊 SESSION SUMMARY")
        print(f"{'='*60}")
        print(f"Posts analyzed: {posts_analyzed}")
        print(f"Opportunities found: {opportunities_found}")
        print(f"Conversion rate: {(opportunities_found/posts_analyzed*100) if posts_analyzed > 0 else 0:.1f}%")
        print(f"Results saved to: opportunities.json")
        print(f"{'='*60}\n")

# ============================================================
# BATCH ANALYSIS MODE
# ============================================================

def analyze_batch(client, posts: list) -> tuple:
    """Analyze multiple posts and return ranked opportunities"""
    results = []
    
    for i, post in enumerate(posts):
        print(f"🔍 Analyzing post {i+1}/{len(posts)}...")
        result = analyze_post(client, post)
        result["original_post"] = post[:200] + "..." if len(post) > 200 else post
        results.append(result)
        time.sleep(2)  # Rate limit protection
    
    opportunities = [r for r in results if r.get("is_opportunity", False)]
    opportunities.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    
    return opportunities, results

# ============================================================
# INTERACTIVE MODE
# ============================================================

def interactive_mode(client):
    """Interactive single-post analysis mode"""
    while True:
        print("\n" + "-"*40)
        print("Options:")
        print("  1. Analyze a single post")
        print("  2. Analyze from file (batch)")
        print("  3. Quick test with sample posts")
        print("  4. Exit")
        
        choice = input("\nChoice (1-4): ").strip()
        
        if choice == "1":
            print("\nPaste the post/message (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            post_text = "\n".join(lines)
            
            if post_text.strip():
                print("\n⏳ Analyzing...")
                result = analyze_post(client, post_text)
                result["original_post"] = post_text[:200] + "..." if len(post_text) > 200 else post_text
                
                if result.get("is_opportunity"):
                    print_opportunity(result)
                else:
                    print(f"\n❌ Not an opportunity")
                    print(f"   Reason: {result.get('pass_reason', result.get('reasoning', 'N/A'))}")
        
        elif choice == "2":
            filepath = input("Enter file path: ").strip()
            try:
                with open(filepath, 'r') as f:
                    posts = [line.strip() for line in f if line.strip()]
                print(f"\n📊 Found {len(posts)} posts to analyze...")
                opportunities, all_results = analyze_batch(client, posts)
                
                print(f"\n{'='*60}")
                print(f"📊 BATCH ANALYSIS COMPLETE")
                print(f"{'='*60}")
                print(f"Total posts: {len(all_results)}")
                print(f"Opportunities: {len(opportunities)}")
                
                for i, opp in enumerate(opportunities):
                    print_opportunity(opp, i)
                    
            except FileNotFoundError:
                print(f"❌ File not found: {filepath}")
        
        elif choice == "3":
            sample_posts = [
                "Just raised our seed round! Now we need to figure out how to tell our story. Any recommendations for Web3 narrative people?",
                "Building in public is hard. I should post more but shipping takes all my time.",
                "Looking for a content writer for our DeFi protocol. Must understand crypto. DM me.",
                "gm frens who's buying the dip",
                "We're launching at Token2049 next month and our messaging is all over the place. Need help fast.",
                "Anyone know a good ghostwriter? Tired of staring at blank drafts when I should be coding.",
            ]
            
            print(f"\n🧪 Running sample analysis on {len(sample_posts)} posts...")
            opportunities, all_results = analyze_batch(client, sample_posts)
            
            print(f"\n{'='*60}")
            print(f"📊 SAMPLE TEST COMPLETE")
            print(f"{'='*60}")
            print(f"Total posts: {len(all_results)}")
            print(f"Opportunities found: {len(opportunities)}")
            
            for i, opp in enumerate(opportunities):
                print_opportunity(opp, i)
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break

# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="GigScan - Autonomous Gig Opportunity Detection Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gigscan.py                    # Interactive mode
  python gigscan.py --watch posts.txt  # Autonomous watch mode
  python gigscan.py --batch posts.txt  # Batch analysis mode
        """
    )
    parser.add_argument('--watch', type=str, help='Watch file for new posts (autonomous mode)')
    parser.add_argument('--batch', type=str, help='Analyze all posts in file')
    parser.add_argument('--interval', type=int, default=5, help='Watch interval in seconds (default: 5)')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🔍 GIGSCAN - Autonomous Gig Opportunity Detection Agent")
    print("="*60)
    print("Track 4: The Scholar | AGENTIC 3.0 Hackathon")
    print("="*60)
    
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = input("\nEnter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    print("\n🚀 Initializing Gemini...")
    try:
        client = setup_gemini(api_key)
        print("✅ Gemini ready!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Route to appropriate mode
    if args.watch:
        watch_file(client, args.watch, args.interval)
    elif args.batch:
        try:
            with open(args.batch, 'r') as f:
                posts = [line.strip() for line in f if line.strip()]
            opportunities, _ = analyze_batch(client, posts)
            for opp in opportunities:
                print_opportunity(opp)
        except FileNotFoundError:
            print(f"❌ File not found: {args.batch}")
    else:
        interactive_mode(client)

if __name__ == "__main__":
    main()
