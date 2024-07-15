from dataclasses import asdict
from typing import Dict
from llmx import TextGenerator, TextGenerationConfig, TextGenerationResponse

from ..scaffold import ChartScaffold
from ...datamodel import Goal


system_prompt = """
You are a helpful assistant highly skilled in writing PERFECT code for visualizations(use simple charts). Given some code template, you complete the template to generate a visualization given the dataset and the goal described. The code you write MUST FOLLOW VISUALIZATION BEST PRACTICES ie. meet the specified goal, apply the right transformation, use the right visualization type, use the right data encoding, and use the right aesthetics (e.g., ensure axis are legible). The transformations you apply MUST be correct and the fields you use MUST be correct. The visualization CODE MUST BE CORRECT and MUST NOT CONTAIN ANY SYNTAX OR LOGIC ERRORS (e.g., it must consider the field types and use them correctly). You MUST first generate a brief plan for how you would solve the task e.g. what transformations you would apply e.g. if you need to construct a new column, what fields you would use, what visualization type you would use, what aesthetics you would use, etc. .
"""


class VizGenerator(object):
    """Generate visualizations from prompt"""

    def __init__(
        self
    ) -> None:

        self.scaffold = ChartScaffold()

    def generate(self, summary: Dict, goal: Goal,
                 textgen_config: TextGenerationConfig, text_gen: TextGenerator, library='altair'):
        """Generate visualization code given a summary and a goal"""

        library_template, library_instructions = self.scaffold.get_template(goal, library)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"The dataset summary is : {summary} \n\n"},
            library_instructions,
            {"role": "user",
             "content":
             f"Always add a legend with various colors where appropriate. The visualization code MUST only use data fields that exist in the dataset (field_names) or fields that are transformations based on existing field_names). Only use variables that have been defined in the code or are in the dataset summary. You MUST return a FULL PYTHON PROGRAM ENCLOSED IN BACKTICKS ``` that starts with an import statement. DO NOT add any explanation. \n\n THE GENERATED CODE SOLUTION SHOULD BE CREATED BY MODIFYING THE SPECIFIED PARTS OF THE TEMPLATE BELOW \n\n {library_template} \n\n.The FINAL COMPLETED CODE BASED ON THE TEMPLATE above is ... \n\n"}]

        completions: TextGenerationResponse = text_gen.generate(
            messages=messages, config=textgen_config)
        response = [x['content'] for x in completions.text]

        return response
    
    def generate_plot(self, summary: Dict, goal: Goal,
                 textgen_config: TextGenerationConfig, text_gen: TextGenerator):
        
        plot_template ={
            "Type": "Type of graph that you are suggesting",
            "X-axis": "X-axis field name",
            "Y-axis": "Y-axis field name",
        }
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"The dataset summary is : {summary} \n\n"},
            {"role": "user",
             "content":
             f"Suggest a graph (use Bar Chart, line Chart, histogram, scatter plot) for the goal {goal.question}. The visualization Chart MUST only use data fields that exist in the dataset (field_names) or fields that are transformations based on existing field_names). Only use variables that have been defined in the dataset summary. You MUST return the fields that needs to be plot with the axis \n\n THE GENERATED RESPONSE SHOULD FOLLOW THE TEMPLATE BELOW \n\n {plot_template} \n\n.The FINAL RESPONSE BASED ON THE TEMPLATE above is ... \n\n"}]

        completions: TextGenerationResponse = text_gen.generate(
            messages=messages, config=textgen_config)
        print("----------plot-----------",completions)