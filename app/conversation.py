# conversation.py

import re


class ConversationState:
    """
    Rebuilds the user's intent from the full conversation history.
    Since the API is stateless, every /chat request contains all messages.
    """

    def __init__(self, messages=None):
        self.messages = messages or []

    def history(self):
        """
        Return conversation as plain text.
        Useful for planner prompts.
        """
        conversation = ""

        for msg in self.messages:
            conversation += (
                f"{msg['role'].capitalize()}: "
                f"{msg['content']}\n"
            )

        return conversation.strip()

    # ---------------------------------------------------------

    def latest_user_message(self):

        for msg in reversed(self.messages):

            if msg["role"] == "user":
                return msg["content"]

        return ""

    # ---------------------------------------------------------

    def get_context(self):
        """
        Extract structured information from the
        complete conversation.

        Planner will use this context.
        """

        context = {
            "role": None,
            "seniority": None,
            "experience": None,
            "purpose": None,
            "skills": [],
            "assessment_1": None,
            "assessment_2": None,
            "compare": False,
            "refine": False,
            "legal": False,
            "off_topic": False
        }

        conversation = self.history().lower()

        # -------------------------------------------------
        # Seniority
        # -------------------------------------------------

        if "entry" in conversation:
            context["seniority"] = "Entry"

        elif "graduate" in conversation:
            context["seniority"] = "Graduate"

        elif "mid" in conversation:
            context["seniority"] = "Mid"

        elif "senior" in conversation:
            context["seniority"] = "Senior"

        elif "director" in conversation:
            context["seniority"] = "Director"

        elif "cxo" in conversation:
            context["seniority"] = "Executive"

        # -------------------------------------------------
        # Experience
        # -------------------------------------------------

        years = re.findall(r"(\d+)\+?\s*years?", conversation)

        if years:
            context["experience"] = years[0]

        # -------------------------------------------------
        # Purpose
        # -------------------------------------------------

        if "selection" in conversation:
            context["purpose"] = "Selection"

        elif "development" in conversation:
            context["purpose"] = "Development"

        elif "reskill" in conversation:
            context["purpose"] = "Reskilling"

        # -------------------------------------------------
        # Skills
        # -------------------------------------------------

        keywords = [
            "java",
            "python",
            "sql",
            "aws",
            "docker",
            "spring",
            "angular",
            "excel",
            "word",
            "networking",
            "linux",
            "customer service",
            "sales",
            "finance",
            "leadership",
            "personality",
            "numerical reasoning"
        ]

        for skill in keywords:

            if skill in conversation:
                context["skills"].append(skill)

        # -------------------------------------------------
        # Role
        # -------------------------------------------------

        roles = [
            "java developer",
            "data analyst",
            "software engineer",
            "full stack engineer",
            "backend engineer",
            "sales",
            "customer service",
            "graduate",
            "financial analyst",
            "contact centre",
            "plant operator",
            "admin assistant"
        ]

        for role in roles:

            if role in conversation:
                context["role"] = role.title()
                break

        # -------------------------------------------------
        # Compare
        # -------------------------------------------------

        if "difference between" in conversation:

            context["compare"] = True

            match = re.search(
                r"difference between (.*?) and (.*)",
                conversation
            )

            if match:

                context["assessment_1"] = match.group(1).strip()
                context["assessment_2"] = match.group(2).strip()

        # -------------------------------------------------
        # Refine
        # -------------------------------------------------

        refine_words = [
            "actually",
            "instead",
            "replace",
            "remove",
            "drop",
            "add",
            "include"
        ]

        if any(word in conversation for word in refine_words):
            context["refine"] = True

        # -------------------------------------------------
        # Legal
        # -------------------------------------------------

        legal_words = [
            "legal",
            "law",
            "hipaa",
            "gdpr",
            "compliance",
            "required by law"
        ]

        if any(word in conversation for word in legal_words):
            context["legal"] = True

        # -------------------------------------------------
        # Off Topic
        # -------------------------------------------------

        off_topic = [
            "salary",
            "interview tips",
            "resume",
            "visa",
            "politics"
        ]

        if any(word in conversation for word in off_topic):
            context["off_topic"] = True

        return context