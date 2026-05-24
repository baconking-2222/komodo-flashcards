"""Komodo 'Word of the week' vocabulary + activity tagging.

These lists match the vocabulary exported by Komodo engineering for the rest of
the product, so the flash cards reinforce the same language students see in
their assemblies, dashboards, and lessons.

  - PRIMARY_WORDS:   for primary-school (5–12) cohorts
  - SECONDARY_WORDS: for secondary-school (13–18) cohorts
  - ACTIVITY_WORDS:  per-activity mapping {primary, secondary}

Tooltip definitions come straight from the curriculum copy.
"""

from __future__ import annotations


PRIMARY_WORDS: dict[str, str] = {
    "Active": (
        "Active means being busy and moving around. It’s about playing games, "
        "running, jumping, or doing anything that keeps your body moving and "
        "strong. Being active helps you feel good and gives you energy."
    ),
    "Balance": (
        "Balance means making sure you have time for all the important things "
        "in life — school, rest, fun, and friends. Just like a bike needs both "
        "wheels to move, you need balance to feel happy and healthy."
    ),
    "Be Proud": (
        "Be proud of what you do, even small things. Every step forward is "
        "something to celebrate."
    ),
    "Be Yourself": (
        "Being yourself means being proud of who you are. You are special just "
        "the way you are."
    ),
    "Brave": (
        "Brave is when you do something that feels a little scary, like trying "
        "something new or speaking in front of the class."
    ),
    "Caring": (
        "Caring means looking after yourself and others. Caring can be "
        "helping, listening, or being gentle with people and things."
    ),
    "Confidence": (
        "Confidence is believing in yourself and your abilities. It’s about "
        "trusting that you can do things, even if you face challenges or make "
        "mistakes."
    ),
    "Cooperation": (
        "Cooperation is when people work together to do something. It’s about "
        "helping each other and sharing ideas to reach a goal."
    ),
    "Courage": (
        "Courage is not about being fearless, but about doing something even "
        "when you’re afraid."
    ),
    "Creativity": (
        "Creativity is using your imagination to come up with new ideas or "
        "make something special. It’s about thinking in fun and different ways."
    ),
    "Curious": (
        "Being curious means wanting to learn new things and ask questions. "
        "It’s like being excited to find out how something works."
    ),
    "Digital balance": (
        "Digital balance means spending the right amount of time on screens, "
        "without it taking up too much of your day. Balance screen time with "
        "other activities to feel more focused and happy."
    ),
    "Empathy": (
        "Empathy is when you imagine how someone else is feeling, like "
        "stepping into their shoes to understand them better."
    ),
    "Enjoyment": (
        "Enjoyment is feeling happiness and fun when you do something you "
        "love. Enjoying the moment helps you feel positive and relaxed."
    ),
    "Explore": (
        "To explore means to try new things or look at something carefully to "
        "learn more about it. It’s like being a detective or an adventurer."
    ),
    "Fairness": (
        "Fairness means treating everyone the same and making sure everyone "
        "has a chance. It’s about playing by the rules, sharing, and being "
        "honest with others."
    ),
    "Family": (
        "Family is a group of people who love and care for each other. They "
        "give you love, care, and a sense of belonging."
    ),
    "Feeling Safe": (
        "Safe means feeling protected and not worried. Safe places and people "
        "help us feel comfortable and happy."
    ),
    "Focus": (
        "Focus means paying attention and staying on track with what you’re "
        "doing, whether it’s learning, playing, or working on a task."
    ),
    "Friendly": (
        "Being friendly means being nice, smiling, and talking to others in a "
        "happy way."
    ),
    "Happiness": (
        "Happiness is when you feel good and joyful. It’s the feeling you get "
        "when you enjoy something or when something makes you smile."
    ),
    "Health": (
        "Health means taking care of your body and mind by eating good food, "
        "staying active, resting, and staying happy."
    ),
    "Honesty": (
        "Honesty means telling the truth and being real with yourself and "
        "others. When you're honest, people can trust you."
    ),
    "Include": (
        "To include means to make sure everyone is part of the group or "
        "activity. Including others makes everyone feel happy and welcome."
    ),
    "Joy": (
        "Joy is a feeling of happiness and excitement. You can find joy in "
        "little things, like laughing with friends or doing something you love."
    ),
    "Kindness": (
        "Kindness means being friendly, caring, and helpful to others. Even "
        "small acts can make a big difference and brighten someone’s day."
    ),
    "Laugh": (
        "Laughing makes you feel happy and spreads joy to others. A good "
        "laugh can make a bad day better."
    ),
    "Learning": (
        "Learning means finding out new things, practicing skills, and growing "
        "your knowledge. It happens when you listen, try, and ask questions."
    ),
    "Love": (
        "Love helps you build strong, happy relationships with others. It "
        "makes you feel good inside and spreads kindness."
    ),
    "Make good choices": (
        "Good choices help you and others feel happy and safe. Thinking before "
        "you act helps you make the best choice."
    ),
    "Mindfulness": (
        "Being mindful means paying attention to what’s happening right now, "
        "like how you feel or what you’re doing. It helps you feel calm."
    ),
    "Notice your breath": (
        "When you notice your breath, it helps you feel calm and focused. "
        "It’s a simple way to relax when you feel upset or need a break."
    ),
    "Notice your emotions": (
        "Noticing your emotions means paying attention to how you’re feeling "
        "inside. It helps you feel more in control and know what you need."
    ),
    "Open-minded": (
        "Being open-minded means being willing to listen to new ideas and try "
        "things that are different."
    ),
    "Patience": (
        "Patience means waiting calmly when things don’t happen right away."
    ),
    "Playfulness": (
        "Playfulness means being lighthearted and having fun. It’s about "
        "enjoying yourself and not taking things too seriously."
    ),
    "Positive thinking": (
        "Positive thinking is about looking for the good in things, even when "
        "things don’t go as planned. It helps you stay calm and look for "
        "solutions."
    ),
    "Practice": (
        "Practicing helps you improve and reach your goals, even if things "
        "feel hard at first. The more you practice, the more confident you "
        "become."
    ),
    "Purpose": (
        "Purpose means having a reason for doing something. It’s knowing what "
        "you want to do or why something is important to you."
    ),
    "Reflect": (
        "Reflect means thinking about your feelings, actions, and experiences. "
        "Reflection helps you understand yourself better and learn from your "
        "experiences."
    ),
    "Relax": (
        "Relax means taking a break and resting your body and mind. It gives "
        "your brain and body a chance to recharge."
    ),
    "Respect": (
        "Respect means treating people, places, and things with kindness and "
        "care. It’s about listening, using kind words, and valuing others’ "
        "feelings and opinions."
    ),
    "Screen time limits": (
        "Screen time limits are rules that help you know how much time you "
        "should spend on devices each day. Setting limits helps you make time "
        "for other important things."
    ),
    "Sharing": (
        "Sharing means giving others a chance to enjoy something you have. "
        "It builds trust and kindness."
    ),
    "Sleep habits": (
        "Sleep habits are the things that help you sleep better — going to "
        "bed on time, a cosy room, and no screens before bed."
    ),
    "Speaking up": (
        "Speaking up means sharing your thoughts or feelings when something "
        "is important to you."
    ),
    "Strengths": (
        "Strengths are the things you’re really good at. Everyone has "
        "different strengths that make them special."
    ),
    "Support": (
        "Support means helping someone feel safe, strong, and happy. You can "
        "support a friend by cheering them on, listening, or just being there."
    ),
    "Teamwork": (
        "Teamwork means working together and helping each other. When we "
        "work as a team, we can do amazing things."
    ),
    "Trust": (
        "Trust means believing in someone and knowing they will be honest and "
        "kind. When you trust someone, you feel safe and supported."
    ),
    "Try again": (
        "Trying again means not giving up, even if something is difficult. "
        "When you keep trying, you get better."
    ),
}


