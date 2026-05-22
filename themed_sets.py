"""Curated themed playlists of activities for specific situations.

Each set is a sequence of activity ids designed to be run together.
Use these in training to walk teachers through a complete 'flow' for a
common classroom scenario (morning regulation, in-the-moment anxiety, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ThemedSet:
    id: str
    name: str
    icon: str  # short emoji or symbol for visual identification
    description: str
    when_to_use: str
    activity_ids: tuple[str, ...]


THEMED_SETS: list[ThemedSet] = [
    ThemedSet(
        id="morning_regulation",
        name="Morning regulation",
        icon="☀️",
        description=(
            "Gentle start-of-day grounding to help students arrive into the classroom calm, "
            "present, and ready to learn."
        ),
        when_to_use="First 10 minutes of the day, or at the start of any new lesson block.",
        activity_ids=(
            "five_senses_checkin",
            "positive_outlook",
            "colour_breathing",
        ),
    ),
    ThemedSet(
        id="anxiety_response",
        name="In-the-moment anxiety",
        icon="🫁",
        description=(
            "Quick, body-based techniques to use when a student (or the whole class) is "
            "showing early signs of stress or overwhelm."
        ),
        when_to_use="Before an exam, after a difficult conversation, or when anxiety is spiking.",
        activity_ids=(
            "butterfly_hugs",
            "five_finger_breathing",
            "colour_breathing",
            "feeling_scan",
        ),
    ),
    ThemedSet(
        id="energy_release",
        name="Energy release / wiggles",
        icon="⚡",
        description=(
            "Physical movement activities to discharge restless energy before students can "
            "settle back into focused work."
        ),
        when_to_use="After lunch, before sustained sitting tasks, or when the room feels restless.",
        activity_ids=(
            "sensory_stomp_shake",
            "tense_release",
            "shape_shifting",
            "tension_tamers",
            "sensory_scrunch",
        ),
    ),
    ThemedSet(
        id="gratitude_connection",
        name="Gratitude & connection",
        icon="💛",
        description=(
            "Builds class culture by surfacing what's going well and acknowledging peers. "
            "Strengthens belonging and positive relationships."
        ),
        when_to_use="Friday afternoon, end of a unit, or when class culture needs a lift.",
        activity_ids=(
            "gratitude_chain",
            "positive_outlook",
            "highlight_reel",
            "appreciation_postits",
        ),
    ),
    ThemedSet(
        id="end_of_day",
        name="End-of-day reflection",
        icon="🌙",
        description=(
            "Help students close the day with intention — naming feelings, noticing wins, "
            "and leaving the classroom in a calm state."
        ),
        when_to_use="Last 10 minutes of the school day or end of week.",
        activity_ids=(
            "highlight_reel",
            "feeling_scan",
            "inner_weather_report",
        ),
    ),
    ThemedSet(
        id="self_worth",
        name="Building self-worth",
        icon="🌱",
        description=(
            "Longer reflective activities that help students articulate their strengths, "
            "supports, and what keeps them well."
        ),
        when_to_use="Pastoral periods, wellbeing weeks, or one-to-one check-ins.",
        activity_ids=(
            "personal_cheerleader",
            "what_keeps_me_well",
            "circle_of_safety",
        ),
    ),
    ThemedSet(
        id="mindfulness_practice",
        name="Mindfulness practice",
        icon="🧘",
        description=(
            "A staircase of formal mindfulness activities — start short and build up to "
            "longer sustained practice over weeks."
        ),
        when_to_use="Weekly mindfulness slot; build the habit progressively across a term.",
        activity_ids=(
            "five_finger_breathing",
            "body_scan",
            "mindful_motion",
            "mindful_listening_walk",
            "guided_imagery",
        ),
    ),
    ThemedSet(
        id="creative_expression",
        name="Creative expression",
        icon="🎨",
        description=(
            "Externalise hard-to-name feelings through art and metaphor. Especially useful "
            "for students who find direct talk difficult."
        ),
        when_to_use="Art lessons, pastoral work, or when discussing emotions feels too direct.",
        activity_ids=(
            "draw_it_out",
            "inner_weather_report",
            "what_keeps_me_well",
        ),
    ),
]


def get_themed_set(set_id: str) -> ThemedSet | None:
    for s in THEMED_SETS:
        if s.id == set_id:
            return s
    return None
