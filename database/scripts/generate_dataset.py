import os, random
from datetime import date, timedelta
import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

# ---------- USERS ----------
users = pd.DataFrame([
["U001","Affan",23,50000,125000,"Moderate",12000,"Emergency fund and Goa trip"],
["U002","Rahul",25,65000,180000,"Conservative",18000,"Emergency fund"],
["U003","Sara",24,80000,250000,"Aggressive",25000,"New car"],
["U004","Arjun",23,45000,85000,"Moderate",9000,"Emergency fund and laptop"],
["U005","Zoya",26,95000,320000,"Conservative",30000,"Long-term savings and investments"],
], columns=["user_id","name","age","monthly_income","current_balance","risk_profile","monthly_savings_target","financial_goal"])

# ---------- EXPENSES ----------
merchants = {
"Food":["Swiggy","Zomato","Dominos","McDonald's","Starbucks"],
"Transport":["Uber","Ola","Rapido","Metro"],
"Shopping":["Amazon","Flipkart","Myntra","AJIO"],
"Entertainment":["Netflix","Spotify","BookMyShow","YouTube"],
"Bills":["Airtel","Jio","ACT Fibernet"],
"Healthcare":["Apollo Pharmacy","Tata 1mg","Apollo Hospitals"],
"Education":["Udemy","Coursera","Amazon Books"],
"Travel":["MakeMyTrip","IndiGo","Air India","IRCTC"],
"Utilities":["Electricity Board","Water Board","Gas Agency"],
"Rent":["Monthly Rent"],"Other":["Local Store","UPI Merchant","Gift"]
}
weights = {
"U001":[.30,.10,.13,.10,.07,.04,.06,.04,.06,.06,.04],
"U002":[.18,.10,.10,.16,.08,.05,.05,.04,.07,.13,.04],
"U003":[.16,.08,.27,.08,.06,.04,.04,.08,.05,.10,.04],
"U004":[.27,.11,.13,.08,.08,.05,.07,.04,.06,.06,.05],
"U005":[.14,.07,.12,.08,.07,.04,.05,.06,.05,.25,.07]
}
cats=list(merchants)
ranges={"Food":(120,1400),"Transport":(80,900),"Shopping":(300,7000),
"Entertainment":(100,1800),"Bills":(250,2500),"Healthcare":(200,4500),
"Education":(300,5000),"Travel":(800,15000),"Utilities":(300,2500),
"Rent":(8000,18000),"Other":(100,3000)}

rows=[]; eid=1
start=date(2026,4,1); today=date(2026,9,18)
counts={"U001":82,"U002":72,"U003":78,"U004":76,"U005":70}

for uid,n in counts.items():
    for _ in range(n):
        d=start+timedelta(days=random.randint(0,(today-start).days))
        idx=max(0,min(5,(d.year-start.year)*12+d.month-start.month))
        cat=np.random.choice(cats,p=np.array(weights[uid])/sum(weights[uid]))
        lo,hi=ranges[cat]
        base_amount=np.random.lognormal(np.log((lo+hi)/3),.52)
        if uid=="U001" and cat=="Food": base_amount*=.8+idx*.12
        if uid=="U003" and cat=="Shopping": base_amount*=1.6
        amount=int(np.clip(base_amount,lo,hi))
        if uid=="U003" and cat=="Shopping" and random.random()<.08:
            amount=random.choice([8500,12000,15000,18000])
        rows.append([f"E{eid:04}",uid,d.isoformat(),cat,random.choice(merchants[cat]),amount,
                     random.choice(["UPI","Card","Cash","Net Banking"])])
        eid+=1
expenses=pd.DataFrame(rows,columns=["expense_id","user_id","date","category","merchant","amount","payment_method"])
expenses=expenses.sort_values(["user_id","date"])

