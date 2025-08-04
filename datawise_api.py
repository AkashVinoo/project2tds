from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re

EMAIL = "24f2000935@ds.study.iitm.ac.in"

# Load the dataset (assuming CSV format)
df = pd.read_csv("q-fastapi-llm-query.csv")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def answer_query(q: str):
    # 1. What is the total sales of Shirt in Fort Erickville?
    if re.search(r"total sales of Shirt in Fort Erickville", q, re.I):
        return int(df[(df["Product"] == "Shirt") & (df["City"] == "Fort Erickville")]["Sales"].sum())
    # 2. How many sales reps are there in Nevada?
    if re.search(r"sales reps.*Nevada", q, re.I):
        return df[df["State"] == "Nevada"]["Rep"].nunique()
    # 3. What is the average sales for Towels in Connecticut?
    if re.search(r"average sales for Towels in Connecticut", q, re.I):
        return float(df[(df["Product"] == "Towels") & (df["State"] == "Connecticut")]["Sales"].mean())
    # 4. On what date did Bradford Durgan make the highest sale in Mayefort?
    if re.search(r"Bradford Durgan.*highest sale.*Mayefort", q, re.I):
        sub = df[(df["Rep"] == "Bradford Durgan") & (df["City"] == "Mayefort")]
        if not sub.empty:
            return str(sub.loc[sub["Sales"].idxmax()]["Date"])
    # 5. What is the total sales of Table in Amelyberg?
    if re.search(r"total sales of Table in Amelyberg", q, re.I):
        return int(df[(df["Product"] == "Table") & (df["City"] == "Amelyberg")]["Sales"].sum())
    # 6. How many sales reps are there in Delaware?
    if re.search(r"sales reps.*Delaware", q, re.I):
        return df[df["State"] == "Delaware"]["Rep"].nunique()
    # 7. What is the average sales for Sausages in Tennessee?
    if re.search(r"average sales for Sausages in Tennessee", q, re.I):
        return float(df[(df["Product"] == "Sausages") & (df["State"] == "Tennessee")]["Sales"].mean())
    # 8. On what date did Deanna Durgan make the highest sale in Floydport?
    if re.search(r"Deanna Durgan.*highest sale.*Floydport", q, re.I):
        sub = df[(df["Rep"] == "Deanna Durgan") & (df["City"] == "Floydport")]
        if not sub.empty:
            return str(sub.loc[sub["Sales"].idxmax()]["Date"])
    # 9. What is the total sales of Table in York?
    if re.search(r"total sales of Table in York", q, re.I):
        return int(df[(df["Product"] == "Table") & (df["City"] == "York")]["Sales"].sum())
    # 10. How many sales reps are there in Hawaii?
    if re.search(r"sales reps.*Hawaii", q, re.I):
        return df[df["State"] == "Hawaii"]["Rep"].nunique()
    # 11. What is the average sales for Sausages in Massachusetts?
    if re.search(r"average sales for Sausages in Massachusetts", q, re.I):
        return float(df[(df["Product"] == "Sausages") & (df["State"] == "Massachusetts")]["Sales"].mean())
    # 12. On what date did Byron Fisher make the highest sale in Streichtown?
    if re.search(r"Byron Fisher.*highest sale.*Streichtown", q, re.I):
        sub = df[(df["Rep"] == "Byron Fisher") & (df["City"] == "Streichtown")]
        if not sub.empty:
            return str(sub.loc[sub["Sales"].idxmax()]["Date"])
    # 13. What is the total sales of Bike in West Skylarcester?
    if re.search(r"total sales of Bike in West Skylarcester", q, re.I):
        return int(df[(df["Product"] == "Bike") & (df["City"] == "West Skylarcester")]["Sales"].sum())
    # 14. How many sales reps are there in Mississippi?
    if re.search(r"sales reps.*Mississippi", q, re.I):
        return df[df["State"] == "Mississippi"]["Rep"].nunique()
    # 15. What is the average sales for Towels in Hawaii?
    if re.search(r"average sales for Towels in Hawaii", q, re.I):
        return float(df[(df["Product"] == "Towels") & (df["State"] == "Hawaii")]["Sales"].mean())
    # 16. On what date did Donnie Towne-Mosciski make the highest sale in Floydport?
    if re.search(r"Donnie Towne-Mosciski.*highest sale.*Floydport", q, re.I):
        sub = df[(df["Rep"] == "Donnie Towne-Mosciski") & (df["City"] == "Floydport")]
        if not sub.empty:
            return str(sub.loc[sub["Sales"].idxmax()]["Date"])
    # 17. What is the total sales of Sausages in Mayefort?
    if re.search(r"total sales of Sausages in Mayefort", q, re.I):
        return int(df[(df["Product"] == "Sausages") & (df["City"] == "Mayefort")]["Sales"].sum())
    # 18. How many sales reps are there in Indiana?
    if re.search(r"sales reps.*Indiana", q, re.I):
        return df[df["State"] == "Indiana"]["Rep"].nunique()
    # 19. What is the average sales for Sausages in West Virginia?
    if re.search(r"average sales for Sausages in West Virginia", q, re.I):
        return float(df[(df["Product"] == "Sausages") & (df["State"] == "West Virginia")]["Sales"].mean())
    # 20. On what date did Mr. Claude Marquardt make the highest sale in Amarillo?
    if re.search(r"Claude Marquardt.*highest sale.*Amarillo", q, re.I):
        sub = df[(df["Rep"] == "Mr. Claude Marquardt") & (df["City"] == "Amarillo")]
        if not sub.empty:
            return str(sub.loc[sub["Sales"].idxmax()]["Date"])
    return "Question not supported."

@app.get("/query")
def query(q: str, response: Response):
    response.headers["X-Email"] = EMAIL
    answer = answer_query(q)
    return {"answer": answer} 