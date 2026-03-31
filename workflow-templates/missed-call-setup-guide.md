# Missed Call Text-Back - Deployment Guide

## Per-Client Setup

### Step 1: Get the Client's Number on Twilio

**Recommended: Port their existing number (1-2 weeks)**
1. console.twilio.com -> Phone Numbers -> Port a Number
2. Client fills out LOA (Letter of Authorization) 
3. Provide: client name, address, current carrier, account number + PIN
4. Twilio handles the port. Number keeps working during transfer.
5. Once ported: calls AND texts come from the same number customers already know

**Alternative: New business or doesnt want to port**
- Buy a new local number in their area code ($1.15/mo)
- Client updates their Google listing, website, cards to the new number

**Never use call forwarding** - texts would come from a different number than the one they called, looks sketchy and kills trust.

### Step 2: Create TwiML Bin
1. console.twilio.com -> Develop -> TwiML Bins -> Create new
2. Name: "CLIENT NAME - Ring Then Text-Back"
3. TwiML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial timeout="20"
        action="https://n8n.myaibuffet.com/webhook/missed-call-CLIENTSLUG"
        method="POST">
    <Number>+1XXXXXXXXXX</Number>
  </Dial>
</Response>
```

Replace `+1XXXXXXXXXX` with the owner's cell phone (where calls should ring).
Replace `CLIENTSLUG` with a URL-safe client identifier (e.g. `addison-pest`).

How it works:
- Customer calls the business number (now on Twilio)
- Twilio rings the owner's cell for 20 seconds
- If no answer, Twilio POSTs to n8n webhook
- n8n sends text-back FROM the same business number

### Step 3: Configure the Twilio Number
1. Phone Numbers -> Active Numbers -> click the ported/new number
2. Voice: "A call comes in" -> TwiML Bin -> select yours
3. Messaging: "A message comes in" -> Webhook -> `https://n8n.myaibuffet.com/webhook/missed-call-reply-CLIENTSLUG` (POST)
4. Save

### Step 4: Deploy n8n Workflow
1. Duplicate "TEMPLATE - Missed Call Text-Back" in n8n
2. Rename: "CLIENT NAME - Missed Call Text-Back"
3. Update webhook paths in both webhook nodes to use CLIENTSLUG
4. Update config vars in BOTH code nodes:
   - `BUSINESS_NAME` - client business name
   - `OWNER_PHONE` - owner's personal cell for SMS alerts
   - `OWNER_EMAIL` - owner's email for lead alerts
   - `TWILIO_SID` - your Twilio account SID
   - `TWILIO_TOKEN` - your Twilio auth token
   - `TWILIO_FROM` - the ported/new Twilio number (the business line)
   - `OPENAI_KEY` - your OpenAI API key
   - `BOOKING_LINK` - client's booking URL
   - `BUSINESS_TYPE` - what they do (for AI context)
5. Update Email node sendTo with owner's email
6. Activate

### Step 5: Test
1. Call the business number from a personal phone
2. Dont answer
3. Wait 20 seconds
4. Verify:
   - Text-back arrives on personal phone FROM the business number
   - Owner gets SMS alert on their cell
   - Owner gets email with caller details
5. Reply to the text-back
6. Verify:
   - AI sends helpful reply
   - Owner gets SMS + email with lead details and what they need

### Step 6: Client Handoff
Tell the client:
- "Your number works exactly the same. Calls ring your phone."
- "If you miss a call, the system texts them back automatically from your number."
- "Youll get a text and email alert with their info."
- "They can reply to book or describe what they need."

## Port Timeline
| Step | Time |
|------|------|
| Submit port request | Day 1 |
| Carrier verification | 1-3 days |
| Port completes | 7-14 days |
| Number live on Twilio | Same day as port |

During the port, their number keeps working normally on their current carrier.

## Cost Per Client
| Item | Cost |
|------|------|
| Twilio number (ported or new) | $1.15/mo |
| SMS (~50 texts/mo) | $0.40/mo |
| Voice minutes (~20 calls/mo) | $0.44/mo |
| OpenAI (~50 AI calls/mo) | $0.25/mo |
| **Total** | **~$2.25/mo** |

## Pricing
- Setup: $1,000-$1,500 (includes port handling)
- Retainer: $99-$149/mo
- Margin: ~98%

## Sales Script
"How many calls do you miss each week?"
(They say 5-10)
"What if 3 of those became customers? Thats what this does."
"We port your number to our system. Everything looks the same to your customers. Calls still ring your phone. But when you miss one, they get a text back automatically from your number. Most businesses see 20-30% of missed calls convert to booked jobs."