SECONDARY_WORDS: dict[str, str] = {
    "Acceptance": (
        "Acceptance means embracing your thoughts, feelings, and experiences "
        "as they are, without judgment. It’s about acknowledging things you "
        "can’t change and focusing on what you can control."
    ),
    "Accountability": (
        "Accountability means being responsible for your actions, choices, "
        "and behaviours. Taking accountability helps build trust and "
        "personal growth."
    ),
    "Achievement": (
        "Achievement is reaching a goal or completing something you’ve worked "
        "hard for. Celebrating achievements boosts self-esteem and keeps you "
        "motivated."
    ),
    "Assertiveness": (
        "Assertiveness means standing up for yourself and expressing your "
        "thoughts, feelings, and needs in a clear, honest, and respectful way."
    ),
    "Balance": (
        "Balance refers to managing different aspects of your life — school, "
        "social life, family, and self-care — so that none of them overwhelms "
        "you."
    ),
    "Being your authentic self": (
        "Authenticity means being true to yourself and not pretending to be "
        "someone you’re not. It builds confidence and helps you connect with "
        "others genuinely."
    ),
    "Beliefs": (
        "Beliefs are the things you think are true or important. They are "
        "ideas or values that guide how you act and make decisions."
    ),
    "Belonging": (
        "Belonging means feeling like you are part of a group or community, "
        "where you are accepted and valued for who you are."
    ),
    "Body positivity": (
        "Body positivity is about accepting and loving your body just the way "
        "it is, focusing on what your body can do and how it supports you."
    ),
    "Boundaries": (
        "Boundaries are limits you set to protect your time, energy, and "
        "well-being. They help you maintain healthy relationships and "
        "prioritise self-care."
    ),
    "Collaboration": (
        "Collaboration means working together as a team to achieve a goal. "
        "Working together builds stronger relationships and helps everyone "
        "grow."
    ),
    "Commitment": (
        "Commitment is dedicating yourself to a goal, task, or relationship, "
        "and sticking with it even when challenges arise."
    ),
    "Community": (
        "Community means the people around you — friends, family, and "
        "neighbours — who help and support each other."
    ),
    "Connection": (
        "Connection means feeling close to others and building relationships. "
        "It’s about sharing, listening, and supporting each other."
    ),
    "Courage": (
        "Courage is the ability to face fear, uncertainty, or challenges even "
        "when you feel scared or unsure."
    ),
    "Create Wellbeing Habits": (
        "Well-being habits are healthy behaviours you repeat regularly. They "
        "help you achieve your goals and improve your life."
    ),
    "Curiosity": (
        "Curiosity means wanting to learn, explore, and ask questions about "
        "the world around you. Curiosity opens up new opportunities for "
        "personal growth."
    ),
    "Digital consumption": (
        "Digital consumption is how much time you spend using devices and "
        "the kind of content you absorb. Mindful consumption protects your "
        "mood and focus."
    ),
    "Digital detox": (
        "A digital detox involves taking time away from screens and social "
        "media to recharge and focus on offline life."
    ),
    "Emotion regulation": (
        "Emotion regulation is about managing your emotions in a healthy "
        "way. It helps you handle stress, difficult emotions, and conflicts."
    ),
    "Empathy": (
        "Empathy is the ability to understand and share the feelings of "
        "others. It strengthens relationships and builds trust."
    ),
    "Encouragement": (
        "Encouragement is giving yourself or someone else a boost of "
        "confidence. It supports growth and boosts self-esteem."
    ),
    "Flexibility": (
        "Flexibility means being adaptable to change, willing to adjust your "
        "plans or mindset when necessary."
    ),
    "Focus": (
        "Focus is the ability to concentrate on one task or goal without "
        "distractions. It improves learning and reduces stress."
    ),
    "Forgiveness": (
        "Forgiveness is letting go of anger or hurt when someone makes a "
        "mistake. It helps you move forward with a lighter heart."
    ),
    "Generosity": (
        "Generosity means giving without expecting anything in return — "
        "your time, things, or help."
    ),
    "Goals": (
        "Goals are things you want to achieve or accomplish. Setting goals "
        "helps you stay focused and motivated."
    ),
    "Gratitude": (
        "Gratitude is the practice of being thankful for what you have, big "
        "or small. It creates happiness and contentment."
    ),
    "Growth Mindset": (
        "A growth mindset is the belief that you can improve through "
        "practice, effort, and learning from mistakes."
    ),
    "Happiness": (
        "Happiness is the state of feeling content and positive — enjoying "
        "life’s good moments, big or small."
    ),
    "Health": (
        "Health means taking care of your body and mind so you feel good and "
        "strong: nutritious food, activity, rest, and managed stress."
    ),
    "Inclusion": (
        "Inclusion means making sure everyone feels welcome and part of the "
        "group. It promotes belonging and a supportive community."
    ),
    "Independence": (
        "Independence means being able to do things on your own and make "
        "your own choices. It builds confidence and self-sufficiency."
    ),
    "Integrity": (
        "Integrity means doing the right thing, even when no one is "
        "watching. It builds trust and respect."
    ),
    "Kindness": (
        "Kindness is being friendly, caring, and helpful to others — and "
        "yourself. It strengthens relationships and creates positive "
        "environments."
    ),
    "Mindfulness": (
        "Mindfulness is the practice of being fully present and paying "
        "attention to the moment, without worrying about the past or future."
    ),
    "Motivation": (
        "Motivation is the drive that pushes you to do something, even when "
        "it’s tough. It can come from within or from outside."
    ),
    "Online boundaries": (
        "Online boundaries are the limits you set for yourself in the "
        "digital world to protect your time, energy, and mental health."
    ),
    "Optimism": (
        "Optimism is the belief that good things are possible. It boosts "
        "resilience and overall well-being."
    ),
    "Patience": (
        "Patience means staying calm when you have to wait for something. "
        "Good things take time."
    ),
    "Perseverance": (
        "Perseverance means not giving up, even when things are tough. "
        "Continuing to try, even if it takes time or is hard."
    ),
    "Perspective taking": (
        "Perspective-taking is the ability to understand a situation from "
        "someone else’s point of view. It fosters empathy and reduces "
        "conflict."
    ),
    "Reflection": (
        "Reflection is thinking about your experiences, actions, and "
        "feelings to learn more about yourself."
    ),
    "Resilience": (
        "Resilience means being able to bounce back after tough times. "
        "Staying strong, learning from challenges, and believing you can "
        "keep going."
    ),
    "Resistance": (
        "Resistance is when you try to stop something from happening or "
        "avoid doing something. Sometimes protective, sometimes it slows "
        "growth."
    ),
    "Responsibility": (
        "Responsibility means taking care of your duties and making good "
        "choices. It builds trust and independence."
    ),
    "Self care": (
        "Self-care means taking care of your body and mind by doing "
        "activities that help you relax and recharge."
    ),
    "Self esteem": (
        "Self-esteem is how you view yourself and your abilities — your "
        "worth, strengths, and confidence to face challenges."
    ),
    "Self respect": (
        "Self-respect means valuing yourself and treating yourself with "
        "dignity, even when things are difficult."
    ),
    "Self-awareness": (
        "Self-awareness is understanding your emotions, thoughts, and "
        "behaviours. It helps you make more informed decisions and improve "
        "relationships."
    ),
    "Self-compassion": (
        "Self-compassion is being gentle with yourself when things don’t go "
        "as planned, treating yourself with kindness."
    ),
    "Self-discipline": (
        "Self-discipline is the ability to stay focused and make smart "
        "choices, even when distractions are around."
    ),
    "Self-efficacy": (
        "Self-efficacy is your belief in your ability to succeed in "
        "specific situations — the confidence to tackle challenges."
    ),
    "Sleep hygiene": (
        "Sleep hygiene refers to the habits and routines that help you get "
        "a good night’s sleep — regular bedtimes, screen-free wind-down, a "
        "calm environment."
    ),
    "Social Connection": (
        "Social connection is the process of building meaningful "
        "relationships. It provides emotional support and a sense of "
        "belonging."
    ),
    "Tolerance": (
        "Tolerance means respecting and accepting people who are different "
        "from you in culture, opinions, or beliefs."
    ),
    "Validation": (
        "Validation is recognising and acknowledging someone’s feelings, "
        "thoughts, or experiences. It strengthens relationships and builds "
        "trust."
    ),
}


