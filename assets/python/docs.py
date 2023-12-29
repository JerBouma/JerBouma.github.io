"""
This file is used to generate the documentation for the project. It is a very custom file and should not be used as a
template for other projects as it is directly related to the project structure and the way the documentation is
generated.
"""

import requests
import base64
import re


def create_markdown_file(file_url: str, header: str, location: str):
    response = requests.get(file_url)
    data = response.json()

    file_content = base64.b64decode(data["content"]).decode("utf-8")

    functions_with_docstrings = []
    function_matches = re.findall(
        r"def\s+(\w+)\([\s\S]*?\"\"\"([\s\S]*?)\"\"\"", file_content
    )

    if function_matches:
        for match in function_matches:
            function_name, docstring = match

            # Description
            description_match = re.match(
                r"([\s\S]*?)(?:Args:|As an example:|$)", docstring, re.DOTALL
            )
            description = description_match.group(1) if description_match else ""
            description = re.sub(
                r"(https?://\S+)", r'[\1](\1){:target="_blank"}', description
            )

            # Arguments
            arguments_match = re.search(
                r"(Args:[\s\S]*?)(```python|$)", docstring, re.DOTALL
            )
            arguments = arguments_match.group(1) if arguments_match else ""
            arguments = re.sub(
                r"(https?://\S+)", r'[\1](\1){:target="_blank"}', arguments
            )

            # Define the regular expression pattern
            pattern = re.compile(r"\w+ \([^)]+\):")

            # Function to replace matches with <u>...</u>
            def replace_match(match):
                return f"- <u>{match.group(0)}</u>"

            # Use the pattern with re.sub to replace matches
            arguments = pattern.sub(replace_match, arguments)

            # Extract example code block
            example_code_match = re.search(
                r"```python([\s\S]*?)```", docstring, re.DOTALL
            )
            example_code = example_code_match.group(1) if example_code_match else ""

            # Extract example result
            example_result_match = re.search(
                r"Which returns:[\s\S]*$", docstring, re.DOTALL
            )
            example_result = (
                example_result_match.group(0) if example_result_match else ""
            )

            functions_with_docstrings.append(
                {
                    "function_name": function_name,
                    "description": re.sub(" +", " ", description.strip())
                    .replace("\n ", " ")
                    .replace("\n ", "\n\n")
                    .replace("-", "\n-"),
                    "arguments": re.sub(" +", " ", arguments.strip()),
                    "example_code": re.sub(" +", " ", example_code.strip()).replace(
                        "\n ", "\n"
                    ),
                    "example_result": re.sub(" +", " ", example_result.strip()),
                }
            )

    markdown_content = header

    for function_info in functions_with_docstrings:
        markdown_content += f'## {function_info["function_name"]}\n'
        markdown_content += f'{function_info["description"]}\n\n'

        if function_info["arguments"]:
            markdown_content += (function_info["arguments"]).replace(
                "Args:", "**Args:**").replace("Raises:", "**Raises:**").replace("Returns:", "**Returns:**").replace("Notes:", "**Notes:**")
            markdown_content += "\n"

        if function_info["example_code"]:
            markdown_content += "{% include code_header.html %}\n"
            markdown_content += "{% highlight python %}\n"
            markdown_content += function_info["example_code"]
            markdown_content += "\n{% endhighlight %}\n\n"

        if function_info["example_result"]:
            example_result = (
                function_info["example_result"].replace("Which returns:", "").strip()
            )
            markdown_content += f"\nWhich returns:\n\n{example_result}\n\n"

    # Save to a file
    with open(location, "w", encoding="utf-8") as file:
        file.write(markdown_content)


