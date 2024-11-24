DEFAULT_GUIDELINE_PROMPT = "Consider the following concept categories:"
GUIDELINE_PROMPT_HUMAN = "The concepts described in this section follow closely the definitions of the International <IR> framework, and should be sufficient to perform the annotation. According to the IR framework, capitals are “stocks of value that are increased, decreased or transformed through the activities and outputs of the organization.” They can be classified in financial, manufactured, intellectual, social and relationship, and human (<IR> framework, section 2C)."
DEFAULT_TASK_PROMPT = "Text: {input}"

CAPITAL_DEFINITION = {
    "Financial": "The pool of funds that is available to an organization for use in the production of goods or the provision of services. It can be obtained through financing or generated through operations and investments. Example: “The discussion also provides information about the financial results of our business segments to provide a better understanding of how those segments and their results affect the financial condition and results of operations of Ameren as a whole.”",
    "Manufactured": "Manufactured physical objects (excluding natural physical objects) that are available to an organization for use in the production of goods or the provision of services, including, buildings, equipment, and infrastructure (such as roads, ports, bridges, etc). Example: “Due to the long lead time for the manufacture, repair, and installation of the components, the energy center is expected to return to service in late June or early July 2021.”",
    "Intellectual": "Organizational, knowledge-based intangibles, including: Intellectual property, such as patents, copyrights, software, rights and licences “Organizational capital” such as tacit knowledge, systems, procedures and protocols. Example: “The absence of revenues from a software licensing agreement with Ameren Missouri decreased margins $5 million.”",
    "Human": "People’s competencies, capabilities and experience, and their motivations to innovate, including their: 1) alignment with and support for an organization’s governance framework, risk management approach, and ethical values; 2) sbility to understand, develop and implement an organization’s strategy; 3) loyalties and motivations for improving processes, goods and services; 4) Other matters related to people management. Example: “As the situation rapidly evolved, we remained focused on safely serving our customers and protecting the health and safety of our employees.”",
    "Social and relationship": "The institutions and the relationships within and between communities, groups of stakeholders and other networks, including: 1) shared norms, and common values and behaviours; 2) key stakeholder relationships, and the trust and willingness to engage that an organization has developed and strives to build and protect with external stakeholders; 3) intangibles associated with the brand and reputation that an organization has developed; 4) an organization’s social licence to operate. Example: “In March 2020, the MoPSC issued an order in Ameren Missouri’s July 2019 electric service regulatory rate review, approving nonunanimous stipulation and agreements.”",
    "Natural": "All renewable and non-renewable environmental resources and processes that provide goods or services that support the past, current or future prosperity of an organization, including air, water, land, minerals, and biodiversity. Example: “These amounts include the 700 MWs of wind generation projects discussed below, which will support Ameren Missouri’s compliance with the state of Missouri’s requirement of achieving 15% of native load sales from renewable energy sources beginning in 2021.”",
}

CAPITAL_DEFINITION_CHATGPT = {
    "Financial": "A sentence that pertains to monetary resources, assets, liabilities, revenues, expenses, or any other financial information related to the company's operations, investments, and financial performance.",
    "Manufactured": "A sentence that refers to physical assets, infrastructure, and tangible resources such as buildings, machinery, equipment, or any other manufactured or constructed items that contribute to the company's value.",
    "Intellectual": "A sentence that relates to intangible assets, knowledge, intellectual property, patents, trademarks, copyrights, research and development activities, or any other intellectual assets that enhance the company's competitiveness and innovation.",
    "Human": "A sentence that involves information about the company's workforce, including employees, skills, expertise, training, recruitment, talent development, and any other human resources aspects that contribute to the company's success.",
    "Social and relationship": "A sentence that deals with the company's relationships and interactions with external stakeholders, communities, customers, suppliers, partners, and any other social or relationship-based assets that affect the company's operations and reputation.",
    "Natural": "A sentence that addresses environmental resources, sustainability efforts, ecological impacts, conservation initiatives, or any other aspects related to the company's use of natural resources and its environmental responsibility.",
}

