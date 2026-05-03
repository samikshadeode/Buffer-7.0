from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_js
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import heapq
import time
import io
from pywebio.output import clear
from collections import defaultdict


#DSA USED:HASH MAPS,BINARY SEARCH,SLIDING WINDOW,GREEDY ALGORITHM,PREFIX SUM,HEAPS,KADANE'S ALGORITHM,FREQUENCY ARRAY


#dict of dicts to store budgets for each category
budgets_data = {
    "stationery":{"name":"stationery", "importance":4,"limit_s":0},
    "grocery":{"name":"grocery", "importance":3,"limit_g":0},
    "rent":{"name":"rent", "importance":1,"limit_r":0},
    "tuition":{"name":"tuition", "importance":2,"limit_t":0}
}
#dict of dicts to store expenses for each category
expenses = {
    "stationery":{"name":"stationery","expense_s":0,"remaining_s":0,"date":datetime.now()},
    "grocery":{"name":"grocery","expense_g":0,"remaining_g":0,"date":datetime.now()},
    "rent":{"name":"rent","expense_r":0,"remaining_r":0,"date":datetime.now()},
    "tuition":{"name":"tuition","expense_t":0,"remaining_t":0,"date":datetime.now()}
}
#dictionary to store total expenses for each category
category_total = {"stationery":0,"grocery":0,"rent":0,"tuition":0}
my_income = 0
total_saved = 0 
transaction_history = [] 
prefix_sum=[] #stores sum of all my transactions up till date
net_flow=[] # stores all my transactions-expenditure and income
prefix_amount=0
savings_per_month=0
savings_amt=0
total_b=0

#some hardcoded dates for demo purposes
demo_date1="2026-04-01"
demo_date2="2026-04-08"
demo_date3="2026-04-15"
demo_date4="2026-04-22"
demo_date5="2026-04-23"
demo_date6="2026-04-24"
demo_date7="2026-04-25"
demo_date8="2026-04-26"

demo_date1=datetime.strptime(demo_date1,"%Y-%m-%d").date()
demo_date2=datetime.strptime(demo_date2,"%Y-%m-%d").date()
demo_date3=datetime.strptime(demo_date3,"%Y-%m-%d").date()
demo_date4=datetime.strptime(demo_date4,"%Y-%m-%d").date()
demo_date5=datetime.strptime(demo_date5,"%Y-%m-%d").date()
demo_date6=datetime.strptime(demo_date6,"%Y-%m-%d").date()
demo_date7=datetime.strptime(demo_date7,"%Y-%m-%d").date()
demo_date8=datetime.strptime(demo_date8,"%Y-%m-%d").date()


transaction_history.append({"category": "stationery", "amount": 50, "date": demo_date1})
transaction_history.append({"category": "stationery", "amount": 50, "date": demo_date2})
transaction_history.append({"category": "stationery", "amount": 50, "date": demo_date3})
transaction_history.append({"category": "tuition", "amount": 40, "date": demo_date4})
transaction_history.append({"category": "tuition", "amount": 80, "date": demo_date5})
transaction_history.append({"category": "rent", "amount": 50, "date": demo_date6})
transaction_history.append({"category": "stationery", "amount": 50, "date": demo_date7})
transaction_history.append({"category": "stationery", "amount": 50, "date": demo_date8})
    
prefix_amount=prefix_amount+50
temp={"date":demo_date1,"amount":prefix_amount}
prefix_sum.append(temp)

prefix_amount=prefix_amount+60
temp={"date":demo_date2,"amount":prefix_amount}
prefix_sum.append(temp)


prefix_amount=prefix_amount+70
temp={"date":demo_date3,"amount":prefix_amount}
prefix_sum.append(temp)

prefix_amount=prefix_amount+80
temp={"date":demo_date4,"amount":prefix_amount}
prefix_sum.append(temp)

prefix_amount=prefix_amount+80
temp={"date":demo_date5,"amount":prefix_amount}
prefix_sum.append(temp)

prefix_amount=prefix_amount+50
temp={"date":demo_date6,"amount":prefix_amount}
prefix_sum.append(temp)

prefix_amount=prefix_amount+50
temp={"date":demo_date7,"amount":prefix_amount}
prefix_sum.append(temp)