# Activity → relevant words.
# Words chosen to reinforce the curriculum vocabulary that activity uses.
ACTIVITY_WORDS: dict[str, dict[str, tuple[str, ...]]] = {
    "five_senses_checkin": {
        "primary": ("Mindfulness", "Notice your breath", "Notice your emotions", "Focus", "Relax"),
        "secondary": ("Mindfulness", "Self-awareness", "Focus", "Self care"),
    },
    "feeling_scan": {
        "primary": ("Notice your emotions", "Notice your breath", "Mindfulness", "Reflect"),
        "secondary": ("Self-awareness", "Emotion regulation", "Mindfulness", "Reflection"),
    },
    "sensory_stomp_shake": {
        "primary": ("Active", "Notice your breath", "Playfulness", "Health"),
        "secondary": (),
    },
    "what_keeps_me_well": {
        "primary": (),
        "secondary": ("Self care", "Self-awareness", "Self esteem", "Reflection", "Create Wellbeing Habits", "Being your authentic self"),
    },
    "personal_cheerleader": {
        "primary": ("Be Proud", "Be Yourself", "Confidence", "Strengths", "Positive thinking"),
        "secondary": ("Self esteem", "Self-compassion", "Encouragement", "Achievement", "Optimism"),
    },
    "positive_outlook": {
        "primary": ("Positive thinking", "Sharing", "Happiness", "Joy"),
        "secondary": ("Optimism", "Social Connection", "Connection", "Happiness"),
    },
    "highlight_reel": {
        "primary": ("Reflect", "Positive thinking", "Be Proud", "Happiness", "Joy"),
        "secondary": ("Gratitude", "Optimism", "Reflection", "Happiness", "Achievement"),
    },
    "guided_imagery": {
        "primary": (),
        "secondary": ("Mindfulness", "Self care", "Focus", "Self-awareness"),
    },
    "five_finger_breathing": {
        "primary": ("Notice your breath", "Mindfulness", "Focus", "Relax"),
        "secondary": ("Mindfulness", "Focus", "Self care", "Emotion regulation"),
    },
    "gratitude_chain": {
        "primary": ("Sharing", "Kindness", "Joy", "Happiness", "Caring"),
        "secondary": ("Gratitude", "Social Connection", "Kindness", "Happiness"),
    },
    "butterfly_hugs": {
        "primary": ("Notice your breath", "Relax", "Feeling Safe", "Caring"),
        "secondary": ("Self care", "Emotion regulation", "Self-compassion", "Mindfulness"),
    },
    "draw_it_out": {
        "primary": ("Creativity", "Notice your emotions", "Reflect", "Be Yourself"),
        "secondary": (),
    },
    "inner_weather_report": {
        "primary": ("Notice your emotions", "Reflect", "Creativity"),
        "secondary": (),
    },
    "tense_release": {
        "primary": ("Notice your breath", "Relax", "Notice your emotions"),
        "secondary": ("Self care", "Emotion regulation", "Mindfulness"),
    },
    "sensory_scrunch": {
        "primary": ("Active", "Relax", "Focus", "Notice your breath"),
        "secondary": ("Self care", "Emotion regulation", "Focus"),
    },
    "shape_shifting": {
        "primary": ("Playfulness", "Active", "Creativity", "Joy"),
        "secondary": (),
    },
    "appreciation_postits": {
        "primary": (),
        "secondary": ("Kindness", "Empathy", "Encouragement", "Validation", "Social Connection", "Inclusion"),
    },
    "circle_of_safety": {
        "primary": (),
        "secondary": ("Belonging", "Community", "Connection", "Social Connection", "Self-awareness"),
    },
    "tension_tamers": {
        "primary": ("Active", "Notice your breath", "Focus", "Relax"),
        "secondary": (),
    },
    "colour_breathing": {
        "primary": ("Notice your breath", "Relax", "Mindfulness", "Creativity"),
        "secondary": ("Mindfulness", "Focus", "Self care", "Emotion regulation"),
    },
    "body_scan": {
        "primary": ("Mindfulness", "Notice your breath", "Relax", "Focus"),
        "secondary": ("Mindfulness", "Self-awareness", "Self care", "Focus"),
    },
    "mindful_motion": {
        "primary": ("Mindfulness", "Focus", "Notice your breath", "Relax"),
        "secondary": ("Mindfulness", "Focus", "Self care"),
    },
    "mindful_listening_walk": {
        "primary": ("Mindfulness", "Focus", "Curious", "Notice your emotions"),
        "secondary": ("Mindfulness", "Focus", "Curiosity", "Self-awareness"),
    },
}


