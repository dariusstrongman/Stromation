# Stromation Workflow Templates

Reusable n8n workflow templates for client deployments.

## Available Templates

### missed-call-textback.json
**Missed Call Text-Back System**

When a customer calls and no one answers, the system instantly:
1. Sends an SMS to the caller with a helpful reply + booking link
2. Alerts the business owner via SMS with caller details
3. When the caller replies, AI extracts what they need
4. Logs the lead and emails full context to the owner

**Deploy for a new client:**
1. Import JSON into n8n
2. Update 8 config vars in both code nodes (business name, Twilio creds, etc.)
3. Set up Twilio voice webhook with fallback to this workflow
4. Activate and test

**Pricing:** $1,000-$1,500 setup + $99-$149/mo retainer

**Stack:** Twilio + n8n + OpenAI + Cal.com
