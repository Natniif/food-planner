import sys
import os 
import json

from scripts.utils import *

script_dir = os.path.dirname(os.path.abspath(__file__))
test_sched = os.path.join(script_dir, "test_schedule.json")

def test_schedule_json_plan_to_array(): 
	expected = [
		"example.json", "example.json", "example.json", "example.json", 
		"example.json", "example.json", "example.json", "example.json", 
		"example.json", "example.json", "example.json", "example.json", 
		"example.json", "example.json", "example.json", "example.json", 
		"example.json", "example.json", "example.json", "example.json", 
		"example.json", 
	]

	result = schedule_json_plan_to_array(test_sched)
	assert result == expected

def test_merge_dict_adding(): 
	recipe_data1 = {
		"macros": {
			"calories": 300,
			"protein[g]": 20,
			"carbs[g]": 10,
			"fat[g]": 40,
		},
		"ingredients": {}
	}

	recipe_data2 = {
		"macros": {
			"calories": 400,
			"protein[g]": 30,
			"carbs[g]": 30,
			"fat[g]": 30,
		},
		"ingredients": {}
	}

	expected = {
		"macros": {
			"calories": 700,
			"protein[g]": 50,
			"carbs[g]": 40,
			"fat[g]": 70,
		},
		"ingredients": {}
	}

	result = merge_dict(recipe_data1, recipe_data2)
	assert result == expected

def test_merge_dict_uneven(): 
	recipe_data1 = {
		"macros": {
			"calories": 300,
			"protein[g]": 20,
			"carbs[g]": 10,
			"fat[g]": 40,
		},
		"ingredients": {
			"chicken[g]": 100,
			"beans[g]": 200
		}
	}

	recipe_data2 = {
		"macros": {
			"calories": 400,
			"protein[g]": 30,
			"carbs[g]": 30,
			"fat[g]": 30,
		},
		"ingredients": {
			"rice[g]d": 200,
			"beans[g]": 300
		}
	}

	expected = {
		"macros": {
			"calories": 700,
			"protein[g]": 50,
			"carbs[g]": 40,
			"fat[g]": 70,
		},
		"ingredients": {
			"chicken[g]": 100,
			"rice[g]d": 200,
			"beans[g]": 500
		}
	}

	result = merge_dict(recipe_data1, recipe_data2)
	assert result == expected

def test_get_sub_data(): 
	json_file ={
		"macros": {
			"kcal": 1020,
			"fat[g]": 20,
			"Carbs[g]": 100,
			"protein[g]": 30
		},

		"ingredients": {
			"rice[g]": 200,
			"chicken[g]": 200,
			"pasta[g]": 500
		}
	} 

	expected =  {
        "rice[g]": 200,
        "chicken[g]": 200,
        "pasta[g]": 500
    }

	assert get_sub_data(json_file, "ingredients") == expected

def test_inventory_required(): 
	inventory = {
		"ingredients": {
			"rice[g]": 100,
			"chicken[g]": 200,
			"beans[g]": 300
		}
	}

	recipe = {
		"macros": {
			"kcal": 1020,
			"fat[g]": 20,
			"Carbs[g]": 100,
			"protein[g]": 30
		},

		"ingredients": {
			"rice[g]": 300,
			"chicken[g]": 500,
			"pasta[g]": 600
		}
	}

	expected = {
			"rice[g]": 200,
			"chicken[g]": 300, 
			"pasta[g]": 600
	}

	assert inventory_required(inventory, recipe) == expected

def test_json_to_dict_single(): 
	json_test = "example.json"

	expected = {
		"macros": {
			"kcal": 1020,
			"fat[g]": 20,
			"Carbs[g]": 100,
			"protein[g]": 30
		},

		"ingredients": {
			"rice[g]": 200,
			"chicken[g]": 200,
			"pasta[g]": 500
		}
	}

	assert json_to_dict(json_test) == expected

def test_json_to_dict_multiple(): 
	json_test = ["example.json", "example.json", "example.json",]

	expected = {
		"macros": {
			"kcal": 3060,
			"fat[g]": 60,
			"Carbs[g]": 300,
			"protein[g]": 90
		},		

		"ingredients": {
			"rice[g]": 600,
			"chicken[g]": 600,
			"pasta[g]": 1500
		}
	}

	assert json_to_dict(*json_test) == expected