CAPITAL_EXAMPLES = [
    """Text: The discussion also provides information about the financial results of our business segments to provide a better understanding of how those segments and their results affect the financial condition and results of operations of Ameren as a whole.
Category: Financial""",
    # """Text: We cannot predict the outcome of this inquiry and what effect, if any, it may have on our business, financial condition or results of operations.
    # Category: Financial""",
    # """Text: Due to the long lead time for the manufacture, repair, and installation of the components, the energy center is expected to return to service in late June or early July 2021.
    # Category: Manufactured""",
    """Text: Outside the United States, the company has three large refineries in South Korea, Singapore and Thailand.
Category: Manufactured""",
    """Text: The absence of revenues from a software licensing agreement with Ameren Missouri decreased margins $5 million.
Category: Intellectual""",
    # """Text: HFI expanded its product line from juices to include Hansen’s Natural Soda ® brand sodas.
    # Category: Intellectual""",
    """Text: As the situation rapidly evolved, we remained focused on safely serving our customers and protecting the health and safety of our employees.
Category: Human""",
    # """Text: Our future success will depend, in part, upon our continued ability to develop and introduce different and innovative beverages that appeal to consumers.
    # Category: Human""",
    # """Text: Concessions for producing areas within this basin expire between 2022 and 2035.
    # Category: Social and relationship""",
    """Text: An unfavorable report on the health effects of caffeine, other ingredients in energy drinks or energy drinks generally, or criticism or negative publicity regarding the caffeine content and/or any other ingredients in our products or energy drinks generally, including product safety concerns, could have an adverse effect on our business, financial condition and results of operations.
Category: Social and relationship""",
    """Text: These amounts include the 700 MWs of wind generation projects discussed below, which will support Ameren Missouri’s compliance with the state of Missouri’s requirement of achieving 15% of native load sales from renewable energy sources beginning in 2021.
Category: Natural""",
]

SENTIMENT_DEFINITION = {
    "Positive": 'A sentence is classified as "Positive" when it conveys information or sentiments that are favorable, optimistic, or suggest good prospects for the company. This includes statements about strong financial performance, growth opportunities, positive developments, or any other content that portrays the company in a positive light.',
    "Negative": 'A sentence is classified as "Negative" when it contains information or sentiments that are unfavorable, pessimistic, or indicate challenges or issues facing the company. This may include discussions about poor financial performance, legal troubles, declining market share, or any content that reflects negatively on the company\'s outlook.',
    "Neutral": 'A sentence is classified as "Neutral" when it does not express a clear positive or negative sentiment about the company. These sentences typically contain factual information, statements of fact without emotional bias, or content that is unrelated to the company\'s financial or operational performance.',
}

SENTIMENT_EXAMPLES = [
    """Text: We provide compensation packages designed to attract and retain talent while maintaining alignment with market compensation surveys.
Category: Positive""",
    """Text: In 2020, we experienced a net decrease in our sales volumes, an increase in our accounts receivable balances that were past due or that were a part of a deferred payment arrangement, and a decline in our cash collections from customers.
Category: Negative""",
    """Text: Outside the United States, the company has three large refineries in South Korea, Singapore and Thailand.
Category: Neutral""",
]

