Create or update an n8n workflow to handle a website form submission.

Form details: $ARGUMENTS

The Stromation n8n instance is at: https://n8n.stromation.com/home/workflows

Steps:
1. Identify which form on the Stromation site this is for (contact, audit request, etc.)
2. Design the n8n workflow:
   - Webhook trigger node to receive the form POST data
   - Data validation/sanitization
   - Email notification (to support@stromation.com and/or the submitter)
   - Optional: save to Google Sheets, Airtable, CRM, etc.
   - Optional: Slack/Discord notification
   - Error handling with notification
3. Provide the webhook URL format for the site's form action
4. If needed, update the HTML form on the website to POST to the n8n webhook
5. Provide test instructions
