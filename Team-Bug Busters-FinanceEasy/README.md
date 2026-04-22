FinanceEasy:
This application is a personal finance management tool designed to help users track expenses, identify spending spikes,optimise budgets and analyze financial streaks.While existing finance trackers perform simple CRUD operations,FinanceEasy's spike detection and optimisation features show proactive intelligence.
This has been developed ensuring minimum time coplexities.
Made entirely in Python and using Python's PyWebiO LIBRARY.

The Data Structures and Algorithms used are:
Hash Maps:
Used through out the project for accessing 'amounts','dates','prefix_sum' etc from list transaction_history,prefix_sum list etc.
Primary source for data retrieval through out the code.
Provides O(1)time complexity so optimal.


Binary Search:
Used for searching for all the transactions made on a particular date.
By keeping the data sorted accordng to date we can apply binary search minimising time complexity to O(logn)

Heap:
Used for calculating the top expenses and displaying it to the user.
Great alternative to sorting as its time complexity is only O(nlogk) where as sorting needs O(nlogn)

Sliding window:
Used to detect any spikes or abnormal inncreases in spending across weeks.
Window of size 3 is used to compare latest weeks transaction with average of last three weeks.


Greedy Algorithm:(knapsack)
Used to optimise budget allocation.
User sets a total budget across all categories and also limits for individual categories.
By comparing the ration of limit to importance for each category we optimally allocate budget to each categopry so that importance is maximum.

Prefix Sum:
Used to calculate total expenditure between two days.
Instead of iterating through the list each time and summing expensses i have used prefix sum to query through financial records in constant time.


Kadane's algorithm:
We used Kadane's Algorithm to identify the "Max Profit Streak." By iterating through the daily net-gains once, this algorithm efficiently identifies the sub-array with the maximum sum, effectively finding the longest and most profitable period in the user's financial history.


Video Link:
https://drive.google.com/file/d/1BgGgif9KXEi3apAFD7AXO7OUKz7hh4fD/view?usp=drivesdk