prefix_amount=prefix_amount+50
temp={"date":demo_date8,"amount":prefix_amount}
prefix_sum.append(temp)


#adding incomes
temp1={"amount":50,"date":demo_date1}
net_flow.append(temp1)

temp2={"amount":60,"date":demo_date2}
net_flow.append(temp2)

temp3={"amount":10,"date":demo_date4}
net_flow.append(temp3)

temp4={"amount":60,"date":demo_date5}
net_flow.append(temp4)

temp5={"amount":70,"date":demo_date5}
net_flow.append(temp5)

temp6={"amount":10,"date":demo_date6}
net_flow.append(temp6)


total_b=250
budgets_data["stationery"]["limit_s"]=200
budgets_data["grocery"]["limit_g"]=100
budgets_data["rent"]["limit_r"]=50
budgets_data["tuition"]["limit_t"]=60



def apply_theme():
    put_html("""
    <style>
        body { background-color: #f3f4f6; font-family: 'Segoe UI', sans-serif; }
        button { border-radius: 8px !important; margin: 5px; font-weight: 600 !important; }
        .output-container { background: white; border-radius: 12px; padding: 15px; margin-top: 20px; }
    </style>
    """)


#set limit for stationery category
def stationery_budget():
    limit_s = float(input("Set Limit:")) 
    budgets_data["stationery"]["limit_s"] = limit_s
    with use_scope('output_area', clear=True):
        put_text("Set budgets for stationery: %f" % limit_s).style('color: green')

#set limit for grocery category
def grocery_budget():
    limit_g = float(input("Set limit"))
    budgets_data["grocery"]["limit_g"] = limit_g
    with use_scope('output_area', clear=True):
        put_text("Set budgets for grocery: %f" % limit_g).style('color: green')

#set limit for rent category
def rent_budget():
    limit_r = float(input("Set limit"))
    budgets_data["rent"]["limit_r"] = limit_r
    with use_scope('output_area', clear=True):
        put_text("Set budgets for rent: %f" % limit_r).style('color: green')

#set limit for tuition category
def tuition_budget():
    limit_t = float(input("Set limit"))
    budgets_data["tuition"]["limit_t"] = limit_t   
    with use_scope('output_area', clear=True):
        put_text("Set budgets for tuition: %f" % limit_t).style('color: green')


#set total limit across all categories
def total_budget():
    global total_b
    total_b = float(input("Enter total budget for all categories"))
    with use_scope('output_area', clear=True):
        put_text("Total budget set to: %f" % total_b).style('color: green')


#show the buttons to set budgets for each category
def budgets():
    global total_b
    with use_scope('output_area', clear=True):
        put_button("Set total budget for all categories",onclick=total_budget)
      
        put_text("Click to set budget for each category:")
        put_button("Set stationery", onclick=stationery_budget)
        put_button("Set grocery", onclick=grocery_budget)
        put_button("Set rent", onclick=rent_budget)
        put_button("Set tuition", onclick=tuition_budget)
        put_markdown("---")
        put_button("Optimise budget", color='success', onclick=lambda: greedy())

#show the button to add income
def add_income():
    global my_income
    temp_income=float(input("Add income"))
    my_income = my_income + temp_income
    temp={"amount":temp_income,"date":datetime.now().date()}
    net_flow.append(temp)
    with use_scope('output_area', clear=True):
        put_text("Income added successfully!").style('font-weight: bold')
        put_text("Total income: " + str(my_income))

def income():
    with use_scope('output_area', clear=True):
        put_text("INCOME CATEGORIES")
        put_button("Awards", onclick=add_income)
        put_button("Salary", onclick=add_income)
        put_button("Coupons", onclick=add_income)
        put_button("Rental", onclick=add_income)


#show the button to add expense records
def records():
    with use_scope('output_area', clear=True):
        put_text("Select Action:")
        put_button("Add income", onclick=income, color='success')
        put_button("Add expense", onclick=expense, color='danger')