# ---------- BUDGETS ----------
limits={
"U001":{"Food":6000,"Transport":4000,"Shopping":5000,"Entertainment":2500,"Bills":3000,"Healthcare":3000,"Education":3000,"Travel":5000,"Utilities":3000,"Rent":12000,"Other":2500},
"U002":{"Food":6500,"Transport":4000,"Shopping":4500,"Entertainment":1800,"Bills":3500,"Healthcare":3000,"Education":2500,"Travel":5000,"Utilities":3000,"Rent":15000,"Other":2500},
"U003":{"Food":8000,"Transport":5000,"Shopping":9000,"Entertainment":4000,"Bills":4000,"Healthcare":5000,"Education":4000,"Travel":10000,"Utilities":4000,"Rent":18000,"Other":4000},
"U004":{"Food":5500,"Transport":3500,"Shopping":4000,"Entertainment":2000,"Bills":3000,"Healthcare":2500,"Education":3500,"Travel":4000,"Utilities":2500,"Rent":10000,"Other":2000},
"U005":{"Food":7000,"Transport":4000,"Shopping":6000,"Entertainment":2500,"Bills":4000,"Healthcare":4000,"Education":4000,"Travel":8000,"Utilities":4000,"Rent":20000,"Other":3500}}
b=[]; bid=1
for uid, d in limits.items():
    for month in pd.date_range("2026-04-01","2026-09-01",freq="MS"):
        for cat,limit in d.items():
            b.append([f"B{bid:04}",uid,cat,limit,month.strftime("%Y-%m")]); bid+=1
budgets=pd.DataFrame(b,columns=["budget_id","user_id","category","monthly_limit","month"])

# ---------- SUBSCRIPTIONS ----------
subscriptions=pd.DataFrame([
["S001","U001","Netflix","Entertainment",649,"2025-01-15","2026-03-01",True],
["S002","U001","Spotify","Entertainment",119,"2025-04-10","2026-09-10",True],
["S003","U001","Adobe Creative Cloud","Software",1675,"2026-01-01","2026-09-12",True],
["S004","U001","Amazon Prime","Shopping",299,"2025-08-20","2026-08-20",True],
["S005","U002","Netflix","Entertainment",649,"2025-05-01","2026-02-15",True],
["S006","U002","Spotify","Entertainment",119,"2025-02-01","2026-09-12",True],
["S007","U002","YouTube Premium","Entertainment",149,"2025-09-01","2026-04-02",True],
["S008","U002","Amazon Prime","Shopping",299,"2025-06-01","2026-03-10",True],
["S009","U003","Netflix","Entertainment",649,"2026-01-01","2026-09-15",True],
["S010","U003","Spotify","Entertainment",119,"2026-01-01","2026-09-16",True],
["S011","U003","Canva Pro","Software",500,"2026-02-01","2026-09-10",True],
["S012","U004","Netflix","Entertainment",649,"2025-03-01","2026-01-10",True],
["S013","U004","Coursera","Education",2100,"2026-06-01","2026-09-05",True],
["S014","U005","Spotify","Entertainment",119,"2025-01-01","2026-09-15",True],
["S015","U005","Amazon Prime","Shopping",299,"2025-01-01","2026-09-01",True],
],columns=["subscription_id","user_id","service","category","monthly_cost","start_date","last_used","active"])

# ---------- SAVINGS GOALS ----------
savings=pd.DataFrame([
["G001","U001","Goa Trip",40000,18000,"2026-12-15","High"],
["G002","U001","Emergency Fund",150000,75000,"2027-06-01","High"],
["G003","U001","New Laptop",100000,35000,"2027-02-01","Medium"],
["G004","U002","Emergency Fund",250000,145000,"2027-06-01","High"],
["G005","U002","Family Vacation",80000,42000,"2027-01-15","Medium"],
["G006","U003","New Car",800000,310000,"2028-03-01","High"],
["G007","U003","Investment Corpus",500000,220000,"2028-12-01","Medium"],
["G008","U004","Emergency Fund",120000,45000,"2027-08-01","High"],
["G009","U004","New Laptop",90000,25000,"2027-02-15","High"],
["G010","U005","Emergency Fund",300000,250000,"2027-01-01","High"],
["G011","U005","Investment Corpus",1000000,450000,"2029-01-01","Medium"],
],columns=["goal_id","user_id","goal_name","target_amount","current_saved","target_date","priority"])