ELEMENT_DEFINITION = {
    "Organizational overview": """Question: What does the organization do and what are the circumstances under which it operates?
This content element refers to the organization’s purpose, mission and vision, and provides essential context by identifying matters such as:
- Culture, ethics and values
- Ownership and operating structure
- Principal activities and markets
- Competitive landscape and market positioning
- Key quantitative information (e.g. the number of employees, revenue and number of countries in which the organization operates).""",
    "External environment": """Question: What are the significant factors affecting the external environment under which the organization operates?
These factors include aspects of the legal, commercial, social, environmental, regulatory,  and political context that affect the organization’s ability to create value in the short, medium or long term. They can affect the organization directly or indirectly (e.g. by influencing the availability, quality and affordability of a capital that the organization uses or affects).""",
    "Governance": """Question: How does the organization’s governance structure support its ability to create value in the short, medium and long term?
This aspect provides insight about how the following is linked to the organization’s ability to create value:
- The organization’s leadership structure, including the skills and diversity (e.g. range of backgrounds, gender, competence and experience) of those charged with governance
- Specific processes used to make strategic decisions and to establish and monitor the culture of the organization, including its attitude to risk and mechanisms for addressing integrity and ethical issues
- Particular actions those charged with governance have taken to influence and monitor the strategic direction of the organization and its approach to risk management
- How the organization’s culture, ethics and values are reflected in its use of and effects on the capitals, including its relationships with key stakeholders
- Whether the organization is implementing governance practices that exceed legal requirements
- The responsibility those charged with governance take for promoting and enabling innovation
- How remuneration and incentives are linked to value creation in the short, medium and long term.""",
    "Business model": """Question: What is the organization’s business model?
An organization’s business model is its system of transforming inputs, through its business activities, into outputs and outcomes that aims to fulfil the organization’s strategic purposes and create value over the short, medium and long term.
The business model includes the elements involved in the process of value creation, namely:
- Inputs: the capitals (resources and relationships) that the organization draws upon for its business activities.
- Business activities:
  - How the organization differentiates itself in the market place (e.g. through product differentiation, market segmentation, delivery channels and marketing)
  - The extent to which the business model relies on revenue generation after the initial point of sale (e.g. extended warranty arrangements or network usage charges)
  - How the organization approaches the need to innovate
  - How the business model has been designed to adapt to change.
- Outputs: an organization’s products and services, and any by-products and waste.
- Outcomes: the internal and external consequences (positive and negative) for the capitals as a result of an organization’s business activities and outputs.""",
    "Risks and opportunities": """"Question: What are the specific risks and opportunities that affect the organization’s ability to create value over the short, medium and long term, and how is the organization dealing with them?
This category refers to the key risks and opportunities that are specific to the organization, including those that relate to the organization’s effects on, and the continued availability, quality and affordability of, relevant capitals in the short, medium and long term. 
This can include identifying:
- The specific source of risks and opportunities, which can be internal, external or, commonly, a mix of the two. External sources include those stemming from the external environment. Internal sources include those stemming from the organization’s business activities.
- The organization’s assessment of the likelihood that the risk or opportunity will come to fruition and the magnitude of its effect if it does. This includes consideration of the specific circumstances that would cause the risk or opportunity to come to fruition. Such disclosure will invariably involve a degree of uncertainty.
- The specific steps being taken to mitigate or manage key risks or to create value from key opportunities, including the identification of the associated strategic objectives, strategies, policies, targets and key performance indicators.""",
    "Strategy and resource allocation": """Question: Where does the organization want to go and how does it intend to get there?
This concept identifies:
- The organization’s short, medium and long-term strategic objectives
- The strategies it has in place, or intends to implement, to achieve those strategic objectives
- The resource allocation plans it has to implement its strategy
- How it will measure achievements and target outcomes for the short, medium and long term.""",
    "Performance": """Question: To what extent has the organization achieved its strategic objectives for the period and what are its outcomes in terms of effects on the capitals?
This concept captures qualitative and quantitative information about performance that may include matters such as:
- Quantitative indicators with respect to targets, risks and opportunities, explaining their significance, their implications, and the methods and assumptions used in compiling them
- The organization’s effects (both positive and negative) on the capitals, including material effects on capitals up and down the value chain.""",
    "Outlook": """Question: What challenges and uncertainties is the organization likely to encounter in pursuing its strategy, and what are the potential implications for its business model and future performance?
An integrated report ordinarily highlights anticipated changes over time and provides information, built on sound and transparent analysis, about:
- The organization’s expectations about the external environment the organization is likely to face in the short, medium and long term
- How that will affect the organization
- How the organization is currently equipped to respond to the critical challenges and uncertainties that are likely to arise.""",
    "Basis of reporting and presentation": """Question: How does the organization determine what matters to include in the report and how are such matters quantified or evaluated?
This category captures decisions about materiality, that is, why a given information was deemed relevant to be reported. It can also refers to methods and frameworks used to evaluate the relevance or presentation decisions.""",
    "Non-financial content": """Some content elements do not express relevant financial concepts but will appear frequently in the documents. These categories should 
- Section/subsection title: headings and subheading of the reports.
- Reference: references to other sections in the document.
- Boilerplate: standardized text that is repeated in disclosures often to satisfy reporting regulations.
- Captions and notes:  should be used when it is a clear caption of a table of figure (e.g., “Table 1 - Cash flow in the first semester of 2021”).
- Removed content: tables, figures and other non-textual elements removed during pre-processing.""",
}