# Create Docs page
markdown_content = """---
title: Docs
excerpt: This the documentation of the FinanceToolkit. This is an open-source toolkit in which 100+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method.
description: This the documentation of the FinanceToolkit. This is an open-source toolkit in which 100+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method.
author_profile: false
permalink: /projects/financetoolkit/docs
classes: wide-sidebar
layout: single
redirect_from:
- /docs
sidebar:
    nav: "financetoolkit-docs"
---

This page includes all the documentation for the Finance Toolkit,an open-source toolkit in which all relevant financial ratios (150+), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. Each functionality includes an example of how to use it and is therefore an excellent way to better understand how to use each functionality. These examples are also directly embedded in the code. For simplicity sake, only the controller modules are included here given that the models themselves should be relatively straightforward. Make sure to also have a look at the example notebooks as found [here](/projects/financetoolkit#how-to-guides-for-the-financetoolkit).

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

The Toolkit Module is meant to be a collection of useful functions that collect and parse data. These is historical data, fundamental data (balance, income and cash flow statements) as well as several others metrics from Financial Modeling Prep like enterprise values, company profiles and more. From this module, you are able to access the related modules as well.

If you are looking for documentation regarding the ratios, technical indicators, models, risk metrics and performance metrics, please have a look below:

<div style="display: flex; justify-content: space-between;">
    <a href="/projects/financetoolkit/docs" class="btn btn--warning" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>


{% include algolia.html %}

"""

create_markdown_file(
    file_url="https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/toolkit_controller.py",
    header=markdown_content,
    location="_pages/financetoolkit/documentation/docs.md",
)

# Create the Ratios page
markdown_content = """---
title: Ratios
excerpt: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
description: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/ratios
classes: wide-sidebar
layout: single
redirect_from:
    - /ratios
sidebar:
    nav: "financetoolkit-docs-ratios"
---

The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, models, technicals, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--warning" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

"""

create_markdown_file(
    file_url="https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/ratios/ratios_controller.py",
    header=markdown_content,
    location="_pages/financetoolkit/documentation/ratios.md",
)

# Create Models page
markdown_content = """---
title: Models
excerpt: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
description: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/models
classes: wide-sidebar
layout: single
redirect_from:
    - /models
sidebar:
    nav: "financetoolkit-docs-models"
---

The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, ratios, technicals, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--warning" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

"""

create_markdown_file(
    file_url="https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/models/models_controller.py",
    header=markdown_content,
    location="_pages/financetoolkit/documentation/models.md",
)

# Create the Technicals page
markdown_content = """---
title: Technicals
excerpt: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
description: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/technicals
classes: wide-sidebar
layout: single
redirect_from:
    - /technicals
sidebar:
    nav: "financetoolkit-docs-technicals"
---

The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, ratios, models, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--warning" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

"""

create_markdown_file(
    file_url="https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/technical/technicals_controller.py",
    header=markdown_content,
    location="_pages/financetoolkit/documentation/technicals.md",
)

# Create the Risk page
markdown_content = """---
title: Risk
excerpt: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
description: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
author_profile: false
permalink: /projects/financetoolkit/docs/risk
classes: wide-sidebar
layout: single
redirect_from:
    - /ratios
sidebar:
    nav: "financetoolkit-docs-risk"
---
The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, ratios, models, technicals, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--warning" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

"""

create_markdown_file(
    file_url="https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/risk/risk_controller.py",
    header=markdown_content,
    location="_pages/financetoolkit/documentation/risk.md",
)

# Create the Performance page
markdown_content = """---
title: Performance
excerpt: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
description: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
author_profile: false
permalink: /projects/financetoolkit/docs/performance
classes: wide-sidebar
layout: single
redirect_from:
    - /ratios
sidebar:
    nav: "financetoolkit-docs-performance"
---
The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, ratios, models, technicals, risk and economics, please have a look below:

<div style="display: flex; justify-content: space-between;">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--warning" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

"""

create_markdown_file(
    file_url="https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/performance/performance_controller.py",
    header=markdown_content,
    location="_pages/financetoolkit/documentation/performance.md",
)

# Create the Economics page
markdown_content = """---
title: Economics
excerpt: The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.
description: The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.
author_profile: false
permalink: /projects/financetoolkit/docs/economics
classes: wide-sidebar
layout: single
redirect_from:
    - /economics
sidebar:
    nav: "financetoolkit-docs-economics"
---

The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, models, ratios, technicals, risk and performance, please have a look below:

<div style="display: flex; justify-content: space-between;">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--warning" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

"""

create_markdown_file(
    file_url="https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/economics/economics_controller.py",
    header=markdown_content,
    location="_pages/financetoolkit/documentation/economics.md",
) 