# ---------- FINANCIAL DECISIONS ----------
decisions=pd.DataFrame([
["D001","U001","2026-08-15","Should I buy a smartwatch?","No",12000,"Prioritized Goa savings","pending"],
["D002","U001","2026-08-20","Should I subscribe to Adobe?","Yes",1675,"Needed for project work","positive"],
["D003","U001","2026-09-05","Can I spend ₹5000 on headphones?","Review",5000,"Food spending was above budget","pending"],
["D004","U002","2026-07-10","Should I upgrade my phone?","No",30000,"Emergency fund prioritized","positive"],
["D005","U002","2026-08-22","Should I keep Netflix?","Review",649,"Usage was low","pending"],
["D006","U003","2026-08-01","Should I buy a ₹15000 gaming accessory?","Yes",15000,"Fit discretionary plan","positive"],
["D007","U003","2026-09-01","Should I invest ₹20000?","Review",20000,"Needs market and risk analysis","pending"],
["D008","U004","2026-08-12","Can I buy a ₹10000 laptop accessory?","No",10000,"Savings goal is behind schedule","positive"],
["D009","U004","Should I subscribe to a new streaming service?","No",499,"Existing subscriptions cover entertainment","positive"],
["D010","U005","2026-08-25","Should I invest ₹50000?","Review",50000,"Compare with goals and risk profile","pending"],
],columns=["decision_id","user_id","date","question","decision","amount","reason","outcome"])
# Fix the one intentionally shortened row above
decisions.loc[decisions["decision_id"]=="D009","date"]="2026-09-02"

# ---------- AGENT ACTIONS ----------
actions=pd.DataFrame([
["A001","U001","2026-09-15T10:30:00","Alert","Food spending exceeded monthly budget","completed"],
["A002","U001","2026-09-15T10:35:00","Recommendation","Flagged unused Netflix subscription for review","completed"],
["A003","U001","2026-09-16T09:20:00","Analysis","Evaluated ₹5000 headphone purchase against savings goals","completed"],
["A004","U002","2026-09-14T11:00:00","Alert","Detected subscriptions with low recent usage","completed"],
["A005","U002","2026-09-16T12:15:00","Recommendation","Suggested redirecting unused subscription costs to emergency fund","completed"],
["A006","U003","2026-09-16T13:10:00","Analysis","Detected elevated shopping expenditure","completed"],
["A007","U003","2026-09-17T14:00:00","Market Check","Prepared context for investment-related question","completed"],
["A008","U004","2026-09-15T09:40:00","Alert","Savings goal is behind planned contribution pace","completed"],
["A009","U004","2026-09-17T10:05:00","Recommendation","Suggested reviewing discretionary shopping expenses","completed"],
["A010","U005","2026-09-17T15:30:00","Analysis","Prepared long-term investment decision context","completed"],
],columns=["action_id","user_id","timestamp","action_type","description","status"])

# ---------- SAVE ----------
all_data={
"users.csv":users,"expenses.csv":expenses,"budgets.csv":budgets,
"subscriptions.csv":subscriptions,"savings_goals.csv":savings,
"financial_decisions.csv":decisions,"agent_actions.csv":actions}

for name,df in all_data.items():
    df.to_csv(os.path.join(DATA,name),index=False)
    print(f"Created {name}: {len(df)} rows")

# ---------- VALIDATION ----------
valid=set(users.user_id)
for df in [expenses,budgets,subscriptions,savings,decisions,actions]:
    assert set(df.user_id).issubset(valid)
assert (expenses.amount>0).all()
assert (budgets.monthly_limit>0).all()
assert (subscriptions.monthly_cost>0).all()
assert (savings.current_saved<=savings.target_amount).all()

print("\nVALIDATION PASSED")
print(f"Total expense transactions: {len(expenses)}")
print(f"Total dataset rows: {sum(len(x) for x in all_data.values())}")
print("\nAll files are in the data/ folder.")
