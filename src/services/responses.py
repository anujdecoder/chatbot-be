import random

messages = {
    "strategy": [
        "Let's discuss your go-to-market strategy!",
        "How are we aligning the marketing strategy with sales?",
        "What are the key components of your GTM plan?",
        "Ready to refine your go-to-market approach?"
    ],
    "execution": [
        "How is the execution of the GTM plan going?",
        "Are there any roadblocks in implementing the GTM strategy?",
        "Let’s review the progress of the GTM rollout.",
        "How can we ensure effective execution of your GTM tactics?"
    ],
    "metrics": [
        "What metrics are you tracking for GTM success?",
        "How are we measuring the effectiveness of the GTM strategy?",
        "Let’s dive into the key performance indicators for your GTM plan.",
        "Are the GTM metrics aligned with your business goals?"
    ],
    "feedback": [
        "What feedback have you received from the market so far?",
        "How is the market responding to your GTM initiatives?",
        "Let’s analyze the feedback to improve the GTM approach.",
        "Are there any adjustments needed based on recent feedback?"
    ]
}
keys = [
    "strategy",
    "execution",
    "metrics",
    "feedback",
]


def generate_response(body: str):
    for k in messages.keys():
        if body.find(k) != -1:
            return random.choice(messages[k])

    return random.choice(messages[random.choice(keys)])