ELEMENT_EXAMPLES = [
    """Text: Ameren, headquartered in St. Louis, Missouri, is a public utility holding company whose primary assets are its equity interests in its subsidiaries.
Category: Organizational overview""",
    """Text: ​​In the 1930s, Hubert Hansen and his sons started a business selling fresh non-pasteurized juices in Los Angeles, California.
Category: Organizational overview""",
    """Text: ​The continued effect of the COVID-19 pandemic on our results of operations, financial position, and liquidity in subsequent periods will depend on its severity and longevity, future regulatory or legislative actions with respect thereto, and the resulting impact on business, economic, and capital market conditions.
Category: External environment""",
    """Text: The United Kingdom Government has also suggested that it may review food labeling laws following the United Kingdom’s departure from the European Union (“Brexit”).
Category: External environment""",
    """Text: The amount and timing of dividends payable on Ameren’s common stock are within the sole discretion of Ameren’s board of directors.
Category: Governance""",
    """Text: ​The plan includes a portfolio of customer energy-efficiency programs through December 2022 and low-income customer energy-efficiency programs through December 2024, along with a rider.
Category: Business model""",
    """Text: In 2015, we acquired various energy brands from TCCC and disposed of our non-energy drink business.
Category: Business model""",
    """Text: ​Ameren and Ameren Missouri results are also affected by seasonal fluctuations in winter heating and summer cooling demands, as well as by energy center maintenance outages.
Category: Risks and opportunities""",
    """Text: Ameren is also targeting a 50% CO2 emission reduction by 2030 and an 85% reduction by 2040 from the 2005 level.
Category: Strategy and resource allocation""",
    """Text: Cash flow provided by operating activities for 2020 was a record $1,281.0 million, an increase of $166.6 million or 14.9%, compared with $1,114.4 million in 2019.
Category: Performance""",
    """Text: Due to the long lead time for the manufacture, repair, and installation of the components, the energy center is expected to return to service in late June or early July 2021.
Category: Outlook""",
    """Text: Ameren’s financial statements are prepared on a consolidated basis and therefore include the accounts of its majority-owned subsidiaries.
Category: Basis of reporting and presentation""",
]

GUIDELINES = {
    "capital_human": {
        "prompt": DEFAULT_TASK_PROMPT,
        "definition": CAPITAL_DEFINITION,
        "guideline_prompt": GUIDELINE_PROMPT_HUMAN,
    },
    "capital": {
        "prompt": DEFAULT_TASK_PROMPT,
        "definition": CAPITAL_DEFINITION_CHATGPT,
        "examples": CAPITAL_EXAMPLES,
        "guideline_prompt": DEFAULT_GUIDELINE_PROMPT,
    },
    "sentiment": {
        "prompt": DEFAULT_TASK_PROMPT,
        "definition": SENTIMENT_DEFINITION,
        "examples": SENTIMENT_EXAMPLES,
    },
    "content": {
        "prompt": DEFAULT_TASK_PROMPT,
        "definition": ELEMENT_DEFINITION,
        "examples": ELEMENT_EXAMPLES,
    },
}
