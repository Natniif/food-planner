from scripts.utils import * 

import os 
import sys
import json 
import argparse

recipe_array = schedule_json_plan_to_array("weeks_plan.json")

concat = json_to_dict(*recipe_array)

print_dict_lines(concat["ingredients"])

print(f"""
	------------------------------
	  Calories per day [g]: {concat["macros"]["kcal"]/7}
	  Protein per day [g]: {concat["macros"]["protein[g]"]/7}
	  Carbs per day [g]: {concat["macros"]["carbs[g]"]/7}
	  Fat per day [g]: {concat["macros"]["fat[g]"]/7}
	------------------------------
	  """)