# ----- Helpers -----

def get_activity_word_pills(activity_id: str, age: str) -> list[dict]:
    """Return [{name, category, description}] for a given activity, filtered
    by which age group applies. Used to render word pills on the presentation
    card with tooltip definitions.

    - age == "Jr"  → only primary words
    - age == "Sr"  → only secondary words
    - age == "All" → both (deduplicated; primary description wins if the same
      word exists in both lists)
    """
    mapping = ACTIVITY_WORDS.get(activity_id, {})
    pills: list[dict] = []
    seen: set[str] = set()

    primary_relevant = age in ("All", "Jr")
    secondary_relevant = age in ("All", "Sr")

    if primary_relevant:
        for w in mapping.get("primary", ()):
            if w in seen:
                continue
            pills.append({
                "name": w,
                "category": "Primary",
                "description": PRIMARY_WORDS.get(w, ""),
            })
            seen.add(w)
    if secondary_relevant:
        for w in mapping.get("secondary", ()):
            if w in seen:
                continue
            pills.append({
                "name": w,
                "category": "Secondary",
                "description": SECONDARY_WORDS.get(w, ""),
            })
            seen.add(w)
    return pills


def get_activity_word_set(activity_id: str) -> set[str]:
    """All word names tagged on this activity (primary + secondary)."""
    m = ACTIVITY_WORDS.get(activity_id, {})
    return set(m.get("primary", ())) | set(m.get("secondary", ()))


def all_words_for_filter() -> list[str]:
    """All unique words referenced by any activity, sorted alphabetically.
    Used to populate the 'Word of the week' sidebar multiselect."""
    out: set[str] = set()
    for d in ACTIVITY_WORDS.values():
        out.update(d.get("primary", ()))
        out.update(d.get("secondary", ()))
    return sorted(out, key=lambda s: s.lower())
