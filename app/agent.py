
from app.catalog_service import CatalogService
from app.llm import GeminiLLM
from app.retriever import Retriever
from app.context_builder import ContextBuilder
from app.planner import Planner

class SHLAgent:
    """
    Executes actions selected by the planner.
    """

    def chat(self, messages):
        """
        Main entry point for the stateless SHL agent.
        """

        # -----------------------------
        # Build context from history
        # -----------------------------
        builder = ContextBuilder()

        context = builder.build(messages)

        # -----------------------------
        # Convert conversation to text
        # -----------------------------
        conversation = ""

        for message in messages:
            conversation += f"{message.role}: {message.content}\n"

        # -----------------------------
        # Ask planner what to do
        # -----------------------------
        planner = Planner()

        decision = planner.plan(
            conversation=conversation,
            context=context
        )

        print("\n========== PLANNER ==========")
        print(decision)
        print("=============================\n")

        action = decision.get("action", "clarify")

        # -----------------------------
        # Execute action
        # -----------------------------
        return self.run(
            action=action,
            context=context
        )

    def build_recommendation_prompt(
            self,
            query,
            assessments,
            additions=None,
            removals=None
    ):
        """
        Build a prompt for Gemini using the retrieved SHL assessments.
        """

        if additions is None:
            additions = []

        if removals is None:
            removals = []

        prompt = f"""
        You are an SHL Assessment Consultant.

        Your job is to recommend SHL assessments ONLY from the retrieved assessments below.

        Rules:

        - Recommend ONLY assessments present in the retrieved list.
        - Never invent assessment names.
        - Never invent URLs.
        - Never recommend assessments outside the retrieved catalog.
        - Choose between 1 and 5 assessments.
        - Rank them from best to least suitable.
        - If additional requirements exist, update the recommendation instead of starting over.
        - If removal requirements exist, avoid those assessments.
        - Keep the response concise and professional.

        Recruiter Request:

        {query}

        Additional Requirements:

        {", ".join(additions) if additions else "None"}

        Requirements to Remove:

        {", ".join(removals) if removals else "None"}

        Retrieved SHL Assessments:

        """

        for i, item in enumerate(assessments, start=1):
            prompt += f"""
    Assessment {i}

    Name: {item.get('name')}
    Duration: {item.get('duration')}
    Job Levels: {item.get('job_levels')}
    Remote: {item.get('remote')}
    Description:
    {item.get('description')}

    """

        prompt += """
        Return ONLY valid JSON.

        Use this exact schema:

        {
          "reply": "<professional explanation>",
          "selected_assessments": [
              "<assessment name>",
              "<assessment name>"
          ]
        }

        Rules:

        - reply should explain the recommendations.
        - selected_assessments must contain between 1 and 5 assessment names.
        - Every assessment name MUST exactly match one of the retrieved assessments.
        - Do NOT invent assessment names.
        - Do NOT include URLs.
        - Return ONLY JSON.
        """

        return prompt
    def __init__(self):

        self.retriever = Retriever()
        self.llm = GeminiLLM()
        self.catalog = CatalogService()

    def run(self, action: str, context: dict):
        """
        Execute the action selected by the planner.
        """

        if action == "clarify":
            return self._clarify(context)

        elif action in ["recommend", "refine"]:
            return self._recommend(context)

        elif action == "compare":
            return self._compare(context)

        elif action == "refuse":
            return self._refuse()

        return {
            "reply": "I couldn't understand your request.",
            "recommendations": [],
            "end_of_conversation": False
        }

    def _clarify(self, context):
        """
        Ask exactly ONE clarification question.
        """

        # 1. Missing role
        if not context.get("role"):
            question = "What role are you hiring for?"

        # 2. Missing seniority
        elif not context.get("seniority"):
            question = (
                "What seniority level is the role "
                "(Entry, Mid, Senior, Executive)?"
            )

        # 3. Missing purpose
        elif not context.get("purpose"):
            question = (
                "Is this assessment for selection, "
                "development, or reskilling?"
            )

        # 4. Missing skills
        elif len(context.get("skills", [])) == 0:
            question = (
                "What are the key skills or competencies "
                "required for this role?"
            )

        else:
            question = (
                "Could you provide a little more information "
                "about your hiring requirements?"
            )

        return {
            "reply": question,
            "recommendations": [],
            "end_of_conversation": False
        }

    def _recommend(self, context):
        """
        Retrieve assessments and let Gemini choose the best ones.
        """

        search_query = context.get("search_query", "")

        additions = context.get("additions", [])
        removals = context.get("removals", [])
        # Improve the search query with refinement requirements
        if additions:
            search_query += " " + " ".join(additions)

        if removals:
            search_query += " excluding " + " ".join(removals)

        if not search_query:
            return {
                "reply": "I need more information before recommending assessments.",
                "recommendations": [],
                "end_of_conversation": False
            }

        # Retrieve top matches from FAISS
        results = self.retriever.search(
            search_query,
            top_k=10
        )

        # Build prompt for Gemini
        prompt = self.build_recommendation_prompt(
            query=search_query,
            assessments=results,
            additions=additions,
            removals=removals
        )

        # Ask Gemini
        import json

        # Ask Gemini
        response = self.llm.generate(prompt)

        # Remove markdown if Gemini returns ```json
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        try:
            llm_output = json.loads(response)

        except Exception:
            llm_output = {
                "reply": response,
                "selected_assessments": []
            }

        # Structured results for frontend/API
        recommendations = []

        selected = llm_output.get("selected_assessments", [])

        recommendations = []

        for name in selected:

            for item in results:

                if item.get("name") == name:
                    recommendations.append({
                        "name": item.get("name"),
                        "url": item.get("link"),
                        "duration": item.get("duration"),
                        "remote": item.get("remote"),
                        "job_levels": item.get("job_levels")
                    })

                    break

        return {
            "reply": llm_output.get("reply", ""),
            "recommendations": recommendations,
            "end_of_conversation": True
        }
    def _compare(self, context):
        """
        Compare two SHL assessments.
        """

        assessment_1 = context.get("assessment_1")
        assessment_2 = context.get("assessment_2")

        if not assessment_1 or not assessment_2:
            return {
                "reply": (
                    "Please tell me which two SHL assessments "
                    "you would like to compare."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        first = self.catalog.search_by_name(assessment_1)
        second = self.catalog.search_by_name(assessment_2)

        if not first or not second:
            return {
                "reply": (
                    "I couldn't find one or both assessments "
                    "in the SHL catalog."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        first = first[0]
        second = second[0]

        reply = f"""
        Comparison of SHL Assessments

        1. {first['name']}
        • Duration : {first.get('duration')}
        • Type : {first.get('keys')}

        2. {second['name']}
        • Duration : {second.get('duration')}
        • Type : {second.get('keys')}

        Both assessments measure different aspects and can be
        used together depending on your hiring requirements.
        """

        return {
            "reply": reply.strip(),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------------------------------

    def _refuse(self):
        """
        Handle out-of-scope requests.
        """

        return {
            "reply": (
                "I can only help with SHL assessment recommendations "
                "and comparisons. I can't assist with general hiring, "
                "legal advice, or unrelated questions."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

def main():

    agent = SHLAgent()

    context = {
        "search_query": "Java Developer Spring SQL"
    }

    result = agent.run("recommend", context)

    print(result)


if __name__ == "__main__":
    main()