def structure_to_string(data):
    claim_strings = []
    for claim in data:
        claim_str = f"{claim['claim_number']}\n{claim['preamble']}\n"
        for component in claim['components']:
            claim_str += f"  {component['component']}\n"
            for subcomponent in component['subcomponents']:
                claim_str += f"    {subcomponent}\n"
        claim_strings.append(claim_str)
    return "\n".join(claim_strings)

def generate_answers_general(client, abstract, patent_title, claims, questions):
    title_example = "Apparatus for docking a printed circuit board"
    question_example = "What is the essential function of the product or process?"
    answer_example = "The goal is to select and secure the electric circuit board in a designated location."
    question_example1 = "What ingredients, materials, or processes are alternatives that can work in the same way?"
    answer_example1 = "Alternative components may include adjustable brackets, spring clips, guide rails, magnetic strips, or standardized slots or holes."

    initial_messages = [
        {
            "role": "system",
            "content": "You are a patent expert and answer questions according to the doctrine of equivalents in a brief and direct manner in less than one hundred words."
        },
        {
            "role": "user",
            "content": f"{question_example}"
        },
        {
            "role": "assistant",
            "content": f"{answer_example}"
        },
        {
            "role": "user",
            "content": f"{question_example1}"
        },
        {
            "role": "assistant",
            "content": f"{answer_example1}"
        }
    ]

    answers = []
    recent_context = []

    for question in questions:
        messages = initial_messages + recent_context + [
            {
                "role": "user",
                "content": f"The patent title is: {patent_title}. The patent abstract is: {abstract}. These are the claims: {claims}. {question}"
            }
        ]

        payload = {
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.5,
            "top_p": 0.1,
            "presence_penalty": 0.5,
            "frequency_penalty": 0.5
        }

        response = client.complete(payload)
        answer = response.choices[0].message.content
        answers.append(answer)
        
        recent_context.extend([
            {
                "role": "user",
                "content": question
            },
            {
                "role": "assistant",
                "content": answer
            }
        ])

    return answers

def query_patent_general(client, patent, questions):
    claims = patent.claims
    abstract = patent.abstract
    patent_title = patent.title

    answers = generate_answers_general(client, abstract, patent_title, structure_to_string(claims), questions)

    return answers