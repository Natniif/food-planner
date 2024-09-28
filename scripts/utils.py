import os 
import sys
import json 
from typing import Dict, List, Any

from rich import print
from rich.console import Console
from rich.pretty import Pretty


def schedule_json_plan_to_array(week_data: str) -> List[str]:
	"""
	Extracts all .json files from weekly plan and flattens into array

	"""

	try:
		with open(week_data, "r") as file: 
			schedule = json.load(file)
	except json.JSONDecodeError as e: 
		raise ValueError(f"Error decoding json: {e}")

	recipes: List[str] = []

	for day, meals in schedule.items(): 
		for meal, file in meals.items(): 
			if file.endswith(".json"): 
				recipes.append(file)

	# assert len(recipes) == 21

	return recipes


def merge_dict(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
	merged_dict = {
		"macros": {},
		"ingredients": {}
	}

	if dict1 == False: 
		return dict2
	elif dict2 == False: 
		return dict1
	elif dict1 == False and dict2 == False: 
		return merged_dict

	# Merge macros by adding values
	for key in dict1['macros']:
		merged_dict['macros'][key] = dict1['macros'][key]

	for key in dict2['macros']:
		if key in merged_dict['macros']:
			merged_dict['macros'][key] += dict2['macros'][key]
		else:
			merged_dict['macros'][key] = dict2['macros'][key]

	# Merge ingredients by summing values for overlapping keys
	for key in dict1['ingredients']:
		merged_dict['ingredients'][key] = dict1['ingredients'][key]

	for key in dict2['ingredients']:
		if key in merged_dict['ingredients']:
			merged_dict['ingredients'][key] += dict2['ingredients'][key]
		else:
			merged_dict['ingredients'][key] = dict2['ingredients'][key]

	return merged_dict


def get_sub_data(json_data: dict, sub_data: str) -> dict:
	if not isinstance(sub_data, str): 
		raise ValueError("sub_data must be a string")

	if isinstance(json_data, dict):
		if sub_data in json_data:
			return json_data[sub_data]
		else:
			raise KeyError(f"Key '{sub_data}' not found in the provided dictionary.")
	else:
		raise TypeError(f"Expected a dictionary, but got {type(json_data)}.")


def inventory_required(inventory: Dict[str, Dict[str, int]], recipe: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    required = {}

    for ingredient, required_amount in recipe['ingredients'].items():
        available_amount = inventory['ingredients'].get(ingredient, 0)
        
        if required_amount > available_amount:
            required[ingredient] = required_amount - available_amount

    return required


def json_to_dict(*json_files) -> Dict[str, Any]:
	'''
	Requires .json suffix
	'''

	recipes_dir = "recipes"

	if not os.path.exists(recipes_dir):
		raise FileNotFoundError(f"The directory {recipes_dir} does not exist.")

	ret = {}

	for i, json_file in enumerate(json_files):

		file_path = os.path.join(recipes_dir, json_file) if json_file != "inventory.json" else "inventory.json"

		if not os.path.exists(file_path):
			raise FileNotFoundError(f"Ths file {file_path} does not exist")
		try:
			with open(file_path, 'r') as file: 
				json_data = json.load(file)
		except json.JSONDecodeError as e: 
			raise ValueError(f"Error decoding JSON: {e}")

		if isinstance(json_data, dict): 
			if i == 0: 
				ret = json_data
			else: 
				ret = merge_dict(ret, json_data)
		else: 
			raise ValueError("The content of the JSON file must be a dictionary")

	return ret

def print_dict_lines(data: dict, indent: int = 0) -> None:
	console = Console()
	for key, value in data.items():
		console.print(' ' * indent + f"[green]{key}:[/green] ", end="")
		if isinstance(value, dict):
			print()  # Print a new line before printing the nested dictionary
			print_dict_lines(value, indent + 4)  # Increase indent for nested dict
		else:
			console.print(value)  # Print the value on the same line