#show the button to add expense records for each category
def expense():
    global prefix_amount
    selected_category = select("Select category", options=["stationery", "grocery", "rent", "tuition"])
    with use_scope('output_area', clear=True):
        if selected_category == "stationery":
            expense1 = float(input("Add expense:"))
            expenses["stationery"]["expense_s"] = expense1 + expenses["stationery"]["expense_s"]
            expenses["stationery"]["remaining_s"] = budgets_data["stationery"]["limit_s"] - expenses["stationery"]["expense_s"]
            transaction_history.append({"category": "stationery", "amount": expense1, "date": datetime.now()})
            put_text("Category:"+selected_category+" Amount:"+str(expense1)+" Remaining budget:"+str(expenses["stationery"]["remaining_s"]))
            prefix_amount=prefix_amount+expense1
            temp={"date":datetime.now().date(),"amount":prefix_amount}
            prefix_sum.append(temp)


        elif selected_category == "grocery":
            expense2 = float(input("Add expense:"))
            expenses["grocery"]["expense_g"] = expense2 + expenses["grocery"]["expense_g"]
            expenses["grocery"]["remaining_g"] = budgets_data["grocery"]["limit_g"] - expenses["grocery"]["expense_g"]
            transaction_history.append({"category": "grocery", "amount": expense2, "date": datetime.now()})
            put_text("Category:"+selected_category+" Amount:"+str(expense2)+" Remaining budget:"+str(expenses["grocery"]["remaining_g"]))
            prefix_amount=prefix_amount+expense2
            temp={"date":datetime.now().date(),"amount":prefix_amount}
            prefix_sum.append(temp)

        elif selected_category == "rent":
            expense3 = float(input("Add expense:"))
            expenses["rent"]["expense_r"] = expense3 + expenses["rent"]["expense_r"]
            expenses["rent"]["remaining_r"] = budgets_data["rent"]["limit_r"] - expenses["rent"]["expense_r"]
            transaction_history.append({"category": "rent", "amount": expense3, "date": datetime.now()})
            put_text("Category:"+selected_category+" Amount:"+str(expense3)+" Remaining budget:"+str(expenses["rent"]["remaining_r"]))
            prefix_amount=prefix_amount+expense3
            temp={"date":datetime.now().date(),"amount":prefix_amount}
            prefix_sum.append(temp)

        elif selected_category == "tuition":
            expense4 = float(input("Add expense:"))
            expenses["tuition"]["expense_t"] = expense4 + expenses["tuition"]["expense_t"]
            expenses["tuition"]["remaining_t"] = budgets_data["tuition"]["limit_t"] - expenses["tuition"]["expense_t"]    
            transaction_history.append({"category": "tuition", "amount": expense4, "date": datetime.now()})
            put_text("Category:"+selected_category+" Amount:"+str(expense4)+" Remaining budget:"+str(expenses["tuition"]["remaining_t"]))
            prefix_amount=prefix_amount+expense4
            temp={"date":datetime.now().date(),"amount":prefix_amount}
            prefix_sum.append(temp)


#run optimisation using knapsack algorithm and display optimal budget allocation
#find the ratio of importance to limit for each category
#ex.if the total limit has importance 9 then how much importance does 1 rs have
#we use greedy algorithm here.First allot the budget to whichever category has highest importance to limit ratio 
#ie investing in whichever category will give greatest importance


def greedy():
     
     global total_b
     total_imp=0
     remaining_budget=total_b

     allocations= {}
     importances = [
        {'name': "stationery", 'limit': budgets_data["stationery"]["limit_s"], 'importance': 9},
        {'name': "grocery", 'limit': budgets_data["grocery"]["limit_g"], 'importance': 8},
        {'name': "rent", 'limit': budgets_data["rent"]["limit_r"], 'importance': 6},
        {'name': "tuition", 'limit': budgets_data["tuition"]["limit_t"], 'importance': 7}
       ]
     importances.sort(key=lambda x: x["importance"] / (x["limit"]), reverse=True)
    
     for importance in importances:
                 if importance['limit']<=remaining_budget:
                       total_imp=total_imp+importance['importance']
                       remaining_budget=remaining_budget-importance['limit']
                       allocations[importance['name']] = importance['limit']
                  
                 else:
                       total_imp=(importance['importance']/importance['limit'])*remaining_budget
                       allocations[importance['name']]=remaining_budget
                       remaining_budget=0
                       break  

      

     with use_scope('output_area', clear=True):
           put_text("Optimal budget allocation:")
           put_table([[k, v] for k, v in allocations.items()])


