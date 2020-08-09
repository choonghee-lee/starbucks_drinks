import csv
import re
from decimal import Decimal

import pandas as pd
from ast import literal_eval

from drinks.models import (
    Category, 
    Size,
    Allergen, 
    Nutrition,
    Drink,
    Description,
    Image
)

FILENAME = "starbucks_drinks.csv"

def run():
    # csv 파일 열기
    df = pd.read_csv(
        FILENAME, 
        converters={
            "descriptions": literal_eval, 
            "size": literal_eval,
            "nutrition": literal_eval,
            "allergens": literal_eval,
            "image_urls": literal_eval,
        },
    )

    for _, row in df.iterrows():
        # 컬럼 가져오기
        drink_product_number = row['product_number']
        drink_name_kr        = row['name_kr']
        drink_name_en        = row['name_en']
        drink_category       = row['category']
        drink_descriptions   = row['descriptions']
        drink_size           = row['size']
        drink_nutrition      = row['nutrition']
        drink_allergens      = row['allergens']
        drink_images         = row['image_urls']

        # 카테고리 저장
        category, created = Category.objects.get_or_create(name = drink_category)

        # 사이즈 저장
        size_name_en     = drink_size[0]
        size_name_kr     = drink_size[1]
        size_milliliter  = Decimal(drink_size[2])
        size_fluid_ounce = None
        if drink_size[3]:
            size_fluid_ounce = Decimal(drink_size[3])

        size, created    = Size.objects.get_or_create(
            name_en     = size_name_en, 
            name_kr     = size_name_kr,
            milliliter  = size_milliliter,
            fluid_ounce = size_fluid_ounce
        )

        # 영양 정보 저장
        nutrition_calorie       = Decimal(drink_nutrition[0])
        nutrition_saturated_fat = Decimal(drink_nutrition[1])
        nutrition_protein       = Decimal(drink_nutrition[2])
        nutrition_sodium        = Decimal(drink_nutrition[3])
        nutrition_sugar         = Decimal(drink_nutrition[4])
        nutrition_caffeine      = Decimal(drink_nutrition[5])

        Nutrition(
            calorie       = nutrition_calorie,
            saturated_fat = nutrition_saturated_fat,
            protein       = nutrition_protein,
            sodium        = nutrition_sodium,
            sugar         = nutrition_sugar,
            caffeine      = nutrition_caffeine,
        ).save()
        nutrition = Nutrition.objects.filter(calorie = nutrition_calorie).order_by('-id')[0]         

        # 알레르기 유발 정보 저장
        for allergen_name in drink_allergens:
            allergen, created = Allergen.objects.get_or_create(name = allergen_name)

        # 음료 저장
        drink, created = Drink.objects.get_or_create(
            product_number = drink_product_number,
            name_kr        = drink_name_kr,
            name_en        = drink_name_en,
            category       = category,
            size           = size,
            nutrition      = nutrition,
        )
        if created:
            for allergen_name in drink_allergens:
                drink.allergens.add(Allergen.objects.get(name = allergen_name))
            drink.save()

        # 설명 저장
        for description_content in drink_descriptions:
            description, created = Description.objects.get_or_create(
                content = description_content,
                drink   = drink,
            )

        # 이미지 URL 저장
        for drink_image_url in drink_images:
            image, created = Image.objects.get_or_create(
                url   = drink_image_url,
                drink = drink,
            )
            
    print("SAVED THE BATCH !!!")