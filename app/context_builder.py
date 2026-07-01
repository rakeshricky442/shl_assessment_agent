import re


class ContextBuilder:
    """
    Builds conversation context from the complete message history.
    The API is stateless, so we rebuild context on every request.
    """

    def build(self, messages):

        context = {
            "role": None,
            "seniority": None,
            "purpose": None,
            "skills": [],
            "assessment_1": None,
            "assessment_2": None,
            "search_query": "",
            "additions": [],
            "removals": []
        }

        # Join all user messages
        conversation = ""

        for message in messages:

            if message.role == "user":

                text = message.content
                conversation += text + "\n"

                lower = text.lower()

                # -------------------------
                # Purpose
                # -------------------------

                if "hire" in lower or "hiring" in lower:
                    context["purpose"] = "Hiring"

                elif "development" in lower:
                    context["purpose"] = "Development"

                elif "reskill" in lower:
                    context["purpose"] = "Reskilling"

                # -------------------------
                # Seniority
                # -------------------------

                if "graduate" in lower:
                    context["seniority"] = "Graduate"

                elif "entry" in lower:
                    context["seniority"] = "Entry-Level"

                elif "mid" in lower:
                    context["seniority"] = "Mid-Level"

                elif "senior" in lower:
                    context["seniority"] = "Senior"

                elif "executive" in lower:
                    context["seniority"] = "Executive"

                # -------------------------
                # Role
                # -------------------------

                if "java" in lower:
                    context["role"] = "Java Developer"

                elif "python" in lower:
                    context["role"] = "Python Developer"

                elif "excel" in lower:
                    context["role"] = "Office Administrator"

                elif "sales" in lower:
                    context["role"] = "Sales"

                elif "manager" in lower:
                    context["role"] = "Manager"

                elif "data analyst" in lower:
                    context["role"] = "Data Analyst"

                # -------------------------
                # Skills
                # -------------------------

                skills = [
                    "java",
                    "spring",
                    "spring boot",
                    "mysql",
                    "sql",
                    "rest",
                    "rest api",
                    "microservices",
                    "aws",
                    "gcp",
                    "docker",
                    "kubernetes",
                    "node.js",
                    "node",
                    "python"
                ]

                for skill in skills:

                    if skill in lower and skill.upper() not in context["skills"]:

                        context["skills"].append(skill.upper())

        context["search_query"] = conversation.strip()

        # -------------------------
        # Refinements
        # -------------------------

        if "personality" in lower:
            context["additions"].append("Personality")

        if "ability" in lower:
            context["additions"].append("Ability")

        if "cognitive" in lower:
            context["additions"].append("Cognitive Ability")

        if "leadership" in lower:
            context["additions"].append("Leadership")

        if "remove java" in lower:
            context["removals"].append("Java")

        if "remove personality" in lower:
            context["removals"].append("Personality")

        return context