#show distribution across all categories using a pie chart    
#hashing used here
def show_pie_chart():
    clear('output_area')
    
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    temp_total = {"stationery": 0, "grocery": 0, "rent": 0, "tuition": 0}
    for th in transaction_history:
        temp_total[th["category"]] += th["amount"]
    
    labels = ["stationery", "grocery", "rent", "tuition"]
    values = [temp_total["stationery"], temp_total["grocery"], temp_total["rent"], temp_total["tuition"]]
    
    plt.figure(figsize=(5, 4))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    
    with use_scope('output_area', clear=True):
        put_image(buf.getvalue())

    plt.close()


#show the top 3 expenses of that month with heap data struct
#not used sorting as time complexity of sorting is nlogn where heap has has time complexity of nlogk where k is 3 here
def top_expenses_using_heap():
    clear('output_area')
   
    month1 = select("Enter month number to see top 3 expenses",options=['January','Februrary','March','April','May','June','July','August','September','October','November','December'])
    if month1=="January":
            month1=1
    elif month1=="February":
            month1=2
    elif month1=="March":
          month1=3
    elif month1=='April':
          month1=4
    elif month1=='May':
          month1=5
    elif month1=='June':
          month1=6
    elif month1=='July':
          month1=7
    elif month1=='August':
          month1=8
    elif month1=='September':
          month1=9
    elif month1=='October':
          month1=10
    elif month1=='November':
          month1=11
    elif month1=='December':
          month1=12    
        

    filtered_month=[]
    for t in transaction_history:
               if t["date"].month==month1:
                       filtered_month.append(t)
             
  
    three_maxi = heapq.nlargest(3, filtered_month, key=lambda x: x["amount"])
    
    with use_scope('output_area', clear=True):
        put_text(f"Top 3 Expenses for month {month1}:")
        if not three_maxi:
            put_text("No records found.")
        else:
            table_data = [['Category', 'Amount']]
            for expense in three_maxi:
                table_data.append([expense["category"], expense["amount"]])
        
           
        put_table(table_data)
           

#search transaction using binary search logic
def search_transaction_by_date():
    clear('output_area')
    date_1= input("Enter date to search transactions", type=DATE)
    date1 = datetime.strptime(date_1, "%Y-%m-%d").date()
    for tx in transaction_history:
         if isinstance(tx["date"], datetime):
                tx["date"] = datetime.strptime(tx["date"], "%Y-%m-%d").date()
   
 

    transaction_history.sort(key=lambda x: x["date"].date() if isinstance(x["date"], datetime) else x["date"])
    
    
    low=0
    high= len(transaction_history)-1
    ans=0
    ans1 = 0
  
    while low <= high:
        mid = (low+high)//2
        if transaction_history[mid]["date"] >= date1:
            ans=mid
            high=mid-1
        else: 
            low = mid+1

    with use_scope('output_area', clear=True):
        put_text(f"Search results for {date1}:")
        
        results = [t for t in transaction_history if t["date"] == date1]
        if results:
            put_table([[r['category'], r['amount']] for r in results])
        else:
            put_text("No transactions found.")


#ask user to add goals and find monthly savings to achive that goal
def goals():
      global savings_amt

      month1=datetime.now().month
      year1=datetime.now().year

      goal=input("Add goal", placeholder="save for Japan trip,gift for mom etc.")
      savings_amt=float(input("Target Amount",type="number",placeholder="Enter amount..."))
      
      month=select("Target month",options=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
      #float(input("Target month",type="number",placeholder="Enter month number..."))
      year=float(input("Target year",type="number",placeholder="Enter year..."))
      if month=="January":
            month=1
      elif month=="February":
            month=2
      elif month=="March":
          month=3
      elif month=='April':
          month=4
      elif month=='May':
          month=5
      elif month=='June':
          month=6
      elif month=='July':
          month=7
      elif month=='August':
          month=8
      elif month=='September':
          month=9
      elif month=='October':
          month=10
      elif month=='November':
          month=11
      elif month=='December':
          month=12    
        
    
        
      duration=(year-year1)*12 + (month-month1)
        
      savings_per_month=(savings_amt/duration)
      

      
      with use_scope('output_area', clear=True):
         put_markdown(f"## 🎯 Goal Tracking: {goal}")
         put_text(f"You have to save: {savings_per_month:.2f} per month to reach your target.")
         put_row([
            put_column([
                put_text("Monthly Requirement").style('color: #888; font-size: 14px'),
                put_text(f"Rs{savings_per_month:.2f}").style('font-size: 22px; font-weight: bold')
            ]),
            put_column([
                put_text("Duration").style('color: #888; font-size: 14px'),
                put_text(f"{int(duration)} Months").style('font-size: 22px; font-weight: bold')
            ])
        ])
         put_markdown("---")
      
         put_button("Show progress towards goal",onclick=lambda:progress())

         put_button("Click to input savings",onclick=savings)


     
   


     


#add savings to total saved and show progress towards goal
def savings():
   global total_saved

   saved = input("Deposit to Savings", type=FLOAT, placeholder="Enter amount...")
   total_saved += saved
    
  
   toast(f"Successfully saved Rs{saved}!", color='success')


 #show how far along the goal user is              
def progress():
      #for goal 1
      #show  a progress bar
      global total_saved
      with use_scope('progress_area', clear=True):
        put_markdown(f"### 📈 Progress Tracker")
        put_processbar('bar1')
        for i in range(1,(1+ total_saved)):
            set_progressbar('bar1',i/savings_amt)
            time.sleep(0.1)


      
      if total_saved>=savings_amt:
            toast("Congratulations! You have achieved your savings goal!", color='success')


     


    

#main interface
def main():
    
    apply_theme()
    put_markdown("#  Personal Finance Manager").style('text-align:center')
    put_markdown("---")
    
   
    put_row([
        put_column([
            put_markdown("###  Budgeting"),
            put_button("Plan Monthly Budget", onclick=budgets),
            put_button("Add Records", onclick=records,  color='info'),
            put_button("Set Financial Goals", onclick=goals, color='warning'),
            put_button("Deposit to Savings", onclick=savings, color='success')
           
        ]),
        put_column([
            put_markdown("###  Analytics"),
            put_button("Show Pie Chart", onclick=show_pie_chart,color='secondary', outline=True),
            put_button("Top Expenses", onclick=top_expenses_using_heap,color='secondary', outline=True),
            put_button("Search Transactions", onclick=search_transaction_by_date,color='secondary', outline=True),
            put_button("Calculate Between 2 Dates", onclick=calculate_transaction_between_2_dates, color='secondary', outline=True),
            put_button("Most profitable day streak!",onclick=most_expensive_day_streak,color='secondary',outline='True'),
            put_button("Click to detect spikes in spending",onclick=spike,color='secondary',outline=True),
            put_button("Click to see recurring transactions",onclick=recurring_pattern,color='secondary',outline=True)
        ]),
        put_column([
            put_markdown("###  Goal Tracking"),
            put_button("See progress towards goals", onclick=lambda:progress(
            ), color='warning')
        
    ]),
    put_column([
        put_markdown("### Budget optimisation"),
        put_button("Budget allocation  ", onclick=lambda: greedy(), color='success')
    ])
    ],size='25% 25% 25% 25%')

    
    put_markdown("---")
    
   
    put_scope('output_area')

#use binary search logic and prefix sum to find total expenditure between 2 dates
def calculate_transaction_between_2_dates():
    clear('output_area')
    global prefix_amount

    
    start_str = input("Enter starting date", type=DATE)
    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
    end_str = input("Enter last date", type=DATE)
    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()

    #if we consider just starting date then transactions ON that date arent considered
    start_date = start_date - timedelta(days=1)
    ans = -1
    low = 0
    high = len(prefix_sum) - 1
    

    #binary search logic to find prefix sum just before start date or start date
    #basically finding floor of a number   ...greatest number smaller than x
    while low <= high:
        mid = low + (high - low) // 2
        if prefix_sum[mid]["date"]<= start_date:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

   
    ans1 = -1
    low = 0
    high = len(prefix_sum) - 1
    
    #binary search logc to find prefix sum just before end date or end date
    while low <= high:
        mid = low + (high - low) // 2
        if prefix_sum[mid]["date"] <= end_date:
            ans1 = mid
            low = mid + 1
        else:
            high = mid - 1

    if ans1!=-1:
        end = prefix_sum[ans1]["amount"] 
        if ans==-1:
             start=0
        else:
              start=prefix_sum[ans]["amount"]

    else:#no transaction before or on the end date so total is zero
         end=0
         start=0
    

    between_2_days = end-start

   
    with use_scope('output_area', clear=True):
        put_text(f"Total transaction between {start_str} and {end_str} is: {between_2_days}")
    

def spike():
        clear('output_area')
        week_total={}
     
        transaction_history.sort(key=lambda x:x['date'].date() if isinstance(x["date"], datetime) else x["date"])         
        #iterate through each transaction and for each day find the corresponding monday(assume the week starts from monday)            
        for th in transaction_history:
              d=th["date"]

              week_start=d-timedelta(days=d.weekday())#week_start stores the corresponding monday
              
              if isinstance(week_start, datetime):
                       week_start = week_start.date()
            
              #basically creating a bucket for each week and storing money in it       
              week_total[week_start]=week_total.get(week_start, 0) + th["amount"]



        sorted_week=sorted(week_total.items(),key=lambda x:x[0]) #list of tuples sorted by week start date

             #compare this weeks spending with last 3 weeks average spending and give user feedback

      #SLIDING WINDOW USED
      #window size of 3 

        for i in range(3,len(sorted_week)):
                curr_wk=sorted_week[i][1]
                weeks_avg=(sorted_week[i-1][1]+sorted_week[i-2][1]+sorted_week[i-3][1])/3
                if(sorted_week[i][1]>weeks_avg*1.5): #if this week spending is more than 1.5 times the average of last 3 weeks spending, then show spike
                  toast("You have a spike in expenses this week",color='error')
                else:
                  toast("Congrats!You spent less than last week!",color='error')
      
        
       


#kadane's algorithm used to find most profitable days(like findind the maximum sum subarray)
#net flow stores expenditure as negative transaction and income as positive transaction
def most_expensive_day_streak():
     clear('output_area')
     max_sum=0
     for th in transaction_history:
            temp={"amount":-th["amount"],"date":th["date"]}
            net_flow.append(temp)
         
   
     net_flow.sort(key=lambda x: x["date"].date() if isinstance(x["date"], datetime) else x["date"])
     streak_start_day=net_flow[0]["date"]
     streak_end_day=net_flow[0]["date"]
    
     for n in net_flow:
        if isinstance(n["date"], datetime):
            n["date"] = n["date"].date()

     curr_sum=0
     for n in net_flow:
            curr_sum=curr_sum+n["amount"]
            
            if curr_sum>max_sum:
               max_sum=curr_sum
               streak_end_day=n["date"]

            if curr_sum<0:
               curr_sum=0
               streak_start_day=n["date"]
               
        
     #no of days the streak lasted  
     streak_days=(streak_end_day-streak_start_day).days +1

    
     with use_scope('output_area', clear=True):
        put_markdown("## 📈 Dynamic Analysis: Max Profit Streak")
        put_text(f"Your highest net-gain streak was: Rs {max_sum} and it was a {streak_days}days streak")
       
               
def login_page():
     put_markdown("Login")

     while True:
          username=input("Username",placeholder="user")
          password=input("Password",placeholder="Enter password")

          if username=="samiksha" and password=="123":
               clear()
               main()
               break
          else:
               put_text("INCORRECT PASSWORD!")



def recurring_pattern():
     #frequency mapping
     clear('output_area')
     table_data=[['Category','Amount','Day']]

     names_of_days=["Monday","Tuessday","Wednesday","Thursday","Friday","Saturday","Sunday"]
     
   
     frequency=defaultdict(int)
     for th in transaction_history:
          day_of_the_week=th["date"].weekday()
          temp=(th["category"],th["amount"],day_of_the_week)
          frequency[temp]= frequency[temp]+1


     for pattern,count in frequency.items():
          if count>=3:
               category, amount, day = pattern
               table_data.append([category, amount, names_of_days[day]])
               put_text(f"Recurring transaction: {category}, Rs{amount}, on day {day}")

     with use_scope('output_area'):
        put_markdown("## Recurring Transactions")
        put_table(table_data)

       

                                       
    
if __name__ == "__main__":
    start_server(login_page, port=8081, debug=True)